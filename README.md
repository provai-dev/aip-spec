# Agent Identity Protocol (AIP) RFC Draft

This repository contains the IETF/RFC XML source for the Agent Identity Protocol Internet-Draft and the public documentation needed to maintain it as a long-lived standards project.

The repository is intended to be conservative, review-heavy, and traceable. The canonical working draft lives in XML. Markdown is not the authoring source on `main`.

## Scope

This repository is the public working tree for:

- Internet-Draft XML source and referenced fragments
- accepted specification edits and public review artifacts
- contributor, maintenance, and release guidance

This repository is not the place for:

- unpublished working notes or draft materials
- internal review materials
- incomplete decision records
- duplicate competing authoring sources

See [docs/PUBLIC-REPOSITORY-BOUNDARY.md](docs/PUBLIC-REPOSITORY-BOUNDARY.md) for the repository boundary policy.

## Repository Layout

Core draft sources:

- `draft.xml`: root xml2rfc document
- `sections/`: section-level XML files included into the draft
- `references/`: normative and informative reference blocks
- `schemas/`: canonical machine-readable schemas for the current working draft
- `examples/`: canonical example JSON for the current working draft
- `drafts/`: append-only archived Internet-Draft revisions
- `history/markdown-era/`: preserved historical schemas and examples from the Markdown-era repository
- `Makefile`: local build, validation, and idnits entry points
- `build_draft.py`: XInclude expansion helper for local builds

Repository documentation:

- `EDITOR_GUIDE.md`: editor procedure for minting new `-NN` draft revisions
- `CHANGELOG.md`: minted draft revision notes
- `CONTRIBUTING.md`: contributor workflow and review expectations
- `CODE_OF_CONDUCT.md`: baseline community behavior policy
- `docs/aip-spec.md`: compatibility page preserved for legacy backlinks
- `docs/DRAFT_ARCHIVING.md`: append-only archival policy for draft revisions
- `docs/MIGRATION-FROM-MARKDOWN.md`: migration record and archived-branch plan
- `docs/VERSIONING.md`: document, draft, and repository versioning rules
- `docs/ISSUE-PROPOSAL-WORKFLOW.md`: public issue and proposal lifecycle
- `docs/AUTHORSHIP.md`: authorship, acknowledgments, and editor guidance
- `docs/MAINTAINERS.md`: maintainer responsibilities and cadence
- `docs/REPOSITORY-STRUCTURE.md`: documentation and file placement guidance
- `.github/ISSUE_TEMPLATE/`: structured issue intake forms
- `.github/PULL_REQUEST_TEMPLATE.md`: required PR checklist

## Getting Started

### Prerequisites

```bash
pip install lxml xml2rfc jsonschema
```

Optional for PDF output:

```bash
pip install weasyprint
```

### Build

```bash
make clean
make html
make text
make validate
make validate-examples
make check-draft
make idnits
```

Outputs are intentionally ignored by Git.

## Canonical Source

The canonical authoring source on `main` is:

- `draft.xml`
- `sections/`
- `references/`
- `schemas/`
- `examples/`

`docs/aip-spec.md` continues to exist only as a compatibility surface for inbound links and historical references. It is not an authoring target and not a normative source on `main`.

Minted revisions are preserved under `drafts/` and must remain append-only.

## Repository Migration

The repository layout changed at `v0.3`.

- The Markdown-era repository history is preserved on branch `archive/markdown-era`.
- The archived branch contains the historical Markdown `v0.3` document that previously lived behind the `docs/aip-spec.md` compatibility path.
- Earlier Markdown-era material, including `v0.2`, is preserved there as part of the full historical repository state.

See [docs/MIGRATION-FROM-MARKDOWN.md](docs/MIGRATION-FROM-MARKDOWN.md) and [docs/aip-spec.md](docs/aip-spec.md) for the compatibility policy.

## Draft Revisions And Archives

The repository uses Internet-Draft revision numbers such as `-00`, `-01`, and `-02`.

- the current working revision is defined by `draft.xml`
- schemas and examples for the working revision live in `schemas/` and `examples/`
- minted revisions are archived under `drafts/<full-draft-name>/`

See [EDITOR_GUIDE.md](EDITOR_GUIDE.md) and [docs/DRAFT_ARCHIVING.md](docs/DRAFT_ARCHIVING.md) for the full release procedure.

## Working Model

This project uses an issue-first standards workflow:

1. A human opens or references a GitHub issue.
2. Research happens before any normative change, proposal text, or fix.
3. A structured research brief is produced.
4. Humans review and approve direction at explicit checkpoints.
5. Only approved outputs are prepared for public integration.

Public workflow details are in [docs/ISSUE-PROPOSAL-WORKFLOW.md](docs/ISSUE-PROPOSAL-WORKFLOW.md).

## Versioning And Releases

This repository manages several different kinds of version identifiers. They must not be conflated.

- Internet-Draft revision: the filename revision such as `-00`, `-01`, `-02`
- proposal revision: revision history within a proposal or issue thread
- repository release tag: optional repository snapshot tags for major editorial milestones
- protocol/spec version markers inside the document, when the draft itself defines version semantics

The rules for incrementing each of these are in [docs/VERSIONING.md](docs/VERSIONING.md).

## Contribution Entry Points

Start here depending on the work:

- editorial or normative contribution: [CONTRIBUTING.md](CONTRIBUTING.md)
- proposal or errata handling: [docs/ISSUE-PROPOSAL-WORKFLOW.md](docs/ISSUE-PROPOSAL-WORKFLOW.md)
- authorship and acknowledgment questions: [docs/AUTHORSHIP.md](docs/AUTHORSHIP.md)
- maintainer responsibilities: [docs/MAINTAINERS.md](docs/MAINTAINERS.md)
- repository organization: [docs/REPOSITORY-STRUCTURE.md](docs/REPOSITORY-STRUCTURE.md)

## Maintenance Principles

- Human judgment is required for all normative, semantic, compatibility-impacting, and public-facing changes.
- No unpublished or unreviewed material may be published or merged into the public standard.
- Traceability matters more than speed. Issues, proposals, approvals, and rationale should remain reconstructable.
- Stable repository policy changes require maintainer review and should be documented in-repo.
- Local drafting practices do not override public review and publication rules.

## Current Draft Build Notes

`xml2rfc` can be sensitive to local XInclude handling. The included `build_draft.py` script resolves XIncludes into `draft-expanded.xml` for local processing.

```bash
make expand
xml2rfc draft-expanded.xml --html -o draft-singla-agent-identity-protocol-00.html
```

CI builds the expanded XML, HTML, and text outputs, then runs `idnits`.

## Contributor Direction

If you want to change the draft on `main`, edit the XML sources and the supporting repository documentation around them. Do not reintroduce a parallel Markdown specification tree on `main`.
