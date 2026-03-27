# Security Policy

## Scope

This policy covers security vulnerabilities in the **AIP specification itself**:
protocol design flaws that could allow impersonation, privilege escalation, token
forgery, delegation abuse, revocation bypass, or cryptographic weaknesses.

**In scope:**
- Flaws in the AIP protocol design documented in `docs/aip-spec.md`
- Weaknesses in the cryptographic requirements (MTI or optional suites)
- Attacks against the delegation chain or capability manifest model
- Revocation bypass or race conditions in the revocation model
- Weaknesses in the DPoP proof-of-possession construction as specified

**Out of scope:**
- Vulnerabilities in third-party AIP implementations — report those to the
  respective project directly
- Vulnerabilities in GitHub infrastructure or the repository itself — report
  those to GitHub
- General feedback on the spec design — use the
  [Errata](/.github/ISSUE_TEMPLATE/errata.yaml) or
  [New Proposal](/.github/ISSUE_TEMPLATE/new-proposal.yaml) issue templates

## How to Report

**Do not open a public GitHub issue for security vulnerabilities.**

Use GitHub's private Security Advisory mechanism:

1. Go to the [Security tab](https://github.com/provai-dev/aip-spec/security) of
   this repository.
2. Click **"Report a vulnerability"**.
3. Fill in the form with as much detail as possible:
   - The spec section(s) affected (reference `docs/aip-spec.md` section numbers)
   - A description of the vulnerability and its impact
   - A proof-of-concept or attack scenario, if available
   - Any suggested mitigations

If you are unable to use GitHub Security Advisories, you may contact the Editors
directly at the address listed in [EDITORS.md](EDITORS.md). Encrypt your message
using the PGP key published there if available.

## Response SLA

| Milestone | Target |
|-----------|--------|
| Acknowledgement | Within 5 business days of report |
| Initial triage and severity assessment | Within 14 calendar days |
| Resolution plan communicated to reporter | Within 30 calendar days |
| Public disclosure | 90 calendar days after initial report (see below) |

These are targets, not guarantees. Complex protocol-level vulnerabilities may
require longer triage. We will communicate proactively with reporters when
timelines slip.

## Disclosure Timeline

AIP follows a coordinated disclosure model with a **90-day embargo window**.

- Within 90 days: the Editors work with the reporter to understand the issue,
  design a mitigation, and publish a corrective AIP or errata.
- At 90 days: if no fix is published, the reporter may disclose at their
  discretion. We ask that reporters notify us 7 days before public disclosure.
- Accelerated disclosure: if active exploitation is detected in the wild, the
  embargo may be shortened by mutual agreement.

We will not pursue legal action against good-faith security researchers operating
within this policy.

## Embargo and Notification

When a critical vulnerability is confirmed, the Editors may notify known
implementers under embargo before public disclosure. To be on the embargo
notification list, open a public issue requesting inclusion and confirm the
organisation or project you represent.

Embargoed information MUST NOT be shared beyond the direct implementer team
until public disclosure.

## Severity Classification

We use a simplified severity scale:

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Remote exploitation enables token forgery, impersonation, or full revocation bypass with no preconditions | Signature verification bypass |
| **High** | Exploitation enables privilege escalation or delegation abuse under realistic conditions | Delegation depth check bypass |
| **Medium** | Exploitation requires specific conditions or yields limited impact | Timing side-channel in token comparison |
| **Low** | Informational or theoretical with no practical exploit path | Ambiguous spec language that could be misimplemented |

## Recognition

Security reporters who identify valid vulnerabilities are recognised in:

- [CONTRIBUTORS.md](CONTRIBUTORS.md) under a "Security Researchers" section
- The CHANGELOG entry for the spec version that resolves the reported issue

We will ask for your preferred name/handle before publishing recognition. You
may request to remain anonymous.

## Reference

The protocol-level threat model is documented in `docs/aip-spec.md`
§ Security Considerations. Implementers building AIP systems should review
that section in full.
