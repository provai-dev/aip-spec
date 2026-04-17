# Migration From Markdown To XML

## Purpose

This document records the repository migration from the earlier Markdown-based specification layout to the IETF/RFC XML-based layout used on `main`.

## Migration Decision

The repository was split into two histories:

- `archive/markdown-era`: the preserved historical Markdown-era repository
- `main`: the clean XML-based working repository

This keeps the active branch unambiguous while preserving the complete earlier repository state.

## Version History

- `v0.2` remains part of the archived Markdown-era history
- the repository-format migration occurs at `v0.3`
- the historical Markdown `v0.3` document is preserved on `archive/markdown-era`

## Canonical Source On Main

The canonical working draft on `main` is:

- `draft.xml`
- `sections/`
- `references/`

Markdown is not the authoring source on `main`.

## Backlink Compatibility

`docs/aip-spec.md` remains on `main` as a compatibility surface.

Its job is to:

- preserve inbound links to the historical path
- explain that the repository migrated from Markdown to XML
- point readers to the new canonical source and workflow
- point historical readers to the archived Markdown `v0.3` document

## Risks Identified During Migration

- contributors may try to edit Markdown on `main` out of habit
- external references may continue to target `docs/aip-spec.md`
- older workflow documentation could imply multiple sources of truth

## Mitigations

- keep `docs/aip-spec.md` as an explicit compatibility page
- state the canonical authoring rule in `README.md` and `CONTRIBUTING.md`
- keep the archived branch name explicit in migration documentation
- avoid carrying the old Markdown authoring tree onto `main`

## Rollback Boundary

The destructive boundary is the branch transition itself.

Rollback options:

1. If the new `main` branch needs to be abandoned, the archived branch preserves the full Markdown-era repository.
2. A new branch can be cut from `archive/markdown-era` for comparison or recovery.
3. The migration does not delete historical Markdown content; it relocates that history to the archived branch.
