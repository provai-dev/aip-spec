---
AIP: 0004
Title: Add aip_approval_step to Credential Token payload schema
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 4.2.3
Requires: ~
Supersedes: ~
---

# AIP-0004: Add aip_approval_step to Credential Token payload schema

## Abstract

The `aip_approval_step` claim is used in §4.6.8 (Step Execution Token) and
validated in Step 10a of the 12-step algorithm (§7.3), but it is not listed
in the §4.2.3 Credential Token payload fields table. This proposal adds it
to the formal schema, paired with `aip_approval_id`, ensuring that both
Approval Envelope claims are discoverable from the canonical claims table.

## Motivation

A reader consulting §4.2.3 to enumerate all possible Credential Token claims
will find `aip_approval_id` but not `aip_approval_step`. The claim only
appears in §4.6.8 (Step Execution Token example) and §7.3 Step 10a
(validation). This creates a gap: an implementer building a token parser
from the claims table alone will not allocate a field for `aip_approval_step`
and will fail validation at Step 10a.

Both claims are always used together — `aip_approval_id` identifies the
Approval Envelope, `aip_approval_step` identifies the step index within it.
They share identical conditionality (OPTIONAL in general, REQUIRED when the
token is a step-claim token). Listing one without the other is an editorial
omission.

## Terminology

This proposal introduces no new terms beyond those defined in the current
working-draft spec/vMAJOR.MINOR/aip-spec.md Section 3.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### Overview

Add one row to the §4.2.3 Credential Token Payload fields table.

### §4.2.3 Credential Token Payload — New Row

After the existing `aip_approval_id` row, add:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `aip_approval_step` | integer | OPTIONAL | Non-negative integer (0-indexed step position); REQUIRED when `aip_approval_id` is present; MUST correspond to a valid step index in the referenced Approval Envelope (see Section 4.6.8) |

### Normative Requirements

1. `aip_approval_step` MUST be present in the Credential Token payload
   if and only if `aip_approval_id` is present.
2. If `aip_approval_step` is present without `aip_approval_id`, or vice
   versa, validators MUST reject the token with `invalid_token`.
3. `aip_approval_step` MUST be a non-negative integer.
4. `aip_approval_step` MUST correspond to a valid step index in the
   Approval Envelope identified by `aip_approval_id`.
5. Validation of `aip_approval_step` is performed at Step 10a of the
   12-step algorithm (§7.3), which is unchanged by this proposal.

### Failure Conditions

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| `aip_approval_step` present without `aip_approval_id` | `invalid_token` | 401 |
| `aip_approval_id` present without `aip_approval_step` | `invalid_token` | 401 |
| `aip_approval_step` is not a non-negative integer | `invalid_token` | 401 |
| `aip_approval_step` exceeds step count in Approval Envelope | `approval_step_invalid` | 403 |

### Schema Changes

Update `spec/v0.3/schemas/credential-token.schema.json` to add
`aip_approval_step` as an optional integer field with `minimum: 0`.
Add a schema-level `if`/`then` constraint: if `aip_approval_id` is
present, `aip_approval_step` is required, and vice versa.

## Security Considerations

This proposal introduces no new threat vectors and does not alter any
existing security requirement. It formalises a claim that is already
validated at Step 10a. The pairing constraint (both present or both absent)
closes a minor ambiguity where a token could contain one claim without
the other.

## Backwards Compatibility

Fully backwards compatible. The `aip_approval_step` claim already exists
in the v0.2 specification at §4.6.8. This proposal only adds it to the
§4.2.3 claims table, making existing practice explicit. Existing valid
tokens are unaffected.

## Test Vectors

This proposal requires no new test vectors. The claim is already validated
at Step 10a; existing test coverage for Approval Envelope step verification
applies.

## Implementation Guidance

Implementers who built their token parser from the §4.2.3 claims table
should add `aip_approval_step` as an optional integer field. No logic
changes are required — the validation path at Step 10a is unchanged.

## Alternatives Considered

**Leave as-is with a cross-reference note.** Rejected because implementers
should not need to read §4.6.8 to discover a claim that appears in
Credential Tokens. The claims table in §4.2.3 is the canonical reference.

## References

### Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.
              <https://www.rfc-editor.org/info/rfc2119>

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119
              Key Words", BCP 14, RFC 8174, May 2017.
              <https://www.rfc-editor.org/info/rfc8174>

### Informative References

None.

## Acknowledgements

Identified during systematic review of §4.2.3 vs §4.6.8 cross-references.

## Changelog

- 2026-04-12 — Initial draft.
