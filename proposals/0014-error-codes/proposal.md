---
AIP: 0014
Title: Consolidate new error codes for v0.3 features
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 13.2
Requires: 0002, 0003, 0005, 0006, 0007, 0008, 0009, 0010
Supersedes: ~
---

# AIP-0014: Consolidate new error codes for v0.3 features

## Abstract

This proposal consolidates all new error codes introduced by AIP-0002
through AIP-0010 into a single addition to §13.2 (Error Handling). It
ensures every new MUST/MUST NOT requirement has a corresponding error
code and that no duplicate or conflicting codes exist.

## Motivation

Each v0.3 proposal defines its error codes inline. This consolidation
ensures the §13.2 error code table is complete, non-overlapping, and
consistently formatted.

## Terminology

This proposal introduces no new terms.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §13.2 Error Handling — New Error Codes

Add the following to the error code table:

| Error Code | HTTP Status | Source AIP | Description |
|------------|-------------|-----------|-------------|
| `revocation_stale` | 403 | 0002 | Tier 2 operation with cached revocation status |
| `dpop_required` | 401 | 0002 | Tier 2 operation without DPoP proof |
| `mtls_required` | 403 | 0002 | Tier 3 operation without mTLS |
| `invalid_scope` | 400 | 0003 | Token contains retired bare `spawn_agents` scope |
| `principal_did_method_forbidden` | 403 | 0005 | Principal uses `did:key` for Tier 2 scope |
| `identity_proofing_insufficient` | 403 | 0005 | G3 identity proofing below requested `acr_values` |
| `grant_not_found` | 404 | 0005 | G1 `grant_id` not found or expired |
| `grant_deployer_mismatch` | 403 | 0005 | G1 `grant_id` does not match deployer |
| `pkce_required` | 400 | 0005 | G3 authorization request missing PKCE |
| `registry_untrusted` | 403 | 0006 | Registry does not match principal DID-Document-declared Registry |
| `overlay_exceeds_manifest` | 400 | 0007 | Overlay violates CO-1 attenuation rule |
| `overlay_issuer_invalid` | 400 | 0007 | Overlay issuer uses `did:key` |
| `overlay_version_conflict` | 409 | 0007 | Overlay version not strictly increasing |
| `overlay_signature_invalid` | 400 | 0007 | Overlay signature verification failure |
| `engagement_terminated` | 403 | 0008 | Engagement has been terminated or completed |
| `engagement_suspended` | 403 | 0008 | Engagement is currently suspended |
| `engagement_participant_removed` | 403 | 0008 | Agent removed from engagement |
| `engagement_gate_pending` | 403 | 0008 | Required approval gate not yet approved |
| `engagement_not_found` | 404 | 0008 | Engagement ID not found |
| `engagement_countersign_required` | 400 | 0008 | Missing required countersignature |
| `change_log_immutable` | 400 | 0008 | Attempt to modify change log entry |
| `change_log_sequence_invalid` | 400 | 0008 | Out-of-sequence change log append |
| `subscription_auth_required` | 401 | 0009 | RPNP subscription without DPoP |
| `invalid_webhook_uri` | 400 | 0009 | Webhook URI not HTTPS |
| `subscription_limit_exceeded` | 429 | 0009 | RPNP subscription limit reached |
| `invalid_target` | 400 | 0010 | Token exchange resource not registered |

### Normative Requirements

1. Every error code MUST be unique across the entire §13.2 table.
2. Each error code MUST map to exactly one HTTP status code.
3. Implementations MUST return the specified HTTP status code for each
   error condition.

### Failure Conditions

This proposal defines error codes; it introduces no additional failure
conditions beyond those already specified in AIP-0002 through AIP-0010.

### Schema Changes

No schema changes.

## Security Considerations

Consistent error codes prevent information leakage from ambiguous error
responses. Each error code is specific enough for debugging but does
not reveal internal state.

## Backwards Compatibility

Breaking change: new error codes are introduced. Existing implementations
will not return these codes until they implement the corresponding v0.3
features.

## Test Vectors

This proposal requires no new test vectors.

## References

### Normative References

   [RFC2119]  <https://www.rfc-editor.org/info/rfc2119>
   [RFC8174]  <https://www.rfc-editor.org/info/rfc8174>

## Changelog

- 2026-04-12 — Initial draft.
