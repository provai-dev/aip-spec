# Draft Archiving

## Purpose

This repository preserves minted Internet-Draft revisions in version control instead of relying on temporary CI artifacts.

## Layout

Minted revisions live under `drafts/` using the full draft identifier, for example:

- `drafts/draft-singla-agent-identity-protocol-00/`
- `drafts/draft-singla-agent-identity-protocol-01/`

Each revision snapshot contains:

- `source/`
- `schemas/`
- `examples/`
- `generated/`
- `metadata.json`

## Rules

- revisions are append-only
- older revisions are never overwritten
- source, schemas, examples, and generated outputs stay attributable to a specific `-NN` draft
- CI may create a missing snapshot for a newly minted revision, but must not mutate an existing one

## Historical Markdown-Era Material

Historical schemas and examples from the pre-XML repository are preserved under `history/markdown-era/`.
