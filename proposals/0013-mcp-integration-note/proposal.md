---
AIP: 0013
Title: MCP Integration Bridge informative note in §1.2
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Informational
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 1.2
Requires: 0010
Supersedes: ~
---

# AIP-0013: MCP Integration Bridge informative note in §1.2

## Abstract

This proposal adds an informative note to §1.2 (Scope and Goals)
describing how AIP integrates with the Model Context Protocol (MCP).
The note positions AIP as the identity and authorization layer that MCP
assumes but does not define, and references the token exchange mechanism
(AIP-0010) as the concrete bridge.

## Motivation

MCP is emerging as a standard for agent-to-tool communication, but it
delegates identity and authorization to external mechanisms. §1.2
currently lists "MCP" nowhere. Implementers building MCP-based agent
systems need a clear pointer to how AIP provides the missing identity
layer.

## Terminology

This proposal introduces no new terms.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §1.2 Scope and Goals — New Informative Note

Add after the existing scope bullets:

> **Integration with Model Context Protocol (MCP):** AIP provides the
> agent identity, authorization, and delegation layer that MCP server
> implementations require but do not define. An AIP-authenticated agent
> can obtain scoped access tokens for MCP servers via the token exchange
> mechanism defined in §7.5. AIP does not replace MCP; it provides the
> identity substrate on which MCP authorization decisions are made. See
> §7.5 (Token Exchange) and §15.5 (OAuth Authorization Server) for the
> concrete integration path.

This note is informative, not normative. No RFC 2119 keywords are used.

### Normative Requirements

None. This proposal is informational.

### Failure Conditions

None.

### Schema Changes

None.

## Security Considerations

This proposal introduces no new threat vectors and does not alter any
existing security requirement. It is a documentation-only change.

## Backwards Compatibility

Fully backwards compatible. Informative text only.

## Test Vectors

This proposal requires no new test vectors.

## Alternatives Considered

**Add a full MCP interoperability section.** Deferred to a future AIP
once MCP's own authorization model stabilises.

## References

### Normative References

   [RFC2119]  <https://www.rfc-editor.org/info/rfc2119>
   [RFC8174]  <https://www.rfc-editor.org/info/rfc8174>

### Informative References

   AIP-0010 — Token Exchange for MCP via RFC 8693.
   Model Context Protocol specification.

## Changelog

- 2026-04-12 — Initial draft.
