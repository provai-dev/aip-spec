## PR Type

<!-- Check all that apply -->
- [ ] Proposal document (new or updated `proposals/XXXX-slug/`)
- [ ] Proposal-to-spec integration (merging an Accepted AIP into `spec/vMAJOR.MINOR/aip-spec.md`)
- [ ] Normative spec change (direct edit to `spec/vMAJOR.MINOR/aip-spec.md`)
- [ ] Editorial (`[EDITORIAL]` prefix — no normative impact)
- [ ] JSON Schema change (`spec/vMAJOR.MINOR/schemas/`)
- [ ] Test vector / conformance suite
- [ ] Governance / process document
- [ ] CI / tooling

---

## Summary

<!-- One paragraph: what does this PR do and why? -->

---

## Linked Issue

Closes #<!-- issue number — required for all non-editorial PRs -->

---

## Proposal Lifecycle Stage

<!-- Fill in only if PR Type includes "Proposal document". -->

- [ ] Draft — iterating on feedback
- [ ] Requesting Last Call — I believe no blocking objections remain (tag `@aip-editors`)
- [ ] Last Call active — ends: YYYY-MM-DD
- [ ] Accepted — ready for spec integration

---

## Spec Sections Affected

<!-- List every section of spec/vMAJOR.MINOR/aip-spec.md that is normatively
     changed. Use section numbers: e.g., "Section 7.3 — Token Validation"
     Leave blank for editorial-only PRs. -->

---

## Normative-Language Checklist

> Required for any PR that modifies normative content in `spec/vMAJOR.MINOR/aip-spec.md`.

- [ ] All new requirements use RFC 2119 / BCP 14 keywords correctly (MUST / SHOULD / MAY)
- [ ] No new requirement conflicts with an existing normative statement
- [ ] All new MUST statements reference the relevant AIP error code from
      `spec/vMAJOR.MINOR/aip-spec.md` Section 13 (Error Handling)
- [ ] If a MUST is added, a corresponding test vector is included in the proposal
      or an issue is filed to track it

---

## Schema Checklist

> Required when `spec/vMAJOR.MINOR/schemas/` files are modified.

- [ ] Schema `$id` is unchanged for backwards-compatible additions
- [ ] Breaking schema changes bump the `$id` version
- [ ] The corresponding spec section in `spec/vMAJOR.MINOR/aip-spec.md`
      references the updated schema path
- [ ] `additionalProperties: false` is preserved where the spec requires it
- [ ] `$comment` field updated if the schema description changed

---

## Security Checklist

> Required for any change affecting authentication, cryptography, DPoP,
> delegation, revocation, or key management.

- [ ] Change reviewed against the AIP threat model (`spec/vMAJOR.MINOR/aip-spec.md`
      § 16 — Security Considerations)
- [ ] DPoP proof-of-possession construction and validation are unaffected or
      explicitly updated
- [ ] No algorithm agility holes introduced; prohibited algorithms remain
      rejected
- [ ] Delegation scope rules (D-1 through D-5) are respected or explicitly
      modified with justification

---

## Backward Compatibility

- [ ] **Non-breaking** — existing valid tokens, registrations, delegation
      chains, and revocations remain valid under this change
- [ ] **Breaking** — migration path described below; VERSIONING.md version
      bump identified

<!-- If breaking: describe what changes and how implementations should migrate -->

---

## Spec Consistency

- [ ] All internal section cross-references in `spec/vMAJOR.MINOR/aip-spec.md`
      still resolve after this change
- [ ] Table of Contents in `spec/vMAJOR.MINOR/aip-spec.md` updated if sections were added
      or renamed
- [ ] `AIP_INDEX.md` reflects current proposal status (CI will verify)
- [ ] README.md links are still accurate

---

## DCO Sign-off

- [ ] All commits in this PR include `Signed-off-by: Full Name <email>`
      (added automatically with `git commit -s`)

---

## Co-authors

<!-- Credit additional authors, one per line. Optional if sole author. -->

Co-authored-by: NAME <email@example.com>
