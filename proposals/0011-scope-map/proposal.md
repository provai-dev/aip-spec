---
AIP: 0011
Title: Scope Map Interface and AIP Scope URI namespace
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 15.6
Requires: ~
Supersedes: ~
---

# AIP-0011: Scope Map Interface and AIP Scope URI namespace

## Abstract

This proposal defines the `urn:aip:scope:` URI namespace for AIP
capability scopes and adds a §15.6 Scope Map endpoint that returns a
machine-readable mapping of scope URIs to human-readable descriptions,
Tier classification, and constraint schemas. This enables programmatic
discovery of available scopes by wallets, deployers, and MCP servers.

## Motivation

AIP scopes (e.g., `email.read`, `transactions`) are currently defined
inline in §3 and §4.5.3 as enumerated strings. There is no
machine-readable registry of valid scopes, no URI namespace for
interoperability with OAuth, and no programmatic way for a wallet or
MCP server to discover what scopes a Registry supports.

The `urn:aip:scope:` namespace enables AIP scopes to be used in
standard OAuth scope parameters (RFC 6749 §3.3) during token exchange
(AIP-0010) and G3 authorization flows (AIP-0005).

## Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### Scope URI Namespace

All AIP capability scopes MUST be representable as URIs in the
`urn:aip:scope:` namespace. The mapping is:

```
scope_string → urn:aip:scope:<scope_string>
```

Examples:
- `email.read` → `urn:aip:scope:email.read`
- `transactions` → `urn:aip:scope:transactions`
- `spawn_agents.create` → `urn:aip:scope:spawn_agents.create`

When used in OAuth `scope` parameters, the URI form MUST be used.
Within AIP Credential Tokens (`aip_scope` array), the short string
form remains canonical.

### §15.6 Scope Map Endpoint (new section)

A conformant AIP Registry MUST implement:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v1/scopes` | Return the scope map |

**Response:** A JSON object mapping scope strings to metadata:

```json
{
  "scopes": {
    "email.read": {
      "uri": "urn:aip:scope:email.read",
      "description": "Read email messages and metadata",
      "tier": 1,
      "destructive": false,
      "constraint_schema": null
    },
    "transactions": {
      "uri": "urn:aip:scope:transactions",
      "description": "Make financial transactions",
      "tier": 2,
      "destructive": true,
      "constraint_schema": {
        "max_single_transaction": { "type": "number" },
        "max_daily_total": { "type": "number" },
        "currency": { "type": "string" },
        "require_confirmation_above": { "type": "number" }
      }
    }
  },
  "aip_version": "0.3"
}
```

**Response fields per scope:**

| Field | Type | Description |
|-------|------|-------------|
| `uri` | string | Full `urn:aip:scope:` URI |
| `description` | string | Human-readable description |
| `tier` | integer | Tier classification (1, 2, or 3) |
| `destructive` | boolean | Whether this scope requires additional confirmation per §4.5.3 |
| `constraint_schema` | object/null | JSON Schema fragment for scope-specific constraints in the Capability Manifest |

### Normative Requirements

1. All AIP scopes MUST have a corresponding `urn:aip:scope:` URI.
2. The scope map endpoint MUST be implemented by conformant Registries.
3. The scope map MUST include tier classification for each scope.
4. OAuth interactions (G3, token exchange) MUST use the URI form.
5. Credential Token `aip_scope` arrays MUST continue using the short
   string form.

### Failure Conditions

No new error codes. The endpoint returns standard HTTP errors (404 if
not implemented, 500 on internal error).

### Schema Changes

Create `spec/v0.3/schemas/scope-map.schema.json`.

## Security Considerations

The scope map is public, read-only information. No authentication is
required. The scope map does not reveal agent-specific data.

## Backwards Compatibility

Fully backwards compatible. The `urn:aip:scope:` namespace and scope
map endpoint are new. Existing `aip_scope` arrays in Credential Tokens
are unchanged.

## Test Vectors

This proposal requires no new test vectors.

## Alternatives Considered

**Embed scope definitions in the spec only.** Rejected because
programmatic discovery is needed for wallet UIs and MCP integration.

**Use OAuth scope strings directly.** Rejected because AIP scopes have
richer semantics (tier, destructive flag, constraint schemas) that
standard OAuth scopes do not carry.

## References

### Normative References

   [RFC2119]  <https://www.rfc-editor.org/info/rfc2119>
   [RFC8174]  <https://www.rfc-editor.org/info/rfc8174>

### Informative References

   AIP-0005 — Three-tier grant model (G3 OAuth scope parameter).
   AIP-0010 — Token Exchange for MCP (scope URI usage).

## Changelog

- 2026-04-12 — Initial draft.
