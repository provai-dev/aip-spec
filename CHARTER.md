# AIP Working Group Charter

## 1. Mission

The Agent Identity Protocol (AIP) working group exists to design, publish, and
maintain an open, interoperable, cryptographically verifiable identity protocol
for autonomous AI agents.

AI agents are taking actions in the world — sending messages, making purchases,
spawning sub-agents, calling APIs — on behalf of humans and organisations. No
open standard exists for a relying party to ask: who authorised this agent, what
is it permitted to do, is it still active, and can I trust its track record? AIP
answers those questions.

The working group's goal is a specification that any engineer can implement from
the document alone, that two independent implementations can interoperate with,
and that is rigorous enough to submit to an external standards body (W3C
Community Group, IETF, or equivalent) as AIP matures.

---

## 2. Scope

### In scope

- The `did:aip` DID method — syntax, registration, resolution, key rotation
- The Principal Chain — cryptographic delegation from human/org principal to agent
- The Capability Manifest — fine-grained, signed permission grants
- The Credential Token — signed JWT format, header and payload structure,
  deterministic validation algorithm
- Revocation — the Revocation Object, CRL format, propagation semantics
- Reputation and Endorsements — endorsement object format, reputation scoring inputs
- The Registration Envelope — the protocol for registering an agent with a Registry
- JSON Schemas for all of the above
- Conformance requirements for Registry implementations
- Cryptographic suite requirements (MTI and optional suites)
- Security considerations and threat model

### Out of scope

- Agent runtime execution environments or LLM APIs
- General-purpose human identity (AIP is for agents acting on behalf of humans,
  not a replacement for existing human identity systems)
- Transport protocols below the HTTP layer
- Application-level authorisation policies beyond the capability model
- Prompt injection prevention (AIP bounds the blast radius; it does not prevent
  the initial attack — see the current working-draft
  `spec/vMAJOR.MINOR/aip-spec.md` § Non-Goals)
- Specific Registry implementations (AIP specifies behaviour, not code)

Scope questions are resolved by the Editor body per the process in
[GOVERNANCE.md](GOVERNANCE.md).

---

## 3. Standards Track Intent

AIP is developed as a community-governed open standard with the intent to pursue
external standardisation as the specification matures and independent
implementations emerge. The working group will evaluate submission to a W3C
Community Group or equivalent body once the specification reaches v1.0.

This is a statement of intent, not a binding commitment. The Editor body will
evaluate the appropriate venue at the time of v1.0.

---

## 4. Intellectual Property Policy

All specification text, JSON Schemas, examples, and tooling in this repository
are dedicated to the public domain under the
[CC0 1.0 Universal](LICENSE) license. No rights reserved.

Contributors MUST sign off each commit with the Developer Certificate of Origin
(DCO) v1.1. See [CONTRIBUTING.md § DCO](CONTRIBUTING.md#dco) for details.
DCO sign-off certifies that the contributor has the right to submit the
contribution and agrees to the CC0 dedication.

Contributors who contribute on behalf of an employer represent that their
employer has authorised them to make the CC0 dedication for the submitted
content.

Do not submit content — text, schemas, algorithms, or examples — that you do
not have the right to contribute.

---

## 5. Stewardship and Transition

AIP was founded by [Provai](https://provai.dev), which provides initial
engineering resources and governance leadership.

The specification is owned by the community, not by Provai. Provai's role is
that of a founding steward: it bootstraps the working group, seeds the initial
Editor body, and provides infrastructure. It does not hold veto power over
specification decisions beyond the rights of its representatives as individual
Editors.

The working group intends to transition governance to a neutral foundation
structure — independent of any single company — as the specification matures and
as independent implementations and community participation grow. This transition
will be proposed via the normal governance process (a Process-type AIP proposal)
and requires super-majority Editor approval.

---

## 6. Relationship to Other Standards

AIP builds on and is designed to interoperate with:

| Standard | Relationship |
|----------|-------------|
| W3C DID v1.1 | AIP's `did:aip` method is a conformant W3C DID method |
| RFC 7519 (JWT) | Credential Tokens are JWTs with AIP-defined claims |
| RFC 9449 (DPoP) | Proof-of-Possession mechanism |
| RFC 2119 / RFC 8174 | All normative requirements use BCP 14 language |
| NIST SP 800-207 | AIP implements Zero Trust principles |
| NIST SP 800-63-4 | AIP agent authentication satisfies AAL2 |

AIP does not compete with OAuth 2.0, OIDC, SPIFFE, or MCP. It provides the
agent identity layer that those protocols assume but do not define. See
the current working-draft `spec/vMAJOR.MINOR/aip-spec.md` § Relationship to
Existing Standards for detail.

---

## 7. Amendment Process

This charter may only be amended by a pull request that:

1. Is opened by a current Editor.
2. Clearly describes the proposed change and its rationale.
3. Remains open for a minimum of 14 calendar days.
4. Receives approval from at least two-thirds of the current Editor body
   (super-majority, excluding the proposing Editor).
5. Is merged by a non-proposing Editor.

Charter amendments are announced in the GitHub Discussions announcement thread
at the time the PR is opened, so the community has visibility.

---

## 8. References

- [GOVERNANCE.md](GOVERNANCE.md) — operational procedures, roles, proposal lifecycle
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to participate
- [EDITORS.md](EDITORS.md) — current Editor and Reviewer roster
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — community standards
- [SECURITY.md](SECURITY.md) — responsible disclosure policy
- [spec/](spec/) — versioned specification directories (canonical)
