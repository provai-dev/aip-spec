---
AIP: XXXX
Title: <Short descriptive title — imperative, 60 characters or fewer>
Author(s): Full Name <email@example.com> (@github-handle)
Status: Draft
Type: Standards Track
Created: YYYY-MM-DD
Last-Call-Ends: ~
Spec-Section: ~
Requires: ~
Supersedes: ~
---

# AIP-XXXX: <Title>

## Abstract

<!-- 3-5 sentences. What does this proposal specify? What problem does it solve?
     What systems does it apply to? A reader must understand the scope from this
     section alone without reading the rest of the document. -->

## Motivation

<!-- Why is the current specification insufficient? What real-world problem does
     this solve that cannot be addressed by an editorial fix?
     Link to the originating Idea issue: closes #<issue-number> -->

## Terminology

<!-- Define every new term introduced by this proposal using RFC 2119 style.
     If no new terms are introduced, write:
     "This proposal introduces no new terms beyond those defined in
     docs/aip-spec.md Section 3." -->

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

<!-- The normative content. Use RFC 2119 keywords throughout.
     Structure subsections to mirror the layout of docs/aip-spec.md so that
     integration is mechanical.

     For schema changes: include the full field table and a diff.
     For algorithm changes: include the complete updated pseudocode or ABNF.
     For new protocol flows: include numbered steps and a failure mode table. -->

### Overview

<!-- High-level description of the change. -->

### Normative Requirements

<!-- Bullet or numbered list of requirements using MUST/SHOULD/MAY.
     Each requirement must be independently verifiable by a relying party. -->

### Failure Conditions

<!-- Map each failure condition to the relevant AIP error code.
     Reference docs/aip-spec.md Section 13 (Error Handling). -->

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| | | |

### Schema Changes

<!-- If this proposal modifies any file in schemas/latest/, show the diff and
     include the updated $id version if the change is breaking. -->

## Security Considerations

<!-- Required for all Standards Track proposals. Address:
     (a) New threat vectors introduced by this change
     (b) Existing threats this proposal mitigates
     (c) Interaction with the AIP threat model in docs/aip-spec.md

     If this proposal has no security impact, write:
     "This proposal introduces no new threat vectors and does not alter any
     existing security requirement." -->

## Backwards Compatibility

<!-- Required. Choose one of three declarations:

     (a) Fully backwards compatible: existing valid tokens, registrations,
         delegation chains, and revocations remain valid under this change.

     (b) Backwards compatible with caveat: [describe what existing deployments
         must do or be aware of].

     (c) Breaking change: [justify the break and provide a complete migration
         path]. Identify the required spec version bump per VERSIONING.md. -->

## Test Vectors

<!-- Required for proposals that add or change a cryptographic operation,
     serialisation format, or validation algorithm.

     Format: input -> expected output, with encoding notes.
     Add vector files to testdata/ as: <component>_<scenario>.json

     If not applicable, write:
     "This proposal requires no new test vectors." -->

## Implementation Guidance

<!-- Optional. Informative notes for implementers. This section is NOT normative.
     Pointers to reference code or SDK support are welcome here. -->

## Alternatives Considered

<!-- What other designs were evaluated and why were they not chosen?
     This section prevents re-litigating the design space during review. -->

## References

### Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.
              <https://www.rfc-editor.org/info/rfc2119>

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119
              Key Words", BCP 14, RFC 8174, May 2017.
              <https://www.rfc-editor.org/info/rfc8174>

### Informative References

<!-- References cited for context or background only. -->

## Acknowledgements

<!-- Credit reviewers and others who shaped this proposal. -->

## Changelog

- YYYY-MM-DD — Initial draft.
