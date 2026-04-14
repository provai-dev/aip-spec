---
AIP: 0016
Title: New threat scenarios TS-12, TS-13, TS-14
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 17.1
Requires: 0003, 0007, 0008
Supersedes: ~
---

# AIP-0016: New threat scenarios TS-12, TS-13, TS-14

## Abstract

This proposal adds three new threat scenarios to §17.1 (Threat Model)
covering: orchestrator compromise cascade (TS-12), overlay manipulation
(TS-13), and engagement state tampering (TS-14).

## Motivation

v0.3 introduces new attack surfaces via `spawn_agents` promotion
(AIP-0003), Capability Overlays (AIP-0007), and Engagement Objects
(AIP-0008). The §17.1 threat model must be updated to document these
threats and their mitigations.

## Terminology

This proposal introduces no new terms.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §17.1 Threat Model — New Scenarios

Add after the existing threat scenarios:

> **TS-12 (Orchestrator Compromise Cascade).** A compromised
> orchestrator with `spawn_agents.create` capability uses its TTL
> window to register child agents before revocation propagates. Each
> child may itself hold `spawn_agents.create`, creating a
> self-replicating delegation tree.
>
> *Mitigation:* `spawn_agents.create` is classified as Tier 2
> (AIP-0003), requiring real-time revocation check, DPoP, and 300s
> max TTL. Child propagation via `propagate_to_children: true` (§9.3)
> revokes the entire subtree.
>
> **TS-13 (Capability Overlay Injection).** An attacker attempts to
> submit a forged Capability Overlay to the Registry, expanding an
> agent's effective permissions beyond the base Capability Manifest.
>
> *Mitigation:* Rule CO-1 (AIP-0007) enforces attenuation only — the
> Registry rejects any overlay that expands beyond the base manifest.
> Overlay signature verification against the issuer's DID key prevents
> forgery. The `issued_by` DID must be `did:web` or `did:aip` (not
> `did:key`), ensuring issuer identity is verifiable and rotatable.
>
> **TS-14 (Engagement State Tampering).** An attacker attempts to
> modify a completed change log entry in an Engagement Object to
> retroactively alter the participant roster or approval gate status.
>
> *Mitigation:* The change log is append-only with monotonic sequence
> numbers (AIP-0008 §4.8.3). Each entry is independently signed by
> the actor's DID key. The Registry rejects modifications with
> `change_log_immutable`. Auditors can reconstruct and verify the
> full engagement history from the signed change log.

### Normative Requirements

1. §17.1 MUST include threat scenarios for all new v0.3 attack surfaces.
2. Each threat scenario MUST reference its mitigation mechanism and
   source AIP.

### Failure Conditions

No new error codes.

### Schema Changes

No schema changes.

## Security Considerations

This proposal documents threats; it does not introduce new mechanisms.
The mitigations are defined in AIP-0003, AIP-0007, and AIP-0008.

## Backwards Compatibility

Fully backwards compatible. Threat model additions are informative.

## Test Vectors

This proposal requires no new test vectors.

## References

### Normative References

   [RFC2119]  <https://www.rfc-editor.org/info/rfc2119>
   [RFC8174]  <https://www.rfc-editor.org/info/rfc8174>

### Informative References

   AIP-0003 — spawn_agents split.
   AIP-0007 — Capability Overlays.
   AIP-0008 — Engagement Objects.

## Changelog

- 2026-04-12 — Initial draft.
