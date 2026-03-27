# AIP Governance

## 1. Purpose and Authority

This document defines the operational procedures for the AIP working group:
roles, responsibilities, the proposal lifecycle, decision-making rules, and
conflict resolution.

This document is subordinate to [CHARTER.md](CHARTER.md), which defines the
working group's mission, scope, and intellectual property policy. In any
conflict between this document and CHARTER.md, CHARTER.md governs.

All participants are subject to the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 2. Roles

### Contributor

Anyone who opens an issue, submits a pull request, or participates in a
discussion in this repository. No special permissions required. Contributors
must sign off commits with the DCO (see [CONTRIBUTING.md](CONTRIBUTING.md)).
Recognised in [CONTRIBUTORS.md](CONTRIBUTORS.md) once their first contribution
is merged.

### Reviewer

A Contributor who has demonstrated sustained, high-quality engagement with
proposals or spec review. Reviewers may approve — but not merge — pull requests.
Reviewers may call for Last Call on a Draft proposal (see § 4).

**Appointment:** Any Editor may grant Reviewer status by opening a pull request
adding the nominee to [EDITORS.md](EDITORS.md) with a written endorsement.
No vote is required; the PR can be merged by any other Editor.

### Editor

Editors are the technical stewards of the specification. They are accountable
for specification quality, correctness, and consistency.

**Editors may:**
- Merge pull requests
- Assign AIP numbers to Draft proposals
- Declare Last Call on a proposal
- Accept or reject proposals
- Cut new spec versions
- Grant or revoke Reviewer status

**Editors are expected to:**
- Provide initial feedback on new PRs within 14 calendar days
- Respond to assigned review requests within 21 calendar days
- Participate in formal votes within 7 calendar days

Failure to engage for more than 60 consecutive calendar days without prior
notice triggers escalation to the full Editor body (see § 6 Conflict
Resolution).

**Appointment:** See § 5.

### The Editor Body

All current Editors acting collectively constitute the governing authority for
decisions that affect the specification or governance. No individual Editor acts
alone on decisions that require a vote. The Editor body operates by consensus
first; formal votes are the fallback (see § 3).

The Editor body must always contain at least two Editors. If it falls to one,
that remaining Editor must immediately begin an appointment process.

---

## 3. Authoritative Source of Truth

`docs/aip-spec.md` is the **canonical AIP specification**.

The files in `spec/latest/` are deprecated working drafts retained for
historical reference only. They MUST NOT be modified (except to maintain their
deprecation notices) and MUST NOT be cited as normative references in proposals
or implementations.

All proposals, PRs, and normative references MUST cite section numbers from
`docs/aip-spec.md`.

---

## 4. Proposal Lifecycle

All normative changes to the specification originate as proposals. The lifecycle
has seven states:

### 4.1 Idea

An **Idea** is a GitHub issue filed using the
[New Proposal](/.github/ISSUE_TEMPLATE/new-proposal.yaml) template. Ideas have
no AIP number. The purpose of an Idea is to establish community interest and
editorial appetite before the author invests effort in a full proposal.

- An Idea remains open for a minimum of **7 calendar days**.
- Any Editor or Reviewer may comment "proceed" to signal the idea is worth a
  formal proposal.
- If no Editor or Reviewer engages within 30 days, the issue is labeled `stale`
  and closed after 45 days with an invitation to re-open.

### 4.2 Draft

A **Draft** is a formal proposal submitted as a pull request adding a
`proposals/XXXX-slug/proposal.md` file.

- The handling Editor assigns an AIP number (sequential, never reused).
- The PR title MUST match `[AIP-XXXX] Short descriptive title`.
- A Draft has no deadline. The author iterates based on review feedback.
- Authors should respond to review comments within **14 calendar days**. PRs
  with no author response for 30 days are labeled `stale` and closed after
  45 days with an invitation to reopen.

### 4.3 Last Call

**Last Call** is a public notice that a Draft is considered ready for
acceptance, inviting the community to raise any remaining blocking objections.

Last Call may be declared by any Editor or Reviewer when:
- All previously raised blocking objections are resolved
- The Security Considerations section is complete and non-trivial
- The Backwards Compatibility section declares one of: fully compatible,
  compatible with caveat, or breaking change with migration path
- The Specification section uses RFC 2119 language throughout

**Process:**
1. The declaring party adds the `last-call` label and posts a pinned comment
   stating the Last Call end date (today + 14 calendar days).
2. An announcement is posted in the GitHub Discussions announcement category.
3. During Last Call, only **blocking objections** (new normative issues,
   security issues, backwards-compat regressions) prevent acceptance.
4. If a blocking objection is raised, the proposal returns to Draft. Last Call
   must be re-declared after resolution.

### 4.4 Accepted

After Last Call expires with no unresolved blocking objections:

1. An Editor updates the `Status` frontmatter to `Accepted` and merges the PR.
2. The Editor integrates the proposal text into `docs/aip-spec.md` in the same
   commit or a fast-follow PR opened within 7 days.
3. CI regenerates `AIP_INDEX.md`.

### 4.5 Rejected

An Editor may reject a proposal at any stage if:
- It is demonstrably out of scope per [CHARTER.md § 2](CHARTER.md#2-scope)
- It introduces unmitigated security risks the author is unable or unwilling
  to address
- No Editor is willing to champion it after **90 days** in Draft

Rejection MUST include a written rationale. The rationale is permanent record.

A rejected proposal may be resubmitted only if it substantively addresses the
rejection rationale. The new submission receives a new AIP number.

### 4.6 Withdrawn

An author may withdraw at any time by commenting "withdrawing" in the PR. The
handling Editor updates the `Status` to `Withdrawn`, moves the directory to
`proposals/withdrawn/XXXX-slug/`, and closes the PR.

### 4.7 Superseded

When an Accepted proposal is replaced by a later one, the older proposal's
`Status` is updated to `Superseded` and a `Superseded-By: AIP-YYYY` field is
added. Proposal documents are never deleted.

---

## 5. Editor Appointment

**Nomination:** Any Editor may nominate a Contributor or Reviewer by opening a
PR to [EDITORS.md](EDITORS.md) with: the nominee's GitHub handle, linked
contributions, a written endorsement, and confirmation the nominee has agreed.

**Approval:** Simple majority of current Editors (excluding the nominator)
within 14 calendar days.

**Resignation:** An Editor opens a PR removing themselves from EDITORS.md. Any
other Editor may merge it.

**Removal:** Two-thirds super-majority of remaining Editors, triggered by
sustained non-responsiveness (60+ days) or a CODE_OF_CONDUCT.md violation.
The subject Editor must be notified privately and given 7 days to respond or
resign voluntarily before the removal PR is opened.

**Lead Editor:** The Editor body may optionally designate one Editor as Lead
Editor in EDITORS.md. The Lead Editor serves as tie-breaker in formal votes
and primary public contact. The role may be vacant.

---

## 6. Decision-Making

### Consensus (Default)

The default is **rough consensus** per IETF RFC 7282. A single sustained
objection does not block if it has been thoroughly heard and the remaining
Editor body judges it unpersuasive. Silence is not consent.

### Formal Vote (Fallback)

Any Editor may call a formal vote by posting "calling formal vote" in the
relevant thread. Votes are open for 7 calendar days; only Editors vote.

| Threshold | Applies to |
|-----------|-----------|
| Simple majority (>50%) | Proposal acceptance/rejection, Reviewer appointments, editorial decisions, this document's amendments |
| Two-thirds super-majority | Breaking normative changes, CHARTER.md amendments, Editor removal, v1.0 stability declaration |

**Tie-breaking:** The Lead Editor casts the deciding vote. If there is no Lead
Editor, the proposal is deferred 30 days and re-voted. If it ties again, it is
rejected without prejudice.

### Off-Repo Decisions Prohibited

No normative decision may be made outside public GitHub threads. Any decision
reached informally MUST be confirmed in a GitHub issue or PR comment before it
is binding.

---

## 7. Conflict Resolution

| Tier | Mechanism | Timeline |
|------|-----------|----------|
| 1 | Direct resolution in the issue/PR thread | No deadline |
| 2 | Editor mediation — tag `@aip-editors`; Editor acknowledges within 7 days | 21 days to resolution |
| 3 | Formal vote — outcome is final and documented | 7-day vote window |

There is no appeal above Tier 3 short of a new proposal to amend this document.

---

## 8. Release Authority

Only the Editor body acting collectively may:
- Declare a proposal Accepted
- Cut a new spec version and create `spec/vMAJOR.MINOR/`
- Declare a version stable (super-majority required for v1.0)
- Deprecate a spec section

Version cuts are announced in GitHub Discussions and documented in CHANGELOG.md.

---

## 9. Guiding Principles

- **Openness** — all deliberation in public GitHub threads
- **Implementer-centricity** — decisions guided by implementer needs; ask
  "does this make correct implementation easier?"
- **Clarity over cleverness** — unambiguous and slightly verbose beats elegant
  and open to interpretation
- **Security by default** — secure behaviour is always the default
- **Backward compatibility where possible** — breaking changes require strong
  justification
- **Explicit over implicit** — if a behaviour is required, state it

---

## 10. References

- [CHARTER.md](CHARTER.md) — mission, scope, IP policy
- [EDITORS.md](EDITORS.md) — current Editor and Reviewer roster
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to participate
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — community standards
- [SECURITY.md](SECURITY.md) — responsible disclosure
- [docs/aip-spec.md](docs/aip-spec.md) — canonical specification
- [RFC 7282](https://www.rfc-editor.org/rfc/rfc7282) — On Consensus and Humming
  in the IETF (informative — basis for the consensus model)
