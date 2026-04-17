# Repository Structure

This repository should remain predictable for contributors and reviewers.

## Top-Level Layout

- `draft.xml`: root xml2rfc source
- `sections/`: main specification content split by section
- `references/`: shared references
- `docs/`: repository policy and contributor documentation
- `.github/`: issue templates, PR template, and repository workflows

Compatibility surface:

- `docs/aip-spec.md`: stable backlink path retained after the Markdown-to-XML migration

## Placement Rules

### Specification text

Put normative and editorial draft content in `draft.xml`, `sections/`, and `references/`.

Do not keep a second live Markdown specification tree on `main`.

### Public process documentation

Put contributor and maintainer documentation in `docs/` or top-level project files such as `README.md` and `CONTRIBUTING.md`.

### Public templates

Put issue forms and PR checklists in `.github/`.

### Non-public draft material

Do not commit unpublished working notes, internal review materials, or incomplete decision records.

## Documentation Change Discipline

- Update the closest authoritative file instead of duplicating policy across many places.
- Link to canonical docs from secondary docs.
- When workflow or governance changes, update the documentation in the same change set.

## Build Artifacts

Generated outputs are not source of truth and should stay untracked unless maintainers intentionally adopt a different publication policy later.
