# Implementation Reports

Implementation reports help the project learn where AIP is clear, where it is ambiguous, and where the draft does not yet match implementer reality.

An implementation report is evidence for standards work. It is not a conformance claim and does not by itself approve a protocol change.

## When To File One

File an implementation report when you have tried to model, prototype, integrate, or reason through part of AIP and found something useful for the public record.

Useful reports include:

- a prototype that successfully models a flow from the draft
- a prototype that fails because the draft is unclear
- a schema or example that was hard to use
- an interop concern between agents, registries, credentials, grants, or approvals
- a security, privacy, audit, or operational concern
- implementation experience from adjacent identity, delegation, registry, or capability systems

## What To Include

Keep the report specific enough that maintainers can reproduce the reasoning.

Include:

- the draft revision or commit reviewed
- affected draft sections, schemas, or examples
- the flow or object you tried to implement
- what worked
- what was ambiguous or blocked
- compatibility or migration concerns
- whether you recommend an editorial, semantic, or normative follow-up
- links to public code or artifacts, if available

Do not include private credentials, customer data, confidential architecture, unpublished internal notes, or vendor-sensitive material.

## Recommended Scope

Good implementation reports are narrow. Prefer one report per implementation question.

Examples:

- "Grant response status values are unclear for partial approvals"
- "Credential token payload maps cleanly to this prototype shape"
- "Revocation object needs clearer timing semantics"
- "Registry trust record example validates but leaves issuer rotation unclear"

## What Happens Next

Maintainers triage the report and decide whether it should become:

- an editorial clarification
- a semantic proposal
- a normative proposal
- a schema or example fix
- a documentation improvement
- a closed report with no draft change

Substantive changes still follow [ISSUE-PROPOSAL-WORKFLOW.md](ISSUE-PROPOSAL-WORKFLOW.md).

## Validation

If the report includes schemas or examples, run:

```bash
make validate-examples
```

If the report includes draft text, run:

```bash
make validate
make html
make text
```

If a command cannot be run locally, say so in the report.
