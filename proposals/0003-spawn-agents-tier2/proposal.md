---
AIP: 0003
Title: Split spawn_agents into create/manage and promote to Tier 2
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 3, 4.5.3, 7.2, 9.3, 17.1
Requires: 0002
Supersedes: ~
---

# AIP-0003: Split spawn_agents into create/manage and promote to Tier 2

## Abstract

This proposal splits the monolithic `spawn_agents` scope into two sub-scopes
— `spawn_agents.create` and `spawn_agents.manage` — and reclassifies both as
Tier 2. The current Tier 1 classification gives compromised orchestrators up
to 75 minutes (60-minute TTL + 15-minute CRL lag) to spawn an unbounded
delegation tree before revocation propagates. Promoting to Tier 2 enforces
real-time revocation checking, a 300-second TTL, and DPoP
proof-of-possession at every spawn and management operation.

## Motivation

`spawn_agents` is the highest-risk capability in the AIP scope set. It
multiplies the attack surface by N for every generation of spawning. Despite
this, the current spec classifies it as Tier 1, granting:

- A maximum TTL of 3600 seconds (1 hour)
- CRL-based revocation only (15-minute cache window)
- No DPoP requirement

A compromised orchestrator with `spawn_agents` can register an unbounded
number of child agents — each with their own `spawn_agents` grants if
`max_delegation_depth > 0` — creating a self-replicating delegation tree
that persists for up to 75 minutes after compromise before CRL-based
revocation can propagate.

This directly contradicts §1.2's design principle: "Security proportional
to risk."

Closes #6

## Terminology

**spawn_agents.create** — The capability to register new child agents with
the Registry, establishing a delegation relationship. This is the
high-risk action: it multiplies the attack surface.

**spawn_agents.manage** — The capability to manage already-spawned child
agents: suspend, resume, update metadata, or trigger voluntary
deregistration. This operates on existing delegation relationships; it
does not create new ones.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### Overview

The monolithic `spawn_agents` scope is replaced by two sub-scopes. Both are
classified as Tier 2. The bare `spawn_agents` scope is retired and MUST be
rejected by conforming implementations.

### §3 Terminology — Scope Changes

In the Tier 1 definition, remove `spawn_agents` from the enumerated scope
list.

In the Tier 2 definition (as revised by AIP-0002), add `spawn_agents.create`
and `spawn_agents.manage` to the enumerated scope list.

The bare scope `spawn_agents` is no longer valid. Implementations MUST
reject tokens containing `spawn_agents` without a sub-scope qualifier and
return error code `invalid_scope`.

### §4.5.3 Wallet Consent Display

Update the consent display table:

| Scope | Human-readable prompt |
|-------|----------------------|
| `spawn_agents.create` | "Create child AI agents on your behalf (up to [max_concurrent] at a time)" |
| `spawn_agents.manage` | "Manage (suspend, resume, update) your existing child AI agents" |

Remove the row for the bare `spawn_agents` scope.

### §7.2 TTL Table

Replace the `spawn_agents` row:

| Scope | Maximum TTL |
|-------|-------------|
| `spawn_agents.create` | 300 seconds (5 minutes) |
| `spawn_agents.manage` | 300 seconds (5 minutes) |

### §9.3 Revocation Checking

`spawn_agents.create` and `spawn_agents.manage` fall under Tier 2 revocation
checking requirements (as defined by AIP-0002):

- Real-time Registry check on EVERY request
- MUST NOT cache revocation status
- DPoP proof-of-possession REQUIRED

### §17.1 Threat Model — New Threat Scenario

Add the following threat scenario:

> **TS-12 (Orchestrator Compromise Cascade).** A compromised orchestrator
> with `spawn_agents.create` capability uses its TTL window to register
> child agents before revocation propagates. Each child may itself hold
> `spawn_agents.create`, creating a self-replicating delegation tree.
>
> *Mitigation:* `spawn_agents.create` is classified as Tier 2, requiring
> real-time revocation check and DPoP at each spawn. Maximum TTL is 300
> seconds, limiting the window to 5 minutes. Child propagation via
> `propagate_to_children: true` (§9.3) remains the recovery mechanism
> for revoking the entire subtree.

### Normative Requirements

1. The bare scope `spawn_agents` MUST NOT appear in a Credential Token's
   `aip_scope` array. Validators MUST reject tokens containing it with
   error code `invalid_scope`.
2. `spawn_agents.create` MUST be classified as Tier 2.
3. `spawn_agents.manage` MUST be classified as Tier 2.
4. Maximum Credential Token lifetime for both sub-scopes MUST be 300
   seconds.
5. DPoP proof-of-possession [RFC9449] MUST be required for both
   sub-scopes.
6. Real-time revocation checking MUST be performed on every operation
   using either sub-scope.
7. Capability Manifest grants using the bare `spawn_agents` scope MUST
   be rejected at registration time. Registries MUST return
   `invalid_scope`.

### Failure Conditions

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| Token contains bare `spawn_agents` scope | `invalid_scope` | 400 |
| `spawn_agents.create` without DPoP proof | `dpop_required` | 401 |
| `spawn_agents.manage` without DPoP proof | `dpop_required` | 401 |
| Registry unreachable during spawn operation | `registry_unavailable` | 503 |
| Manifest submitted with bare `spawn_agents` | `invalid_scope` | 400 |

### Schema Changes

Update `spec/v0.3/schemas/capability-manifest.schema.json`: in the `scope`
enum (or pattern), replace `spawn_agents` with `spawn_agents.create` and
`spawn_agents.manage`. The bare `spawn_agents` value MUST be removed from
the valid scope list.

## Security Considerations

This proposal is a pure security improvement. It raises the security bar
for the highest-risk capability in the protocol:

- **Blast radius reduction:** The exploitation window drops from ~75
  minutes (3600s TTL + 15-min CRL) to ~5 minutes (300s TTL + real-time
  check).
- **DPoP binding:** Every spawn operation is now bound to key material,
  preventing stolen-token relay.
- **Scope separation:** Management operations (suspend, resume) are
  distinguished from creation operations, enabling finer-grained audit
  and revocation.

**No new threat vectors introduced.** The scope split reduces the attack
surface by allowing principals to grant `spawn_agents.manage` without
granting `spawn_agents.create`.

## Backwards Compatibility

Breaking change. Existing tokens and manifests containing the bare
`spawn_agents` scope are invalid under this proposal.

**Migration path:**

1. Replace `spawn_agents` with `spawn_agents.create` (if the agent needs
   to create new child agents) or `spawn_agents.manage` (if it only
   manages existing children), or both.
2. Update Credential Token TTL from 3600s to 300s for these scopes.
3. Enable DPoP proof generation for spawn operations.
4. Ensure real-time Registry connectivity for spawn operations.

No backwards-compatibility carve-out is provided. The bare `spawn_agents`
scope is retired immediately upon v0.3 adoption.

## Test Vectors

This proposal requires no new cryptographic test vectors. The scope
validation change is a string comparison. Conformance tests should verify:

1. A token with `spawn_agents` (bare) is rejected with `invalid_scope`.
2. A token with `spawn_agents.create` and TTL > 300s is rejected.
3. A token with `spawn_agents.create` without DPoP is rejected.
4. A manifest submitted with bare `spawn_agents` is rejected.

## Implementation Guidance

Orchestrators that create high volumes of ephemeral agents in tight loops
will need to manage DPoP proofs and 300-second credential refreshes per
spawn batch. This is operationally manageable and consistent with how
high-frequency financial transaction systems handle Tier 2 tokens.

For orchestrators that only need to manage existing children (suspend,
resume, update metadata), granting only `spawn_agents.manage` reduces the
security surface without requiring `spawn_agents.create` privileges.

## Alternatives Considered

**Move spawn_agents to Tier 2 without splitting.** This was the original
proposal in Issue #6. The split was adopted because it enables principals
to grant management-only access (lower risk) separately from creation
access (highest risk), following the principle of least privilege.

**Keep spawn_agents.manage at Tier 1.** Rejected per decision B-10: no
backwards-compatibility carve-out. Managing child agents (including
resuming suspended agents) has meaningful security implications that
warrant Tier 2 protections.

**Add a max_spawn_rate field instead.** Rate limiting at the manifest
level does not address the fundamental issue: CRL-based revocation is
too slow for this capability class.

## References

### Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.
              <https://www.rfc-editor.org/info/rfc2119>

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119
              Key Words", BCP 14, RFC 8174, May 2017.
              <https://www.rfc-editor.org/info/rfc8174>

   [RFC9449]  Fett, D., Campbell, B., Bradley, J., Lodderstedt, T.,
              Jones, M., and D. Waite, "OAuth 2.0 Demonstrating
              Proof of Possession (DPoP)", RFC 9449, September 2023.
              <https://www.rfc-editor.org/info/rfc9449>

### Informative References

   AIP-0002 — Reframe Tiers as threat-model declarations.

## Acknowledgements

Issue #6 analysis by @itisparas. OWASP LLM Top 10 discussion on
orchestrator blast radius informed the threat scenario.

## Changelog

- 2026-04-12 — Initial draft.
