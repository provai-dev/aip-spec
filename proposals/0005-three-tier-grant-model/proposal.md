---
AIP: 0005
Title: Three-tier grant model (G1/G2/G3) with OAuth AS and identity proofing
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 3, 4.5, 15.1, 15.5, 15.6
Requires: 0002
Supersedes: ~
---

# AIP-0005: Three-tier grant model (G1/G2/G3) with OAuth AS and identity proofing

## Abstract

This proposal restructures §4.5 (AIP-GRANT) into three distinct grant
tiers, introduces a new §15.5 defining the AIP Registry as an OAuth 2.1
Authorization Server, and adds identity-proofing requirements for Tier 2
principals. The three grant tiers are:

- **G1 (Registry-Mediated):** The Registry acts as intermediary between
  deployer and principal wallet, suitable for consumer-facing flows.
- **G2 (Direct Deployer):** The deployer communicates directly with the
  principal wallet, suitable for enterprise self-service deployments.
- **G3 (Full Ceremony):** The current AIP-GRANT flow extended with
  OAuth 2.1 Authorization Code + PKCE, suitable for high-assurance
  deployments requiring verifiable identity proofing.

## Motivation

The current AIP-GRANT protocol (§4.5) defines a single grant flow — the
full ceremony — for all deployment scenarios. This creates friction in two
directions:

1. **Consumer/SaaS deployments** find the full ceremony too heavyweight.
   A user installing an AI agent from a marketplace should not need to
   understand GrantRequest objects and Ed25519 signing. The Registry
   already holds the trust anchor; it can mediate a simpler flow.

2. **Regulated/enterprise deployments** find the full ceremony
   insufficient. Financial services, healthcare, and government
   deployments require verifiable identity proofing of the authorising
   principal — not just possession of a DID private key, but proof that
   the DID holder passed KYC, holds a specific organisational role, or
   authenticated at a specific assurance level.

Additionally, the current spec does not address how AIP integrates with
the broader OAuth ecosystem. Agents operating in environments with
existing OAuth infrastructure (MCP servers, API gateways) need a
standards-based token exchange path.

## Terminology

**Grant Tier** — One of three standardised authorization ceremony
profiles (G1, G2, G3) that determines the interaction pattern between
deployer, principal, and Registry.

**Registry-Mediated Grant (G1)** — A grant flow in which the Registry
acts as intermediary, presenting the consent UI and forwarding the signed
Principal Token to the deployer.

**Direct Deployer Grant (G2)** — A grant flow in which the deployer
communicates directly with the principal wallet, using AIP-GRANT
GrantRequest/GrantResponse objects.

**Full Ceremony Grant (G3)** — A grant flow that extends G2 with
OAuth 2.1 Authorization Code flow [RFC6749], PKCE [RFC7636], and
identity-proofing claims.

**Identity Proofing** — The process by which a principal demonstrates
that their DID is bound to a verified real-world identity, expressed
via `acr` and `amr` claims in the Principal Token.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### Overview

This proposal:

1. Restructures §4.5 into three subsections (§4.5.1–4.5.3) for G1, G2,
   and G3 respectively, with shared requirements in a common preamble.
2. Adds `acr` and `amr` claims to the Principal Token schema (§4.2.4).
3. Adds a new §15.5 defining the Registry's OAuth 2.1 AS capabilities.
4. Forbids `did:key` for Tier 2 principals.
5. Adds identity-proofing metadata to the Registry's well-known
   configuration.

### §3 Terminology — New Definitions

Add the following definitions to §3:

> **Grant Tier** — One of three standardised AIP-GRANT ceremony profiles:
> G1 (Registry-Mediated), G2 (Direct Deployer), G3 (Full Ceremony).
>
> **Identity Proofing Level** — The assurance level at which the
> principal's real-world identity has been verified, expressed as an
> `acr` value in the Principal Token.

### §4.5 AIP-GRANT — Restructured

#### §4.5.0 Common Requirements

The following requirements apply to ALL grant tiers:

1. The resulting Principal Token MUST conform to §4.2.4.
2. The principal MUST explicitly consent to the requested capabilities
   per §4.5.3 (Wallet Consent Requirements, unchanged).
3. The `nonce` in every grant interaction MUST be cryptographically
   random with at least 128 bits of entropy.
4. The resulting Registration Envelope MUST conform to §5.
5. A deployer MUST declare the grant tier used in the Registration
   Envelope via a new `grant_tier` field (values: `"G1"`, `"G2"`,
   `"G3"`).

#### §4.5.1 G1 — Registry-Mediated Grant

**Use case:** Consumer-facing deployments, marketplaces, SaaS platforms.

**Flow:**

```
 Agent Deployer          AIP Registry          Principal Wallet
 |                       |                     |
 |-- POST /v1/grants --> |                     |
 |   (GrantRequest)      |                     |
 |                       |-- Consent Request -> |
 |                       |   (via redirect or   |
 |                       |    push notification) |
 |                       |                     |
 |                       |   [Human reviews     |
 |                       |    & signs]          |
 |                       |                     |
 |                       |<- GrantResponse ---- |
 |                       |   (signed PT)        |
 |<-- grant_id + status  |                     |
 |                       |                     |
 |-- POST /v1/agents --> |                     |
 |   (RegEnvelope with   |                     |
 |    grant_id ref)      |                     |
 |<-- AID -------------- |                     |
```

**Normative requirements specific to G1:**

1. The deployer MUST submit the GrantRequest to the Registry via
   `POST /v1/grants`.
2. The Registry MUST validate the GrantRequest per §4.5.2 before
   forwarding to the principal wallet.
3. The Registry MUST present the consent UI to the principal via the
   principal's registered wallet endpoint or redirect URI.
4. The Registry MUST NOT modify the requested capabilities when
   forwarding to the principal wallet.
5. The Registry MUST store the signed GrantResponse and associate it
   with a `grant_id`.
6. The deployer MUST reference the `grant_id` in the Registration
   Envelope instead of embedding the Principal Token directly.
7. The Registry MUST verify that the `grant_id` is valid, unexpired,
   and matches the deployer before accepting the Registration Envelope.

**Principal DID requirements for G1:** The principal MAY use `did:key`,
`did:web`, or `did:aip` for Tier 1 operations. For Tier 2 operations
in the token, the principal MUST NOT use `did:key` (see §4.5.4).

#### §4.5.2 G2 — Direct Deployer Grant

**Use case:** Enterprise self-service, developer tools, CLI-based
deployments.

This is the current AIP-GRANT flow as specified in v0.2 §4.5. The
deployer communicates directly with the principal wallet using
GrantRequest/GrantResponse objects via the transport bindings defined
in §4.5.5.

**Normative requirements specific to G2:**

1. The GrantRequest and GrantResponse schemas are unchanged from v0.2.
2. All transport bindings (Web Redirect, QR Code, Deep Link) remain
   valid for G2.
3. The deployer MUST submit the signed Principal Token in the
   Registration Envelope (no `grant_id` indirection).

**Principal DID requirements for G2:** Same as G1.

#### §4.5.3 G3 — Full Ceremony Grant

**Use case:** Regulated industries, high-value operations, deployments
requiring verifiable identity proofing.

G3 extends G2 with OAuth 2.1 Authorization Code flow [RFC6749] and
PKCE [RFC7636]. The principal's identity is verified at a declared
assurance level, and the proof is captured in `acr`/`amr` claims.

**Flow:**

```
 Agent Deployer    OAuth AS (Registry)    Principal Wallet/IdP
 |                 |                      |
 |-- AuthZ Req --> |                      |
 |   (PKCE, scope) |                      |
 |                 |-- AuthN + Consent --> |
 |                 |   (identity proofing  |
 |                 |    at declared acr)   |
 |                 |                      |
 |                 |<- AuthZ Code -------- |
 |<-- AuthZ Code - |                      |
 |                 |                      |
 |-- Token Req --> |                      |
 |   (code + PKCE) |                      |
 |<-- PT + acr/amr |                      |
 |                 |                      |
 |-- RegEnvelope ->|                      |
 |<-- AID -------- |                      |
```

**Normative requirements specific to G3:**

1. The Registry MUST implement the OAuth 2.1 Authorization Server
   interface defined in §15.5.
2. The authorization request MUST include PKCE (`code_challenge_method`
   MUST be `S256`) per [RFC7636].
3. The authorization request MUST include `acr_values` declaring the
   minimum identity-proofing level required.
4. The token response MUST include a Principal Token with `acr` and
   `amr` claims reflecting the actual authentication performed.
5. The `acr` value in the Principal Token MUST be equal to or stronger
   than the `acr_values` requested. If the IdP cannot satisfy the
   requested level, the authorization MUST fail with
   `identity_proofing_insufficient`.
6. For Tier 2 operations, G3 is RECOMMENDED. For Tier 3 deployments,
   G3 is REQUIRED.

**Principal DID requirements for G3:** The principal MUST use `did:web`
or `did:aip`. `did:key` MUST NOT be used.

#### §4.5.4 Principal DID Method Restrictions

> For any grant tier, when the resulting token contains one or more
> Tier 2 scopes (as defined in §3), the principal's DID MUST NOT use
> the `did:key` method. The principal MUST use `did:web` or `did:aip`.
>
> *Rationale:* `did:key` encodes only a bare public key with no
> binding to a verifiable controller, no key rotation support, and no
> revocation mechanism. For Tier 2 operations — which declare real-time
> revocation and DPoP — the principal's identity must be resolvable
> and rotatable.

Validators MUST reject Principal Tokens where the `iss` is a `did:key`
DID and the token contains any Tier 2 scope. Error code:
`principal_did_method_forbidden`.

### §4.2.4 Principal Token — New Claims

Add the following rows to the Principal Token payload fields table:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `acr` | string | OPTIONAL | Authentication Context Class Reference per [RFC9068] §2.2.3.1; REQUIRED when grant tier is G3 |
| `amr` | array | OPTIONAL | Authentication Methods References per [RFC8176]; REQUIRED when `acr` is present |

### §5 Registration Envelope — New Field

Add the following field to the Registration Envelope schema:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `grant_tier` | string | REQUIRED | One of: `"G1"`, `"G2"`, `"G3"` |
| `grant_id` | string | CONDITIONAL | REQUIRED when `grant_tier` is `"G1"`; pattern: `^gnt:[0-9a-f]{8}-...` (UUID v4 with `gnt:` prefix) |

### §15.1 Required Endpoints — New Grant Endpoint

Add to the required endpoints table:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/grants` | Submit GrantRequest for Registry-Mediated (G1) flow |
| `GET` | `/v1/grants/{id}` | Retrieve grant status (G1 only) |

### §15.5 OAuth 2.1 Authorization Server (new section)

> #### 15.5. OAuth 2.1 Authorization Server
>
> A conformant AIP Registry supporting G3 grants MUST implement an
> OAuth 2.1 Authorization Server [RFC6749] with the following
> requirements:
>
> 1. The authorization endpoint MUST be published in the Registry's
>    well-known configuration at
>    `/.well-known/oauth-authorization-server` per [RFC8414].
> 2. PKCE [RFC7636] with `code_challenge_method: "S256"` is REQUIRED
>    for all authorization requests.
> 3. The `scope` parameter MUST use AIP scope URIs from the
>    `urn:aip:scope:` namespace (see AIP-0011).
> 4. The token endpoint MUST return a signed Principal Token (not a
>    standard OAuth access token) as the `access_token` value, with
>    `token_type: "AIP+JWT"`.
> 5. The token response MUST include `acr` and `amr` claims reflecting
>    the authentication performed.
> 6. The authorization server MUST support the `acr_values` parameter
>    to declare minimum identity-proofing requirements.
> 7. DPoP [RFC9449] MUST be supported on the token endpoint.
>
> **Well-known metadata additions:** The Registry's
> `/.well-known/aip-registry` configuration (§15.1) MUST include:
>
> | Field | Type | Description |
> |-------|------|-------------|
> | `grant_tiers_supported` | array | List of supported grant tiers: `["G1", "G2", "G3"]` |
> | `acr_values_supported` | array | List of supported `acr` values |
> | `amr_values_supported` | array | List of supported `amr` values |
> | `oauth_authorization_server` | string | URI of the OAuth AS metadata document (present only if G3 supported) |
> | `identity_proofing_required_for_tier2` | boolean | Whether this Registry requires G3 for Tier 2 operations |

### Normative Requirements

1. Every AIP grant ceremony MUST declare its grant tier (G1, G2, or G3)
   in the Registration Envelope.
2. G1 grants MUST be mediated by the Registry; the deployer MUST NOT
   communicate directly with the principal wallet.
3. G2 grants MUST use direct deployer-to-wallet communication per the
   existing AIP-GRANT transport bindings.
4. G3 grants MUST use OAuth 2.1 Authorization Code flow with PKCE and
   MUST include `acr`/`amr` claims in the resulting Principal Token.
5. `did:key` MUST NOT be used as the principal's DID method when the
   token contains any Tier 2 scope.
6. Registries MUST advertise supported grant tiers and identity-proofing
   capabilities in their well-known configuration.
7. Registries supporting G3 MUST publish OAuth AS metadata per
   [RFC8414].

### Failure Conditions

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| Principal uses `did:key` for Tier 2 scope | `principal_did_method_forbidden` | 403 |
| G3 identity proofing below requested `acr_values` | `identity_proofing_insufficient` | 403 |
| G1 `grant_id` not found or expired | `grant_not_found` | 404 |
| G1 `grant_id` does not match deployer | `grant_deployer_mismatch` | 403 |
| Registration Envelope missing `grant_tier` | `invalid_envelope` | 400 |
| G3 authorization request missing PKCE | `pkce_required` | 400 |

### Schema Changes

1. Update `spec/v0.3/schemas/registration-envelope.schema.json`: add
   `grant_tier` (required, enum) and `grant_id` (conditional) fields.
2. Update `spec/v0.3/schemas/principal-token.schema.json`: add `acr`
   (optional string) and `amr` (optional array of strings) fields.
3. Create `spec/v0.3/schemas/grant-request.schema.json` (new, for G1
   Registry-mediated grant request).

## Security Considerations

**G1 Registry trust:** In G1, the Registry mediates the entire grant flow.
This increases the Registry's trust surface — a compromised Registry could
forge consent. Mitigation: the principal wallet still performs independent
verification of the GrantRequest and signs the Principal Token; the
Registry cannot produce a valid PT without the principal's private key.

**did:key prohibition for Tier 2:** `did:key` provides no key rotation,
no revocation, and no controller binding. For Tier 2 operations requiring
real-time revocation, the principal's identity must be resolvable and
rotatable. The prohibition ensures that Tier 2 principals have a
verifiable, revocable identity.

**G3 identity proofing:** G3 introduces a dependency on external Identity
Providers. A compromised IdP could issue false `acr`/`amr` claims.
Mitigation: the `acr` claim is bound to the Principal Token signature;
the Relying Party can verify the principal's DID and cross-check the
`acr` against the Registry's advertised `acr_values_supported`.

**PKCE requirement:** PKCE prevents authorization code interception
attacks in the G3 flow. `S256` is the only permitted challenge method;
`plain` MUST NOT be used.

## Backwards Compatibility

Breaking change. The `grant_tier` field is REQUIRED in the Registration
Envelope. Existing v0.2 Registration Envelopes do not include this field.

**Migration path:**

1. Existing v0.2 deployments using the current AIP-GRANT flow map to G2.
2. v0.3 Registration Envelopes MUST include `grant_tier: "G2"` for the
   existing flow.
3. Registries SHOULD accept v0.2 envelopes without `grant_tier` during a
   transition period, treating them as G2. This transition period ends
   when v0.3 is declared stable.
4. New deployments targeting consumer flows should adopt G1.
5. Regulated deployments should adopt G3.

## Test Vectors

This proposal requires no new cryptographic test vectors. The OAuth 2.1
flow uses standard PKCE; the `acr`/`amr` claims are standard JWT claims.
Conformance tests should verify:

1. A Registration Envelope without `grant_tier` is rejected (v0.3 mode).
2. A G1 envelope without `grant_id` is rejected.
3. A G3 Principal Token without `acr` is rejected.
4. A Principal Token with `did:key` issuer and Tier 2 scope is rejected.

## Implementation Guidance

**For Registry implementers:** G1 requires the Registry to implement a
consent forwarding mechanism. This may be a redirect to the principal's
wallet URI (similar to OAuth redirect) or a push notification to a
registered wallet endpoint. The mechanism is transport-specific and
outside the scope of this proposal.

**For wallet implementers:** Wallets should support all three grant tiers.
G1 consent requests arrive from the Registry (not the deployer); wallets
MUST verify that the Registry is a trusted AIP Registry before presenting
consent.

**For deployers:** Choose the grant tier based on the deployment context:
- G1 for consumer-facing products with Registry-managed consent
- G2 for developer tools and enterprise self-service
- G3 for regulated industries or high-value operations

## Alternatives Considered

**Single flow with optional identity proofing.** Rejected because it
conflates the consent mechanism (who mediates) with the assurance level
(what proofing is required). The three-tier model separates these concerns.

**Separate AS from Registry.** Considered making the OAuth AS a separate
service from the Registry. Rejected because the Registry already holds the
trust anchor and publishing the AS as a Registry capability simplifies
deployment.

**Allow did:key for Tier 2 with additional constraints.** Rejected because
`did:key` fundamentally lacks rotation and revocation capabilities. No
amount of additional constraints can compensate for the missing features.

## References

### Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.
              <https://www.rfc-editor.org/info/rfc2119>

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119
              Key Words", BCP 14, RFC 8174, May 2017.
              <https://www.rfc-editor.org/info/rfc8174>

   [RFC6749]  Hardt, D., Ed., "The OAuth 2.0 Authorization Framework",
              RFC 6749, October 2012.
              <https://www.rfc-editor.org/info/rfc6749>

   [RFC7636]  Sakimura, N., Ed., Bradley, J., and N. Agarwal, "Proof Key
              for Code Exchange by OAuth Public Clients", RFC 7636,
              September 2015.
              <https://www.rfc-editor.org/info/rfc7636>

   [RFC8176]  Jones, M., Hunt, P., and A. Nadalin, "Authentication Method
              Reference Values", RFC 8176, June 2017.
              <https://www.rfc-editor.org/info/rfc8176>

   [RFC8414]  Jones, M., Sakimura, N., and J. Bradley, "OAuth 2.0
              Authorization Server Metadata", RFC 8414, June 2018.
              <https://www.rfc-editor.org/info/rfc8414>

   [RFC9068]  Bertocci, V., "JSON Web Token (JWT) Profile for OAuth 2.0
              Access Tokens", RFC 9068, October 2021.
              <https://www.rfc-editor.org/info/rfc9068>

   [RFC9449]  Fett, D., Campbell, B., Bradley, J., Lodderstedt, T.,
              Jones, M., and D. Waite, "OAuth 2.0 Demonstrating
              Proof of Possession (DPoP)", RFC 9449, September 2023.
              <https://www.rfc-editor.org/info/rfc9449>

### Informative References

   AIP-0002 — Reframe Tiers as threat-model declarations.

## Acknowledgements

The three-tier grant model draws on OAuth 2.1 patterns and NIST SP 800-63-4
identity proofing levels.

## Changelog

- 2026-04-12 — Initial draft.
