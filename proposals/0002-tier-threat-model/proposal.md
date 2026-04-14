---
AIP: 0002
Title: Reframe Tiers as threat-model declarations
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 3, 9.3, 16
Requires: ~
Supersedes: ~
---

# AIP-0002: Reframe Tiers as threat-model declarations

## Abstract

This proposal reframes the Tier 1 / Tier 2 / Tier 3 definitions in §3
(Terminology) and §9.3 (Revocation Checking) from an operational performance
distinction to a threat-model declaration. Each Tier declares which security
properties the deploying principal asserts hold at execution time. The proposal
also adds a normative conformance table to §16 that maps each Tier to its
security claims, enabling independent verification.

## Motivation

The current spec describes Tiers as an operational distinction framed around
performance and availability tradeoffs. Tier 1 is described as "suitable for
high-frequency, low-consequence operations where some revocation staleness is
acceptable" — language that invites implementers to choose Tier 1 for
consequential operations on performance grounds alone.

This framing obscures the fundamental purpose: each Tier is a security claim
about which threats are mitigated at execution time. A deploying principal
selecting Tier 1 for a financial transaction is not making a performance
choice — they are declaring that a 15-minute revocation staleness window is
acceptable for that operation's threat profile, which is almost certainly
incorrect.

The OWASP LLM Top 10 project independently identified this gap, noting that
authorization "probably needs to split into two sub-checks — one verifying
the capability token (cryptographic, instantaneous) and one verifying that
the agent's behavioral history makes it admissible."

Closes #14

## Terminology

**Threat-model declaration** — A normative statement by the deploying
principal (or Registry operator, for Tier 3) asserting which security
properties hold for a given operation or deployment. The declaration
determines mandatory security mechanisms, revocation-checking mode, and
maximum Credential Token lifetime.

**Cryptographic admissibility** — The property that an agent's Credential
Token and delegation chain are cryptographically valid at claim time:
signatures verify, claims are well-formed, the token is not expired, and the
delegation chain has not been broken.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### Overview

This proposal replaces the Tier definitions in §3, updates the revocation
checking requirements in §9.3, and adds a Tier conformance table to §16. The
scope enumeration for each Tier (which scopes map to which Tier) is unchanged;
only the framing and conformance obligations change.

### §3 Terminology — Tier Definitions (replacement text)

The following replaces the current Tier 1, Tier 2, Tier 3, and NOTE
definitions in §3:

> The Tier assignment for an operation is a **threat-model declaration**. It
> specifies which security properties the deploying principal asserts hold at
> execution time. Tier selection on performance or availability grounds alone,
> without regard to the security properties declared, is a misconfiguration.
>
> **Tier 1 (Bounded-staleness)** — Interactions in which every scope in the
> token's `aip_scope` array is drawn exclusively from the following set:
> `email.read`, `email.write`, `email.send`, `email.delete`,
> `calendar.read`, `calendar.write`, `calendar.delete`, `web.browse`,
> `web.forms_submit`, `web.download`, and `spawn_agents.create`.
>
> Tier 1 declares:
>
> 1. *Cryptographic admissibility* — The agent's Credential Token and
>    delegation chain are cryptographically valid at claim time.
> 2. *Bounded revocation staleness* — Revocation status may lag by up to 15
>    minutes (CRL cache window). The deploying principal accepts this
>    staleness for all scopes in the token.
>
> Tier 1 does **not** declare:
>
> - That the agent's authorization is current at execution time.
> - That revocation issued within the last 15 minutes has propagated.
>
> CRL-based revocation checking is sufficient. Maximum Credential Token
> lifetime is 3600 seconds.
>
> **Tier 2 (Real-time revocation)** — Interactions in which at least one
> scope in the token's `aip_scope` array is any of: `transactions` or any
> scope with the prefix `transactions.`, `communicate.whatsapp`,
> `communicate.telegram`, `communicate.sms`, `communicate.voice`,
> `filesystem.execute`, or `spawn_agents.manage`.
>
> Tier 2 declares:
>
> 1. *Cryptographic admissibility* — Same as Tier 1.
> 2. *Real-time revocation* — Registry check is live and per-action.
>    Revocation is effective within RPNP delivery latency (at most 5
>    seconds for subscribing Relying Parties, where RPNP is deployed).
>
> Real-time revocation checking against the Registry MUST be performed.
> Maximum Credential Token lifetime is 300 seconds. DPoP
> proof-of-possession [RFC9449] is REQUIRED.
>
> **Tier 3 (Enterprise / regulated)** — An organisational deployment
> classification that extends Tier 2 with additional transport-layer
> security. Tier 3 is declared by Registry operators and MUST be
> documented in the Registry's well-known configuration (Section 15.1).
> Tier 3 applies to all Tier 2 scopes within the designated deployment.
>
> Tier 3 declares all Tier 2 security properties, plus:
>
> 3. *Mutual authentication* — mTLS channel authentication between
>    Relying Party and Registry.
> 4. *OCSP real-time status* — OCSP-style per-certificate revocation
>    status checking per [RFC6960], supplementing CRL-based checks.
>
> NOTE: A token's Tier is always determined by its highest-risk scope.
> A token with one Tier 2 scope and nine Tier 1 scopes is a Tier 2
> token in its entirety.

### §9.3 Revocation Checking (replacement text)

The following replaces the current §9.3 Tier-specific paragraphs (the
child-agent propagation and Approval Envelope revocation interaction
paragraphs are unchanged):

> **Tier 1 — Bounded-staleness revocation.** TTL ≤ 3600s. Validate
> against CRL at issuance time. CRL MUST be refreshed every 15 minutes.
> The deploying principal accepts that revocation events within the cache
> window may not be reflected.
>
> **Tier 2 — Real-time revocation.** TTL ≤ 300s. Real-time Registry
> check on EVERY request. MUST NOT cache revocation status. If Registry
> unreachable: MUST deny and return `registry_unavailable`.
>
> **Tier 3 — Enterprise/regulated revocation.** All Tier 2 requirements
> apply. Additionally: MUST use mTLS for Registry communication. MUST
> support OCSP per [RFC6960]. Tier 3 supplements, not replaces, Tier 2.

### §16 Versioning and Compatibility — Tier Conformance Table (new subsection)

Add the following subsection at the end of §16, before §17:

> ### 16.1. Tier Conformance
>
> An implementation claiming conformance at a given Tier MUST satisfy
> every security property declared by that Tier.
>
> | Property | Tier 1 | Tier 2 | Tier 3 |
> |----------|--------|--------|--------|
> | Cryptographic admissibility | REQUIRED | REQUIRED | REQUIRED |
> | Max Credential Token TTL | 3600s | 300s | 300s |
> | Revocation mode | CRL (15-min refresh) | Real-time per-action | Real-time per-action |
> | Bounded revocation staleness (≤15 min) | DECLARED | N/A | N/A |
> | Real-time revocation (≤5s RPNP) | N/A | REQUIRED | REQUIRED |
> | DPoP proof-of-possession | NOT REQUIRED | REQUIRED | REQUIRED |
> | mTLS channel authentication | NOT REQUIRED | NOT REQUIRED | REQUIRED |
> | OCSP real-time status | NOT REQUIRED | NOT REQUIRED | REQUIRED |
>
> A conformance test suite MUST independently verify each REQUIRED
> property. Implementations MUST NOT claim Tier 2 conformance if they
> cache revocation status or omit DPoP. Implementations MUST NOT claim
> Tier 3 conformance without demonstrating mTLS and OCSP support.
>
> Tier selection is the responsibility of the deploying principal (for
> Tier 1 and Tier 2) or the Registry operator (for Tier 3). Selection
> based solely on performance or availability characteristics, without
> regard to the security properties each Tier declares, is a
> misconfiguration and MUST be flagged by conformance tooling.

### Normative Requirements

1. Each Tier definition in §3 MUST enumerate the security properties it
   declares, using the terminology defined in this proposal.
2. Tier definitions MUST NOT use language that frames Tier selection as a
   performance or availability tradeoff.
3. §9.3 revocation checking paragraphs MUST use Tier names that match the
   §3 definitions (e.g., "Bounded-staleness" for Tier 1).
4. §16 MUST include a conformance table mapping each Tier to its required
   security properties.
5. Conformance tooling MUST flag Tier selection that does not match the
   operation's threat profile as a misconfiguration.
6. `spawn_agents.manage` MUST be classified as a Tier 2 scope (see
   AIP-0003 for the `spawn_agents` split).

### Failure Conditions

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| Tier 2 operation attempted with cached revocation status | `revocation_stale` | 403 |
| Tier 2 operation attempted without DPoP proof | `dpop_required` | 401 |
| Tier 3 operation attempted without mTLS | `mtls_required` | 403 |
| Registry unreachable during Tier 2/3 check | `registry_unavailable` | 503 |

### Schema Changes

No schema changes. Tier assignment is determined by scope content, not by
a schema field. The `aip_scope` array schema is unchanged.

## Security Considerations

This proposal strengthens the security posture of AIP by making the threat
model explicit in each Tier definition. The primary security improvement is
eliminating the risk that implementers select Tier 1 for consequential
operations based on performance framing rather than threat analysis.

**Risks addressed:**

- **Tier misselection:** The current framing permits reading Tier 1 as
  "suitable" for any operation where staleness is tolerable. The revised
  framing requires the deploying principal to consciously accept bounded
  revocation staleness as a security property, not a convenience.
- **Conformance ambiguity:** Without a conformance table, implementations
  could claim Tier 2 while caching revocation status. The table makes
  each property independently testable.

**No new threat vectors introduced.** The scope-to-Tier mapping is
unchanged; only the framing and conformance obligations are tightened.

## Backwards Compatibility

Backwards compatible with caveat: the normative scope-to-Tier mapping is
unchanged, so existing valid tokens remain valid. However, implementations
that previously selected Tier 1 for operations that should be Tier 2 based
on threat analysis (not scope content) are now explicitly non-conformant.
Conformance tooling may flag these as misconfigurations.

No schema changes. No token format changes. No version bump required beyond
the v0.3 minor increment already planned.

## Test Vectors

This proposal requires no new test vectors. The scope-to-Tier mapping
algorithm is unchanged; conformance testing validates security property
satisfaction, not token structure.

## Implementation Guidance

Implementers should review their Capability Manifest authoring to ensure
Tier selection reflects the threat model of each operation, not availability
preferences. A Tier 1 assignment for `transactions.*` scopes was never valid
(the scope mapping already forced Tier 2), but the revised framing makes the
rationale explicit.

Registry operators deploying Tier 3 should document the additional mTLS and
OCSP requirements in their well-known configuration and provide integration
guides for Relying Parties.

## Alternatives Considered

**Keep the operational framing and add a security note.** This was rejected
because a non-normative note does not change conformance obligations. The
operational framing would continue to be cited as justification for Tier
misselection.

**Merge behavioral admissibility into Tier 2.** Issue #14 originally
proposed that Tier 2 declare behavioral admissibility (trust score
freshness). This proposal defers behavioral admissibility to AIP-0008
(Engagement Objects), which defines the trust-score model. Tier 2's security
claims are limited to cryptographic admissibility and real-time revocation.

**Remove Tier 3 entirely.** Tier 3 was considered for removal on the grounds
that mTLS and OCSP are deployment decisions, not protocol-level
requirements. Retained because enterprise/regulated deployments need a
normative anchor for these requirements, and the Tier framework provides a
natural home.

## References

### Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.
              <https://www.rfc-editor.org/info/rfc2119>

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119
              Key Words", BCP 14, RFC 8174, May 2017.
              <https://www.rfc-editor.org/info/rfc8174>

   [RFC6960]  Santesson, S., Myers, M., Ankney, R., Malpani, A.,
              Galperin, S., and C. Adams, "X.509 Internet Public Key
              Infrastructure Online Certificate Status Protocol - OCSP",
              RFC 6960, June 2013.
              <https://www.rfc-editor.org/info/rfc6960>

   [RFC9449]  Fett, D., Campbell, B., Bradley, J., Lodderstedt, T.,
              Jones, M., and D. Waite, "OAuth 2.0 Demonstrating
              Proof of Possession (DPoP)", RFC 9449, September 2023.
              <https://www.rfc-editor.org/info/rfc9449>

### Informative References

   OWASP LLM Top 10, Issue #802 — Authorization sub-check separation.
   <https://github.com/OWASP/www-project-top-10-for-large-language-model-applications/issues/802>

## Acknowledgements

This proposal incorporates analysis from the OWASP LLM Top 10 project
discussion on authorization layer separation.

## Changelog

- 2026-04-12 — Initial draft.
