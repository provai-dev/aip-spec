---
AIP: 0015
Title: Version bump to 0.3 and compatibility rules
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 16
Requires: 0002, 0003, 0005
Supersedes: ~
---

# AIP-0015: Version bump to 0.3 and compatibility rules

## Abstract

This proposal updates §16 (Versioning and Compatibility) to document
the version bump from v0.2 to v0.3, enumerate all breaking changes, and
define backward-compatibility rules for validators handling v0.2 tokens.

## Motivation

v0.3 introduces breaking changes (AIP-0003 `spawn_agents` retirement,
AIP-0005 `grant_tier` field, AIP-0006 Registry Trust Anchoring). §16
must be updated to document these changes, specify `aip_version: "0.3"`,
and define how validators handle v0.2 tokens during the transition.

## Terminology

This proposal introduces no new terms.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §16 Versioning and Compatibility (replacement text)

Replace the current §16 content with:

> AIP follows Semantic Versioning. Before v1.0, MINOR versions MAY
> include breaking changes. v0.2 and v0.3 are partially compatible:
> validators SHOULD accept `aip_version: "0.2"` tokens with the
> following caveats:
>
> - `aip_version: "0.2"` tokens may contain the bare `spawn_agents`
>   scope. Validators SHOULD treat this as `spawn_agents.create` for
>   backward compatibility but MUST log a deprecation warning.
> - `aip_version: "0.2"` Registration Envelopes do not include
>   `grant_tier`. Validators SHOULD treat absent `grant_tier` as
>   `"G2"` during the transition period.
> - `aip_version: "0.2"` Principal Tokens do not include `acr`/`amr`
>   claims. Validators MUST treat their absence as non-applicable.
> - Validators receiving `aip_version: "0.2"` from agents that should
>   be on v0.3 SHOULD log a warning.
> - Step 6a (Registry Trust Anchoring) MAY be skipped for
>   `aip_version: "0.2"` tokens.
>
> Breaking changes from v0.2:
>
> - `aip_version` is now `"0.3"` for conforming implementations.
> - `X-AIP-Version: 0.3` replaces `X-AIP-Version: 0.2`.
> - The bare `spawn_agents` scope is retired; use
>   `spawn_agents.create` and `spawn_agents.manage` (AIP-0003).
> - Registration Envelopes MUST include `grant_tier` (AIP-0005).
> - Principal DID Documents for Tier 2 agents MUST include an
>   `AIPRegistry` service entry (AIP-0006).
> - The `/.well-known/aip-registry` response MUST include
>   `signature`, `registry_name`, and `endpoints` (AIP-0006).
> - §14.6 backoff formula corrected (AIP-0012).
>
> Implementations MUST NOT silently accept tokens from unsupported
> versions without logging a version warning.

### §16.1 Tier Conformance

Tier conformance table as defined by AIP-0002 (included in that
proposal; this proposal cross-references it).

### Normative Requirements

1. `aip_version` MUST be `"0.3"` for tokens conforming to this version.
2. `X-AIP-Version` header value MUST be `"0.3"`.
3. All breaking changes listed above MUST be implemented.

### Failure Conditions

No new error codes beyond those in AIP-0014.

### Schema Changes

Update `aip_version` enum in all schemas from `"0.2"` to `"0.3"`.

## Security Considerations

The transition period allowing v0.2 tokens introduces a window where
deprecated features (bare `spawn_agents`, absent `grant_tier`) are
accepted. Validators MUST log deprecation warnings to ensure operators
are aware of the transition.

## Backwards Compatibility

Breaking change per VERSIONING.md §3 (MINOR version with breaking
changes, permitted pre-v1.0).

## Test Vectors

This proposal requires no new test vectors.

## References

### Normative References

   [RFC2119]  <https://www.rfc-editor.org/info/rfc2119>
   [RFC8174]  <https://www.rfc-editor.org/info/rfc8174>

### Informative References

   AIP-0002, AIP-0003, AIP-0005, AIP-0006, AIP-0012.

## Changelog

- 2026-04-12 — Initial draft.
