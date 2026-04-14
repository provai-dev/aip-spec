---
AIP: 0010
Title: Token Exchange for MCP via RFC 8693
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 7.5
Requires: 0005
Supersedes: ~
---

# AIP-0010: Token Exchange for MCP via RFC 8693

## Abstract

This proposal adds §7.5 defining a standardised token exchange flow that
allows an AIP-authenticated agent to obtain a scoped access token for a
Model Context Protocol (MCP) server or other OAuth-protected resource.
The exchange uses RFC 8693 (OAuth 2.0 Token Exchange) with the AIP
Credential Token as the `subject_token`, RFC 8707 resource indicators,
and DPoP binding on the exchange request.

## Motivation

AI agents operating in MCP environments need to bridge AIP identity into
the OAuth ecosystem. An agent with a valid AIP Credential Token must be
able to obtain a scoped access token for an MCP server without the human
principal re-authenticating. The current spec has no mechanism for this.

## Terminology

**Token Exchange** — An RFC 8693 flow in which the AIP Registry (acting
as OAuth AS per AIP-0005 §15.5) accepts an AIP Credential Token as
`subject_token` and issues a scoped access token for a target resource.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §7.5 Token Exchange for MCP (new section)

#### 7.5.1. Overview

An AIP agent MAY exchange its Credential Token for a scoped access token
targeting a specific MCP server or OAuth-protected resource. The exchange
is performed at the Registry's token endpoint (§15.5).

#### 7.5.2. Exchange Request

The agent sends an RFC 8693 token exchange request:

```
POST /v1/oauth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded
DPoP: <DPoP proof JWT>

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=<AIP Credential Token>
&subject_token_type=urn:ietf:params:oauth:token-type:jwt
&resource=https://mcp-server.example.com/
&scope=urn:aip:scope:email.read urn:aip:scope:calendar.read
```

**Normative requirements:**

1. `grant_type` MUST be `urn:ietf:params:oauth:grant-type:token-exchange`.
2. `subject_token` MUST be a valid AIP Credential Token.
3. `subject_token_type` MUST be `urn:ietf:params:oauth:token-type:jwt`.
4. `resource` MUST be present per RFC 8707, identifying the target
   resource server.
5. `scope` MUST use AIP scope URIs from the `urn:aip:scope:` namespace
   (see AIP-0011). The requested scopes MUST be a subset of the
   Credential Token's `aip_scope`.
6. DPoP proof [RFC9449] MUST be included, binding the exchange to the
   agent's key material.

#### 7.5.3. Exchange Validation

The Registry (as OAuth AS) MUST:

1. Validate the `subject_token` using the full 12-step algorithm (§7.3).
2. Verify the DPoP proof binds to the agent's public key.
3. Verify the requested `scope` is a subset of the `subject_token`'s
   `aip_scope` (attenuation only, never expansion).
4. Verify the `resource` is a registered MCP server or resource.
5. Issue an access token with:
   - `aud` set to the `resource` URI
   - `scope` set to the granted scopes
   - `sub` set to the agent's AID
   - `act.sub` set to the root principal's DID (actor chain per
     RFC 8693 §4.1)
   - TTL ≤ the remaining TTL of the `subject_token`
6. The access token MUST be a JWT per RFC 9068.

#### 7.5.4. Exchange Response

```json
{
  "access_token": "<JWT>",
  "token_type": "DPoP",
  "expires_in": 300,
  "scope": "urn:aip:scope:email.read urn:aip:scope:calendar.read",
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token"
}
```

### Normative Requirements

1. Token exchange MUST use RFC 8693.
2. DPoP MUST be required on the exchange request.
3. Scope attenuation only — exchanged token MUST NOT exceed source scope.
4. Access token TTL MUST NOT exceed subject token remaining TTL.
5. Access token MUST include `act.sub` for principal traceability.

### Failure Conditions

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| Subject token validation fails | `invalid_token` | 401 |
| Requested scope exceeds subject token scope | `insufficient_scope` | 403 |
| Resource not registered | `invalid_target` | 400 |
| DPoP proof missing or invalid | `dpop_required` | 401 |

### Schema Changes

No schema changes to existing files. The token exchange endpoint is
defined in §15.5 (AIP-0005).

## Security Considerations

**Scope attenuation:** The exchanged token can never exceed the source
Credential Token's scopes. This preserves the delegation chain's
attenuation guarantee through the exchange boundary.

**DPoP binding:** Requiring DPoP on the exchange request prevents
stolen Credential Tokens from being exchanged by a different party.

**TTL propagation:** The exchanged token's TTL is bounded by the source
token's remaining TTL, preventing TTL laundering.

**Principal traceability:** The `act.sub` claim preserves the root
principal's identity in the exchanged token, enabling audit.

## Backwards Compatibility

Fully backwards compatible. Token exchange is a new capability. Agents
and RPs that do not use MCP are unaffected.

## Test Vectors

This proposal requires no new cryptographic test vectors.

## Alternatives Considered

**Direct AIP token presentation to MCP.** Rejected because MCP servers
expect standard OAuth tokens, not AIP-specific JWT formats.

**Client Credentials grant.** Rejected because it does not carry the
delegation chain or principal identity.

## References

### Normative References

   [RFC2119]  <https://www.rfc-editor.org/info/rfc2119>
   [RFC8174]  <https://www.rfc-editor.org/info/rfc8174>
   [RFC8693]  Jones, M., Nadalin, A., Campbell, B., Bradley, J., and
              C. Mortimore, "OAuth 2.0 Token Exchange", RFC 8693,
              January 2020.
              <https://www.rfc-editor.org/info/rfc8693>
   [RFC8707]  Campbell, B., Bradley, J., and H. Tschofenig, "Resource
              Indicators for OAuth 2.0", RFC 8707, February 2020.
              <https://www.rfc-editor.org/info/rfc8707>
   [RFC9068]  <https://www.rfc-editor.org/info/rfc9068>
   [RFC9449]  <https://www.rfc-editor.org/info/rfc9449>

### Informative References

   AIP-0005 — Three-tier grant model (OAuth AS at Registry).
   AIP-0011 — Scope Map Interface (AIP scope URIs).

## Changelog

- 2026-04-12 — Initial draft.
