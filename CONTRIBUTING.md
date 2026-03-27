# Contributing to AIP

AIP is an open community standard. Contributions are welcome from everyone —
implementers, security researchers, protocol designers, and curious engineers.
The specification is made stronger by diverse perspectives.

This document explains how to contribute effectively. Please read it before
opening an issue or pull request.

---

## 1. Canonical Specification

`docs/aip-spec.md` is the single canonical AIP specification. All contributions
that change normative spec content MUST modify `docs/aip-spec.md` directly.

The files under `spec/latest/` are deprecated working drafts. Do not modify
them (except an Editor maintaining their deprecation notices). Do not cite them
in proposals or implementations.

---

## 2. Ways to Contribute

| Type | Process | Effort |
|------|---------|--------|
| Report an ambiguity, typo, or broken link | Open an [Editorial](/.github/ISSUE_TEMPLATE/editorial.yaml) issue or submit a PR directly | Low |
| Report a spec bug or errata | Open an [Errata](/.github/ISSUE_TEMPLATE/errata.yaml) issue | Low–Medium |
| Propose a new normative requirement | Full proposal process (see § 6) | High |
| Review and discuss a proposal | Comment on open PRs and issues | Any |
| Report a security vulnerability | Private disclosure via [SECURITY.md](SECURITY.md) | — |

---

## 3. Good Standing

A Contributor is in **good standing** if they:
- Have not been subject to a CODE_OF_CONDUCT.md enforcement action resulting in
  a ban
- Have engaged constructively in at least one public thread

Good standing is the default. Loss of good standing requires an explicit
enforcement action.

Good standing matters because it is referenced in
[GOVERNANCE.md § 5](GOVERNANCE.md#5-editor-appointment) (Reviewer and Editor
nomination eligibility).

---

## 4. DCO — Developer Certificate of Origin

Every commit to this repository **MUST** include a DCO sign-off trailer:

```
Signed-off-by: Full Name <email@example.com>
```

Add it automatically with:

```sh
git commit -s -m "Your commit message"
```

The DCO (v1.1, https://developercertificate.org/) certifies that you have the
right to submit the contribution and agree to its CC0 1.0 dedication. AIP uses
DCO rather than a CLA because CC0 makes copyright assignment unnecessary — DCO
simply certifies the right to contribute.

If you are contributing on behalf of an employer, you represent that your
employer has authorised you to make the CC0 dedication.

**CI enforces DCO sign-off.** PRs with unsigned commits will not be merged.

<details>
<summary>Full DCO 1.1 text</summary>

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```
</details>

---

## 5. How to File an Issue

Use the appropriate issue template — issues that skip templates may be closed
and asked to resubmit:

| Template | When to use |
|----------|-------------|
| [New Proposal (AIP)](/.github/ISSUE_TEMPLATE/new-proposal.yaml) | You have an idea for a normative change |
| [Errata](/.github/ISSUE_TEMPLATE/errata.yaml) | You found an error or ambiguity in the spec |
| [Editorial](/.github/ISSUE_TEMPLATE/editorial.yaml) | Typo, broken link, formatting |
| [Security](/.github/ISSUE_TEMPLATE/security.yaml) | **Do not use for vulnerabilities** — this template redirects to private disclosure |
| [Discussion](/.github/ISSUE_TEMPLATE/discussion.yaml) | Questions, open-ended design discussion |

---

## 6. How to Write a Formal Proposal

The full lifecycle is defined in [GOVERNANCE.md § 4](GOVERNANCE.md#4-proposal-lifecycle).
Here is the practical walkthrough:

**Step 1 — File an Idea issue**
Open a [New Proposal](/.github/ISSUE_TEMPLATE/new-proposal.yaml) issue. Describe
the problem and the direction you're thinking. Wait at least 7 days for Editor
or Reviewer engagement. If an Editor or Reviewer comments "proceed", move to
Step 2.

**Step 2 — Write the proposal**
Fork the repository. Create a directory:

```
proposals/XXXX-short-slug/
```

Use `XXXX` as a placeholder; an Editor will assign the actual AIP number when
you open the PR. Copy the templates from `proposals/_template/`:

```sh
cp -r proposals/_template proposals/XXXX-my-proposal
```

Fill in `proposal.md` completely. All required frontmatter fields must be
present. All required sections must be non-empty.

**Step 3 — Open a pull request**
Title your PR: `[AIP-XXXX] Short descriptive title`

Link the originating Idea issue in the PR description. The handling Editor
assigns the AIP number and begins review.

**Step 4 — Iterate on review**
Respond to review comments within 14 calendar days. If you need more time,
say so in the PR — Editors are reasonable. PRs with no author response for
30 days are labeled `stale`.

**Step 5 — Last Call**
When you believe no blocking objections remain, you can request Last Call by
commenting "requesting Last Call" in the PR. An Editor or Reviewer declares it
formally. Last Call is 14 calendar days — the community's final window to raise
blocking issues.

**Step 6 — Acceptance and integration**
After Last Call with no blocking objections, an Editor merges the proposal and
integrates it into `docs/aip-spec.md`. Your work becomes part of the canonical
spec.

---

## 7. How to Submit an Editorial Fix

Small fixes (typos, grammar, broken links, formatting in `docs/aip-spec.md`)
may be submitted as a PR directly without an Idea issue.

- Title MUST start with `[EDITORIAL]`
- A single Editor can review and merge without Last Call
- DCO sign-off still required

---

## 8. Discussion Channels

| Channel | Purpose |
|---------|---------|
| GitHub Issues | Structured discussion on specific proposals and errata |
| GitHub Discussions | Open-ended questions, design explorations, community announcements |
| Discord ([discord.gg/FpeHxaKV](https://discord.gg/FpeHxaKV)) | Informal real-time chat |

**No normative decisions are made outside of GitHub.** Discord and other channels
are for informal discussion only. Any decision that matters must be recorded in
a GitHub issue or PR comment.

---

## 9. Review Expectations

**For authors:**
- Respond to review comments within 14 calendar days
- If you go silent for 30 days, the PR is labeled `stale`; 45 days, it is
  closed (with an invitation to reopen)

**For Editors:**
- Provide initial feedback on new PRs within 14 calendar days
- Blocking objections must be clearly labeled as such; non-blocking feedback
  should be labeled `nit` or `suggestion`

---

## 10. Copyright and Licensing

All contributions to this repository are dedicated to the public domain under
[CC0 1.0 Universal](LICENSE). By contributing, you agree to this dedication.

You retain the right to be credited in [CONTRIBUTORS.md](CONTRIBUTORS.md).
Add yourself to the appropriate section in the same PR as your first contribution.

---

## 11. Questions?

- For spec questions: [GitHub Discussions](https://github.com/provai-dev/aip-spec/discussions)
- For governance questions: open an issue or tag `@aip-editors`
- For security concerns: [SECURITY.md](SECURITY.md)
- For conduct concerns: see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
