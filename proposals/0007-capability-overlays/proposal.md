---
AIP: 0007
Title: Capability Overlays — third-party scope narrowing
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 4.7, 7.3, 15.1
Requires: ~
Supersedes: ~
---

# AIP-0007: Capability Overlays — third-party scope narrowing

## Abstract

This proposal introduces Capability Overlays (§4.7) — signed documents
that allow a third party (e.g., a hiring operator in a cross-operator
engagement) to narrow an agent's effective capabilities without touching
the delegation chain. Overlays are stored in the Registry, signed by the
issuer's DID key, and applied at validation Step 9e as an intersection
with the base Capability Manifest. Rule CO-1 guarantees that overlays
can only attenuate, never expand.

## Motivation

The v0.2 Capability Manifest is monolithic and principal-signed at
registration time. In cross-operator scenarios, a hiring operator needs to
narrow an external agent's permissions mid-engagement — e.g., removing
access to a data source on day 3 of a 14-day assignment. The only current
options are full revocation (`scope_revoke` in §9.1, which is permanent)
or becoming part of the delegation chain (which conflates trust
relationships).

Capability Overlays provide a non-destructive, temporary, third-party
attenuation mechanism that preserves the delegation chain's integrity.

Closes #9

## Terminology

**Capability Overlay** — A Registry-stored, issuer-signed document that
restricts an agent's effective capability set for a specific engagement
or issuer context. Overlays apply the intersection of the base manifest
and overlay constraints.

**Overlay Issuer** — The party that signs and submits a Capability
Overlay. The issuer MUST use `did:web` or `did:aip` (not `did:key`).

**Effective Capability Set** — The intersection of the base Capability
Manifest and all active overlays applicable to the current validation
context.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §4.7 Capability Overlays (new section)

#### 4.7.1. Overview

A Capability Overlay is a signed restriction document stored in the
Registry. It narrows an agent's effective capability set for operations
within a specific engagement or issuer context.

**Rule CO-1 (Attenuation Only):** An overlay MUST NOT expand any
constraint value beyond what the base Capability Manifest permits. The
effective capability set is always the intersection of the base manifest
and all active overlays scoped to the engagement or issuer.

#### 4.7.2. Overlay Schema

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `overlay_id` | string | REQUIRED | Pattern: `^co:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
| `aid` | string | REQUIRED | The target agent's AID |
| `engagement_id` | string | OPTIONAL | Pattern: `^eng:[0-9a-f]{8}-...` (UUID v4 with `eng:` prefix); links to Engagement Object (AIP-0008) |
| `issued_by` | string | REQUIRED | DID of the overlay issuer; MUST be `did:web` or `did:aip` (MUST NOT be `did:key`) |
| `overlay_type` | string | REQUIRED | MUST be `"restrict"` |
| `issued_at` | string | REQUIRED | ISO 8601 UTC timestamp |
| `expires_at` | string | REQUIRED | ISO 8601 UTC timestamp; MUST be strictly after `issued_at` |
| `version` | integer | REQUIRED | Positive integer; monotonically increasing per `(aid, engagement_id, issued_by)` tuple |
| `constraints` | object | REQUIRED | Uses the same schema as Capability Manifest `capabilities` sub-object |
| `signature` | string | REQUIRED | Base64url EdDSA signature by `issued_by` over JCS canonical JSON (RFC 8785) of the document excluding the `signature` field |

#### 4.7.3. Overlay Rules

1. **CO-1 (Attenuation Only):** For every field in `constraints`, the
   value MUST be equal to or more restrictive than the corresponding
   value in the base Capability Manifest. The Registry MUST reject
   overlays that violate CO-1 with `overlay_exceeds_manifest`.

2. **CO-2 (Issuer DID Method):** The `issued_by` DID MUST use `did:web`
   or `did:aip`. Overlays signed by `did:key` MUST be rejected with
   `overlay_issuer_invalid`.

3. **CO-3 (Version Monotonicity):** A new overlay for the same
   `(aid, engagement_id, issued_by)` tuple MUST have a strictly higher
   `version` than the current active overlay. The new version replaces
   the previous one atomically. The Registry MUST reject downgrades
   with `overlay_version_conflict`.

4. **CO-4 (Expiry Handling):** Expired overlays MUST be treated as
   absent. When an overlay expires, the base Capability Manifest applies
   without restriction for that issuer/engagement context. Overlays MUST
   NOT be treated as "full capability restored" — they simply cease to
   apply.

5. **CO-5 (Engagement Termination):** If an Engagement Object (AIP-0008)
   associated with an overlay's `engagement_id` is terminated, all
   overlays for that engagement MUST be invalidated atomically by the
   Registry.

6. **CO-6 (Multiple Overlays):** When multiple overlays apply to the
   same agent (different issuers or engagements), the effective
   capability set is the intersection of ALL applicable overlays with
   the base manifest.

#### 4.7.4. Effective Capability Computation

The effective capability set for a validation context is computed as:

```
effective = base_manifest.capabilities
for each active_overlay in applicable_overlays:
    effective = intersect(effective, active_overlay.constraints)
```

Where `intersect` applies per-field:
- Boolean fields: `effective = base AND overlay` (false wins)
- Numeric limits: `effective = min(base, overlay)`
- Path arrays: `effective = intersection(base_paths, overlay_paths)`
- Scope removal: if overlay sets a scope to `false`, that scope is
  removed from the effective set

### §7.3 Step 9e — Overlay Application (new sub-step)

Insert after Step 9d:

> **Step 9e — Capability Overlay application (conditional).**
> If the Relying Party is aware of active Capability Overlays for the
> agent (fetched from `GET /v1/agents/{aid}/overlays`), compute the
> effective capability set per §4.7.4. Validate `aip_scope` against
> the effective capability set instead of the base manifest. Fail:
> `insufficient_scope`.
>
> Relying Parties SHOULD fetch overlays for Tier 2 operations. For
> Tier 1, overlay checking is OPTIONAL.

### §15.1 Required Endpoints — New Overlay Endpoints

Add to the required endpoints table:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/agents/{aid}/overlays` | Submit a Capability Overlay |
| `GET` | `/v1/agents/{aid}/overlays` | List active overlays for an agent |
| `GET` | `/v1/agents/{aid}/overlays/{overlay_id}` | Retrieve specific overlay |
| `DELETE` | `/v1/agents/{aid}/overlays/{overlay_id}` | Revoke an overlay (issuer only) |

The `POST` endpoint MUST verify:
1. The overlay signature against the `issued_by` DID's public key.
2. Rule CO-1 (attenuation only) against the agent's current base
   Capability Manifest.
3. Version monotonicity (CO-3).

### Normative Requirements

1. Capability Overlays MUST NOT expand capabilities beyond the base
   Capability Manifest (Rule CO-1).
2. Overlay issuers MUST use `did:web` or `did:aip` (Rule CO-2).
3. Overlay versioning MUST be monotonically increasing (Rule CO-3).
4. Expired overlays MUST be treated as absent (Rule CO-4).
5. Engagement termination MUST invalidate associated overlays (Rule CO-5).
6. Multiple overlays MUST be applied as intersection (Rule CO-6).
7. Relying Parties SHOULD apply overlays for Tier 2 operations.

### Failure Conditions

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| Overlay violates CO-1 (expands beyond manifest) | `overlay_exceeds_manifest` | 400 |
| Overlay issuer uses `did:key` | `overlay_issuer_invalid` | 400 |
| Overlay version not strictly increasing | `overlay_version_conflict` | 409 |
| Overlay signature verification failure | `overlay_signature_invalid` | 400 |
| Scope denied by effective capability set | `insufficient_scope` | 403 |

### Schema Changes

Create `spec/v0.3/schemas/capability-overlay.schema.json` with the
fields defined in §4.7.2.

## Security Considerations

**Attenuation guarantee (CO-1):** The overlay can only restrict, never
expand. This preserves the monotonic attenuation guarantee of the
delegation chain. The Registry enforces CO-1 at submission time, and
Relying Parties verify it at validation time.

**Overlay injection:** A malicious agent cannot inject false overlays
because overlays are stored in the Registry and fetched independently
by the Relying Party. Overlays are not carried in the Credential Token.

**Issuer trust:** The Relying Party must resolve the `issued_by` DID
independently to verify the overlay signature. This is the same
resolution path used for the root principal in Step 8d. Only `did:web`
and `did:aip` are permitted, ensuring the issuer has a verifiable,
rotatable identity.

**Overlay expiry:** Expired overlays are treated as absent (not as
unrestricted). This prevents a denial-of-service where an attacker
creates overlays with past expiry dates to bypass capability checks.

**Engagement termination interaction:** When an Engagement Object is
terminated, all associated overlays are invalidated atomically. This
prevents stale overlays from persisting after the engagement ends.

## Backwards Compatibility

Fully backwards compatible. Capability Overlays are a new feature;
existing tokens, manifests, and validation flows are unaffected. Relying
Parties that do not fetch overlays will validate against the base manifest
only (the v0.2 behaviour).

## Test Vectors

This proposal requires no new cryptographic test vectors. Conformance
tests should verify:

1. An overlay that expands a capability beyond the base manifest is
   rejected (CO-1 enforcement).
2. An overlay signed by a `did:key` issuer is rejected.
3. An overlay with version ≤ current active version is rejected.
4. An expired overlay is treated as absent (base manifest applies).
5. Multiple overlays produce the correct intersection.

## Implementation Guidance

**For hiring operators:** Create a Capability Overlay when onboarding an
external agent. Set `engagement_id` to link the overlay to the
Engagement Object. Update the overlay (increment version) to adjust
permissions mid-engagement. Delete the overlay or let it expire when
the engagement ends.

**For Registry implementers:** Store overlays indexed by `(aid,
engagement_id, issued_by)`. Enforce CO-1 at submission time by comparing
each constraint field against the base manifest. Implement atomic
replacement on version update.

**For Relying Party implementers:** Fetch overlays at Step 9e for Tier 2
operations. Cache overlay responses for at most 60 seconds. Apply the
intersection algorithm in §4.7.4.

## Alternatives Considered

**Embed overlay in the Credential Token.** Rejected because the agent
controls the token content. Overlays must be stored externally to prevent
the agent from omitting or tampering with them.

**Use scope_revoke for temporary restrictions.** Rejected because
`scope_revoke` is permanent and irreversible. Overlays are temporary
and versioned.

**Extend the delegation chain with a "restrictor" token.** Rejected
because it conflates trust relationships. The hiring operator is not
part of the delegation chain; they should not need to become one to
apply constraints.

## References

### Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.
              <https://www.rfc-editor.org/info/rfc2119>

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119
              Key Words", BCP 14, RFC 8174, May 2017.
              <https://www.rfc-editor.org/info/rfc8174>

   [RFC8785]  Rundgren, A., Jordan, B., and S. Erdtman, "JSON
              Canonicalization Scheme (JCS)", RFC 8785, June 2020.
              <https://www.rfc-editor.org/info/rfc8785>

### Informative References

   AIP-0008 — Engagement Objects (engagement lifecycle and overlay
   termination interaction).

## Acknowledgements

Design informed by production operator feedback on cross-operator
capability management in [w3c/did-use-cases#155](https://github.com/w3c/did-use-cases/issues/155).

## Changelog

- 2026-04-12 — Initial draft.
