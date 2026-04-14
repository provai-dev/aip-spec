---
AIP: 0006
Title: Registry Trust Anchoring via principal DID Document
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 6.2, 6.3.4, 7.3, 13.2, 17.7
Requires: 0002
Supersedes: ~
---

# AIP-0006: Registry Trust Anchoring via principal DID Document

## Abstract

This proposal closes the Registry self-declaration attack surface by
introducing a normative validation step (Step 6a) that anchors Registry
trust in the root principal's DID Document. For Tier 2 operations, a
Relying Party MUST resolve the principal's DID independently of the agent,
locate an `AIPRegistry` service entry, and verify that the Registry from
which revocation and capability data was fetched matches the principal's
declared Registry. The proposal also extends the `/.well-known/aip-registry`
schema (§6.3.4) with a self-signature field and Registry metadata.

## Motivation

In v0.2, the `aip_registry` claim in the Credential Token (§4.2.3) is
OPTIONAL and described as "advisory" in §17.7. The spec provides no
mechanism for a Relying Party to independently discover the authoritative
Registry for a given agent. This creates a concrete attack: a compromised
agent sets `aip_registry` to point at a fake Registry that returns
falsified capability manifests and revocation status.

A production operator in [w3c/did-use-cases#155](https://github.com/w3c/did-use-cases/issues/155)
identified this: "the agent is declaring its own lookup location. If the
agent is compromised, it could point a verifier at a fake endpoint."

The fix: anchor Registry trust in the root principal's DID Document —
a resource the agent cannot modify. For `did:web:acme.com`, the
authoritative Registry is declared at `https://acme.com/.well-known/did.json`,
entirely under Acme's control.

Closes #11

## Terminology

**AIPRegistry service entry** — A W3C DID Document `service` array
element with `type: "AIPRegistry"` that declares the authoritative AIP
Registry for agents delegated by that principal.

**Registry Trust Anchoring** — The process by which a Relying Party
independently verifies that the Registry serving an agent's data is the
Registry declared by the agent's root principal.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### Overview

This proposal adds three normative changes:

1. §6.2 — Principal DID Documents MUST include an `AIPRegistry` service
   entry for Tier 2 operations.
2. §6.3.4 — The `/.well-known/aip-registry` response gains a
   self-signature, Registry name, and endpoint map.
3. §7.3 Step 6a — A new validation step (after TTL check, before
   revocation) that verifies Registry trust anchoring for Tier 2.

### §6.2 DID Document Structure — AIPRegistry Service Entry

Add the following requirement to §6.2:

> A principal's DID Document that authorises agents for Tier 2 operations
> MUST include an `AIPRegistry` service entry in its `service` array:
>
> ```json
> {
>   "id": "did:web:acme.com#aip-registry",
>   "type": "AIPRegistry",
>   "serviceEndpoint": "https://registry.acme.com"
> }
> ```
>
> The `serviceEndpoint` MUST be an HTTPS URI pointing to the base URL
> of the authoritative AIP Registry for agents delegated by this
> principal. The `type` MUST be exactly `"AIPRegistry"` (case-sensitive).
>
> For principals using `did:key`: an `AIPRegistry` service entry cannot
> be declared (DID Key documents have no service array). Per AIP-0005,
> `did:key` principals MUST NOT authorise Tier 2 operations.
>
> For principals using `did:web` or `did:aip`: the `AIPRegistry` service
> entry is REQUIRED when the principal authorises any agent with Tier 2
> scopes. It is OPTIONAL for principals authorising only Tier 1 agents.

### §6.3.4 Well-Known Publication — Extended Schema

Replace the current §6.3.4 well-known response schema with:

> The response MUST be a JSON object containing:
>
> | Field | Type | Required | Description |
> |-------|------|----------|-------------|
> | `registry_aid` | string | REQUIRED | The Registry's `did:aip` AID |
> | `registry_name` | string | REQUIRED | Human-readable Registry name (maxLength: 128) |
> | `aip_version` | string | REQUIRED | The `aip_version` this Registry conforms to |
> | `public_key` | object | REQUIRED | JWK representation of the Registry's Ed25519 public key |
> | `endpoints` | object | REQUIRED | Map of service names to relative or absolute URI paths |
> | `signature` | string | REQUIRED | Base64url EdDSA signature of the canonical JSON (RFC 8785 JCS) of the document excluding the `signature` field |
>
> The `endpoints` object MUST include at minimum:
>
> | Key | Description |
> |-----|-------------|
> | `agents` | Base path for agent endpoints (e.g., `/v1/agents`) |
> | `crl` | CRL endpoint path (e.g., `/v1/crl`) |
> | `revocations` | Revocation submission path (e.g., `/v1/revocations`) |
>
> **Self-signature verification:** Relying Parties MUST verify the
> `signature` field against the `public_key` in the same document. This
> ensures the well-known document has not been tampered with in transit.
> The signature is computed over the RFC 8785 JCS canonical serialisation
> of the document with the `signature` field removed.
>
> **First-contact bootstrapping:** On first contact with a Registry,
> Relying Parties MUST:
>
> 1. Fetch `/.well-known/aip-registry` over HTTPS.
> 2. Verify the self-signature.
> 3. Pin the `public_key` and `registry_aid` locally.
> 4. On subsequent contacts, verify that the pinned key matches.
>
> Key rotation for Registry keys is an administrative operation that
> requires out-of-band communication to Relying Parties. A future AIP
> will define the Registry key rotation protocol.
>
> Cached values MUST NOT be used beyond 300 seconds without
> revalidation.

### §7.3 Step 6a — Registry Trust Anchoring (new step)

Insert after Step 6 (TTL) and before Step 7 (Revocation):

> **Step 6a — Registry Trust Anchoring (Tier 2 MUST; Tier 1 SHOULD).**
>
> 1. Extract `principal_did` from `aip_chain[0].iss` (the root
>    principal's DID).
> 2. Resolve `principal_did` using the DID method's own resolution
>    mechanism. The resolution MUST be independent of any agent-provided
>    data.
> 3. Locate a `service` entry with `type: "AIPRegistry"` in the
>    resolved DID Document.
> 4. Extract the `serviceEndpoint` URI.
> 5. Verify that the Registry from which the Relying Party has been
>    fetching revocation status and capability data for this token
>    matches the `serviceEndpoint` URI (origin comparison per
>    [RFC6454]).
> 6. If `aip_registry` is present in the Credential Token and does not
>    match the DID-Document-declared Registry, Fail:
>    `registry_untrusted`.
> 7. If the DID Document does not contain an `AIPRegistry` service
>    entry and the token contains Tier 2 scopes, Fail:
>    `registry_untrusted`.
>
> For Tier 1 operations, this step is RECOMMENDED but not required.
> Tier 1 Relying Parties MAY skip this step and rely on CRL-based
> revocation without Registry trust anchoring.
>
> **Resolution failure handling:** If DID resolution fails or times
> out, the Relying Party MUST treat this as `registry_unavailable`
> for Tier 2 operations.

### §4.2.3 Credential Token — aip_registry Claim Update

Update the description of the `aip_registry` claim:

> `aip_registry` — URI of the AIP Registry. OPTIONAL. When present,
> MUST match the `AIPRegistry` service endpoint declared in the root
> principal's DID Document (verified at Step 6a). A mismatch MUST
> cause rejection with `registry_untrusted`.
>
> For Tier 2 operations, if `aip_registry` is absent, the Relying
> Party MUST discover the Registry via Step 6a (DID Document lookup).

### §13.2 Error Codes — New Entry

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `registry_untrusted` | 403 | The Registry serving this agent's data does not match the principal's DID-Document-declared Registry |

### §17.7 Registry Security — Updated Text

Replace the advisory language with:

> Relying Parties MUST NOT trust the `aip_registry` claim in a
> Credential Token as the sole indicator of Registry authority. For
> Tier 2 operations, the authoritative Registry MUST be independently
> verified via the root principal's DID Document (Step 6a). The
> `aip_registry` claim is a convenience for Tier 1 Relying Parties
> and an early-exit optimisation; it is never authoritative.

### Normative Requirements

1. Principal DID Documents authorising Tier 2 agents MUST include an
   `AIPRegistry` service entry.
2. The `/.well-known/aip-registry` response MUST include a
   self-signature verifiable against the included public key.
3. Relying Parties validating Tier 2 tokens MUST perform Step 6a.
4. `aip_registry` claim mismatch with the DID-Document-declared
   Registry MUST be rejected with `registry_untrusted`.
5. Registry trust anchoring for Tier 1 is RECOMMENDED but OPTIONAL.
6. First-contact bootstrapping MUST pin the Registry's public key.

### Failure Conditions

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| Registry mismatch (aip_registry vs DID Document) | `registry_untrusted` | 403 |
| No AIPRegistry service in DID Doc for Tier 2 token | `registry_untrusted` | 403 |
| Principal DID resolution failure during Step 6a | `registry_unavailable` | 503 |
| Well-known self-signature verification failure | `registry_unavailable` | 503 |

### Schema Changes

1. Update `spec/v0.3/schemas/did-document.schema.json`: add
   `AIPRegistry` as a valid `service.type` value.
2. Create or update `spec/v0.3/schemas/well-known-registry.schema.json`:
   add `registry_name`, `endpoints`, and `signature` fields.

## Security Considerations

**Primary security improvement:** Closes the self-declaration attack
surface for Tier 2 operations. A compromised agent cannot redirect a
Relying Party to a fake Registry because the RP independently resolves
the principal's DID Document — a resource the agent does not control.

**did:web trust dependency:** For principals using `did:web`, the trust
anchor is the principal's web domain. Domain compromise would allow
redirecting the `AIPRegistry` service endpoint. This is appropriate —
domain control is a reasonable root of trust for enterprise operators.
Mitigations: HSTS, DNSSEC, Certificate Transparency monitoring.

**Resolution latency:** Step 6a adds a DID resolution round-trip. For
`did:web`, this is an HTTPS fetch. For `did:aip`, this is a Registry
lookup. Relying Parties MAY cache resolved DID Documents for up to 300
seconds. The step is placed after TTL (Step 6) so that expired tokens
are rejected without the resolution cost.

**First-contact TOFU:** The initial pin of a Registry's public key is
trust-on-first-use. A MitM at first contact could substitute a fake
Registry key. Mitigation: operators SHOULD distribute Registry public
keys out-of-band for high-assurance deployments.

**Tier 1 tradeoff:** Step 6a is SHOULD (not MUST) for Tier 1. This is
an explicit, documented tradeoff: Tier 1's bounded-staleness declaration
(AIP-0002) already accepts a 15-minute revocation window, making
Registry trust anchoring less critical.

## Backwards Compatibility

Breaking change for Tier 2: principal DID Documents MUST now include
an `AIPRegistry` service entry, and the `/.well-known/aip-registry`
response requires new fields.

**Migration path:**

1. Principal DID Document operators must add an `AIPRegistry` service
   entry to their DID Documents before their agents can pass Tier 2
   validation.
2. Registry operators must add `registry_name`, `endpoints`, and
   `signature` to their `/.well-known/aip-registry` response.
3. Tier 1 operations are unaffected (Step 6a is SHOULD, not MUST).

## Test Vectors

This proposal requires no new cryptographic test vectors. Conformance
tests should verify:

1. A Tier 2 token is rejected when the principal DID Document lacks
   an `AIPRegistry` service entry.
2. A Tier 2 token is rejected when `aip_registry` conflicts with the
   DID-Document-declared Registry.
3. A well-known response with invalid self-signature is rejected.
4. Step 6a is skipped (not failed) for Tier 1 tokens when the DID
   Document lacks an `AIPRegistry` entry.

## Implementation Guidance

**For principal DID Document operators:** Add an `AIPRegistry` service
entry to your DID Document if any agents delegated by your principal
will use Tier 2 scopes. For `did:web`, update the document at
`https://yourdomain.com/.well-known/did.json`.

**For Registry operators:** Update `/.well-known/aip-registry` to
include the self-signature. Compute the signature over JCS canonical
JSON of the document excluding the `signature` field.

**For Relying Party implementers:** Cache resolved DID Documents for up
to 300 seconds to amortise the resolution cost. Implement Step 6a after
Step 6 (TTL) to avoid unnecessary resolution for expired tokens.

## Alternatives Considered

**Trust the aip_registry claim with HPKP-style pinning.** Rejected
because the claim is agent-provided. Even with pinning, the first-contact
problem remains, and the agent controls the initial claim value.

**Registry-to-Registry federation.** A model where Registries attest to
each other's legitimacy. Rejected as too complex for v0.3; may be
revisited in a future AIP.

**Out-of-band Registry directory.** A centralised directory of known
legitimate Registries. Rejected because it introduces a single point
of failure and contradicts AIP's decentralised design.

**Place Step 6a at Step 3a (before claims validation).** Rejected per
decision B-9: performing DID resolution before validating basic JWT
structure and TTL wastes resolution resources on malformed or expired
tokens.

## References

### Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.
              <https://www.rfc-editor.org/info/rfc2119>

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119
              Key Words", BCP 14, RFC 8174, May 2017.
              <https://www.rfc-editor.org/info/rfc8174>

   [RFC6454]  Barth, A., "The Web Origin Concept", RFC 6454,
              December 2011.
              <https://www.rfc-editor.org/info/rfc6454>

   [RFC8785]  Rundgren, A., Jordan, B., and S. Erdtman, "JSON
              Canonicalization Scheme (JCS)", RFC 8785, June 2020.
              <https://www.rfc-editor.org/info/rfc8785>

   [W3C-DID]  W3C, "Decentralized Identifiers (DIDs) v1.0",
              W3C Recommendation, 19 July 2022.
              <https://www.w3.org/TR/did-core/>

### Informative References

   AIP-0002 — Reframe Tiers as threat-model declarations.
   AIP-0005 — Three-tier grant model (did:key prohibition for Tier 2).
   W3C DID Use Cases, Issue #155 — Production operator feedback on
   Registry trust.
   <https://github.com/w3c/did-use-cases/issues/155>

## Acknowledgements

Registry trust anchoring design informed by production operator feedback
in W3C DID Use Cases Issue #155 and Issue #11 in this repository.

## Changelog

- 2026-04-12 — Initial draft.
