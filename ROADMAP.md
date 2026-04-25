# Open-Source Roadmap

This roadmap describes the public work that would make the Agent Identity Protocol easier to review, test, and implement.

It is not a promise that a particular feature will enter the draft. Normative changes still require the issue-first workflow, research, compatibility analysis, and maintainer approval described in [CONTRIBUTING.md](CONTRIBUTING.md).

## Current Focus

The project is focused on turning the current Internet-Draft into a reviewable, implementation-informed standards asset.

Near-term work should improve:

- draft clarity and internal consistency
- schema and example coverage
- implementation feedback loops
- contributor onboarding
- archival and release discipline

## Workstreams

### 1. Draft Quality

Goal: make the XML draft easier to review and less ambiguous.

Good issues:

- ambiguous requirement language
- unclear section dependencies
- missing terminology definitions
- inconsistent naming across sections
- examples that do not match nearby normative text

Validation:

- `make validate`
- `make check-draft`
- `make html`
- `make text`

### 2. Schemas And Examples

Goal: keep machine-readable artifacts synchronized with the draft.

Good issues:

- schema fields that are underspecified in the draft
- examples that do not validate
- missing examples for important flows
- unnecessary divergence between similar objects
- unclear extension or compatibility behavior

Validation:

- `make validate-examples`
- review affected `schemas/` and `examples/` together

### 3. Implementation Reports

Goal: collect evidence from people trying to model, prototype, or implement AIP concepts.

Good reports:

- prototype notes
- integration experiments
- unclear implementation choices
- interop risks
- security or operational concerns
- places where the draft is too abstract for a builder to use

Start here:

- [docs/IMPLEMENTER-WALKTHROUGH.md](docs/IMPLEMENTER-WALKTHROUGH.md)
- [docs/IMPLEMENTATION-REPORTS.md](docs/IMPLEMENTATION-REPORTS.md)
- GitHub issue template: `Implementation Report`

### 4. Contributor Experience

Goal: make participation possible without private context.

Good issues:

- missing setup steps
- unclear validation failures
- broken links
- confusing repository layout
- policy docs that conflict with actual workflow

Validation:

- follow `README.md` from a clean checkout
- confirm the relevant docs point at one source of truth

### 5. Public Review And Release Hygiene

Goal: keep drafts, archives, issue history, and release state reconstructable.

Good issues:

- archive/index inconsistencies
- unclear draft revision state
- stale compatibility notices
- release checklist gaps
- outdated maintainer guidance

Validation:

- `make check-draft`
- review [EDITOR_GUIDE.md](EDITOR_GUIDE.md)
- review [docs/DRAFT_ARCHIVING.md](docs/DRAFT_ARCHIVING.md)

## Not In Scope For This Roadmap

- private working notes
- unpublished decision records
- internal approval bookkeeping
- closed commercial implementation materials
- parallel Markdown authoring paths for the live draft

See [docs/PUBLIC-REPOSITORY-BOUNDARY.md](docs/PUBLIC-REPOSITORY-BOUNDARY.md).

## How To Choose A First Contribution

If you are reviewing the draft, start with `Draft Quality`.

If you are building against the draft, start with `Implementation Reports`.

If you are working on tooling, start with `Schemas And Examples`.

If you are improving the repository, start with `Contributor Experience`.

For anything that changes specification behavior, open or reference an issue before drafting text.
