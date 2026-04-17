# Editor Guide

This guide defines how editors create, review, archive, and publish Internet-Draft revisions of the AIP specification.

The repository uses Internet-Draft draft numbers such as `-00`, `-01`, and `-02`. Those suffixes are authoritative and must be handled consistently across draft text, schemas, examples, archived snapshots, and publication decisions.

## Editorial Model

- `draft.xml`, `sections/`, and `references/` define the current draft text.
- `schemas/` defines the current machine-readable schema state.
- `examples/` defines the current example JSON state.
- `drafts/` preserves append-only archived draft revisions.
- `history/markdown-era/` preserves historical schemas and examples from the pre-XML repository.

## Draft Versioning Policy

### Existing Draft Numbering Model

The repository follows the Internet-Draft naming model embedded in `draft.xml` and generated outputs:

- `draft-singla-agent-identity-protocol-00`
- `draft-singla-agent-identity-protocol-01`
- `draft-singla-agent-identity-protocol-02`

The `-NN` suffix identifies a concrete draft revision. Once a revision has been archived under `drafts/`, editors must treat it as immutable.

### When Not To Create A New Draft Number

The following normally do not justify minting the next `-NN` revision by themselves:

- isolated issue discussion that has not been approved
- small fixes still under review
- local editorial cleanups not yet ready for minting
- unapproved schema or example experiments

These may accumulate toward the next revision, but they do not automatically create one.

### When Changes Roll Into The Next Draft

The following usually roll into the next approved revision:

- approved editorial changes
- accepted errata
- integrated proposal outcomes
- schema corrections that are part of approved text changes
- example updates required by approved draft behavior

### When A New Draft Revision Is Required

Editors should create the next `-NN` revision when a coherent approved change set is ready to be preserved as a distinct draft, especially:

- normative changes
- structural changes
- schema changes that alter the repository's machine-readable contract
- example changes needed to reflect approved behavior
- a substantial approved editorial bundle that should be inspectable as its own draft revision

### Current Working Draft Versus Next Revision

Use this rule:

1. If the change is not approved, it is not ready to mint.
2. If the current `-NN` revision is already archived under `drafts/`, further substantive work must not continue under that same revision number.
3. Once approved work is ready after an archived revision, editors must bump to the next `-NN` revision before continuing substantive edits on `main`.

## How To Increment From One Draft To The Next

Example: `-00` to `-01`

1. Confirm the current revision is ready for minting and archival.
2. Confirm every included change has issue or proposal traceability, a research summary, a decision record, and explicit approval.
3. Run the validation and archival checks in this guide.
4. Archive the exact current revision under `drafts/draft-singla-agent-identity-protocol-00/`.
5. Update `draft.xml` so both `docName` and `seriesInfo` move from `-00` to `-01`.
6. Regenerate outputs for the new working revision name.
7. Update release notes or changelog entries.
8. Merge or publish only after the final approval gate.

The helper `scripts/prepare_next_draft.py` automates the `draft.xml` bump after the current revision has been archived.

## New Draft Creation Checklist

### Traceability

- [ ] All included changes are linked to GitHub issues, proposals, or errata.
- [ ] Each included issue has a research summary.
- [ ] Each included issue has a decision record.
- [ ] Each included issue has explicit human/editor approval.
- [ ] Accepted proposals are fully integrated and internally consistent.

### Draft Text

- [ ] `draft.xml`, `sections/`, and `references/` reflect the approved changes.
- [ ] Issue references, anchors, and internal links were checked.
- [ ] Editorial consistency was reviewed.
- [ ] Changelog or release notes were updated.

### Schemas

- [ ] Relevant files under `schemas/` were updated.
- [ ] Schema names remain consistent with repository conventions such as `schemas/capability-manifest.schema.json`.
- [ ] Schema changes were reviewed alongside the corresponding text changes.
- [ ] Schema evolution is traceable to specific issues or proposals.

### Examples

- [ ] Relevant files under `examples/` were updated.
- [ ] Current examples were validated against the corresponding current schemas.
- [ ] Older examples remain preserved exactly through archived revisions and historical archives.
- [ ] Example evolution is traceable to specific issues or proposals.

### Archival And Approval

- [ ] The archival snapshot includes exact draft source, schemas, examples, and generated outputs.
- [ ] Previous snapshots remain untouched.
- [ ] Metadata includes timestamp, approvals, source issues, and notes.
- [ ] Final human/editor approval was recorded before minting the next `-NN` revision.
- [ ] Tagging, publishing, or promotion steps were recorded if applicable.

## Responsibilities

### Editors

Editors are responsible for:

- enforcing the `-NN` revision model
- deciding when a change belongs in the current working draft versus the next revision
- ensuring issue to proposal to schema to example to revision traceability
- ensuring schemas, examples, and draft text evolve together
- preserving append-only history in `drafts/`
- refusing to mint or publish a new revision without explicit human/editor approval

### Reviewers

Reviewers are responsible for:

- checking technical coherence
- checking compatibility implications
- reviewing schema and example changes with the matching text changes
- identifying missing approvals, missing traceability, or incomplete integration

### Contributors

Contributors are responsible for:

- linking changes to issues or proposals
- providing research context and rationale
- updating draft text, schemas, and examples together when needed
- not unilaterally declaring or publishing a new `-NN` revision

### Approvers

Approvers are responsible for:

- confirming the included changes are ready
- confirming the archival checklist is complete
- authorizing the next `-NN` revision before minting or publication

## Schema Management

Schemas remain canonical under `schemas/`. Editors must determine affected schemas by checking:

- changed draft sections
- changed protocol objects
- changed validation rules
- changed examples
- changed object constraints or field semantics

Schema review must occur in the same PR or review cycle as the corresponding draft changes.

## Example Management

Examples remain canonical under `examples/`. Editors must:

- update examples whenever approved changes affect object shape or behavior
- keep current examples aligned with current schemas
- preserve historical examples in archived revision snapshots
- preserve Markdown-era examples under `history/markdown-era/`

## Tooling

Useful helper scripts:

- `scripts/check_draft_consistency.py`
- `scripts/validate_examples.py`
- `scripts/archive_current_draft.py`
- `scripts/prepare_next_draft.py`

These scripts support editors; they do not replace human approval.

## Internal Workflow Expectations

Any internal assistant or workflow used with this repository must:

- use the real `-00`, `-01`, `-02` draft numbering model
- use `schemas/` and existing schema filenames
- update draft text, schemas, and examples together
- use archived repository history instead of re-deriving prior revisions
- prepare archival snapshots for each minted revision
- never autonomously mint or publish a new revision without explicit human/editor approval
