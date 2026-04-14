---
AIP: 0001
Title: Repository versioning layout — directory-based immutable snapshots
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Process
Created: 2026-04-11
Last-Call-Ends: ~
Spec-Section: ~
Requires: ~
Supersedes: ~
---

# AIP-0001: Repository versioning layout — directory-based immutable snapshots

## Abstract

This proposal restructures the `aip-spec` repository so that every released
spec version and every working-copy version lives under a single versioned
directory containing its own copy of the specification document, JSON Schemas,
and examples. It replaces the mixed convention in which `docs/aip-spec.md`,
`schemas/latest/`, and `examples/latest/` are treated as "working copy" while
frozen snapshots are prescribed as `spec/vMAJOR.MINOR/` plus
`docs/aip-spec-vMAJOR.MINOR.md`. The restructure establishes a single location
per version and eliminates the `latest/` directories as a dual source of truth.

## Motivation

Prior to this proposal, the repository has three partially-overlapping
conventions for locating spec source files:

1. `docs/aip-spec.md` — single canonical markdown working copy.
2. `schemas/latest/` and `examples/latest/` — working-copy directories for
   JSON Schemas and examples.
3. `spec/vMAJOR.MINOR/` and `docs/aip-spec-vMAJOR.MINOR.md` — prescribed
   snapshot locations per `VERSIONING.md` §4. These have never been
   exercised: no version has yet been formally released.

This arrangement creates three problems:

- **Dual sources of truth.** A contributor modifying a JSON Schema must edit
  `schemas/latest/`; a contributor reading a "snapshot" is told to look at
  `spec/vMAJOR.MINOR/`. These locations hold different file layouts, have
  different immutability rules, and are cross-referenced inconsistently
  throughout the repository.
- **No atomic snapshot.** Freezing v0.2 under the prior convention requires
  copying the markdown file to one location and the schemas/examples to a
  second location. A reader retrieving "v0.2" from `docs/aip-spec-v0.2.md`
  cannot locate the matching v0.2 schemas without a second lookup under
  `spec/v0.2/` or cross-reference chasing.
- **Implicit "latest" is ambiguous.** `schemas/latest/` is modified during
  draft work on an unreleased version, yet it is labelled "latest," which
  implementers read as "latest released." An implementer pinning to
  `schemas/latest/` between the start of v0.3 draft work and the v0.3 release
  is unknowingly consuming a moving target.

This gap was surfaced during planning for the v0.2 → v0.3 normative change
batch. A single location-per-version was the simplest way to make the change
batch auditable.

## Terminology

This proposal introduces no new terms beyond those defined in
`docs/aip-spec.md` Section 3.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### Overview

After this proposal, every spec version — released or in-progress — lives
under a single versioned directory:

```
spec/
  v0.2/
    aip-spec.md              ; immutable v0.2 specification
    schemas/                 ; immutable v0.2 JSON Schemas
    examples/                ; immutable v0.2 examples
  v0.3/
    aip-spec.md              ; working copy of v0.3 (mutable until v0.3 is released)
    schemas/                 ; working copy of v0.3 JSON Schemas
    examples/                ; working copy of v0.3 examples
```

The following legacy locations are transformed or removed:

- `docs/aip-spec.md` — **retained as a stub pointer** for external inbound-link
  compatibility. The stub MUST contain no normative content; it MUST contain
  only a one-paragraph redirect notice pointing at `spec/v0.2/aip-spec.md`
  (the most recent released version) and at `spec/v0.3/aip-spec.md` (the
  current working draft). Its original full content is copied verbatim into
  `spec/v0.2/aip-spec.md` (frozen) and `spec/v0.3/aip-spec.md` (working copy,
  initially byte-identical to v0.2).
- `schemas/latest/` — removed. Its content is copied verbatim into
  `spec/v0.2/schemas/` and `spec/v0.3/schemas/`.
- `examples/latest/` — removed. Its content is copied verbatim into
  `spec/v0.2/examples/` and `spec/v0.3/examples/`.
- `docs/archive/aip-spec-pre-editorial.md` — retained in place as
  pre-versioning historical context; not part of the new layout.
- `docs/aip-spec-vMAJOR.MINOR.md` — no longer prescribed as a separate
  snapshot path. The equivalent file is `spec/vMAJOR.MINOR/aip-spec.md`.

### Normative Requirements

1. Every released spec version MUST live under `spec/vMAJOR.MINOR/`. The
   directory MUST contain, at minimum, `aip-spec.md` and — if the version
   introduces or modifies any JSON-serialised resource — `schemas/` and
   `examples/` subdirectories.
2. Once a version is released (per the Version Cutting procedure in
   `VERSIONING.md` §4), every file under `spec/vMAJOR.MINOR/` is
   **immutable**. Editors MUST NOT modify files under a released version
   directory for any reason. Errata MUST be applied in the next version.
3. Work-in-progress for an unreleased version MUST be performed directly
   under that version's `spec/vMAJOR.MINOR/` directory. Draft status applies
   to the directory as a whole until the version is released.
4. The "current working version" at any point in time is the
   `spec/vMAJOR.MINOR/` directory whose `aip-spec.md` preamble declares
   `Status: Draft` and has the highest version number. Exactly one such
   directory MUST exist at any time.
5. Cross-references in governance documents, CI workflows, issue templates,
   PR templates, and the proposal template MUST reference the current working
   version directory by its explicit version (`spec/v0.3/`, etc.), not via a
   `latest` pointer.
6. The `schemas/` and `examples/` top-level directories MUST NOT exist after
   this proposal is integrated. Their historical contents are captured in
   `spec/v0.2/schemas/` and `spec/v0.2/examples/`.
7. The `docs/` top-level directory MAY continue to exist for documentation
   that is not part of any spec version (for example, pre-editorial
   historical files, non-normative reading guides, or meta-documentation).
   A file at `docs/aip-spec.md` MAY exist **only** as a non-normative stub
   pointer to the authoritative `spec/vMAJOR.MINOR/aip-spec.md` locations;
   it MUST NOT contain any normative specification content. No per-version
   specification document (`docs/aip-spec-vMAJOR.MINOR.md`) is permitted
   under this layout; all versioned content lives under `spec/`.
8. `README.md` MUST include a one-time redirect note informing external
   readers that `docs/aip-spec.md` is a stub and directing them to
   `spec/vMAJOR.MINOR/aip-spec.md` for authoritative content.

### Failure Conditions

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| N/A — Process proposal; no runtime error codes. | — | — |

### Schema Changes

This proposal does not modify any JSON Schema. It relocates the existing
schemas from `schemas/latest/` to `spec/v0.2/schemas/` (frozen) and
`spec/v0.3/schemas/` (working copy), byte-for-byte.

### VERSIONING.md Amendments

`VERSIONING.md` is updated as follows:

- §1: Revise the sentence "Frozen snapshots of each released version live at
  `spec/vMAJOR.MINOR/` and `docs/aip-spec-vMAJOR.MINOR.md`" to read
  "Every spec version — released or working — lives under
  `spec/vMAJOR.MINOR/`. Released versions are immutable."
- §4 (Cutting a New Version): Replace steps 3 and 4 with a single step:
  "The directory `spec/vMAJOR.MINOR/` becomes immutable. No additional
  snapshot files are created; the directory itself is the snapshot."
- §5 (Immutability Rule): Strike "and `docs/aip-spec-vMAJOR.MINOR.md`" from
  the immutability statement. The directory under `spec/vMAJOR.MINOR/` is
  the sole immutable artefact.
- §5 (Immutability Rule): Strike the paragraph beginning "`docs/aip-spec.md`
  always reflects the latest version..." and replace with "Implementations
  MUST pin to a specific `spec/vMAJOR.MINOR/` directory."

### Repository File Renames and Rewrites

The following files are modified by this proposal to update path references
away from `docs/aip-spec.md`, `schemas/latest/`, and `examples/latest/` to
`spec/vX.Y/aip-spec.md`, `spec/vX.Y/schemas/`, and `spec/vX.Y/examples/`:

- `README.md`
- `CONTRIBUTING.md`
- `GOVERNANCE.md`
- `SECURITY.md`
- `CHARTER.md`
- `VERSIONING.md`
- `AIP_INDEX.md`
- `proposals/_template/proposal.md`
- `.github/workflows/aip-validate.yaml`
- `.github/workflows/aip-index.yaml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/new-proposal.yaml`
- `.github/ISSUE_TEMPLATE/errata.yaml`
- `.github/ISSUE_TEMPLATE/editorial.yaml`
- `.github/ISSUE_TEMPLATE/discussion.yaml`
- `.github/ISSUE_TEMPLATE/config.yaml`

The CI workflow `aip-validate.yaml` is additionally updated to:

- Validate `spec/*/schemas/*.json` for each draft version directory, not
  `schemas/latest/*.json`.
- Validate `spec/*/examples/*.json` for each draft version directory, not
  `examples/latest/*.json`.
- Run the internal Markdown link checker on the current working-copy
  `spec/vMAJOR.MINOR/aip-spec.md` (discovered by finding the highest draft
  version), not on `docs/aip-spec.md`.
- Remove the deprecation warning for `spec/latest/`, which no longer exists
  as a concept under this proposal.

## Security Considerations

This proposal introduces no new threat vectors and does not alter any existing
security requirement.

A secondary security benefit is that pinning becomes unambiguous.
Implementations are instructed (VERSIONING.md §5, as amended) to pin to a
specific `spec/vMAJOR.MINOR/` directory. This eliminates the prior ambiguity in
which `schemas/latest/` could drift under an implementer pinned to a named
version but fetching schemas by the "latest" alias.

## Backwards Compatibility

**Breaking change** — but only for repository tooling and cross-references, not
for the specification content itself.

Migration path for external consumers:

- Any tool or implementation that fetched `docs/aip-spec.md` must now fetch
  `spec/v0.2/aip-spec.md` (for the immutable v0.2 content) or
  `spec/v0.3/aip-spec.md` (for the v0.3 working draft).
- Any tool that fetched `schemas/latest/` must now fetch `spec/v0.2/schemas/`
  or `spec/v0.3/schemas/`.
- Any tool that fetched `examples/latest/` must analogously update.
- URLs in external documentation that point at `docs/aip-spec.md` will 404
  after this proposal is integrated. A one-line redirect note will be added
  to `README.md` for discoverability.

Migration path for in-repo tooling: performed mechanically as part of
integrating this proposal.

No Credential Token, Principal Token, Registration Envelope, or other
protocol artefact is affected. No `aip_version` bump is required; this is a
process change, not a normative spec change, and does not map onto the
semantic-version policy in `VERSIONING.md` §3.

## Test Vectors

This proposal requires no new test vectors.

## Implementation Guidance

Editors integrating this proposal SHOULD perform the migration in a single
commit so that cross-references remain consistent. The migration commit MUST
include:

1. Copy `docs/aip-spec.md` to `spec/v0.2/aip-spec.md` (the immutable v0.2
   snapshot).
2. Copy `spec/v0.2/aip-spec.md` to `spec/v0.3/aip-spec.md` byte-identical.
   The preamble of the v0.3 copy remains `v0.2` until the first content
   proposal is integrated; only at that point does the preamble bump to
   `v0.3 (Draft)` and the "Changes in this version" section begin
   accumulating integrated AIP references. This ensures every commit in
   the v0.3 working copy is individually traceable to a merged proposal.
3. Overwrite `docs/aip-spec.md` with a one-paragraph stub pointer per
   Requirement 7 of this proposal. Retain the filename so that external
   inbound links do not return 404.
4. `git mv schemas/latest spec/v0.2/schemas` and `cp -r spec/v0.2/schemas
   spec/v0.3/schemas`.
5. `git mv examples/latest spec/v0.2/examples` and `cp -r spec/v0.2/examples
   spec/v0.3/examples`.
6. `rmdir schemas examples` if they become empty (retain if other
   subdirectories exist).
7. Apply the cross-reference updates listed under "Repository File Renames
   and Rewrites" above, and add the one-time redirect note to `README.md`
   per Requirement 8.

## Alternatives Considered

- **Option A (minimal snapshot) — Keep `docs/aip-spec.md` as the sole
  working copy; copy it to `docs/aip-spec-v0.2.md` on version cut; leave
  `schemas/latest/` and `examples/latest/` as working copies and copy them
  to flat `schemas/v0.2/` / `examples/v0.2/` on version cut.** Rejected
  because it preserves the dual-source-of-truth problem: the "working
  copy" and the "snapshot" of the same version live in different
  directories, and a reader of the snapshot must cross-reference the
  working copy to find the matching schemas.
- **Option B (split spec into core/overview/security) — In addition to
  versioned directories, also split the monolithic `aip-spec.md` into
  `core.md`, `overview.md`, and `security.md` per the (outdated) CLAUDE.md
  description.** Rejected as out of scope: it is its own editorial
  decision that deserves its own proposal and community review.
  Integrating it alongside this proposal would entangle a structural
  choice with a restructure and make both harder to review.
- **Symlinked `latest/` inside each version directory.** Rejected because
  symlinks in git repositories have inconsistent cross-platform handling
  and are not a stable artefact for external consumers.

## References

### Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.
              <https://www.rfc-editor.org/info/rfc2119>

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119
              Key Words", BCP 14, RFC 8174, May 2017.
              <https://www.rfc-editor.org/info/rfc8174>

### Informative References

- `VERSIONING.md` — existing versioning policy this proposal amends.
- `GOVERNANCE.md` — proposal lifecycle reference.

## Acknowledgements

Surfaced during planning for the v0.2 → v0.3 normative change batch.

## Changelog

- 2026-04-11 — Initial draft.
