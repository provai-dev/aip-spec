---
AIP: 0012
Title: Correct §14.6 graduated backoff formula
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 14.6
Requires: ~
Supersedes: ~
---

# AIP-0012: Correct §14.6 graduated backoff formula

## Abstract

This proposal fixes two defects in the §14.6 graduated backoff formula:
(1) `base_delay` conflates the exponential base with the `Retry-After`
floor, causing the geometric series to collapse; (2) jitter is tied to
`Retry-After`, producing unbounded variance. The corrected formula
separates `BACKOFF_BASE` (fixed exponential unit) from `Retry-After`
(mandatory floor).

## Motivation

The current formula `retry_delay = min(base_delay * 2^attempt, max_delay)
+ jitter` with `base_delay = max(Retry-After, 1)` and
`jitter = random(0, base_delay)` has two defects:

1. A server returning `Retry-After: 300` causes the client to use 300
   as the exponential base, reaching the 3600s cap in one attempt.
2. Jitter of up to 300s is added on top, defeating thundering-herd
   mitigation.

Two implementations following the current text verbatim produce retry
intervals that differ by orders of magnitude for the same 429 response.

Closes #18

## Terminology

This proposal introduces no new terms beyond those defined in the current
working-draft spec/vMAJOR.MINOR/aip-spec.md Section 3.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §14.6 Graduated Backoff Requirements (replacement text)

Replace the formula block with:

```
Implementations SHOULD use the following backoff formula:

  BACKOFF_BASE = 1         ; fixed exponential base, in seconds
  MAX_DELAY    = 3600      ; hard ceiling, in seconds

  computed_delay = min(BACKOFF_BASE * 2^attempt, MAX_DELAY)
  jitter         = random(0, BACKOFF_BASE)
  retry_delay    = max(computed_delay + jitter, Retry-After)
```

The `Retry-After` value from the 429 response acts as a mandatory
minimum: clients MUST NOT retry before `Retry-After` seconds have
elapsed, even if `computed_delay + jitter` is smaller. When no
`Retry-After` header is present, clients MUST treat it as 0 and rely
solely on the exponential formula.

The cease-retry threshold (5 attempts → 1 hour silence) is unchanged.

### Normative Requirements

1. `BACKOFF_BASE` MUST be a fixed constant (1 second), independent of
   `Retry-After`.
2. `jitter` MUST be bounded by `BACKOFF_BASE`, not by `Retry-After`.
3. `Retry-After` MUST be treated as a floor, not as an exponential base.

### Failure Conditions

No new error codes.

### Schema Changes

No schema changes.

## Security Considerations

The corrected formula reduces the risk of thundering-herd amplification
by ensuring jitter remains bounded. No new threat vectors introduced.

## Backwards Compatibility

Backwards compatible with caveat: implementations that interpreted the
original formula's intent (separating floor from base) are already
conformant. Implementations that followed the formula literally will
produce different retry intervals under the corrected formula.

## Test Vectors

| Attempt | Retry-After | computed_delay | jitter range | retry_delay range |
|---------|-------------|----------------|-------------|-------------------|
| 0 | 0 | 1 | [0, 1) | [1, 2) |
| 3 | 0 | 8 | [0, 1) | [8, 9) |
| 3 | 300 | 8 | [0, 1) | [300, 300) |
| 12 | 0 | 3600 | [0, 1) | [3600, 3601) |

## Implementation Guidance

Most implementations already separate `Retry-After` from the exponential
base. This errata makes that separation normative.

## Alternatives Considered

**Keep the formula and add a clarifying note.** Rejected because the
formula as written is unambiguously wrong; a note cannot fix it.

## References

### Normative References

   [RFC2119]  <https://www.rfc-editor.org/info/rfc2119>
   [RFC8174]  <https://www.rfc-editor.org/info/rfc8174>

## Changelog

- 2026-04-12 — Initial draft.
