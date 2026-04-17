# Contributing

This repository is maintained as a standards and specification project, not a feature branch for rapid iteration. Contributions should optimize for clarity, compatibility analysis, and reviewability.

## Before You Start

Read these first:

- [README.md](README.md)
- [docs/aip-spec.md](docs/aip-spec.md)
- [docs/MIGRATION-FROM-MARKDOWN.md](docs/MIGRATION-FROM-MARKDOWN.md)
- [docs/ISSUE-PROPOSAL-WORKFLOW.md](docs/ISSUE-PROPOSAL-WORKFLOW.md)
- [docs/VERSIONING.md](docs/VERSIONING.md)
- [docs/AUTHORSHIP.md](docs/AUTHORSHIP.md)
- [docs/REPOSITORY-STRUCTURE.md](docs/REPOSITORY-STRUCTURE.md)

## Contribution Types

The repository accepts several kinds of contributions:

- errata reports and defect analyses
- proposal issues and proposal pull requests
- editorial clarifications
- normative changes with explicit rationale and compatibility analysis
- build and repository maintenance improvements

## Canonical Authoring Rule

On `main`, the specification is authored in:

- `draft.xml`
- `sections/`
- `references/`

Do not submit normative draft changes by editing Markdown snapshots or by adding a second authoring path. `docs/aip-spec.md` exists only for backlink compatibility.

## Required Workflow

All substantial work starts from a GitHub issue number.

1. Open a new issue or confirm the existing issue that tracks the work.
2. Assemble or update a research brief before proposing a change.
3. Record assumptions, affected sections, linked issues, prior discussion, and compatibility concerns.
4. Obtain human maintainer approval before drafting normative text, applying fixes, or finalizing public-facing output.
5. Submit a pull request tied to the tracked issue.

## Research Expectations

Contributors should not jump directly from issue report to patch text. Before proposing direction, investigate:

- the exact reported problem
- current draft text and related sections
- prior issues, PRs, and external discussion if relevant
- precedent in related standards or neighboring protocol work
- compatibility, migration, and downstream implementation effects
- whether the change is editorial, semantic, or normative

Summarize that work in the issue or PR description.

## Human Review Gates

Human review is mandatory before:

- choosing among competing directions
- drafting or finalizing proposal text
- applying fixes with semantic or compatibility impact
- merging or publishing any result

Do not proceed past a review gate without explicit human approval.

## Pull Request Expectations

Each PR should:

- reference the issue number
- explain whether the change is editorial, semantic, or normative
- describe compatibility impact
- summarize research performed
- note unresolved questions
- include validation performed

Normative changes should be easy to isolate from editorial cleanup. Prefer small, reviewable PRs over mixed bundles.

## Style For Specification Edits

- Preserve xml2rfc and RFC-style conventions already used by the document.
- Use RFC 2119 or RFC 8174 keywords only where justified.
- Keep normative requirements precise and testable.
- Avoid silent behavior changes. If behavior changes, say so directly.
- Keep examples, references, and registry text synchronized with normative sections.
- Preserve backlink compatibility for `docs/aip-spec.md`.

## Validation

Before submitting:

```bash
make clean
make validate
make html
make text
make idnits
```

If a command cannot be run locally, state that in the PR.

## Historical Markdown Content

The Markdown-era repository is preserved on branch `archive/markdown-era`.

- The historical Markdown `v0.3` document remains there for path continuity with the old `docs/aip-spec.md`.
- Earlier Markdown-era content, including `v0.2`, remains there as part of the archived branch.

Do not restore the old Markdown authoring tree onto `main`.

## Authorship And Credit

Do not add or remove document authorship casually. See [docs/AUTHORSHIP.md](docs/AUTHORSHIP.md) for the distinction between document editor status, acknowledged contribution, and substantial normative authorship.

## Non-Public Working Materials

Do not commit unpublished working notes, internal review materials, or other non-public draft artifacts. This repository should contain only reviewable public outputs and the public rationale needed to understand them. See [docs/PUBLIC-REPOSITORY-BOUNDARY.md](docs/PUBLIC-REPOSITORY-BOUNDARY.md).
