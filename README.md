# AIP — Agent Identity Protocol

> The open standard for verifiable AI agent identity.

[![Status](https://img.shields.io/badge/status-draft-yellow)](https://github.com/provai-dev/aip-spec)
[![Spec Version](https://img.shields.io/badge/spec-v0.1-blue)](docs/aip-spec.md)
[![License](https://img.shields.io/badge/license-CC0%201.0-green)](LICENSE)
[![DID Method](https://img.shields.io/badge/DID%20method-did%3Aaip-blue)](https://www.w3.org/TR/did-core/)
[![RFC 2119](https://img.shields.io/badge/language-RFC%202119-orange)](https://www.rfc-editor.org/rfc/rfc2119)

---

## What AIP Is

AI agents are sending emails, making purchases, spawning sub-agents, and calling
APIs — autonomously, on behalf of humans. When an agent knocks on a door, there
is currently no standard way to ask: who authorised this agent, what is it
allowed to do, is it still active, and can I trust its track record?

AIP is a layered identity protocol that answers those questions. It defines a
W3C DID-conformant agent identifier, a cryptographic principal delegation chain,
a fine-grained capability manifest, a signed credential token with a
deterministic validation algorithm, a standard revocation mechanism, and a
reputation data format.

Two implementations conforming to this specification interoperate without
coordination. See [CHARTER.md](CHARTER.md) for the full mission and scope.

---

## How to Read the Spec

1. **Start here:** [`docs/aip-spec.md`](docs/aip-spec.md) — the canonical
   consolidated specification. All normative requirements, schemas, and
   algorithms are in this file.
2. **Architecture background:** `docs/aip-spec.md` §§ 1–3 cover the
   architecture, design philosophy, and relationship to existing standards.
3. **For implementers:** §§ 4–12 define the normative requirements. §§ 13–16
   cover error handling, rate limiting, versioning, and security.
4. **Schemas:** [`schemas/latest/`](schemas/latest/) — JSON Schemas for all
   AIP data structures.
5. **Examples:** [`examples/latest/`](examples/latest/) — annotated example
   JSON for common scenarios.

---

## Quick Example

```javascript
// npm install @provai/aip

import { aip } from '@provai/aip'

// Create a W3C DID-conformant Agent Identity
const agent = await aip.createAgent({
  name: 'Jarvis',
  type: 'personal',
  model: 'claude-sonnet-4-6',
  principal: 'did:key:z6Mkk...'  // human's DID
})

console.log(agent.aid)
// → "did:aip:personal:9f3a1c82b4e6d7f0a2b5c8e1d4f7a0b3"

// Sign a credential token
const token = await agent.sign({
  purpose: 'email.read',
  expires_in: '1h'
})

// Verify at any relying party
const result = await aip.verify(token)
// → { valid: true, aid: "did:aip:...", scope: ['email.read'], ... }
```

---

## Conformance

An implementation is AIP-conformant if it:

1. Generates Agent IDs conforming to the `did:aip` DID method syntax defined
   in `docs/aip-spec.md` § 4.1
2. Issues and verifies Credential Tokens according to the validation algorithm
   in `docs/aip-spec.md` § 7.3
3. Implements the mandatory-to-implement (MTI) cryptographic suites in
   `docs/aip-spec.md` § 16.1
4. Enforces Capability Manifest scope intersection during delegation as defined
   in `docs/aip-spec.md` § 8.2

A conformance test suite is planned for v0.2.

---

## Repository Structure

```
aip-spec/
│
├── docs/
│   └── aip-spec.md             ← Canonical specification (read this)
│
├── schemas/
│   └── latest/                 ← JSON Schemas for all AIP data structures
│       ├── agent-identity.schema.json
│       ├── capability-manifest.schema.json
│       ├── credential-token.schema.json
│       ├── endorsement.schema.json
│       ├── principal-token.schema.json
│       ├── registration-envelope.schema.json
│       └── revocation-object.schema.json
│
├── examples/
│   └── latest/                 ← Example JSON for common scenarios
│
├── proposals/                  ← AIP proposals (community-driven changes)
│   └── _template/              ← Template for new proposals
│
├── CHARTER.md                  ← Mission, scope, IP policy
├── GOVERNANCE.md               ← Roles, lifecycle, decision-making
├── EDITORS.md                  ← Current Editor and Reviewer roster
├── CONTRIBUTING.md             ← How to contribute
├── CODE_OF_CONDUCT.md          ← Community standards
├── SECURITY.md                 ← Responsible disclosure policy
├── VERSIONING.md               ← Versioning policy
├── AIP_INDEX.md                ← Auto-generated index of all proposals
└── LICENSE                     ← CC0 1.0 Universal
```

---

## Status and Roadmap

| Document | Version | Status |
|----------|---------|--------|
| [AIP Specification](docs/aip-spec.md) | v0.1 | Standards Track — Draft |

**Current:** v0.1 draft. The protocol is specified but not yet validated by
independent implementations.

**v0.2 targets:** Conformance test suite, formal DID method registration with
W3C, and at least one reference implementation against the test suite.

**v1.0 criteria:** Two independent conforming implementations, published
conformance test suite, and super-majority Editor vote declaring the spec stable.

See [AIP_INDEX.md](AIP_INDEX.md) for active proposals and [VERSIONING.md](VERSIONING.md)
for the full versioning policy.

---

## Relationship to Existing Standards

AIP builds on existing standards rather than replacing them:

| Standard | Relationship |
|----------|-------------|
| [W3C DID v1.1](https://www.w3.org/TR/did-core/) | AIP's `did:aip` is a conformant DID method |
| [RFC 7519 — JWT](https://www.rfc-editor.org/rfc/rfc7519) | Credential Tokens are JWTs with AIP-defined claims |
| [RFC 9449 — OAuth DPoP](https://www.rfc-editor.org/rfc/rfc9449) | Proof-of-Possession mechanism |
| [NIST SP 800-207](https://doi.org/10.6028/NIST.SP.800-207) | AIP implements Zero Trust Architecture principles |
| [SPIFFE/SPIRE](https://spiffe.io/) | Complementary — SPIFFE for service workloads, AIP for reasoning agents |
| [MCP](https://modelcontextprotocol.io/specification) | AIP is the agent identity layer beneath MCP's authorisation flow |

---

## How to Contribute

AIP is a community-governed open standard. All are welcome.

- **Quick fix** (typo, broken link): submit a PR with title `[EDITORIAL] ...`
- **Found a spec bug**: open an [Errata issue](.github/ISSUE_TEMPLATE/errata.yaml)
- **New idea for the spec**: open a [New Proposal issue](.github/ISSUE_TEMPLATE/new-proposal.yaml)
- **Questions**: [GitHub Discussions](https://github.com/provai-dev/aip-spec/discussions)
  or [Discord](https://discord.gg/FpeHxaKV)
- **Security vulnerability**: see [SECURITY.md](SECURITY.md) — private disclosure only

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the full process, including the
DCO sign-off requirement.

---

## Governance

AIP is governed by a body of Editors listed in [EDITORS.md](EDITORS.md). The
governance model — roles, proposal lifecycle, decision-making, and conflict
resolution — is defined in [GOVERNANCE.md](GOVERNANCE.md).

AIP was founded by [Provai](https://provai.dev). The specification is owned by
the community. Provai provides engineering resources and initial governance
leadership and intends to transition to a neutral foundation structure as the
specification matures. See [CHARTER.md § 5](CHARTER.md#5-stewardship-and-transition)
for the transition plan.

---

## License

[CC0 1.0 Universal](LICENSE) — no rights reserved, implement freely.
