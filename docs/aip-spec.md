# Agent Identity Protocol (AIP)
## Specification — Draft v0.1

**Authors:** Paras Singla ([@itisparas](https://github.com/itisparas)), ProvAI
**Repository:** https://github.com/provai-dev/aip-spec
**Status:** Draft — not yet stable, expect changes before v1.0
**License:** CC0 1.0 Universal — implement freely, no rights reserved
**Date:** March 22, 2026

## Abstract

   The Agent Identity Protocol (AIP) defines an open, layered identity
   framework for autonomous AI agents. AIP specifies a W3C DID-
   conformant agent identifier (`did:aip`), a cryptographically
   verifiable principal delegation chain, a fine-grained capability
   manifest, a signed credential token format and deterministic 12-step
   validation algorithm, a standardised revocation mechanism, and a
   reputation data format. Two independent implementations conforming to
   this specification MUST produce interoperable systems. This document
   is the consolidated RFC-style rendering of AIP-CORE v0.1 and AIP-
   SECURITY v0.1; the informational architecture overview is covered in
   Section 1.

## Status of This Memo

   This document is an internal draft specification of the ProvAI
   project. It describes a proposed internet standard for AI agent
   identity. Distribution of this document is unrestricted. Comments
   and contributions are welcome via the project repository at
   https://github.com/provai-dev/aip-spec.

   This specification is released under CC0 1.0 Universal. No rights
   reserved. Implement freely.

## Copyright Notice

   Copyright (C) ProvAI (2026). All rights reserved as permitted under
   CC0 1.0 Universal.

---

## Table of Contents

```
1.  Introduction
    1.1.  Motivation
    1.2.  Design Philosophy
    1.3.  Architecture Layers
2.  Conventions and Definitions
3.  Terminology
4.  Resource Model
    4.1.  Resource Naming
    4.2.  JSON Schema Representations
        4.2.1.  Agent Identity
        4.2.2.  Capability Manifest
        4.2.3.  Credential Token
        4.2.4.  Principal Token
        4.2.5.  Registration Envelope
        4.2.6.  Revocation Object
        4.2.7.  Endorsement
    4.3.  Field Constraints
5.  Registration Protocol
    5.1.  Registration Envelope
    5.2.  Registration Validation (12-Step Algorithm)
    5.3.  Error Responses
6.  Agent Resolution
    6.1.  DID Resolution
    6.2.  DID Document Structure
7.  Credential Tokens
    7.1.  Token Structure
    7.2.  Token Issuance
    7.3.  Token Validation
8.  Delegation
    8.1.  Delegation Chain
    8.2.  Capability Scope Rules
    8.3.  Delegation Validation
9.  Revocation
    9.1.  Revocation Object
    9.2.  Certificate Revocation List (CRL)
    9.3.  Revocation Checking
10. Principal Chain
11. Reputation and Endorsements
    11.1.  Endorsement Object
    11.2.  Reputation Scoring
12. Lifecycle States
13. Error Handling
    13.1.  Error Response Format
    13.2.  Standard Error Codes
    13.3.  Error Detail Types
14. Rate Limiting
15. Versioning and Compatibility
16. Security Considerations
    16.1.  Threat Model
    16.2.  Cryptographic Requirements
    16.3.  Proof-of-Possession (DPoP)
    16.4.  Key Management
    16.5.  Token Security
    16.6.  Delegation Chain Security
    16.7.  Registry Security
    16.8.  Revocation Security
    16.9.  Privacy Considerations
17. IANA Considerations
18. Normative References
19. Informative References
Acknowledgements
Authors' Addresses
```

---

## 1. Introduction

   In 2026, AI agents are deployed in production environments, operating
   autonomously on behalf of individuals and organisations. An agent may
   send emails, book appointments, make purchases, access file systems,
   spawn child agents to complete subtasks, and communicate across
   multiple platforms, all without explicit human approval for each
   action.

   This creates an identity vacuum. When an agent presents itself to an
   API, a payment processor, or another agent, there is no standard
   mechanism to establish: the agent's persistent identity across
   interactions; the human or organisation on whose authority it acts;
   the specific actions it is permitted to take; whether it has been
   compromised or revoked; or whether it has a trustworthy history.

   AIP fills this vacuum. It is designed as neutral, open
   infrastructure, the same way HTTP, OAuth, and JWT provide
   infrastructure that any application can build on without vendor
   dependency.

### 1.1. Motivation

   The absence of an identity standard creates concrete operational
   problems. Services cannot implement fine-grained agent access
   control. Humans have no auditable record of what their agents did.
   Compromised agents cannot be reliably stopped. Agent-to-agent
   systems have no basis for trust.

   Current agent deployments operate in one of two modes: no access, or
   full access. AIP introduces fine-grained capability declarations. A
   principal can grant `email.read` without `email.send`, or
   `transactions` with a `max_daily_total` constraint. These constraints
   are expressed in a signed manifest stored in the Registry and
   verified independently by every relying party.

### 1.2. Design Philosophy

   AIP is built on five design principles:

   Neutral and open. The spec is released under CC0 and the `did:aip`
   DID method is registered with the W3C.

   Build on existing standards. AIP builds on W3C DID, JWT [RFC7519],
   JWK [RFC7517], DPoP [RFC9449], and CRL patterns from [RFC5280].

   Human sovereignty. Every agent action must trace to a human or
   authorised organisational principal.

   Security proportional to risk. AIP defines three security tiers
   matching overhead to risk level.

   Deterministic verification. The Validation Algorithm is fully
   deterministic: two independent implementations executing the same
   steps on the same token MUST reach the same result.

   Zero Trust Architecture. AIP implements the zero trust principles
   defined in [SP-800-207]. No agent is implicitly trusted by virtue
   of its origin, network location, or prior successful interaction.
   Every Credential Token MUST be validated against the Registry on
   every interaction. Short-lived Credential Tokens (Section 7.2)
   bound by a mandatory TTL limit the blast radius of any credential
   compromise. Revocation is checked in real time for Tier 2 sensitive
   operations (Section 16.3). DPoP proof-of-possession (Section 16.3)
   ensures that possession of a valid Credential Token is insufficient
   for impersonation without the corresponding private key material,
   satisfying the anti-replay requirement of [SP-800-207] Section 3.

   Least Privilege. Agents are granted only the specific capabilities
   required for their declared purpose, expressed as signed Capability
   Manifests (Section 8). Capability grants are always additive from
   principal to agent and never exceed the granting principal's own
   capability set. A child agent MUST NOT be granted capabilities that
   the delegating parent does not itself hold (Rule D-1, Section 8.2).
   The max_delegation_depth field (Section 8.1) bounds the depth of
   sub-agent hierarchies, limiting transitive capability propagation.
   Capability constraints allow fine-grained least-privilege expression
   within each capability category, consistent with [SP-800-207]
   Section 3 (Tenets 5 and 6).

   Relationship to SPIFFE/SPIRE. SPIFFE is designed for
   workload identity within enumerable, infrastructure-managed
   environments. AIP is designed for autonomous agents that are created
   dynamically, operate across organisational boundaries, and act on
   behalf of named human principals whose authority must be
   cryptographically traceable. An enterprise MAY deploy SPIFFE for its
   internal service mesh and AIP for its agent fleet without conflict.
   The two mechanisms are complementary and operate at distinct layers
   of the identity stack.

   Relationship to MCP. The Model Context Protocol [MCP] defines how
   AI agents discover and invoke tools and data sources. AIP is the
   agent identity layer that sits beneath MCP's authorisation flow:
   AIP establishes that an agent is who it claims to be (identification
   via Credential Token), that it was authorised by a named human
   principal (delegation chain in the Principal Token), and that it
   holds specific capabilities (Capability Manifest). AIP does not
   replace MCP's tool-access OAuth flow — it provides the agent
   identity that OAuth's "sub" claim cannot supply when the subject is
   an autonomous agent rather than a human user.

   Out of scope — Prompt injection prevention. AIP is an identity and
   authorisation protocol. Whether the content an agent processes
   contains adversarial instructions is an application-layer and
   model-layer concern outside this specification's scope. AIP
   mitigates the persistence window of a successful prompt injection
   attack: a compromised agent MAY be immediately revoked via
   full_revoke (Section 9.1), and revocation MUST propagate to all
   child agents within the TTL window defined in Section 7.2. AIP
   does not prevent the initial injection — it limits the attacker's
   persistence.

### 1.3. Architecture Layers

   AIP is structured as six ordered layers:

```
   +------------------------------------------------------+
   |  Layer 6 - Reputation          Trust over time       |
   +------------------------------------------------------+
   |  Layer 5 - Revocation          Standard kill switch  |
   +------------------------------------------------------+
   |  Layer 4 - Credential Token & Verification           |
   |                                Cryptographic proof   |
   +------------------------------------------------------+
   |  Layer 3 - Capabilities        What the agent can do |
   +------------------------------------------------------+
   |  Layer 2 - Principal Chain     Who authorised it     |
   +------------------------------------------------------+
   |  Layer 1 - Core Identity       Who the agent IS      |
   +------------------------------------------------------+
```

---

## 2. Conventions and Definitions

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
   "OPTIONAL" in this document are to be interpreted as described in
   BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all
   capitals, as shown here.

   JSON is used throughout this document as defined in [RFC8259].

   URIs are used as defined in [RFC3986].

   ABNF notation is used as defined in [RFC5234].

   HTTP status codes and headers are as defined in [RFC9110].

---

## 3. Terminology

   The following terms are used throughout this document.

   **Agent** — An autonomous software system powered by a large
   language model that can perceive inputs, reason about them, and
   execute actions in the world on behalf of a principal.

   **AID (Agent Identity)** — A globally unique, persistent identifier
   for an agent conforming to the `did:aip` DID method defined in
   Section 6.

   **Principal** — The human or organisational entity on whose
   authority an agent acts. Every AIP delegation chain MUST have a
   verifiable principal at its root.

   **Capability Manifest** — A versioned, signed JSON document stored
   in the Registry that declares the specific permissions granted to
   an agent.

   **Credential Token** — A signed JWT-format token presented by an
   agent to a relying party as proof of identity and authorisation for
   a specific interaction.

   **Relying Party** — Any service, API, or agent that receives and
   verifies an AIP Credential Token.

   **Delegation** — The act of granting a subset of capabilities from
   a principal or parent agent to a child agent.

   **Delegation Depth** — A non-negative integer counter incremented at
   each delegation step. The first agent directly authorised by the root
   principal has delegation depth 0.

   **Registry** — A service implementing the Registry Interface defined
   in Section 5 that stores AID public keys, revocation status, and
   reputation data.

   **Scope** — A string identifier naming a specific capability
   permission, using dot-notation format, as defined in Section 4.3.

   **Principal Chain** — The complete, cryptographically verifiable
   sequence from a root principal through all intermediate agents to the
   acting agent, embedded in every Credential Token as the `aip_chain`
   array of signed Principal Token JWTs.

   **Ephemeral Agent** — An agent spawned to complete a specific task
   and automatically revoked upon completion.

   **Orchestrator** — An agent whose primary function is spawning and
   managing other agents.

   **DPoP (Demonstrating Proof of Possession)** — A cryptographic
   mechanism per [RFC9449] that proves the presenter of a token also
   holds the private key corresponding to the token's public key.

   **DID Resolution** — The process of retrieving a DID Document for a
   given DID, per [W3C-DID] Section 7. AIP implementations MUST support
   resolution of at minimum `did:key` and `did:web` DID methods.
   Resolved DID Documents MAY be cached for a maximum of 300 seconds.
   If resolution fails or times out, implementations MUST treat the
   result as `registry_unavailable` and MUST reject the operation rather
   than proceed with an unverified key.

---

## 4. Resource Model

### 4.1. Resource Naming

   Agent Identities (AIDs) are W3C Decentralized Identifiers [W3C-DID]
   using the `did:aip` method. The AID syntax conforms to [RFC3986] URI
   syntax and the DID Core specification. The ABNF grammar is:

```abnf
   aip-did    = "did:aip:" namespace ":" unique-id
   namespace  = LOALPHA *( LOALPHA / DIGIT )
                *( "-" 1*( LOALPHA / DIGIT ) )
   unique-id  = 32LOHEXDIG
   LOALPHA    = %x61-7A        ; a-z only
   DIGIT      = %x30-39        ; 0-9
   LOHEXDIG   = DIGIT / "a" / "b" / "c" / "d" / "e" / "f"
                               ; lowercase hex only -- MUST NOT use A-F
```

   The `namespace` MUST begin with a lowercase alpha character,
   MUST NOT end with a hyphen, and MUST NOT contain consecutive hyphens.
   Both `namespace` and `unique-id` MUST use only lowercase characters.
   Implementations MUST reject AIDs containing uppercase hex digits or
   uppercase namespace characters.

   The following namespace values are defined. Implementations MUST
   recognise these values. Additional namespaces MAY be defined by the
   community and registered in the AIP Namespace Registry.

   | Namespace      | Description                                             |
   |----------------|---------------------------------------------------------|
   | `personal`     | An agent acting for a single human principal            |
   | `enterprise`   | An agent acting within an organisational deployment     |
   | `service`      | A persistent agent providing a capability as a service  |
   | `ephemeral`    | An agent created for a single task; revoked on completion |
   | `orchestrator` | An agent whose primary function is spawning child agents |

   Compound typed identifiers use prefixed UUID v4 values:

   | Object Type          | Prefix | Example                              |
   |----------------------|--------|--------------------------------------|
   | Capability Manifest  | `cm:`  | `cm:550e8400-e29b-41d4-a716-...`     |
   | Revocation Object    | `rev:` | `rev:6ba7b810-9dad-11d1-80b4-...`    |
   | Endorsement Object   | `end:` | `end:6ba7b811-9dad-11d1-80b4-...`    |

### 4.2. JSON Schema Representations

   All AIP objects MUST be validated against the JSON Schemas defined
   in this section. The canonical schema files are located in the
   `schemas/latest/` directory of the AIP specification repository.

   Signing note for non-JWT objects: Capability Manifests, Revocation
   Objects, Endorsement Objects, and Core Identity Objects are signed
   using EdDSA with an explicit canonical field ordering for
   serialisation before signing. The signing field order for each object
   is defined in the relevant subsection below. Before computing the
   signature, the `signature` field (or `previous_key_signature` for
   identity objects) MUST be set to the empty string `""`.

#### 4.2.1. Agent Identity

   The Core Identity Object is the persistent identity record for an
   AIP agent. It MUST be submitted as part of a Registration Envelope
   (Section 5.1) and MUST conform to the following schema.

   Canonical signing field order for `previous_key_signature`:
   `aid`, `name`, `type`, `model`, `created_at`, `version`,
   `public_key`, `previous_key_signature`.

   | Field                    | Type    | Required | Constraints                  |
   |--------------------------|---------|----------|------------------------------|
   | `aid`                    | string  | REQUIRED | MUST match `did:aip` ABNF; pattern `^did:aip:[a-z][a-z0-9]*(-[a-z0-9]+)*:[0-9a-f]{32}$` |
   | `name`                   | string  | REQUIRED | minLength: 1, maxLength: 64  |
   | `type`                   | string  | REQUIRED | MUST exactly match the namespace component of `aid`; pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` |
   | `model`                  | object  | REQUIRED | See sub-fields below         |
   | `model.provider`         | string  | REQUIRED | minLength: 1, maxLength: 64  |
   | `model.model_id`         | string  | REQUIRED | minLength: 1, maxLength: 128 |
   | `model.attestation_hash` | string  | OPTIONAL | pattern: `^sha256:[0-9a-f]{64}$` |
   | `created_at`             | string  | REQUIRED | ISO 8601 UTC; format: date-time; immutable after registration |
   | `version`                | integer | REQUIRED | minimum: 1; MUST increment by exactly 1 on key rotation |
   | `public_key`             | object  | REQUIRED | JWK per [RFC7517]; Ed25519 (kty=OKP, crv=Ed25519) per [RFC8037] |
   | `public_key.kty`         | string  | REQUIRED | const: `"OKP"`               |
   | `public_key.crv`         | string  | REQUIRED | const: `"Ed25519"`           |
   | `public_key.x`           | string  | REQUIRED | pattern: `^[A-Za-z0-9_-]{43}$` (32 bytes base64url, no padding) |
   | `public_key.kid`         | string  | REQUIRED | pattern: `^did:aip:[a-z][a-z0-9]*(-[a-z0-9]+)*:[0-9a-f]{32}#key-[1-9][0-9]*$`; starts at `#key-1` |
   | `previous_key_signature` | string  | OPTIONAL (version=1); REQUIRED (version>=2) | base64url EdDSA signature of new object (with this field set to `""`) signed by retiring key; pattern: `^[A-Za-z0-9_-]+$` |

   Normative requirements:

   The `aid`, `type`, and `created_at` fields MUST NOT change after
   initial registration.

   The `type` field MUST exactly match the namespace component of the
   `aid` field. A mismatch MUST be rejected.

   The `version` field MUST start at 1 and MUST increment by exactly 1
   on each key rotation.

   The `public_key.kid` MUST use format `<aid>#key-<n>` where `<n>`
   starts at 1 and increments by 1 on each rotation. The value
   `#key-0` is not valid and MUST be rejected.

   When `version` is 2 or greater, `previous_key_signature` MUST be
   present and MUST be a non-empty base64url string.

   Implementations receiving an unrecognised `type` value SHOULD treat
   the agent as type `service` for capability enforcement purposes and
   MUST log an unknown-type warning.

#### 4.2.2. Capability Manifest

   The Capability Manifest is a versioned, signed JSON document that
   declares the specific permissions granted to an agent. It is issued
   by the principal or parent agent (`granted_by`) and stored in the
   Registry.

   Canonical signing field order: `manifest_id`, `aid`, `granted_by`,
   `version`, `issued_at`, `expires_at`, `capabilities`, `signature`.

   | Field         | Type    | Required | Constraints                       |
   |---------------|---------|----------|-----------------------------------|
   | `manifest_id` | string  | REQUIRED | pattern: `^cm:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
   | `aid`         | string  | REQUIRED | MUST match `did:aip` ABNF         |
   | `granted_by`  | string  | REQUIRED | MUST be a valid W3C DID; pattern: `^did:[a-z][a-z0-9]*:.+$` |
   | `version`     | integer | REQUIRED | minimum: 1; MUST increment on every update including `scope_revoke` |
   | `issued_at`   | string  | REQUIRED | ISO 8601 UTC; format: date-time   |
   | `expires_at`  | string  | REQUIRED | ISO 8601 UTC; MUST be after `issued_at` |
   | `capabilities`| object  | REQUIRED | See Section 4.3 for all sub-fields |
   | `signature`   | string  | REQUIRED | base64url EdDSA signature; pattern: `^[A-Za-z0-9_-]+$` |

   A new `manifest_id` MUST be generated on every update, including
   `scope_revoke` operations. Reusing a `manifest_id` for a different
   manifest version is forbidden.

   Relying parties MUST verify the manifest `signature` field using the
   public key of the `granted_by` DID before trusting any capability
   declared within it. A manifest whose signature is invalid MUST be
   rejected as if the capability were not present.

   An absent or empty `capabilities` object (`{}`) MUST be interpreted
   as no capabilities granted. Implementations MUST NOT treat an absent
   capabilities object as implicitly granting any permission.

   The `version` field MUST be incremented on every update to the
   manifest. Relying parties MAY cache the manifest `version` to detect
   staleness: if the Registry returns a manifest with the same or lower
   `version` than a previously seen one, the relying party SHOULD
   re-fetch.

#### 4.2.3. Credential Token

   An AIP Credential Token is a compact JWT with the following format:

```
   aip-token = JWT-header "." JWT-payload "." JWT-signature
```

   The token MUST be a valid JWT as defined by [RFC7519].

   JWT Header fields:

   | Field | Requirement | Value / Constraints                             |
   |-------|-------------|--------------------------------------------------|
   | `typ` | MUST        | `"AIP+JWT"`                                       |
   | `alg` | MUST        | `"EdDSA"` (REQUIRED); `"ES256"` (OPTIONAL); `"RS256"` (OPTIONAL, legacy enterprise only; MUST NOT be the sole supported algorithm) |
   | `kid` | MUST        | DID URL identifying the signing key, e.g., `did:aip:personal:9f3a...#key-2`; MUST match the `kid` in the signing agent's Core Identity Object |

   Credential Token Payload fields:

   | Field         | Type         | Required | Constraints                       |
   |---------------|--------------|----------|-----------------------------------|
   | `iss`         | string       | REQUIRED | MUST match `did:aip` ABNF; MUST equal `sub` of last `aip_chain` element |
   | `sub`         | string       | REQUIRED | MUST match `did:aip` ABNF; MUST equal `iss` for non-delegated tokens |
   | `aud`         | string/array | REQUIRED | Single string or array; MUST include the relying party's identifier; minLength: 1 per element |
   | `iat`         | integer      | REQUIRED | Unix timestamp; MUST NOT be in the future (30-second clock skew tolerance) |
   | `exp`         | integer      | REQUIRED | Unix timestamp; MUST be strictly greater than `iat`; TTL limits per Section 7.2 |
   | `jti`         | string       | REQUIRED | UUID v4 canonical lowercase; pattern: `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
   | `aip_version` | string       | REQUIRED | AIP protocol version that produced this token. MUST be `"0.1"` for tokens conforming to this specification. Implementations MUST reject tokens where `aip_version` identifies a version not supported by the validator. |
   | `aip_scope`   | array        | REQUIRED | minItems: 1; uniqueItems: true; each item matches `^[a-z_]+([.][a-z_]+)*$` |
   | `aip_chain`   | array        | REQUIRED | minItems: 1; maxItems: 11; each element is a compact-serialised signed Principal Token JWT |
   | `aip_registry`| string       | OPTIONAL | URI of AIP Registry; format: uri  |

   Duplicate scope strings MUST NOT appear in `aip_scope`.

   The `aip_version` claim enables forward-compatible version
   negotiation. A validator receiving a Credential Token with an
   unrecognised `aip_version` value MUST reject the token with an
   `invalid_token` error and SHOULD include the received
   `aip_version` value in the `error_description` field to aid
   client debugging. A validator MAY support multiple `aip_version`
   values simultaneously to facilitate migration across protocol
   versions.

#### 4.2.4. Principal Token

   A Principal Token is a JWT payload encoding one delegation link in
   the AIP principal chain. Principal Tokens are embedded as compact-
   serialised JWTs in the `aip_chain` array of a Credential Token.

   Principal Tokens use standard JWT signing (base64url(header) +
   "." + base64url(payload) compact serialisation), not a custom
   canonicalization order.

   | Field                  | Type         | Required | Constraints                |
   |------------------------|--------------|----------|----------------------------|
   | `sub`                  | string       | REQUIRED | MUST match `did:aip` ABNF  |
   | `principal`            | object       | REQUIRED | See sub-fields below       |
   | `principal.type`       | string       | REQUIRED | enum: `["human", "organisation"]` |
   | `principal.id`         | string       | REQUIRED | W3C DID; pattern: `^did:[a-z][a-z0-9]*:.+$`; MUST be byte-for-byte identical across all chain elements; MUST NOT use `did:aip` method |
   | `delegated_by`         | string/null  | REQUIRED | null when `delegation_depth` is 0; MUST be a `did:aip` AID when `delegation_depth` > 0 |
   | `delegation_depth`     | integer      | REQUIRED | minimum: 0, maximum: 10; MUST equal the array index of this token in `aip_chain` |
   | `max_delegation_depth` | integer      | REQUIRED | minimum: 0, maximum: 10; default: 3 when absent; only the value from `aip_chain[0]` governs the chain |
   | `issued_at`            | string       | REQUIRED | ISO 8601 UTC; format: date-time |
   | `expires_at`           | string       | REQUIRED | ISO 8601 UTC; MUST be strictly after `issued_at` |
   | `purpose`              | string       | OPTIONAL | maxLength: 128              |
   | `task_id`              | string/null  | OPTIONAL; REQUIRED for ephemeral agents | minLength: 1, maxLength: 256 when non-null |
   | `scope`                | array        | REQUIRED | minItems: 1; uniqueItems: true; each item matches `^[a-z_]+([.][a-z_]+)*$` |

   The `principal.id` field MUST be byte-for-byte identical across
   every Principal Token in the same `aip_chain` array. Relying parties
   MUST verify this consistency. An intermediate agent MUST NOT
   substitute its own AID, any other DID, or a modified form of the
   original principal DID.

   The `principal.id` MUST NOT begin with `did:aip:`. A root principal
   MUST be a human or organisational DID, never an AIP agent AID.

#### 4.2.5. Registration Envelope

   The Registration Envelope is the request body submitted to
   `POST /v1/agents` to register a new AIP agent. The Registry MUST
   validate all components and MUST either accept all or reject all.
   Partial registration MUST NOT be possible.

   | Field                | Type   | Required | Constraints                       |
   |----------------------|--------|----------|-----------------------------------|
   | `identity`           | object | REQUIRED | MUST conform to agent-identity schema; `version` MUST be 1; `previous_key_signature` MUST NOT be present |
   | `capability_manifest`| object | REQUIRED | MUST conform to capability-manifest schema; `version` MUST be 1; `aid` MUST equal `identity.aid` |
   | `principal_token`    | string | REQUIRED | Compact JWT (header.payload.signature); pattern: `^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$` |

   The Registration Envelope as a whole is not signed; each component
   (`capability_manifest`, `principal_token`) carries its own
   cryptographic signature.

#### 4.2.6. Revocation Object

   A Revocation Object is a signed document submitted to the Registry to
   revoke or modify an agent's credentials.

   Canonical signing field order: `revocation_id`, `target_aid`, `type`,
   `issued_by`, `reason`, `timestamp`, `propagate_to_children`,
   `scopes_revoked`, `signature`.

   | Field                    | Type    | Required | Constraints                    |
   |--------------------------|---------|----------|--------------------------------|
   | `revocation_id`          | string  | REQUIRED | pattern: `^rev:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
   | `target_aid`             | string  | REQUIRED | MUST match `did:aip` ABNF      |
   | `type`                   | string  | REQUIRED | enum: `["full_revoke", "scope_revoke", "delegation_revoke", "principal_revoke"]` |
   | `issued_by`              | string  | REQUIRED | W3C DID; pattern: `^did:[a-z][a-z0-9]*:.+$`; MUST be in the target agent's delegation chain or be the root principal |
   | `reason`                 | string  | REQUIRED | enum: `["device_compromised", "key_compromised", "task_complete", "policy_violation", "principal_request", "account_closure", "parent_revoked", "other"]` |
   | `timestamp`              | string  | REQUIRED | ISO 8601 UTC; format: date-time |
   | `propagate_to_children`  | boolean | OPTIONAL | default: false; when true, Registry MUST also revoke all agents delegated by `target_aid` |
   | `scopes_revoked`         | array   | REQUIRED when `type` is `scope_revoke`; MUST NOT be present for other types | minItems: 1; uniqueItems: true; each item matches `^[a-z_]+([.][a-z_]+)*$` |
   | `signature`              | string  | REQUIRED | base64url EdDSA signature; pattern: `^[A-Za-z0-9_-]+$` |

   Registries MUST verify the `signature` before processing any
   revocation. Unsigned or invalidly signed Revocation Objects MUST be
   rejected.

   The `reason` value `parent_revoked` is generated exclusively by the
   Registry when propagating child revocations. External parties MUST
   NOT use this reason value.

#### 4.2.7. Endorsement

   An Endorsement Object is a signed task-outcome record submitted by
   one AIP agent to endorse another.

   Canonical signing field order: `endorsement_id`, `from_aid`,
   `to_aid`, `task_id`, `outcome`, `notes`, `timestamp`, `signature`.

   | Field            | Type        | Required | Constraints                         |
   |------------------|-------------|----------|-------------------------------------|
   | `endorsement_id` | string      | REQUIRED | pattern: `^end:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
   | `from_aid`       | string      | REQUIRED | MUST match `did:aip` ABNF; MUST NOT equal `to_aid` |
   | `to_aid`         | string      | REQUIRED | MUST match `did:aip` ABNF; MUST NOT equal `from_aid` |
   | `task_id`        | string      | REQUIRED | minLength: 1, maxLength: 256        |
   | `outcome`        | string      | REQUIRED | enum: `["success", "partial", "failure"]` |
   | `notes`          | string/null | OPTIONAL | maxLength: 512                      |
   | `timestamp`      | string      | REQUIRED | ISO 8601 UTC; format: date-time     |
   | `signature`      | string      | REQUIRED | base64url EdDSA signature; pattern: `^[A-Za-z0-9_-]+$` |

   The Registry MUST verify the signature of every submitted Endorsement
   Object using the public key registered for the `from_aid`. The
   Registry MUST NOT increment `endorsement_count` for unverified
   submissions. The Registry MUST NOT accept endorsements where
   `from_aid` equals `to_aid`.

### 4.3. Field Constraints

   Capability Manifest `capabilities` object sub-fields:

   **email capability:**

   | Sub-field                  | Type    | Constraints                              |
   |----------------------------|---------|------------------------------------------|
   | `email.read`               | boolean | default: false                           |
   | `email.write`              | boolean | default: false                           |
   | `email.send`               | boolean | default: false                           |
   | `email.delete`             | boolean | default: false                           |
   | `email.max_recipients_per_send` | integer | OPTIONAL; minimum: 1, maximum: 100; MUST be enforced at send time when `email.send` is true |

   **calendar capability:**

   | Sub-field          | Type    | Constraints    |
   |--------------------|---------|----------------|
   | `calendar.read`    | boolean | default: false |
   | `calendar.write`   | boolean | default: false |
   | `calendar.delete`  | boolean | default: false |

   **filesystem capability:**

   | Sub-field              | Type    | Constraints                                      |
   |------------------------|---------|--------------------------------------------------|
   | `filesystem.read`      | array   | Allowed read paths; MUST use absolute paths; empty array MUST be treated as deny-all; each path: minLength: 1, maxLength: 512 |
   | `filesystem.write`     | array   | Allowed write paths; MUST use absolute paths; empty array MUST be treated as deny-all |
   | `filesystem.execute`   | boolean | default: false; Tier 2 sensitive scope; requires DPoP and 300-second TTL cap |
   | `filesystem.delete`    | boolean | default: false; deletion only permitted on paths also listed in `write` |

   An empty array `[]` for `filesystem.read` or `filesystem.write`
   MUST be interpreted as deny-all. Implementations MUST NOT treat an
   empty array as allow-all.

   **web capability:**

   | Sub-field                    | Type    | Constraints                             |
   |------------------------------|---------|------------------------------------------|
   | `web.browse`                 | boolean | default: false                           |
   | `web.forms_submit`           | boolean | default: false                           |
   | `web.download`               | boolean | default: false                           |
   | `web.max_requests_per_hour`  | integer | OPTIONAL; minimum: 1, maximum: 10000; rolling 60-minute UTC window |

   **transactions capability:**

   | Sub-field                         | Type    | Constraints                    |
   |-----------------------------------|---------|--------------------------------|
   | `transactions.enabled`            | boolean | REQUIRED in this object        |
   | `transactions.max_single_transaction` | number | REQUIRED when `enabled` is true; exclusiveMinimum: 0 |
   | `transactions.max_daily_total`    | number  | REQUIRED when `enabled` is true; exclusiveMinimum: 0 |
   | `transactions.currency`           | string  | REQUIRED when `enabled` is true; ISO 4217; pattern: `^[A-Z]{3}$` |
   | `transactions.require_confirmation_above` | number | OPTIONAL; minimum: 0; MUST be <= `max_single_transaction` when both fields are present |

   A `require_confirmation_above` value above `max_single_transaction`
   is vacuous and MUST be rejected by the Registry.

   **communicate capability:**

   | Sub-field              | Type    | Constraints                              |
   |------------------------|---------|------------------------------------------|
   | `communicate.enabled`  | boolean | REQUIRED; master switch; when false, all channel flags are ignored |
   | `communicate.whatsapp` | boolean | default: false                           |
   | `communicate.telegram` | boolean | default: false                           |
   | `communicate.sms`      | boolean | default: false                           |
   | `communicate.voice`    | boolean | default: false                           |

   When `communicate.enabled` is true, at least one channel MUST be
   explicitly present and set to true. An enabled communicate capability
   with all channels absent or false is a configuration error and MUST
   be rejected.

   **spawn_agents capability:**

   | Sub-field                     | Type    | Constraints                       |
   |-------------------------------|---------|-----------------------------------|
   | `spawn_agents.enabled`        | boolean | REQUIRED in this object           |
   | `spawn_agents.max_concurrent` | integer | REQUIRED when `enabled` is true; minimum: 1, maximum: 100 |
   | `spawn_agents.types_allowed`  | array   | OPTIONAL; items: enum `["personal", "enterprise", "service", "ephemeral", "orchestrator"]` |

   **Defined Scope Identifiers:**

   The following scope identifiers are defined. Implementations MUST
   recognise these identifiers. Additional scopes MAY be defined by
   extension.

```
   email.read          -- Read access to email messages and metadata
   email.write         -- Create and modify draft email messages
   email.send          -- Send email messages
   email.delete        -- Permanently delete email messages

   calendar.read       -- Read access to calendar events and metadata
   calendar.write      -- Create and modify calendar events
   calendar.delete     -- Delete calendar events

   filesystem.read     -- Read files from specified paths
   filesystem.write    -- Write files to specified paths
   filesystem.execute  -- Execute scripts or commands (Tier 2)
   filesystem.delete   -- Permanently delete files

   web.browse          -- Retrieve public web content via HTTP GET
   web.forms_submit    -- Submit HTML forms (HTTP POST to web services)
   web.download        -- Download and persist files from the web

   transactions        -- Execute financial transactions (Tier 2)

   communicate.whatsapp    -- Send messages via WhatsApp
   communicate.telegram    -- Send messages via Telegram
   communicate.sms         -- Send SMS messages
   communicate.voice       -- Initiate or receive voice calls

   spawn_agents            -- Create child agents via AIP delegation
```

   Where this document references `transactions.*` or `communicate.*`,
   this means: any token whose `aip_scope` array contains `transactions`
   (the bare capability key) OR any scope beginning with `transactions.`
   as a prefix, or `communicate.enabled: true` in the Capability
   Manifest respectively.

---

## 5. Registration Protocol

### 5.1. Registration Envelope

   An agent is registered by submitting a Registration Envelope to
   `POST /v1/agents`. The Registry MUST implement this endpoint. The
   request body MUST be a JSON object with the following top-level
   fields:

   - `identity`: The Core Identity Object (Section 4.2.1)
   - `capability_manifest`: The initial Capability Manifest (Section
     4.2.2)
   - `principal_token`: A compact-serialised signed Principal Token JWT
     (Section 4.2.4)

   The `principal_token` MUST have `delegation_depth` equal to 0 and
   `delegated_by` equal to null. The `sub` field of the decoded
   principal token payload MUST equal `identity.aid`.

### 5.2. Registration Validation

   The Registry MUST perform the following checks in order before
   accepting a Registration Envelope. The Registry MUST either accept
   all or reject all — partial registration MUST NOT be possible.

   Check 1. `identity` MUST be present and MUST be valid JSON
   conforming to the Core Identity Object schema.

   Check 2. `identity.aid` MUST match the `did:aip` ABNF grammar
   defined in Section 4.1.

   Check 3. `identity.type` MUST equal the namespace component of
   `identity.aid`. A mismatch MUST be rejected.

   Check 4. `identity.aid` MUST NOT already exist in the Registry.

   Check 5. `identity.public_key` MUST be an Ed25519 JWK with
   `kty="OKP"`, `crv="Ed25519"`, and a 43-character base64url `x`
   value.

   Check 6. `capability_manifest.expires_at` MUST be in the future at
   the time of registration.

   Check 7. `capability_manifest.aid` MUST equal `identity.aid`.

   Check 8. The `principal_token` string MUST be decodable as a compact-
   serialised JWT and MUST conform to the Principal Token schema
   (Section 4.2.4).

   Check 9. The decoded `principal_token` payload `sub` MUST equal
   `identity.aid`.

   Check 10. The decoded `principal_token` payload `principal.id` MUST
   NOT begin with `did:aip:`.

   Check 11. If `identity.type` is `ephemeral`, the decoded
   `principal_token` payload `task_id` MUST be non-null and non-empty.

   Check 12. `capability_manifest.signature` MUST be verifiable against
   the `granted_by` DID's public key.

   Check 13. If `identity.version` is 2 or greater,
   `identity.previous_key_signature` MUST be present and MUST verify
   using the key at the previous version.

### 5.3. Error Responses

   All AIP error responses MUST use the following JSON structure:

```json
   {
     "error": "<error_code>",
     "error_description": "<human-readable description>",
     "error_uri": "https://provai.dev/errors/<error_code>"
   }
```

   Implementations MUST use the exact string values for the `error`
   field as defined in Section 13.2.

   Implementations MUST NOT return HTTP 200 for error conditions.

---

## 6. Agent Resolution

### 6.1. DID Resolution

   Every AID MUST have a corresponding W3C DID Document that is
   resolvable by any standard DID resolver. The DID Document is derived
   deterministically from the Core Identity Object stored in the
   Registry.

   Implementations MUST generate and serve DID Documents from the
   Registry's `GET /v1/agents/{aid}` endpoint when the `Accept:
   application/did+ld+json` or `Accept: application/did+json` header is
   present.

   AIP implementations MUST support DID resolution for at minimum
   `did:key` and `did:web` DID methods. Resolved DID Documents MAY be
   cached for a maximum of 300 seconds. If resolution fails or times
   out, implementations MUST treat the result as `registry_unavailable`
   and MUST reject the operation.

   The Registry MUST return DID resolution metadata alongside the DID
   Document. The `didResolutionMetadata` object MUST include:

```json
   {
     "contentType": "application/did+ld+json",
     "retrieved": "<ISO 8601 UTC timestamp of resolution>",
     "did": {
       "didString": "<the resolved AID>",
       "methodSpecificId": "<the 32-hex unique-id component>"
     }
   }
```

   If the AID has been revoked, the Registry MUST return a
   `deactivated: true` flag in `didDocumentMetadata` alongside the DID
   Document, per [W3C-DID] Section 7.1.2.

### 6.2. DID Document Structure

   A conformant `did:aip` DID Document MUST include the following
   fields:

   | Field                | Requirement        | Value                              |
   |----------------------|--------------------|------------------------------------|
   | `@context`           | MUST               | `["https://www.w3.org/ns/did/v1", "https://w3id.org/security/suites/jws-2020/v1"]` |
   | `id`                 | MUST               | The AID string                     |
   | `verificationMethod` | MUST               | Array with at least one entry for the current public key |
   | `authentication`     | MUST               | Array referencing the current verification method |
   | `controller`         | MUST               | The AID itself                     |

   The following fields are OPTIONAL but RECOMMENDED:

   | Field                   | Value                                          |
   |-------------------------|------------------------------------------------|
   | `assertionMethod`       | Same reference as `authentication`             |
   | `capabilityInvocation`  | Same reference                                 |
   | `service`               | Registry endpoint for AIP-specific resolution  |

   The `verificationMethod` array entry MUST be constructed from the
   `public_key` JWK in the Core Identity Object as follows:

```json
   {
     "id": "<aid>#key-<n>",
     "type": "JsonWebKey2020",
     "controller": "<aid>",
     "publicKeyJwk": {
       "kty": "OKP",
       "crv": "Ed25519",
       "x": "<base64url-encoded public key bytes>"
     }
   }
```

   During key rotation, the DID Document MUST reflect only the current
   active key in `verificationMethod`. Historical keys MUST NOT appear
   in the current DID Document but are accessible via
   `/v1/agents/{aid}/public-key/{key-id}`.

   The CRUD operations for `did:aip` are:

   | Operation   | Mechanism                                         |
   |-------------|---------------------------------------------------|
   | Create      | `POST /v1/agents` with Registration Envelope      |
   | Read        | `GET /v1/agents/{aid}` with DID Accept header     |
   | Update      | `PUT /v1/agents/{aid}` for key rotation only      |
   | Deactivate  | `POST /v1/revocations` with `full_revoke` object  |

---

## 7. Credential Tokens

### 7.1. Token Structure

   An AIP Credential Token is transmitted as an HTTP Authorization
   header:

```
   Authorization: AIP <token>
   X-AIP-Version: 1
```

   For interactions requiring Proof-of-Possession, the DPoP proof MUST
   be included as an additional header:

```
   Authorization: AIP <token>
   DPoP: <dpop-proof>
   X-AIP-Version: 1
```

### 7.2. Token Issuance

   Implementations MUST enforce the following maximum token lifetimes
   (TTL = `exp - iat`):

   | Scope Category                                            | Maximum TTL             |
   |-----------------------------------------------------------|-------------------------|
   | All standard scopes (`email.*`, `calendar.*`, `web.*`, etc.) | 3600 seconds (1 hour) |
   | `transactions.*` or `communicate.*`                       | 300 seconds (5 minutes) |
   | `filesystem.execute`                                      | 300 seconds (5 minutes) |
   | `spawn_agents`                                            | 3600 seconds (1 hour)   |

   Relying parties MUST reject tokens where `exp - iat` exceeds the
   maximum TTL for the requested scopes. When a token contains scopes
   from multiple categories, the most restrictive TTL applies.

   Zero-duration and negative-duration tokens (where `exp <= iat`) MUST
   be rejected.

### 7.3. Token Validation

   A relying party MUST execute the following 12 steps in order when
   validating an AIP Credential Token. The relying party MUST reject the
   token at the first step that fails and MUST NOT proceed to subsequent
   steps.

   **Step 1 — Parse token structure.** Parse the token as a JWT. If
   parsing fails, return `invalid_token`.

   **Step 2 — Verify header fields.** The `typ` field MUST be
   `"AIP+JWT"`. The `alg` field MUST be one of the approved suites
   (Section 16.2). If either check fails, return `invalid_token`.

   **Step 3 — Identify signing agent.** Extract the `kid` field from
   the header. This MUST be a valid DID URL with a `did:aip` base and
   a key fragment. Extract the base AID. Retrieve the historical public
   key matching the full `kid` value from the Registry. If the key
   version is not found, return `unknown_aid`.

   **Step 4 — Verify signature.** Verify the token signature using the
   retrieved public key. If verification fails, return `invalid_token`.

   **Step 5 — Verify claims.**
   a) The `iat` value MUST NOT be in the future (clock skew tolerance:
      at most 30 seconds).
   b) The `exp` value MUST be strictly greater than `iat`. If
      `exp <= iat`, return `invalid_token`.
   c) The `exp` value MUST be in the future. If expired, return
      `token_expired`.
   d) The `aud` value MUST match the relying party's identifier. If
      not, return `invalid_token`.
   e) The `jti` value MUST NOT match any previously seen JTI for this
      issuer within the token's validity window. If matched, return
      `token_replayed`.
   f) The `aip_version` claim MUST be present. If absent, return
      `invalid_token`. The `aip_version` value MUST identify a
      protocol version supported by the validator. If the version is
      unrecognised, return `invalid_token`.

   **Step 6 — Check TTL constraints.** Verify that `exp - iat` does
   not exceed the maximum TTL for the requested scopes per Section 7.2.
   If exceeded, return `invalid_token`.

   **Step 7 — Check revocation status.** Query the revocation status of
   the `iss` AID from the Registry. If revoked, return `agent_revoked`.

   **Step 8 — Verify delegation chain.** Decode each element of
   `aip_chain` as a compact-serialised JWT. For each Principal Token at
   index `i` (from 0 to n-1):

   a) Verify the token is a valid JWT conforming to the Principal Token
      schema (Section 4.2.4).
   b) Verify `delegation_depth` equals exactly `i`. For i=0 this means
      `delegation_depth` MUST be 0. For i>0 it MUST equal i. If not,
      return `invalid_delegation_depth`.
   c) Verify `delegation_depth` does not exceed `max_delegation_depth`
      from the root Principal Token (index 0). If the root token's
      `max_delegation_depth` is absent, treat it as 3. If exceeded,
      return `invalid_delegation_depth`. Only the value from
      `aip_chain[0]` governs the entire chain.
   d) Resolve the signing party's public key and verify the token
      signature: for index 0, resolve the root principal's DID from
      `aip_chain[0].principal.id` per [W3C-DID] Section 7; for index
      `i > 0`, retrieve the public key for `aip_chain[i-1].sub` from
      the Registry. If DID resolution fails, return
      `registry_unavailable`.
   e) Verify the `delegated_by` field of each token at index `i > 0`
      matches the `sub` field of the token at index `i-1`. If not,
      return `delegation_chain_invalid`.
   f) Verify each `sub` AID in the chain (excluding the root principal)
      has not been revoked. If revoked, return `agent_revoked`.
   g) Verify no AID appears more than once across all `sub` values in
      the chain. If circular, return `delegation_chain_invalid`.
   h) Verify the `expires_at` field of each Principal Token is strictly
      after its `issued_at` field. Verify `expires_at` is in the future
      (30-second clock skew tolerance). If any chain token has expired
      or has `expires_at <= issued_at`, return `chain_token_expired`.
   i) Verify `principal.id` is identical across all chain elements. If
      `principal.id` differs between any two chain elements, return
      `delegation_chain_invalid`.
   j) Verify that `principal.id` from `aip_chain[0]` does NOT begin
      with `did:aip:`. If it does, return `delegation_chain_invalid`.

   If any check a-j fails, return the specific error code indicated.

   **Step 8 Post-Check A.** After all per-element checks pass, verify
   that the `iss` claim in the Credential Token payload equals the `sub`
   field of the last element of `aip_chain`. If `iss` does not match
   `aip_chain[n-1].sub`, return `delegation_chain_invalid`.

   **Step 8 Post-Check B.** For non-delegated tokens (where `aip_chain`
   contains exactly one element), verify that `iss` equals `sub` in the
   Credential Token payload. If not, return `delegation_chain_invalid`.
   For delegated tokens (chain length > 1), `iss` and `sub` MAY differ.

   **Step 9 — Verify capability scope.** Fetch the agent's Capability
   Manifest from the Registry using the base AID from Step 3.

   For Tier 2 operations, the Capability Manifest MUST be fetched fresh
   on every request. Cached manifests MUST NOT be used for Tier 2. For
   Tier 1 operations, manifests MAY be cached for a maximum of 60
   seconds.

   a) Verify the manifest `signature` using the public key of
      `granted_by`, resolved per [W3C-DID] Section 7. If signature
      verification fails or the manifest cannot be retrieved, return
      `manifest_invalid`.
   b) Verify the manifest `expires_at` is in the future. If expired,
      return `manifest_expired`.
   c) For delegated agents (chain length > 1): fetch each ancestor
      agent's Capability Manifest, up to a maximum of
      `max_delegation_depth` additional fetches (default cap: 3).
      Verify that the acting agent's requested scopes and constraint
      values do not exceed those of any ancestor. Ancestor manifests MAY
      be cached for a maximum of 60 seconds. If an ancestor manifest is
      unavailable, return `manifest_invalid`. If the scope inheritance
      rule (Section 8.2) is violated, return `insufficient_scope`.
   d) Verify each scope in `aip_scope` is present and enabled in the
      verified manifest using the following exhaustive mapping:

   | Scope string           | Manifest field requirement                                   |
   |------------------------|--------------------------------------------------------------|
   | `email.read`           | `capabilities.email.read: true`                              |
   | `email.write`          | `capabilities.email.write: true`                             |
   | `email.send`           | `capabilities.email.send: true`                              |
   | `email.delete`         | `capabilities.email.delete: true`                            |
   | `calendar.read`        | `capabilities.calendar.read: true`                           |
   | `calendar.write`       | `capabilities.calendar.write: true`                          |
   | `calendar.delete`      | `capabilities.calendar.delete: true`                         |
   | `filesystem.read`      | `capabilities.filesystem.read` is a non-empty array          |
   | `filesystem.write`     | `capabilities.filesystem.write` is a non-empty array         |
   | `filesystem.execute`   | `capabilities.filesystem.execute: true`                      |
   | `filesystem.delete`    | `capabilities.filesystem.delete: true`                       |
   | `web.browse`           | `capabilities.web.browse: true`                              |
   | `web.forms_submit`     | `capabilities.web.forms_submit: true`                        |
   | `web.download`         | `capabilities.web.download: true`                            |
   | `transactions`         | `capabilities.transactions.enabled: true`                    |
   | `communicate.whatsapp` | `capabilities.communicate.enabled: true` AND `capabilities.communicate.whatsapp: true` |
   | `communicate.telegram` | `capabilities.communicate.enabled: true` AND `capabilities.communicate.telegram: true` |
   | `communicate.sms`      | `capabilities.communicate.enabled: true` AND `capabilities.communicate.sms: true` |
   | `communicate.voice`    | `capabilities.communicate.enabled: true` AND `capabilities.communicate.voice: true` |
   | `spawn_agents`         | `capabilities.spawn_agents.enabled: true`                    |

   If any requested scope is not present or not enabled per these
   mappings, return `insufficient_scope`.

   **Step 10 — Verify Proof-of-Possession (conditional).** If any scope
   in `aip_scope` is `transactions` or matches `transactions.*`, or
   matches `communicate.*`, or is `filesystem.execute`, the relying
   party MUST verify the DPoP proof per Section 16.3. If the DPoP proof
   is absent or invalid, return `dpop_proof_required`.

   **Step 11 — Tier 3 supplementary checks (conditional).** For relying
   parties operating under Tier 3 (enterprise/regulated) requirements:
   a) Verify the mutual TLS client certificate presented by the agent
      maps to the AID in `iss`. If mTLS is not established, return
      `invalid_token`.
   b) Perform an OCSP check for the agent's certificate per [RFC5280].
      If the OCSP response indicates revocation, return `agent_revoked`.
      If the OCSP responder is unreachable, return
      `registry_unavailable`.

   Tier 3 checks supplement, they do not replace, Steps 1 through 10.

   **Step 12 — Accept.** All checks passed. The token is valid. Proceed
   with the requested operation.

---

## 8. Delegation

### 8.1. Delegation Chain

   Every Credential Token MUST include a verifiable Principal Chain
   linking the acting agent to its root principal. The chain MUST be
   cryptographically signed at each delegation step.

   The root principal MUST be one of the following:

   - A human identified by a W3C DID (e.g., `did:key:z6Mk...` or
     `did:web:...`)
   - An organisational entity identified by a W3C DID

   Implementations MUST NOT accept a root principal that is itself an
   AIP agent AID. `principal.id` MUST NOT use the `did:aip` DID method.

   The maximum delegation depth is 10 (hard maximum). The default
   maximum delegation depth MUST NOT exceed 3.

### 8.2. Capability Scope Rules

   The following Delegation Rules MUST be enforced by all
   implementations:

   **Rule D-1.** A delegated agent MUST NOT issue a Capability Manifest
   granting scopes that are not a subset of its own granted scopes.
   Additionally, all constraint values (e.g., `max_single_transaction`)
   in the child's manifest MUST be less than or equal to the
   corresponding constraint values in the parent's manifest.

   **Rule D-2.** A delegated agent MUST NOT issue a Principal Token with
   a `max_delegation_depth` value greater than its own remaining
   delegation depth (`max_delegation_depth` - `delegation_depth`).

   **Rule D-3.** Implementations MUST reject any Credential Token where
   the `delegation_depth` value of any token in the chain exceeds the
   `max_delegation_depth` value set in the root Principal Token.

   **Rule D-4.** For the root Principal Token (index 0 in `aip_chain`),
   `delegation_depth` MUST be exactly 0. For every subsequent Principal
   Token at index `i > 0`, `delegation_depth` MUST be exactly `i`. No
   gaps, skips, or repeated values are permitted.

   **Rule D-5.** Each token in the delegation chain MUST be signed by
   the private key corresponding to the public key registered for the
   `delegated_by` AID, or the root principal's key for depth 0.

   Scope Inheritance Rule: When an agent issues a delegation to a child
   agent, for each scope `s` granted to the child, `s` MUST be present
   in the parent agent's own Capability Manifest scopes AND all
   constraint values for `s` in the child's manifest MUST be less than
   or equal to the corresponding constraint values in the parent's
   manifest.

   Implementations MUST enforce this rule at delegation time.
   Relying parties MUST independently verify this rule during validation
   per Validation Algorithm Step 9c.

### 8.3. Delegation Validation

   Ancestor Manifest Fetch Limits: To prevent unbounded Registry
   requests during validation, implementations MUST NOT fetch more
   ancestor manifests than the `max_delegation_depth` value of the
   chain's root token (defaulting to 3). If a chain's depth exceeds
   this limit during validation, the implementation MUST return
   `manifest_invalid`.

   Ancestor Manifest Caching: Ancestor Capability Manifests MAY be
   cached for a maximum of 60 seconds. The acting agent's manifest MUST
   follow the Tier 1/2 freshness rules.

   Ancestor Manifest Unavailability: If any ancestor's Capability
   Manifest cannot be retrieved, the relying party MUST return
   `manifest_invalid` and MUST NOT fall back to cached data older than
   60 seconds.

---

## 9. Revocation

### 9.1. Revocation Object

   Revocation is performed by submitting a signed Revocation Object to
   `POST /v1/revocations`. The Revocation Object schema is defined in
   Section 4.2.6.

   Four revocation types are defined:

   **full_revoke** — Permanently revokes the AID. No further tokens
   issued by this AID are accepted. Sets `deactivated: true` in DID
   Document metadata.

   **scope_revoke** — Removes specific capability scopes from the agent's
   Capability Manifest. Requires the `scopes_revoked` field. Does NOT
   invalidate already-issued Credential Tokens. The practical effect is
   bounded by the TTL of outstanding tokens for the affected scopes.
   For immediate scope removal, issuers SHOULD issue a `full_revoke` and
   re-register the agent with a reduced Capability Manifest.

   **delegation_revoke** — Invalidates all delegation chains rooted at
   the target AID. Child agents lose their delegation authority. The
   target AID itself remains valid for direct principal interactions.

   **principal_revoke** — Issued by the root principal to revoke their
   entire authorisation of the target agent. Equivalent to `full_revoke`
   from the principal's perspective. Child agents are also invalidated.

### 9.2. Certificate Revocation List (CRL)

   The Registry MUST expose a Certificate Revocation List at
   `GET /v1/crl`. The CRL MUST be updated within 15 minutes of a new
   Revocation Object being accepted. The CRL endpoint MUST be served
   from a CDN or distributed infrastructure.

   Relying parties SHOULD validate against the CRL at token issuance
   time (Tier 1 operations).

### 9.3. Revocation Checking

   Implementations MUST enforce the following revocation checking tiers
   based on the agent's active capability scopes:

   **Tier 1 — Standard capabilities.** Tokens MUST have TTL less than
   or equal to 3600 seconds. Relying parties SHOULD validate against
   the CRL at token issuance time. The CRL MUST be refreshed at minimum
   every 15 minutes.

   **Tier 2 — Sensitive capabilities** (`transactions.*`,
   `communicate.*`, `filesystem.execute`). Tokens MUST have TTL less
   than or equal to 300 seconds. Relying parties MUST perform a real-
   time revocation check against the Registry on every request. Relying
   parties MUST NOT cache the revocation status for these AIDs. If the
   Registry cannot be reached during a required real-time check, the
   relying party MUST deny the request and return `registry_unavailable`.
   Relying parties MUST NOT fall back to cached revocation data for Tier
   2 operations.

   **Tier 3 — Enterprise/regulated deployments.** Implementations
   operating at Tier 3 MUST use mutual TLS (mTLS) authentication.
   The Registry MUST support OCSP responses per [RFC5280]. Tier 3
   supplements, but does not replace, Tier 2 requirements.

   Child Agent Propagation: When the Registry processes a Revocation
   Object with `propagate_to_children: true`, the Registry MUST:

   1. Look up all AIDs indexed as direct children of the `target_aid`
      using the delegation relationship index maintained at registration
      time from `delegated_by` fields.
   2. Issue a Revocation Object for each identified child AID with
      `reason: "parent_revoked"`, `propagate_to_children: true`, and
      `issued_by` set to the `target_aid` of the triggering Revocation
      Object. The Registry MUST sign these auto-generated Revocation
      Objects using its own administrative key.
   3. Process child revocations recursively (depth-first).
   4. Complete the entire recursive process within 15 seconds of
      receiving the original Revocation Object on the authoritative
      Registry.

   Replica Registries MUST synchronise revocation status from the
   authoritative Registry within 45 seconds. The end-to-end revocation
   propagation window MUST NOT exceed 60 seconds combined.

   Replica operators who cannot meet the 45-second synchronisation SLA
   MUST NOT serve revocation status for Tier 2 operations.

---

## 10. Principal Chain

   The Principal Chain is the cryptographic proof connecting an agent's
   actions to the authorising human or organisation. It is embedded in
   every Credential Token as the `aip_chain` array.

   The `principal.id` field MUST be byte-for-byte identical in every
   Principal Token in the `aip_chain` array. An intermediate agent
   MUST NOT change it. Specifically:

   - The `principal.id` value in every Principal Token MUST identify
     the same originating human or organisation.
   - Even when a sub-agent delegates to a further sub-agent, every token
     in that chain MUST carry the same root principal DID.
   - A compromised intermediate agent MUST NOT be able to re-root the
     chain under a different principal it controls.

   Every element in `aip_chain` is a compact-serialised JWT (header +
   payload + signature) whose payload conforms to the Principal Token
   schema (Section 4.2.4). Elements are ordered root-to-leaf (index 0
   is the delegation issued directly by the root principal; index n-1
   is the immediate parent of the acting agent).

   The maximum `aip_chain` length is 11 (corresponding to the hard
   maximum delegation depth of 10). Implementations MUST reject tokens
   with `aip_chain` length exceeding 11.

   Cryptographic non-repudiation: Every Credential Token carries a
   delegation chain in which each link is independently signed by the
   delegating principal's private key. Because principal.id is
   byte-identical across all chain elements and is bound to the
   signing key, every agent action is cryptographically attributable
   to the human or organisational principal that authorised it. A
   principal MUST NOT be able to repudiate an action taken by their
   agent if the signed Principal Tokens in the delegation chain are
   intact — the chain constitutes cryptographic evidence that cannot
   be constructed without access to the principal's private key. This
   property satisfies the non-repudiation requirement of
   [SP-800-63-4] Section 11.

---

## 11. Reputation and Endorsements

### 11.1. Endorsement Object

   Any relying party or agent MAY submit a signed Endorsement Object to
   the Registry after a completed interaction. The Endorsement Object
   schema is defined in Section 4.2.7.

   The Registry MUST verify the signature of every submitted Endorsement
   Object. The Registry MUST NOT increment `endorsement_count` for
   unverified submissions.

   Only `success` and `partial` outcomes increment `endorsement_count`.
   The `failure` outcome increments `incident_count`.

### 11.2. Reputation Scoring

   The Registry MUST expose reputation data for every registered AID
   via `GET /v1/agents/{aid}/reputation`.

   The following fields MUST be present in the reputation record:

   | Field                    | Type         | Description                         |
   |--------------------------|--------------|-------------------------------------|
   | `registration_date`      | string       | ISO 8601 UTC of first registration  |
   | `task_count`             | integer (>= 0) | Total interactions with Endorsement Objects submitted |
   | `successful_task_count`  | integer (>= 0) | Interactions with `success` or `partial` outcome |
   | `endorsement_count`      | integer (>= 0) | Verified positive endorsements     |
   | `incident_count`         | integer (>= 0) | Verified failures plus policy violations |
   | `revocation_history`     | array        | Ordered list of revocation events, oldest first |
   | `last_active`            | string/null  | ISO 8601 UTC of most recent verified interaction, or null |

   The Registry MUST enforce that `successful_task_count` never exceeds
   `task_count` at write time.

   The Registry MAY expose a reference advisory score, clearly labelled
   as `advisory_only: true`. Relying parties MUST NOT treat an advisory
   score as normative.

   Advisory score `tier` values: `unverified`, `known`, `trusted`,
   `verified`, `sovereign`.

   Reputation Non-Transferability: Reputation data is bound to a
   specific AID. Implementations MUST NOT transfer reputation from a
   revoked AID to a new AID. Endorsements from an AID whose current
   revocation status is `revoked` (via `full_revoke` or
   `principal_revoke`) MUST NOT be weighted. Historical `scope_revoke`
   events alone do not disqualify an AID's endorsements.

   AIP standardises reputation inputs. Implementations MUST NOT define
   a mandatory scoring formula. Relying parties MAY apply their own
   scoring models to the standardised data.

   Note on continuous audit logging: AIP Endorsement Objects
   (Section 11.1) provide post-interaction signed records that
   constitute a tamper-evident audit trail for completed agent
   interactions. AIP does not define a real-time continuous action
   log format — continuous logging is expected to be implemented at
   the application layer and is outside the scope of this protocol.

---

## 12. Lifecycle States

   An AID has exactly two lifecycle states: `active` and `revoked`.

   The AIP specification does not define an `inactive` status distinct
   from `revoked`. The Dead Man's Switch mechanism (Section 16.8)
   achieves its effect through the standard `full_revoke` mechanism.

   AID Lifecycle rules:

   An AID MUST be registered with an AIP Registry before use.

   An AID MUST remain valid until explicitly revoked via the mechanism
   defined in Section 9.

   Implementations MUST NOT allow an AID to be reused after revocation.

   Key rotation MUST increment the `version` field, update the
   `public_key` JWK in the Registry, and include a valid
   `previous_key_signature` signed by the retiring private key. The
   AID MUST NOT change on key rotation.

   Outstanding tokens signed under the previous key MUST remain valid
   until their `exp` time. Relying parties MUST verify tokens against
   the key version identified by the token's `kid` header.

   For ephemeral agents: Agents with namespace `ephemeral` MUST have a
   non-null `task_id` in their Principal Token. Ephemeral agents MUST
   be explicitly revoked upon task completion. If an ephemeral agent's
   stored `expires_at` timestamp passes and no explicit Revocation
   Object has been received, the Registry SHOULD automatically issue a
   `full_revoke` with `reason: "task_complete"`.

---

## 13. Error Handling

### 13.1. Error Response Format

   All AIP error responses MUST use the following JSON structure:

```json
   {
     "error": "<error_code>",
     "error_description": "<human-readable description>",
     "error_uri": "https://provai.dev/errors/<error_code>"
   }
```

   The `error` field MUST contain one of the defined error code strings.
   The `error_description` field SHOULD contain a human-readable
   explanation of the error.

   Implementations MUST use the exact string values for the `error`
   field as defined in Section 13.2.

   Implementations MUST NOT return HTTP 200 for error conditions.

### 13.2. Standard Error Codes

   | Error Code                 | HTTP Status | Description                                  |
   |----------------------------|-------------|----------------------------------------------|
   | `invalid_token`            | 401         | Token is malformed, has an invalid signature, or contains invalid header/payload claims |
   | `token_expired`            | 401         | Token `exp` claim is in the past             |
   | `token_replayed`           | 401         | Token `jti` has been seen before within the validity window |
   | `dpop_proof_required`      | 401         | The requested scope requires DPoP Proof-of-Possession, which was absent or invalid |
   | `agent_revoked`            | 403         | The AID has been revoked                     |
   | `insufficient_scope`       | 403         | The requested operation is not within the agent's granted and currently valid scopes |
   | `invalid_delegation_depth` | 403         | `delegation_depth` does not equal its chain index, or exceeds `max_delegation_depth` |
   | `chain_token_expired`      | 403         | One or more Principal Tokens in `aip_chain` have passed their `expires_at` timestamp |
   | `delegation_chain_invalid` | 403         | The delegation chain has a structural error: circular delegation, `iss` mismatch, inconsistent `principal.id`, `principal.id` using `did:aip`, or broken `sub`/`delegated_by` linkage |
   | `manifest_invalid`         | 403         | Capability Manifest signature verification failed, or manifest could not be retrieved |
   | `manifest_expired`         | 403         | Capability Manifest has passed its `expires_at` timestamp |
   | `unknown_aid`              | 404         | The AID is not registered in any accessible Registry |
   | `registry_unavailable`     | 503         | The Registry could not be reached to complete a required verification step |

### 13.3. Error Detail Types

   For `registry_unavailable` responses with HTTP status 503,
   implementations SHOULD include a `Retry-After` header per [RFC9110]
   indicating when the service is expected to become available again.

   For rate limiting responses (HTTP 429), the response MUST include a
   `Retry-After` header per [RFC6585] Section 4.

---

## 14. Rate Limiting

   The Registry SHOULD implement rate limiting on all endpoints to
   protect against denial-of-service attacks and credential stuffing.

   When rate limiting is applied, the Registry MUST return HTTP 429 with
   a `Retry-After` header per [RFC6585] Section 4 indicating when the
   client may retry.

   The response body SHOULD conform to the error response format
   (Section 13.1) with an appropriate `error_description`.

---

## 15. Versioning and Compatibility

   AIP follows Semantic Versioning: MAJOR.MINOR (no PATCH for spec
   versions).

   Before v1.0: MINOR versions MAY include breaking changes. Stability
   is not guaranteed.

   Versioned spec documents are frozen under `spec/vMAJOR.MINOR/`. Any
   change requires a new version.

   `spec/latest/` always reflects the most recent approved version but
   is not authoritative for implementations. Implementations SHOULD pin
   to a specific version.

   Every new version MUST include a `CHANGELOG.md` with a summary of
   changes, a breaking changes list, and a migration guide where
   applicable.

   Deprecated features MUST be documented. Removal is only allowed in
   a MAJOR version bump.

   Implementations that receive an unknown `type` value in an Agent
   Identity Object SHOULD treat the agent as type `service` for
   capability enforcement purposes and MUST log an unknown-type warning.

   Implementations that receive a Credential Token with an unsupported
   `alg` value MUST return `invalid_token` and MUST NOT attempt to
   verify the token with a different algorithm.

---

## 16. Security Considerations

### 16.1. Threat Model

   The following assets are within scope for AIP security:

   | Asset                | Value                                                 |
   |----------------------|-------------------------------------------------------|
   | Agent private keys   | Compromise allows impersonation of the agent          |
   | Credential Tokens    | Theft allows replay attacks within the validity window |
   | Capability Manifests | Tampering allows privilege escalation                 |
   | Delegation Chains    | Forgery allows unauthorised agent action              |
   | Revocation Records   | Suppression allows continued operation of compromised agents |
   | Principal Identity   | Compromise breaks the root of trust for all delegated agents |

   AIP considers the following threat actors:

   **T1 — External Attacker.** No legitimate access to AIP
   infrastructure. Attempts to intercept tokens, forge identities, or
   exploit protocol weaknesses.

   **T2 — Compromised Agent.** A legitimate AIP agent whose private key
   or runtime has been compromised. May attempt to escalate capabilities
   or impersonate other agents.

   **T3 — Malicious Sub-Agent.** An ephemeral or service agent that
   attempts to acquire capabilities beyond those delegated to it.

   **T4 — Rogue Registry.** A Registry implementation that returns
   false revocation or reputation data.

   **T5 — Insider Principal.** A human or organisational principal who
   revokes agents maliciously or issues excessive delegations.

   **TS-1 (Bearer Token Theft).** Mitigation: DPoP Proof-of-Possession
   (Section 16.3), short token TTLs (Section 7.2), TLS transport
   (Section 16.5).

   **TS-2 (Capability Escalation via Delegation).** Mitigation: Scope
   intersection rule (Section 8.2). Relying parties MUST verify scope
   inheritance across the entire delegation chain (Step 9c).

   **TS-3 (Revocation Suppression).** Mitigation: Short TTLs for
   sensitive scopes (max 300 seconds), multiple revocation channels
   (CRL + real-time check), signed Revocation Objects.

   **TS-4 (Principal Impersonation).** Mitigation: The root Principal
   Token MUST be signed by the principal's key. Relying parties MUST
   verify this signature at Step 8d and verify `principal.id`
   consistency at Step 8i.

   **TS-5 (Token Replay).** Mitigation: `jti` MUST be a UUID v4.
   Relying parties MUST maintain a (`iss`, `jti`) replay cache (Section
   16.5). DPoP proofs bind each request to a specific HTTP method, URL,
   and timestamp.

   **TS-6 (Delegation Depth Exhaustion).** Mitigation:
   `max_delegation_depth` is set by the root principal and cannot be
   increased. Hard maximum is 10. Default MUST NOT exceed 3.

   **TS-7 (Registry Unavailability Attack).** Mitigation: Short token
   TTLs. Relying parties MUST NOT fall back to expired cache for Tier 2
   scopes. Section 16.7 defines Registry availability requirements.

   **TS-8 (Root Principal Key Compromise).** The most severe failure
   mode. Upon discovery of compromise, the principal MUST: (1) rotate
   the principal's DID key immediately; (2) issue `full_revoke`
   Revocation Objects for all agents whose delegation chain roots at
   the compromised key; (3) re-register all required agents under the
   new principal key; (4) notify all relying parties.

### 16.2. Cryptographic Requirements

   Implementations MUST support the following cryptographic suites
   (Mandatory-To-Implement):

   | Operation              | Algorithm        | Specification | Status  |
   |------------------------|------------------|---------------|---------|
   | Signing / Verification | Ed25519 (EdDSA)  | [RFC8037]     | MUST    |
   | Hashing                | SHA-256          | [FIPS-180-4]  | MUST    |
   | Key representation     | JWK              | [RFC7517]     | MUST    |
   | Key exchange (future)  | X25519           | [RFC7748]     | SHOULD  |

   Authenticator Assurance Level: AIP agent authentication satisfies
   NIST SP 800-63-4 [SP-800-63-4] Authenticator Assurance Level 2
   (AAL2) for agent-to-service interactions. The three AAL2 conditions
   are met as follows:

   (1) Bound cryptographic authenticator: Each agent holds an Ed25519
       private key whose corresponding public key is registered in the
       AIP Registry at agent creation time (Section 6.1). The key is
       bound to the agent's credential_id and cannot be reused across
       agents.

   (2) Cryptographic authentication protocol: Authentication is
       performed via DPoP (Demonstrating Proof of Possession,
       RFC 9449). The DPoP proof MUST include the htm (HTTP method),
       htu (HTTP URI), iat (issued-at), and jti (unique token ID)
       claims, binding the proof to the specific request and preventing
       replay across different endpoints or time windows.

   (3) Phishing resistance: The htu claim in the DPoP proof binds
       the authentication to the target endpoint URI. An attacker who
       intercepts a valid DPoP proof MUST NOT be able to replay it
       against a different endpoint, satisfying the phishing-resistance
       requirement of [SP-800-63-4] Section 5.2.

   Implementations that process AIP Credential Tokens MUST enforce
   DPoP validation as specified in Section 16.3. Accepting a
   Credential Token without DPoP proof validation does not satisfy
   AAL2 and is explicitly non-conformant with this specification.

   Implementations MAY additionally support the following optional
   suites:

   | Operation | Algorithm            | Specification | Notes                              |
   |-----------|----------------------|---------------|------------------------------------|
   | Signing   | ES256 (ECDSA P-256)  | [RFC7518]     | For WebAuthn ecosystem compatibility |
   | Signing   | RS256 (RSA-PKCS1)    | [RFC7518]     | For legacy enterprise environments ONLY |

   Implementations MUST NOT use RS256 as the sole supported algorithm.
   Ed25519 support is non-negotiable for conformance.

   Prohibited algorithms — Implementations MUST NOT use:

   - `none` — unsigned tokens MUST be rejected
   - `HS256`, `HS384`, `HS512` — symmetric HMAC is unsuitable for this
     trust model
   - `RS256` with RSA keys less than 2048 bits
   - `RS512` — not a supported algorithm in AIP at any key length;
     MUST NOT be accepted
   - `MD5` or `SHA-1` for any purpose

   Algorithm Agility: The `alg` header in a Credential Token MUST be
   explicitly specified. Implementations MUST NOT infer the algorithm
   from context or default to an unspecified algorithm. When an
   implementation receives a token with an unsupported `alg` value, it
   MUST return `invalid_token` and MUST NOT attempt to verify the token
   with a different algorithm.

   Key Length Requirements:

   | Algorithm     | Minimum Key Length                        |
   |---------------|-------------------------------------------|
   | Ed25519       | 256 bits (fixed)                          |
   | ECDSA (P-256) | 256 bits (fixed)                          |
   | RSA           | 2048 bits minimum; 4096 bits RECOMMENDED  |

### 16.3. Proof-of-Possession (DPoP)

   For any interaction involving `transactions.*`, `communicate.*`, or
   `filesystem.execute` scopes, the agent MUST demonstrate Proof-of-
   Possession of the private key corresponding to its registered public
   key.

   AIP uses the OAuth DPoP mechanism defined in [RFC9449] adapted for
   AIP Credential Tokens.

   DPoP proofs MUST always use `EdDSA` (Ed25519) regardless of which
   algorithm the agent uses for its Credential Token. This applies even
   when the agent's Credential Token is signed with the optional ES256
   or RS256 suites. Relying parties MUST reject DPoP proofs with any
   `alg` value other than `EdDSA`.

   **DPoP Proof Header:**

```json
   {
     "typ": "dpop+jwt",
     "alg": "EdDSA",
     "jwk": {
       "kty": "OKP",
       "crv": "Ed25519",
       "x": "<base64url-encoded public key bytes, no padding>",
       "kid": "<DID URL identifying the key version>"
     }
   }
```

   The `kid` field in the DPoP proof JWK MUST match the `kid` in the
   corresponding Credential Token's JWT header. Omitting `kid` from the
   DPoP JWK is a MUST NOT — implementations that omit it MUST be
   rejected.

   **DPoP Proof Payload:**

```json
   {
     "jti": "<UUID v4 — unique per request>",
     "htm": "<HTTP method — exactly as sent, uppercase>",
     "htu": "<HTTP URI — scheme + host + path only, no query string or fragment>",
     "iat": "<Unix timestamp — MUST be within 30 seconds of server time>",
     "ath": "<base64url(SHA-256(ASCII(token-string)))>"
   }
```

   The `ath` value MUST be computed as follows:

```
   ath = BASE64URL( SHA-256( ASCII( "<header>.<payload>.<signature>" ) ) )
```

   This computation is identical to the `ath` computation in [RFC9449]
   Section 4.2. The token string to hash is the three-segment compact
   JWT only, without any surrounding whitespace or scheme prefix.

   Relying Party Validation of DPoP Proof: When a scope requiring DPoP
   is requested, the relying party MUST:

   1. Verify the DPoP proof JWT is present in the `DPoP` HTTP header.
   2. Verify the `alg` is `EdDSA` — any other value MUST be rejected.
   3. Verify the `jwk` in the DPoP header contains a `kid` field that
      matches the `kid` in the Credential Token's JWT header. Retrieve
      the public key for that specific `kid` from the Registry. If
      `kid` is absent or does not match, reject with
      `dpop_proof_required`.
   4. Verify the `htm` matches the HTTP method of the current request
      (case-sensitive, uppercase).
   5. Verify the `htu` matches the URI of the current request (scheme +
      host + path, no query string or fragment).
   6. Verify the `iat` is within the server's clock skew tolerance
      (maximum 30 seconds).
   7. Verify the `jti` has not been seen before within the `iat`
      validity window. This replay cache MUST be maintained separately
      from the Credential Token `jti` replay cache and MUST be keyed by
      (`kid`, `jti`) pair.
   8. Verify the `ath` value per the exact computation above.
   9. Verify the DPoP proof signature using the `jwk` in the proof
      header.

   If any check fails, return `dpop_proof_required` with HTTP 401.

   Nonce Support: Relying parties SHOULD implement DPoP nonces per
   [RFC9449] Section 8 to prevent pre-generated proof stockpiling. When
   nonces are required, the relying party MUST include a `DPoP-Nonce`
   response header on first request. Nonces SHOULD expire after a short
   window (RECOMMENDED: 60 seconds).

### 16.4. Key Management

   Private Key Storage: Implementations MUST store agent private keys
   in a secure context. Private keys MUST NOT be stored in plaintext
   on disk. Private keys SHOULD be stored in a hardware security module
   (HSM), secure enclave, or OS-level keychain where available. Private
   keys MUST NOT be transmitted in any protocol message. Private keys
   MUST NOT be included in logs or diagnostic output.

   Key Rotation: Agents SHOULD rotate their signing keys periodically.
   Key rotation MUST:

   1. Generate a new Ed25519 keypair in the secure context.
   2. Construct an updated Core Identity Object with an incremented
      `version` field, new `public_key` JWK with the next sequential
      `kid`, and a `previous_key_signature` signed by the retiring
      private key.
   3. Submit the updated Core Identity Object to the Registry. The
      Registry MUST verify `previous_key_signature` before accepting.
   4. Upon Registry confirmation, begin using the new private key.
   5. Retain the previous private key in secure storage until all
      outstanding tokens signed by it have expired.

   Implementations MUST NOT invalidate outstanding tokens upon key
   rotation. Relying parties MUST verify tokens against the key version
   identified by the token's `kid` DID URL fragment.

   Key Compromise Response: If an agent's private key is suspected to
   have been compromised, the principal MUST: (1) immediately issue a
   Revocation Object for the affected AID with `reason: "key_compromised"`;
   (2) register a new AID with a new keypair; (3) re-establish any
   required delegations under the new AID.

   Principals SHOULD use hardware security keys (e.g., FIDO2/WebAuthn)
   or HSM-backed keys for their root DID to reduce the risk of private
   key extraction.

### 16.5. Token Security

   Transport Security: All AIP Credential Tokens MUST be transmitted
   over TLS 1.2 or higher. Implementations MUST NOT transmit tokens
   over unencrypted HTTP connections. Implementations SHOULD use TLS
   1.3 where available.

   JTI Replay Cache: Relying parties MUST maintain a replay cache of
   (`iss`, `jti`) pairs. The cache MUST cover a window of at least the
   maximum token TTL for the scopes being served. The cache MAY be
   cleared of entries older than the maximum TTL. The cache MUST be
   consistent — distributed deployments MUST use a shared cache (e.g.,
   Redis) to prevent replay across instances.

   Audience Validation: Relying parties MUST validate the `aud` claim.
   Tokens with an `aud` claim that does not include the relying party's
   identifier MUST be rejected with `invalid_token`.

   Token Binding Prohibition: Implementations MUST NOT bind Credential
   Tokens to TLS sessions. DPoP Proof-of-Possession (Section 16.3) is
   the required binding mechanism.

### 16.6. Delegation Chain Security

   Chain Depth Default: The default `max_delegation_depth` for new
   agents MUST NOT exceed 3. Principals MAY increase this value up to
   the hard maximum of 10. Implementations MUST reject any attempt to
   set `max_delegation_depth` above 10.

   Circular Delegation Prevention: Implementations MUST detect and
   reject circular delegation chains where an AID appears more than once
   in the `aip_chain` array. The validation algorithm MUST check for AID
   uniqueness across the entire chain.

   Ephemeral Agent Expiry: Agents with namespace `ephemeral` MUST have
   a non-null `task_id` in their Principal Token. Ephemeral agents MUST
   be explicitly revoked upon task completion. The Registry uses the
   `expires_at` value from the decoded `principal_token` payload stored
   at registration time as the basis for the auto-revocation mechanism.

### 16.7. Registry Security

   Registry Authentication: All write operations to the Registry MUST
   be authenticated.

   For registration and key rotation: The submitting party MUST be
   verified as the agent itself or the principal authorising the
   registration.

   For revocation: The `issued_by` DID MUST be verified to be in the
   delegation chain of the target AID or to be the root principal.
   Registries MUST reject Revocation Objects where this cannot be
   verified.

   For endorsement submission: The Registry MUST verify that the
   Endorsement Object signature is valid for the `from_aid`'s registered
   public key.

   For internally generated Revocation Objects (child propagation or
   ephemeral agent auto-revocation), the Registry MUST sign using a
   designated Registry administrative key. The public key for this
   administrative key MUST be published in the Registry's well-known
   configuration and MUST be distinct from any agent's public key.

   Registry Availability: A Registry claiming AIP conformance MUST meet
   the following minimum availability requirements for public endpoints:

   - Read endpoints (key retrieval, revocation status) MUST target
     99.9% uptime.
   - The CRL endpoint MUST be updated within 15 minutes of a new
     Revocation Object being accepted.
   - The CRL endpoint MUST be served from a CDN or distributed
     infrastructure.

   Multi-Registry Environments: An AID MAY be registered in multiple
   Registries for redundancy. The Registry that accepted the original
   registration is the authoritative Registry for that AID. Revocation
   MUST be submitted to the authoritative Registry.

   Registry Trust: Relying parties MUST NOT blindly trust arbitrary
   Registries. Implementations SHOULD maintain a list of trusted
   Registry root certificates or public keys. The `aip_registry` claim
   in a Credential Token is advisory.

### 16.8. Revocation Security

   Revocation Object Authenticity: Every Revocation Object MUST be
   signed by the principal or parent agent that has authority to revoke
   the target AID. Registries MUST reject unsigned or invalidly signed
   Revocation Objects.

   Revocation Timing Attack: Adversaries may attempt to delay
   revocation propagation. Mitigations: short TTL on sensitive tokens
   (max 5 minutes) limits the value of this attack window; Tier 2
   real-time revocation checks eliminate the CRL window for high-risk
   operations; Registry SHOULD support webhook subscriptions for high-
   priority relying parties.

   Dead Man's Switch (Optional): Implementations MAY implement a Dead
   Man's Switch mechanism: if an active agent fails to submit a signed
   heartbeat to the Registry within a configured window (RECOMMENDED:
   24 hours), the Registry MAY issue a `full_revoke` Revocation Object
   for the AID with `reason: "other"`. This is OPTIONAL and MUST be
   explicitly configured by the principal. AIP does not define an
   `inactive` status; the Dead Man's Switch achieves its effect through
   the standard `full_revoke` mechanism.

### 16.9. Privacy Considerations

   Principal Identity Minimisation: The `principal.id` field in the
   Principal Token contains the principal's DID, which may be linkable
   to a real person. Implementations SHOULD use pairwise DIDs (a
   different DID per service) for the principal's identity where the
   DID method supports this (e.g., `did:peer`).

   Reputation Data and Linkability: The reputation record for an AID
   reveals the agent's activity history. Relying parties that submit
   endorsements to a public Registry are contributing to a linkable
   activity record. Principals SHOULD be informed of this trade-off.
   Registries MUST NOT expose raw interaction logs.

   AID Correlation: Because AIDs are persistent, they can be used to
   correlate an agent's activity across relying parties. Principals who
   wish to prevent cross-service correlation SHOULD use separate AIDs
   per relying party. Ephemeral agents inherently limit correlation
   surface to the duration of a single task.

   Registry Data Retention: Registries MUST provide a mechanism for
   principals to request deletion of an AID's reputation and endorsement
   data, subject to applicable law. Core identity records (AID, public
   key, revocation status) MAY be retained for audit purposes even after
   a deletion request.

---

## 17. IANA Considerations

   This document defines the `did:aip` DID method, submitted for
   registration with the W3C DID Method Registry per the process defined
   in [W3C-DID] Section 9.

   The `AIP+JWT` token type is used in the `typ` header of AIP
   Credential Tokens to distinguish AIP tokens from other JWT usage.
   This type is specific to AIP and is not registered with IANA in this
   draft.

   The `AIP` HTTP Authorization scheme (used in
   `Authorization: AIP <token>`) is specific to AIP and is not
   registered as an IANA HTTP Authentication Scheme in this draft.

   This specification does not require any actions from IANA beyond
   the DID Method registration noted above.

---

## 18. Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119,
              DOI 10.17487/RFC2119, March 1997,
              <https://www.rfc-editor.org/info/rfc2119>.

   [RFC3986]  Berners-Lee, T., Fielding, R., and L. Masinter, "Uniform
              Resource Identifier (URI): Generic Syntax", STD 66,
              RFC 3986, DOI 10.17487/RFC3986, January 2005,
              <https://www.rfc-editor.org/info/rfc3986>.

   [RFC5234]  Crocker, D., Ed., and P. Overell, "Augmented BNF for
              Syntax Specifications: ABNF", STD 68, RFC 5234,
              DOI 10.17487/RFC5234, January 2008,
              <https://www.rfc-editor.org/info/rfc5234>.

   [RFC5280]  Cooper, D., Santesson, S., Farrell, S., Boeyen, S.,
              Housley, R., and W. Polk, "Internet X.509 Public Key
              Infrastructure Certificate and Certificate Revocation
              List (CRL) Profile", RFC 5280, DOI 10.17487/RFC5280,
              May 2008, <https://www.rfc-editor.org/info/rfc5280>.

   [RFC6585]  Nottingham, M. and R. Fielding, "Additional HTTP Status
              Codes", RFC 6585, DOI 10.17487/RFC6585, April 2012,
              <https://www.rfc-editor.org/info/rfc6585>.

   [RFC7515]  Jones, M., Bradley, J., and N. Sakimura, "JSON Web
              Signature (JWS)", RFC 7515, DOI 10.17487/RFC7515,
              May 2015, <https://www.rfc-editor.org/info/rfc7515>.

   [RFC7517]  Jones, M., "JSON Web Key (JWK)", RFC 7517,
              DOI 10.17487/RFC7517, May 2015,
              <https://www.rfc-editor.org/info/rfc7517>.

   [RFC7518]  Jones, M., "JSON Web Algorithms (JWA)", RFC 7518,
              DOI 10.17487/RFC7518, May 2015,
              <https://www.rfc-editor.org/info/rfc7518>.

   [RFC7519]  Jones, M., Bradley, J., and N. Sakimura, "JSON Web Token
              (JWT)", RFC 7519, DOI 10.17487/RFC7519, May 2015,
              <https://www.rfc-editor.org/info/rfc7519>.

   [RFC7748]  Langley, A., Hamburg, M., and S. Turner, "Elliptic
              Curves for Security", RFC 7748, DOI 10.17487/RFC7748,
              January 2016, <https://www.rfc-editor.org/info/rfc7748>.

   [RFC8037]  Liusvaara, I., "CFRG Elliptic Curves for JOSE",
              RFC 8037, DOI 10.17487/RFC8037, January 2017,
              <https://www.rfc-editor.org/info/rfc8037>.

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in
              RFC 2119 Key Words", BCP 14, RFC 8174,
              DOI 10.17487/RFC8174, May 2017,
              <https://www.rfc-editor.org/info/rfc8174>.

   [RFC8259]  Bray, T., Ed., "The JavaScript Object Notation (JSON)
              Data Interchange Format", STD 90, RFC 8259,
              DOI 10.17487/RFC8259, December 2017,
              <https://www.rfc-editor.org/info/rfc8259>.

   [RFC9110]  Fielding, R., Ed., Nottingham, M., Ed., and J. Reschke,
              Ed., "HTTP Semantics", STD 97, RFC 9110,
              DOI 10.17487/RFC9110, June 2022,
              <https://www.rfc-editor.org/info/rfc9110>.

   [RFC9449]  Fett, D., Campbell, B., Bradley, J., Lodderstedt, T.,
              Jones, M., and D. Waite, "OAuth 2.0 Demonstrating Proof
              of Possession (DPoP)", RFC 9449,
              DOI 10.17487/RFC9449, September 2023,
              <https://www.rfc-editor.org/info/rfc9449>.

   [W3C-DID]  Sporny, M., Guy, A., Sabadello, M., and D. Reed,
              "Decentralized Identifiers (DIDs) v1.1", W3C Candidate
              Recommendation, 2025,
              <https://www.w3.org/TR/did-core/>.

   [FIPS-180-4]  National Institute of Standards and Technology,
              "Secure Hash Standard (SHS)", FIPS PUB 180-4,
              August 2015,
              <https://doi.org/10.6028/NIST.FIPS.180-4>.

---

## 19. Informative References

   [RFC4122]  Leach, P., Mealling, M., and R. Salz, "A Universally
              Unique IDentifier (UUID) URN Namespace", RFC 4122,
              DOI 10.17487/RFC4122, July 2005,
              <https://www.rfc-editor.org/info/rfc4122>.

   [RFC9562]  Davis, K., Peabody, B., and P. Leach, "Universally
              Unique IDentifiers (UUIDs)", RFC 9562,
              DOI 10.17487/RFC9562, May 2024,
              <https://www.rfc-editor.org/info/rfc9562>.

   [RFC7807]  Nottingham, M. and E. Wilde, "Problem Details for HTTP
              APIs", RFC 7807, DOI 10.17487/RFC7807, March 2016,
              <https://www.rfc-editor.org/info/rfc7807>.

   [RFC9457]  Nottingham, M., Wilde, E., and S. Dalal, "Problem
              Details for HTTP APIs", RFC 9457, DOI 10.17487/RFC9457,
              July 2023, <https://www.rfc-editor.org/info/rfc9457>.

   [SEMVER]   Preston-Werner, T., "Semantic Versioning 2.0.0",
              <https://semver.org/>.

   [W3C-DID-REGISTRY]  W3C, "DID Specification Registries",
              <https://www.w3.org/TR/did-spec-registries/>.

   [MCP]         Anthropic, "Model Context Protocol Specification",
                 2024. <https://modelcontextprotocol.io/specification>

   [NISTIR-8587] National Institute of Standards and Technology,
                 "Protecting Tokens and Assertions from Forgery, Theft,
                 and Misuse", NIST Internal Report 8587,
                 DOI 10.6028/NIST.IR.8587, 2024.
                 <https://doi.org/10.6028/NIST.IR.8587>

   [SP-800-207]  National Institute of Standards and Technology,
                 "Zero Trust Architecture", NIST Special Publication
                 800-207, DOI 10.6028/NIST.SP.800-207, August 2020.
                 <https://doi.org/10.6028/NIST.SP.800-207>

   [SP-800-63-4] National Institute of Standards and Technology,
                 "Digital Identity Guidelines", NIST Special Publication
                 800-63-4 (3rd Revision), 2022.
                 <https://pages.nist.gov/800-63-4/>

---

## Acknowledgements

   AIP builds directly on the work of the following open standards
   communities, whose members' prior art is the foundation of this
   protocol:

   - W3C DID Working Group — Decentralized Identifiers (DIDs) v1.1
   - IETF OAuth Working Group — RFC 6749, RFC 9449 (DPoP), RFC 7519
     (JWT)
   - NIST NCCoE — AI Agent Identity and Authorization Concept Paper
     (2026)

---

## Authors' Addresses

   Paras Singla
   Independent
   GitHub: @itisparas

   ProvAI
   https://provai.dev
   Email: spec@provai.dev
   Repository: https://github.com/provai-dev/aip-spec

---

*AIP Specification v0.1 — Standards Track Draft*
*Released under CC0 1.0 Universal — No rights reserved*
*Provai — https://provai.dev*
