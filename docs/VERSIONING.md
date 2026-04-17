# Versioning And Release Guidance

This repository needs disciplined version handling because several unrelated version numbers can coexist.

## Migration Baseline

- `v0.2` belongs to the archived Markdown-era repository history.
- The repository-format migration occurs at `v0.3`.
- The archived branch `archive/markdown-era` preserves the historical Markdown `v0.3` document that previously backed `docs/aip-spec.md`.
- On `main`, `v0.3` and later are maintained through the XML draft sources.

## Version Types

### 1. Internet-Draft Revision

This is the `-00`, `-01`, `-02` style revision embedded in generated draft filenames.

Increment the Internet-Draft revision when:

- a new public IETF submission is prepared
- the draft content has materially changed since the last submitted revision

Do not increment it for:

- local experiments
- unpublished proposal drafts
- internal review iterations

### 2. Proposal Revision

Proposal revisions are tracked inside issues, PR descriptions, or proposal documents.

Increment proposal revision labels when:

- the proposed direction materially changes
- maintainers request a replacement draft
- new compatibility analysis changes the recommended direction

Use simple labels such as `Proposal v1`, `v2`, `v3` in issue or PR history rather than inventing a second formal semver stream unless needed later.

### 3. Repository Snapshot Tags

Repository tags are optional and should be used sparingly for major public milestones, for example:

- pre-submission cleanup snapshots
- post-adoption or major editorial consolidation points
- published release candidates for wider review

If used, prefer annotated tags with a short rationale.

### 4. Protocol Or Spec Version Markers

If the specification defines wire-level or semantic version indicators, those are protocol artifacts and must be changed only when the actual protocol semantics require it.

Do not treat repository release tags as protocol version changes.

## How To Decide What To Increment

### Editorial-only updates

- do not change protocol version markers
- usually do not require a new proposal revision unless the editorial wording affects interpretation
- may be included in the next draft revision if a public submission is planned

### Normative or semantic updates

- require issue-linked rationale and explicit human approval
- may require a new proposal revision before integration
- may require a new Internet-Draft revision if prepared for public submission
- may require protocol version changes only if interoperability or semantics demand it

### Build or repository documentation changes

- do not change protocol version markers
- do not require draft revision unless a new public document is being published

## Release Checklist

Before preparing a public draft revision:

1. Confirm all included changes have issue references and recorded approvals.
2. Confirm proposal text and normative edits match the approved direction.
3. Run repository validation and capture notable warnings.
4. Review changelog notes or submission summary.
5. Verify filename revision and any in-document references to the revision.
6. Confirm public outputs do not expose unpublished working materials.

## Version Increment Responsibility

Maintainers decide when a version increment is official. Contributors may recommend increments, but they do not declare them unilaterally.
