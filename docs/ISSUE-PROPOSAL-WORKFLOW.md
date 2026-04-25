# Issue And Proposal Workflow

This repository uses an issue-driven workflow for all substantial standards work.

## Core Rule

Every substantive proposal, errata analysis, fix, or spec edit begins from a human-provided GitHub issue number.

On `main`, all approved draft edits are applied to the XML sources, schemas, and examples rather than to historical Markdown snapshots.

That issue number is the traceability anchor for:

- research
- options analysis
- human approvals
- proposal text
- validation
- final integration

Implementation reports also use GitHub issues. They are evidence for future work, not approval to change the draft. See [IMPLEMENTATION-REPORTS.md](IMPLEMENTATION-REPORTS.md).

## Workflow Stages

### 1. Intake

- A human opens or references a GitHub issue.
- The issue is classified as errata, proposal, editorial clarification, defect, or maintenance.
- Implementation reports are classified as implementation feedback and may later spawn errata, proposal, schema, example, or documentation follow-ups.
- Scope and urgency are clarified.

### 2. Research

- Investigate the reported problem before proposing a solution.
- Review the relevant draft text, related sections, linked issues, linked PRs, prior comments, and outside precedent where appropriate.
- Identify compatibility concerns, affected implementers, and downstream consequences.
- Produce a structured research brief.

### 3. Human Review Gate: Research

A human reviews the brief and either:

- approves continued work
- asks for more research
- narrows scope
- redirects the effort
- closes the issue

No fix or proposal direction should be selected before this gate.

### 4. Direction And Proposal Options

- Prepare one or more options with tradeoffs.
- State whether each option is editorial, semantic, or normative.
- Highlight compatibility and migration implications.

### 5. Human Review Gate: Direction

A human explicitly selects or rejects the direction.

### 6. Drafting

- Prepare proposal text, spec edits, or candidate fixes that match the approved direction.
- Keep the diff scoped to the issue.
- Update rationale and open questions if new information appears.

### 7. Validation And Review

- Validate internal consistency, style, references, examples, and compatibility claims.
- Check the final artifact against the approved direction and research record.
- Capture any residual risks.

### 8. Human Review Gate: Final Approval

A human decides whether the result is ready for merge, further revision, or withdrawal.

### 9. Public Integration

- Merge only the final approved output.
- Preserve the issue link and approval trail.
- Do not publish unpublished working materials or internal review materials.

## Research Brief Minimum Contents

Each issue-level research brief should capture:

- issue number and title
- status and owner
- problem statement
- source evidence
- affected draft sections and references
- linked issues and PRs
- precedent and comparison points
- compatibility analysis
- downstream impact
- open questions
- candidate directions, if appropriate
- recommendation status

Maintainers may use structured research templates so long as the public record remains reviewable and sufficient.

## Change Classes

### Editorial

Improves wording, organization, grammar, or clarity without changing intended semantics.

### Semantic

Clarifies or alters interpretation in a way that can affect implementers or readers.

### Normative

Introduces, removes, or changes requirements, allowed behavior, protocol rules, or interoperability expectations.

When classification is disputed, treat the change as the more severe class until maintainers decide otherwise.

## Review Expectations

- Substantial changes should be discussed in the issue before the PR is finalized.
- PR descriptions should summarize the approved direction and reference the issue.
- Reviewers should be able to reconstruct why the change exists without private context.
