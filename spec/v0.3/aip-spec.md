# Agent Identity Protocol (AIP)
## Specification — Draft v0.3

**Authors:** Paras Singla ([@itisparas](https://github.com/itisparas)), ProvAI  
**Repository:** https://github.com/provai-dev/aip-spec  
**Status:** Draft — not yet stable, expect changes before v1.0  
**License:** CC0 1.0 Universal — implement freely, no rights reserved  
**Date:** April 12, 2026  
**Previous version:** [v0.2](../v0.2/aip-spec.md)  

## Abstract

 The Agent Identity Protocol (AIP) defines an open, layered identity
 framework for autonomous AI agents. AIP specifies a W3C DID-
 conformant agent identifier (`did:aip`), a cryptographically
 verifiable principal delegation chain, a fine-grained Capability
 Manifest, a signed Credential Token format and deterministic 12-step
 validation algorithm, a standardised revocation mechanism, a
 reputation data format, a principal authorization protocol (AIP-
 GRANT), and a chained workflow approval mechanism. Two independent
 implementations conforming to this specification are required to
 produce interoperable systems.

## Status of This Memo

 This document is a draft specification of the ProvAI project. It
 describes a proposed internet standard for AI agent identity.
 Distribution of this document is unrestricted.

 This specification is released under CC0 1.0 Universal. No rights
 reserved. Implement freely.

## Copyright Notice

 Copyright (C) ProvAI (2026). All rights reserved as permitted under
 CC0 1.0 Universal.

---

## Table of Contents

```
1. Introduction
 1.1. Motivation
 1.2. Design Philosophy
 1.3. Architecture Layers
2. Conventions and Definitions
 2.1. Canonical JSON Serialization
3. Terminology
4. Resource Model
 4.1. Resource Naming
 4.2. JSON Schema Representations
 4.2.1. Agent Identity
 4.2.2. Capability Manifest
 4.2.3. Credential Token
 4.2.4. Principal Token
 4.2.5. Registration Envelope
 4.2.6. Revocation Object
 4.2.7. Endorsement
 4.3. Field Constraints
 4.4. Delegation Rules
 4.5. AIP-GRANT: Principal Authorization Protocol
 4.5.1. Overview and Roles
 4.5.2. GrantRequest Object
 4.5.3. Wallet Consent Requirements
 4.5.4. GrantResponse Object
 4.5.5. Transport Bindings
 4.5.6. Principal Token Construction from Grant
 4.5.7. Sub-Agent Delegation Flow
 4.5.8. AIP-GRANT Error Codes
 4.6. Chained Approval Envelopes
 4.6.1. Motivation: The Cascading Approval Problem
 4.6.2. The Token-Expiry-While-Pending Problem
 4.6.3. Approval Envelope Schema
 4.6.4. Step Schema
 4.6.5. Compensation Step Schema
 4.6.6. Approval Envelope Lifecycle
 4.6.7. Action Hash Computation
 4.6.8. Step Claim and Execution Protocol
 4.6.9. SAGA Compensation Semantics
 4.6.10. Approval Envelope Validation Rules
 4.7. Capability Overlays
 4.8. Engagement Objects
5. Registration Protocol
 5.1. Registration Envelope
 5.2. Registration Validation
 5.3. Error Responses
6. Agent Resolution
 6.1. DID Resolution
 6.2. DID Document Structure
 6.3. Registry Genesis
7. Credential Tokens
 7.1. Token Structure
 7.2. Token Issuance
 7.3. Token Validation
 7.4. Token Refresh and Long-Running Tasks
 7.4.1. Agent Self-Refresh
 7.4.2. Pre-emptive Refresh Requirements
 7.4.3. Delegation Chain Expiry
 7.4.4. Interaction with Approval Envelopes
 7.5. Token Exchange for MCP
8. Delegation
 8.1. Delegation Chain
 8.2. Capability Scope Rules
 8.3. Delegation Validation
9. Revocation
 9.1. Revocation Object
 9.2. Certificate Revocation List (CRL)
 9.3. Revocation Checking
 9.4. Registry Push Notification Protocol (RPNP)
10. Principal Chain
11. Reputation and Endorsements
 11.1. Endorsement Object
 11.2. Reputation Scoring
12. Lifecycle States
13. Error Handling
 13.1. Error Response Format
 13.2. Standard Error Codes
 13.3. Error Detail Types
14. Rate Limiting and Abuse Prevention
 14.1. Rate Limit Response Format
 14.2. Per-Endpoint Rate Limit Categories
 14.3. Registration Abuse Prevention
 14.4. Validation-Driven Lookup Limits
 14.5. Approval Envelope Rate Limits
 14.6. Graduated Backoff Requirements
15. Registry Interface
 15.1. Required Endpoints
 15.2. AID URL Encoding
 15.3. Response Format
 15.4. Approval Envelope Endpoints
 15.5. OAuth 2.1 Authorization Server
 15.6. Scope Map
 15.7. Engagement Endpoints
 15.8. RPNP Subscription Endpoints
16. Versioning and Compatibility
 16.1. Tier Conformance
17. Security Considerations
 17.1. Threat Model
 17.2. Cryptographic Requirements
 17.3. Proof-of-Possession (DPoP)
 17.4. Key Management
 17.5. Token Security
 17.6. Delegation Chain Security
 17.7. Registry Security
 17.8. Revocation Security
 17.9. Approval Envelope Security
 17.10. Privacy Considerations
18. IANA Considerations
19. Normative References
20. Informative References
Appendix A: Changes from Version 0.1
Appendix B: Changes from Version 0.2
Acknowledgements
Authors' Addresses
```

---

## 1. Introduction

 Autonomous AI agents are deployed in production environments to act
 on behalf of human and organisational principals. An agent may send
 emails, book appointments, make purchases, access file systems, spawn
 child agents to complete subtasks, and communicate across multiple
 platforms, all without explicit human approval for each action.

 This creates an identity gap. When an agent presents itself to an
 API, a payment processor, or another agent, there is no standard
 mechanism to establish: the agent's persistent identity across
 interactions; the human or organisation on whose authority it acts;
 the specific actions it is permitted to take; whether it has been
 compromised or revoked; or whether it has a trustworthy history.

 AIP addresses this gap. It is designed as neutral, open
 infrastructure analogous to HTTP, OAuth, and JWT, providing
 infrastructure that any application can build on without vendor
 dependency.

### 1.1. Motivation

 The absence of an identity standard creates concrete operational
 problems. Services cannot implement fine-grained agent access
 control. Humans have no auditable record of what their agents did.
 Compromised agents cannot be reliably stopped. Agent-to-agent
 systems have no basis for trust.

 Existing deployments typically operate in one of two modes: no
 access, or full access. AIP introduces fine-grained capability
 declarations. A
 principal can grant `email.read` without `email.send`, or
 `transactions` with a `max_daily_total` constraint.

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
 steps on the same token will reach the same result.

 Zero Trust Architecture. AIP implements the zero trust principles
 defined in [SP-800-207] and satisfies NIST SP 800-63-4
 [SP-800-63-4] AAL2 for agent-to-service interactions. No agent is
 implicitly trusted by virtue of its origin, network location, or
 prior successful interaction. Every Credential Token must be
 validated against the Registry on every interaction. Short-lived
 Credential Tokens (Section 7.2) bound by a mandatory TTL limit the
 blast radius of any credential compromise. Revocation is checked in
 real time for Tier 2 sensitive operations (Section 17.3). DPoP
 proof-of-possession (Section 17.3) ensures that possession of a
 valid Credential Token is insufficient for impersonation without the
 corresponding private key material, satisfying the anti-replay
 requirement of [SP-800-207] Section 3.

 Integration with Model Context Protocol (MCP). AIP provides the
 agent identity, authorization, and delegation layer that MCP server
 implementations require but do not define. An AIP-authenticated agent
 can obtain scoped access tokens for MCP servers via the token exchange
 mechanism defined in Section 7.5. AIP does not replace MCP; it
 provides the identity substrate on which MCP authorization decisions
 are made. See Section 7.5 (Token Exchange) and Section 15.5 (OAuth
 Authorization Server) for the concrete integration path.

 Least Privilege. Agents are granted only the specific capabilities
 required for their declared purpose, expressed as signed Capability
 Manifests (Section 8). Capability grants are always additive from
 principal to agent and never exceed the granting principal's own
 capability set. A child agent must not be granted capabilities that
 the delegating parent does not itself hold (Rule D-1, Section 8.2).
 The max_delegation_depth field (Section 8.1) bounds the depth of
 sub-agent hierarchies, limiting transitive capability propagation.
 Capability constraints allow fine-grained least-privilege expression
 within each capability category, consistent with [SP-800-207]
 Section 3 (Tenets 5 and 6).

 Relationship to SPIFFE/SPIRE. SPIFFE is designed for workload
 identity within enumerable, infrastructure-managed environments. AIP
 is designed for autonomous agents that are created dynamically,
 operate across organisational boundaries, and act on behalf of named
 human principals whose authority must be cryptographically
 traceable. An enterprise may deploy SPIFFE for its internal service
 mesh and AIP for its agent fleet without conflict. The two
 mechanisms are complementary and operate at distinct layers of the
 identity stack.

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
 attack: a compromised agent may be immediately revoked via
 full_revoke (Section 9.1), and revocation propagates to all child
 agents within the TTL window defined in Section 7.2. AIP does not
 prevent the initial injection — it limits the attacker's persistence.

### 1.3. Architecture Layers

 AIP is structured as six ordered layers:

 Figure 1: AIP Architecture Layers
```
 +------------------------------------------------------+
 | Layer 6 - Reputation Trust over time |
 +------------------------------------------------------+
 | Layer 5 - Revocation Standard kill switch |
 +------------------------------------------------------+
 | Layer 4 - Credential Token & Verification |
 | Cryptographic proof |
 +------------------------------------------------------+
 | Layer 3 - Capabilities What the agent can do |
 +------------------------------------------------------+
 | Layer 2 - Principal Chain Who authorised it |
 | incl. AIP-GRANT and Approval Envelopes |
 +------------------------------------------------------+
 | Layer 1 - Core Identity Who the agent IS |
 +------------------------------------------------------+
```

---

## 2. Conventions and Definitions

 The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
 "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
 "OPTIONAL" in this document are to be interpreted as described in
 BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all
 capitals, as shown here.

 This document uses "MUST" in preference to "SHALL" throughout for
 consistency. Where earlier drafts used "SHALL", the normative force
 is identical; the term has been normalised to "MUST" per this
 convention.

 JSON is used throughout this document as defined in [RFC8259].
 URIs are used as defined in [RFC3986]. ABNF notation is used as
 defined in [RFC5234], including its core rules (ALPHA, DIGIT,
 HEXDIG, SP, etc.) as defined in RFC5234 Appendix B.1. HTTP status
 codes, headers, and semantics are as defined in [RFC9110].

 All Ed25519 signatures are computed per [RFC8032]. DPoP proofs are
 constructed per [RFC9449].

### 2.1. Canonical JSON Serialization

 Several objects in this specification are signed outside the JWT
 framework. For those objects, the following canonical JSON
 serialization procedure MUST be used when computing or verifying
 signatures, and when computing Action Hashes (Section 4.6.7):

 (1) Represent the object as a JSON value per [RFC8259].
 (2) Recursively sort all object keys in lexicographic ascending
     order (Unicode code point order). Array element order MUST be
     preserved; arrays MUST NOT be sorted.
 (3) Remove all insignificant whitespace (no spaces, tabs, or
     newlines outside string values).
 (4) Encode the result as a UTF-8 byte sequence with no BOM.
 (5) Before computing any signature, set the object's "signature"
     field to the empty string "". The "signature" field MUST be
     included in the serialisation at its lexicographically correct
     position with value "".

 This procedure is equivalent to the JSON Canonicalization Scheme
 (JCS) defined in [RFC8785]. Implementations SHOULD use an RFC8785-
 conformant library to ensure correctness. When this procedure is
 used to compute Action Hashes (Section 4.6.7), implementations
 MUST use an RFC8785-conformant library; custom serializer
 implementations MUST NOT be used for that purpose.

 EXAMPLE (informative):
```
 {"z": 1, "a": 2, "m": [3,1,2]}  →  {"a":2,"m":[3,1,2],"z":1}
```

 NOTE: This canonical serialization applies to Capability Manifests,
 Agent Identity Objects, Revocation Objects, Endorsement Objects,
 GrantRequest Objects (when signed), and Approval Envelopes. It does
 NOT apply to JWT-format objects (Credential Tokens, Principal
 Tokens), which use standard JWS compact serialization per [RFC7515].

---

## 3. Terminology

 **Agent** — An autonomous software system powered by a large language
 model that can perceive inputs, reason about them, and execute actions
 in the world on behalf of a principal.

 **AID (Agent Identity)** — A globally unique, persistent identifier
 for an agent conforming to the `did:aip` DID method defined in
 Section 6.

 **Principal** — The human or organisational entity on whose authority
 an agent acts. Every AIP delegation chain MUST have a verifiable
 principal at its root.

 **Agent Deployer** — The party that provisions an agent on behalf of
 a principal. May be the principal themselves or a service.

 **Principal Wallet** — Software that holds the principal's DID
 private key and implements the AIP-GRANT consent and signing
 ceremony (Section 4.5). Throughout this document, "wallet" used
 alone refers to the Principal Wallet unless the context explicitly
 states otherwise.

 **Capability Manifest** — A versioned, signed JSON document stored
 in the Registry that declares the specific permissions granted to an
 agent.

 **Credential Token** — A signed JWT-format token presented by an
 agent to a Relying Party as proof of identity and authorisation for
 a specific interaction.

 **Step Execution Token** — A short-lived Credential Token issued
 by the AIP Registry attesting that a specific Approval Envelope
 step has been claimed by its designated actor. Defined in
 Section 4.6.8. Distinguished from agent-issued Credential Tokens
 by having "iss" equal to the Registry AID and carrying the claiming
 agent's delegation chain in "aip_chain".

 **Relying Party** — Any service, API, or agent that receives and
 verifies an AIP Credential Token.

 **Delegation** — The act of granting a subset of capabilities from a
 principal or parent agent to a child agent.

 **Delegation Depth** — A non-negative integer counter incremented at
 each delegation step. The first agent directly authorised by the root
 principal has delegation depth 0.

 **Tier** — A threat-model declaration specifying which security
 properties the deploying principal asserts hold at execution time.
 Tier determines the applicable revocation-checking mode, maximum
 Credential Token lifetime, and mandatory security mechanisms. Tier
 selection on performance or availability grounds alone, without
 regard to the security properties declared, is a misconfiguration.
 Three Tiers are defined:

 **Tier 1 (Bounded-staleness)** — Interactions in which every scope
 in the token's "aip_scope" array is drawn exclusively from the
 following set: "email.read", "email.write", "email.send",
 "email.delete", "calendar.read", "calendar.write",
 "calendar.delete", "web.browse", "web.forms_submit",
 "web.download", and "spawn_agents.create".

 Tier 1 declares:
 1. *Cryptographic admissibility* — The agent's Credential Token
    and delegation chain are cryptographically valid at claim time.
 2. *Bounded revocation staleness* — Revocation status may lag by
    up to 15 minutes (CRL cache window). The deploying principal
    accepts this staleness for all scopes in the token.

 Tier 1 does **not** declare:
 - That the agent's authorization is current at execution time.
 - That revocation issued within the last 15 minutes has propagated.

 CRL-based revocation checking is sufficient. Maximum Credential
 Token lifetime is 3600 seconds.

 **Tier 2 (Real-time revocation)** — Interactions in which at least
 one scope in the token's "aip_scope" array is any of:
 "transactions" or any scope with the prefix "transactions.",
 "communicate.whatsapp", "communicate.telegram", "communicate.sms",
 "communicate.voice", "filesystem.execute", "spawn_agents.create",
 or "spawn_agents.manage".

 Tier 2 declares:
 1. *Cryptographic admissibility* — Same as Tier 1.
 2. *Real-time revocation* — Registry check is live and per-action.
    Revocation is effective within RPNP delivery latency (at most 5
    seconds for subscribing Relying Parties, where RPNP is deployed).

 Real-time revocation checking against the Registry MUST be
 performed. Maximum Credential Token lifetime is 300 seconds. DPoP
 proof-of-possession [RFC9449] is REQUIRED.

 **Tier 3 (Enterprise / regulated)** — An organisational deployment
 classification that extends Tier 2 with additional transport-layer
 security. Tier 3 is declared by Registry operators and MUST be
 documented in the Registry's well-known configuration (Section
 15.1). Tier 3 applies to all Tier 2 scopes within the designated
 deployment.

 Tier 3 declares all Tier 2 security properties, plus:
 3. *Mutual authentication* — mTLS channel authentication between
    Relying Party and Registry.
 4. *OCSP real-time status* — OCSP-style per-certificate revocation
    status checking per [RFC6960], supplementing CRL-based checks.

 NOTE: A token's Tier is always determined by its highest-risk
 scope. A token with one Tier 2 scope and nine Tier 1 scopes is
 a Tier 2 token in its entirety.

 The bare scope "spawn_agents" is retired as of v0.3. Tokens
 containing "spawn_agents" without a sub-scope qualifier MUST be
 rejected with "invalid_scope".

 **Grant Tier** — One of three standardised AIP-GRANT ceremony
 profiles: G1 (Registry-Mediated), G2 (Direct Deployer), G3 (Full
 Ceremony). See Section 4.5.

 **Threat-model declaration** — A normative statement by the
 deploying principal (or Registry operator, for Tier 3) asserting
 which security properties hold for a given operation or deployment.

 **Cryptographic admissibility** — The property that an agent's
 Credential Token and delegation chain are cryptographically valid
 at claim time: signatures verify, claims are well-formed, the
 token is not expired, and the delegation chain has not been broken.

 **Capability Overlay** — A Registry-stored, issuer-signed document
 that restricts an agent's effective capability set for a specific
 engagement or issuer context. See Section 4.7.

 **Engagement Object** — A Registry-stored resource representing a
 multi-party engagement with a defined lifecycle, participant
 roster, approval gates, and an append-only signed change log. See
 Section 4.8.

 **Registry** — A service implementing the Registry Interface defined
 in Section 15 that stores AID public keys, revocation status,
 reputation data, and Approval Envelopes.

 **Registry AID** — The `did:aip` Agent Identity of an AIP Registry
 instance, established during Registry Genesis (Section 6.3). The
 Registry AID is used as the "iss" claim of Step Execution Tokens
 and as the signer of CRL documents (Section 9.2).

 **Registry Genesis** — The one-time initialisation procedure by
 which a new AIP Registry creates and persists its own `did:aip`
 Agent Identity. Defined in Section 6.3.

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

 **GrantRequest** — A structured object constructed by the Agent
 Deployer to initiate an AIP-GRANT authorization ceremony.

 **GrantResponse** — A structured object returned by the Principal
 Wallet after the principal reviews and signs or declines the grant.

 **Approval Envelope** — A principal-signed document authorising a
 pre-declared sequence of dependent agent actions forming one logical
 workflow transaction.

 **Approval Step** — An atomic action within an Approval Envelope,
 bound to a specific actor, Relying Party, and action_hash.

 **Action Hash** — A SHA-256 hash of the canonicalised action
 parameters for an Approval Step, binding the principal's approval to
 specific action content.

 **DPoP (Demonstrating Proof of Possession)** — A cryptographic
 mechanism per [RFC9449] that proves the presenter of a token also
 holds the private key corresponding to the token's public key.

 **DID Resolution** — The process of retrieving a DID Document for a
 given DID, per [W3C-DID] Section 7. AIP implementations MUST support
 resolution of at minimum `did:key` and `did:web` DID methods.
 Resolved DID Documents MAY be cached for a maximum of 300 seconds.

---

## 4. Resource Model

### 4.1. Resource Naming

 Agent Identities (AIDs) are W3C Decentralized Identifiers [W3C-DID]
 using the `did:aip` method. The ABNF grammar uses core rules from
 [RFC5234] Appendix B.1 (DIGIT) and defines two additional terminal
 rules:

```abnf
   aip-did    = "did:aip:" namespace ":" unique-id
   namespace  = LOALPHA *( LOALPHA / DIGIT )
                *( "-" 1*( LOALPHA / DIGIT ) )
   unique-id  = 32LOHEXDIG
   LOALPHA    = %x61-7A        ; a-z only, lowercase
   LOHEXDIG   = DIGIT / "a" / "b" / "c" / "d" / "e" / "f"
                               ; lowercase hex digit only
```

 The `namespace` MUST begin with a lowercase alpha character,
 MUST NOT end with a hyphen, and MUST NOT contain consecutive hyphens.

 Implementations MUST reject AIDs containing uppercase hex digits or
 uppercase namespace characters.

 The following namespace values are defined:

 | Namespace | Description |
 |----------------|---------------------------------------------------------|
 | `personal` | An agent acting for a single human principal |
 | `enterprise` | An agent acting within an organisational deployment |
 | `service` | A persistent agent providing a capability as a service |
 | `ephemeral` | An agent created for a single task; revoked on completion |
 | `orchestrator` | An agent whose primary function is spawning child agents |
 | `registry` | An AIP Registry instance; at most one active AID per deployment |

 A `registry`-namespace AID MUST NOT be registered via the standard
 `POST /v1/agents` endpoint. It MUST be created exclusively via the
 Registry Genesis procedure (Section 6.3). Validators resolving a
 Step Execution Token `iss` claim whose AID uses the `registry`
 namespace MUST treat that AID as a trusted root and MUST NOT
 attempt to validate its principal delegation chain.

 Compound typed identifiers use prefixed UUID v4 values:

 | Object Type | Prefix | Example |
 |----------------------|---------|---------------------------------------|
 | Capability Manifest | `cm:` | `cm:550e8400-e29b-41d4-a716-...` |
 | Revocation Object | `rev:` | `rev:6ba7b810-9dad-11d1-80b4-...` |
 | Endorsement Object | `end:` | `end:6ba7b811-9dad-11d1-80b4-...` |
 | Grant Request | `gr:` | `gr:550e8401-e29b-41d4-a716-...` |
 | Approval Envelope | `apr:` | `apr:550e8402-e29b-41d4-a716-...` |

### 4.2. JSON Schema Representations

 All AIP objects MUST be validated against the JSON Schemas defined
 in this section. Canonical schema files are in `schemas/v0.3/`.

 Signing note for non-JWT objects: Capability Manifests, Revocation
 Objects, Endorsement Objects, and Agent Identity Objects are signed
 using EdDSA with an explicit canonical field ordering. Before
 computing the signature, the `signature` field MUST be set to `""`.

#### 4.2.1. Agent Identity

 Canonical signing field order: `aid`, `name`, `type`, `model`,
 `created_at`, `version`, `public_key`, `previous_key_signature`.

 | Field | Type | Required | Constraints |
 |--------------------------|---------|----------|------------------------------|
 | `aid` | string | REQUIRED | MUST match `did:aip` ABNF; pattern `^did:aip:[a-z][a-z0-9]*(-[a-z0-9]+)*:[0-9a-f]{32}$` |
 | `name` | string | REQUIRED | minLength: 1, maxLength: 64 |
 | `type` | string | REQUIRED | MUST exactly match the namespace component of `aid`; pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` |
 | `model` | object | REQUIRED | See sub-fields below |
 | `model.provider` | string | REQUIRED | minLength: 1, maxLength: 64 |
 | `model.model_id` | string | REQUIRED | minLength: 1, maxLength: 128 |
 | `model.attestation_hash` | string | OPTIONAL | pattern: `^sha256:[0-9a-f]{64}$` |
 | `created_at` | string | REQUIRED | ISO 8601 UTC; format: date-time; immutable after registration |
 | `version` | integer | REQUIRED | minimum: 1; MUST increment by exactly 1 on key rotation |
 | `public_key` | object | REQUIRED | JWK per [RFC7517]; Ed25519 (kty=OKP, crv=Ed25519) per [RFC8037] |
 | `public_key.kty` | string | REQUIRED | const: `"OKP"` |
 | `public_key.crv` | string | REQUIRED | const: `"Ed25519"` |
 | `public_key.x` | string | REQUIRED | pattern: `^[A-Za-z0-9_-]{43}$` (32 bytes base64url, no padding) |
 | `public_key.kid` | string | REQUIRED | pattern: `^did:aip:[a-z][a-z0-9]*(-[a-z0-9]+)*:[0-9a-f]{32}#key-[1-9][0-9]*$`; starts at `#key-1` |
 | `previous_key_signature` | string | OPTIONAL (version=1); REQUIRED (version≥2) | base64url EdDSA signature of new object (with this field set to `""`) signed by retiring key; pattern: `^[A-Za-z0-9_-]+$` |

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

 | Field | Type | Required | Constraints |
 |---------------|---------|----------|-----------------------------------|
 | `manifest_id` | string | REQUIRED | pattern: `^cm:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
 | `aid` | string | REQUIRED | MUST match `did:aip` ABNF |
 | `granted_by` | string | REQUIRED | MUST be a valid W3C DID; pattern: `^did:[a-z][a-z0-9]*:.+$` |
 | `version` | integer | REQUIRED | minimum: 1; MUST increment on every update including `scope_revoke` |
 | `issued_at` | string | REQUIRED | ISO 8601 UTC; format: date-time |
 | `expires_at` | string | REQUIRED | ISO 8601 UTC; MUST be after `issued_at` |
 | `capabilities`| object | REQUIRED | See Section 4.3 for all sub-fields |
 | `signature` | string | REQUIRED | base64url EdDSA signature; pattern: `^[A-Za-z0-9_-]+$` |

 A new `manifest_id` MUST be generated on every update, including
 `scope_revoke` operations. Reusing a `manifest_id` for a different
 manifest version is forbidden.

 Relying Parties MUST verify the manifest `signature` field using the
 public key of the `granted_by` DID before trusting any capability
 declared within it. A manifest whose signature is invalid MUST be
 rejected as if the capability were not present.

 An absent or empty `capabilities` object (`{}`) MUST be interpreted
 as no capabilities granted. Implementations MUST NOT treat an absent
 capabilities object as implicitly granting any permission.

 The `version` field MUST be incremented on every update to the
 manifest. Relying Parties MAY cache the manifest `version` to detect
 staleness: if the Registry returns a manifest with the same or lower
 `version` than a previously seen one, the Relying Party SHOULD
 re-fetch.

#### 4.2.3. Credential Token

 An AIP Credential Token is a compact JWT with the following format:

```
 aip-token = JWT-header "." JWT-payload "." JWT-signature
```

 The token MUST be a valid JWT as defined by [RFC7519].

 JWT Header fields:

 | Field | Requirement | Value / Constraints |
 |-------|-------------|--------------------------------------------------|
 | `typ` | MUST | `"AIP+JWT"` |
 | `alg` | MUST | `"EdDSA"` (REQUIRED); `"ES256"` (OPTIONAL); `"RS256"` (OPTIONAL, legacy enterprise only; MUST NOT be the sole supported algorithm) |
 | `kid` | MUST | DID URL identifying the signing key, e.g., `did:aip:personal:9f3a...#key-2`; MUST match the `kid` in the signing agent's Agent Identity |

 Credential Token Payload fields:

 | Field | Type | Required | Constraints |
 |---------------|--------------|----------|-----------------------------------|
 | `aip_version` | string | REQUIRED | MUST be `"0.3"` for this spec |
 | `iss` | string | REQUIRED | MUST match `did:aip` ABNF; MUST equal `sub` of last `aip_chain` element |
 | `sub` | string | REQUIRED | MUST match `did:aip` ABNF; MUST equal `iss` for non-delegated tokens |
 | `aud` | string/array | REQUIRED | Single string or array; MUST include the Relying Party's identifier; minLength: 1 per element |
 | `iat` | integer | REQUIRED | Unix timestamp; MUST NOT be in the future (30-second clock skew tolerance) |
 | `exp` | integer | REQUIRED | Unix timestamp; MUST be strictly greater than `iat`; TTL limits per Section 7.2 |
 | `jti` | string | REQUIRED | UUID v4 canonical lowercase; pattern: `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
 | `aip_scope` | array | REQUIRED | minItems: 1; uniqueItems: true; each item matches `^[a-z_]+([.][a-z_]+)*$` |
 | `aip_chain` | array | REQUIRED | minItems: 1; maxItems: 11; each element is a compact-serialised signed Principal Token JWT |
 | `aip_registry`| string | OPTIONAL | URI of AIP Registry; format: uri |
 | `aip_approval_id` | string | OPTIONAL | pattern: `^apr:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`; REQUIRED when token is a step-claim token (see Section 4.6.8) |
 | `aip_approval_step` | integer | OPTIONAL | Non-negative integer (0-indexed step position); REQUIRED when `aip_approval_id` is present; MUST correspond to a valid step index in the referenced Approval Envelope (see Section 4.6.8) |
 | `aip_engagement_id` | string | OPTIONAL | pattern: `^eng:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`; present when token is scoped to an Engagement Object (see Section 4.8) |

 If `aip_approval_step` is present without `aip_approval_id`, or
 vice versa, validators MUST reject the token with `invalid_token`.

 Duplicate scope strings MUST NOT appear in `aip_scope`.

 The `aip_version` claim MUST be `"0.3"` for tokens conforming to
 this specification. A validator receiving a Credential Token with an
 unrecognised `aip_version` value MUST reject the token with an
 `invalid_token` error and SHOULD include the received `aip_version`
 value in the `error_description` field to aid client debugging. A
 validator MAY support multiple `aip_version` values simultaneously
 to facilitate migration across protocol versions. Validators
 receiving tokens with `aip_version` `"0.1"` SHOULD continue to
 accept them per Section 16 backward compatibility rules, rejecting
 only on features not present in v0.1.

#### 4.2.4. Principal Token

 A Principal Token is a JWT payload encoding one delegation link in
 the AIP principal chain. Principal Tokens are embedded as compact-
 serialised JWTs in the `aip_chain` array of a Credential Token.

 Principal Tokens use standard JWT signing (base64url(header) +
 "." + base64url(payload) compact serialisation), not a custom
 canonicalization order.

 | Field | Type | Required | Constraints |
 |------------------------|--------------|----------|----------------------------|
 | `iss` | string | REQUIRED | W3C DID or `did:aip` AID; for `delegation_depth` 0: MUST equal `principal.id`; for `delegation_depth` > 0: MUST equal `delegated_by` |
 | `sub` | string | REQUIRED | MUST match `did:aip` ABNF |
 | `principal` | object | REQUIRED | See sub-fields below |
 | `principal.type` | string | REQUIRED | enum: `["human", "organisation"]` |
 | `principal.id` | string | REQUIRED | W3C DID; pattern: `^did:[a-z][a-z0-9]*:.+$`; MUST be byte-for-byte identical across all chain elements; MUST NOT use `did:aip` method |
 | `delegated_by` | string/null | REQUIRED | null when `delegation_depth` is 0; MUST be a `did:aip` AID when `delegation_depth` > 0 |
 | `delegation_depth` | integer | REQUIRED | minimum: 0, maximum: 10; MUST equal the array index of this token in `aip_chain` |
 | `max_delegation_depth` | integer | REQUIRED | minimum: 0, maximum: 10; default: 3 when absent; only the value from `aip_chain[0]` governs the chain |
 | `issued_at` | string | REQUIRED | ISO 8601 UTC; format: date-time |
 | `expires_at` | string | REQUIRED | ISO 8601 UTC; MUST be strictly after `issued_at` |
 | `purpose` | string | OPTIONAL | maxLength: 128 |
 | `task_id` | string/null | OPTIONAL; REQUIRED for ephemeral agents | minLength: 1, maxLength: 256 when non-null |
 | `scope` | array | REQUIRED | minItems: 1; uniqueItems: true; each item matches `^[a-z_]+([.][a-z_]+)*$` |

 The `iss` claim identifies the party whose private key signs this
 Principal Token. At `delegation_depth` 0, the issuer is the root
 principal (`iss` MUST equal `principal.id`), and the token MUST be
 signed with the principal's DID private key. At `delegation_depth`
 > 0, the issuer is the parent agent (`iss` MUST equal
 `delegated_by`), and the token MUST be signed with that agent's
 private key. Validators MUST verify the token signature against the
 key of the `iss` DID, consistent with Step 8d of Section 7.3.

 The `principal.id` field MUST be byte-for-byte identical across
 every Principal Token in the same `aip_chain` array. Relying Parties
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

 | Field | Type | Required | Constraints |
 |----------------------|--------|----------|-----------------------------------|
 | `identity` | object | REQUIRED | MUST conform to agent-identity schema; `version` MUST be 1; `previous_key_signature` MUST NOT be present |
 | `capability_manifest`| object | REQUIRED | MUST conform to capability-manifest schema; `version` MUST be 1; `aid` MUST equal `identity.aid` |
 | `principal_token` | string | REQUIRED | Compact JWT (header.payload.signature); pattern: `^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$`; `delegation_depth` MUST be 0; `delegated_by` MUST be null |

#### 4.2.6. Revocation Object

 Canonical signing field order: `revocation_id`, `target_aid`, `type`,
 `issued_by`, `reason`, `timestamp`, `propagate_to_children`,
 `scopes_revoked`, `signature`.

 | Field | Type | Required | Constraints |
 |-------------------------|---------|----------|-------------------------------|
 | `revocation_id` | string | REQUIRED | pattern: `^rev:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
 | `target_aid` | string | REQUIRED | MUST match `did:aip` ABNF |
 | `type` | string | REQUIRED | enum: `["full_revoke", "scope_revoke", "delegation_revoke", "principal_revoke"]` |
 | `issued_by` | string | REQUIRED | W3C DID; in target's chain |
 | `reason` | string | REQUIRED | enum of defined reasons |
 | `timestamp` | string | REQUIRED | ISO 8601 UTC |
 | `propagate_to_children` | boolean | OPTIONAL | default: false |
 | `scopes_revoked` | array | REQUIRED when `scope_revoke`; MUST NOT otherwise | minItems: 1 |
 | `signature` | string | REQUIRED | base64url EdDSA |

#### 4.2.7. Endorsement

 Canonical signing field order: `endorsement_id`, `from_aid`,
 `to_aid`, `task_id`, `outcome`, `notes`, `timestamp`, `signature`.

 | Field | Type | Required | Constraints |
 |------------------|-------------|----------|-------------------------------------|
 | `endorsement_id` | string | REQUIRED | pattern: `^end:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
 | `from_aid` | string | REQUIRED | MUST NOT equal `to_aid` |
 | `to_aid` | string | REQUIRED | MUST NOT equal `from_aid` |
 | `task_id` | string | REQUIRED | minLength: 1, maxLength: 256 |
 | `outcome` | string | REQUIRED | enum: `["success", "partial", "failure"]` |
 | `notes` | string/null | OPTIONAL | maxLength: 512 |
 | `timestamp` | string | REQUIRED | ISO 8601 UTC |
 | `signature` | string | REQUIRED | base64url EdDSA of `from_aid` |

### 4.3. Field Constraints

 Capability `capabilities` sub-fields are defined in full in
 `schemas/v0.3/capability-manifest.schema.json`. The following is a
 normative summary.

 **Defined Scope Identifiers:**

```
 email.read email.write email.send
 email.delete calendar.read calendar.write
 calendar.delete filesystem.read filesystem.write
 filesystem.execute filesystem.delete web.browse
 web.forms_submit web.download transactions
 communicate.whatsapp communicate.telegram communicate.sms
 communicate.voice spawn_agents
```

 Where this document references `transactions.*` or `communicate.*`,
 this means the bare capability key OR any scope beginning with that
 prefix OR `capabilities.transactions.enabled: true` /
 `capabilities.communicate.enabled: true` in the Capability Manifest.

 Empty arrays `[]` for `filesystem.read` or `filesystem.write` MUST
 be interpreted as deny-all. A `require_confirmation_above` value
 above `max_single_transaction` is vacuous and MUST be rejected.

 When `communicate.enabled` is true, at least one channel MUST be
 explicitly set to true.

### 4.4. Delegation Rules

 **Rule D-1.** A delegated agent MUST NOT grant scopes or looser
 constraint values than its own Capability Manifest contains.

 **Rule D-2.** A delegated agent MUST NOT issue a Principal Token with
 `max_delegation_depth` greater than its remaining depth
 (`max_delegation_depth` - `delegation_depth`).

 **Rule D-3.** Implementations MUST reject any Credential Token where
 the `delegation_depth` of any chain token exceeds the root token's
 `max_delegation_depth`.

 **Rule D-4.** The root Principal Token (index 0) MUST have
 `delegation_depth` = 0. Each subsequent token at index `i` MUST have
 `delegation_depth` = `i`. No gaps, skips, or repeated values are
 permitted.

 **Rule D-5.** Each delegation chain token MUST be signed by the
 private key of the `delegated_by` AID (or root principal for depth 0).

---

### 4.5. AIP-GRANT: Principal Authorization Protocol

 This section defines the AIP-GRANT protocol — the standardised
 ceremony by which a human or organisational principal reviews,
 consents to, and cryptographically authorises an AI agent identity.
 AIP-GRANT is the AIP analogue of the OAuth 2.0 Authorization Code
 Flow [RFC6749].

 Two independent implementations conforming to this section MUST
 produce interoperable grant interactions.

#### 4.5.1. Overview and Roles

 **Agent Deployer** — Constructs the GrantRequest and submits the
 Registration Envelope after a successful grant. The deployer MUST
 generate the agent's Ed25519 keypair before initiating the grant.
 The deployer MAY be the principal themselves (self-service) or an
 application acting on the principal's behalf.

 **Principal Wallet** — Holds the principal's DID private key and
 executes the signing ceremony. The Principal Wallet MUST verify the
 GrantRequest, MUST present all requested capabilities in human-
 readable form per Section 4.5.3, and MUST obtain explicit affirmative
 consent before signing. The Principal Wallet MUST NOT sign a
 Principal Token without explicit human approval.

 **AIP Registry** — Accepts the Registration Envelope after a
 successful grant. The Registry's role is defined in Section 5 and is
 unchanged by AIP-GRANT.

 Flow summary:

 Figure 2: AIP-GRANT Flow
```
 Agent Deployer Principal Wallet AIP Registry
 | | |
 |-- GrantRequest ---------> | |
 | (capabilities, | |
 | purpose, nonce) | |
 | [Display consent UI] |
 | [Human reviews & signs] |
 | | |
 |<-- GrantResponse -------- | |
 | (signed PrincipalToken)| |
 | | |
 |-- RegistrationEnvelope -----------------------> |
 | (identity + manifest + | |
 | principal_token) | |
 |<-- AID ---------------------------------------- |
```

#### 4.5.2. GrantRequest Object

 The GrantRequest is a JSON object constructed by the Agent Deployer.
 It MUST be signed by the deployer's Ed25519 key when transmitted over
 the Web Redirect or QR Code bindings. The `nonce` MUST be
 cryptographically random and MUST contain at least 128 bits of
 entropy.

 | Field | Type | Required | Constraints |
 |------------------------------|---------|----------|------------------------------|
 | `grant_request_id` | string | REQUIRED | pattern: `^gr:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
 | `aip_version` | string | REQUIRED | MUST be `"0.3"` |
 | `agent_name` | string | REQUIRED | maxLength: 64; displayed in consent UI |
 | `agent_type` | string | REQUIRED | registered namespace value |
 | `model.provider` | string | REQUIRED | displayed in consent UI |
 | `model.model_id` | string | REQUIRED | displayed in consent UI |
 | `requested_capabilities` | object | REQUIRED | Capability Manifest `capabilities` sub-schema |
 | `purpose` | string | REQUIRED | minLength: 1; maxLength: 512; plain-language purpose displayed verbatim |
 | `delegation_valid_for_seconds` | integer | REQUIRED | min: 300; max: 31536000 |
 | `max_delegation_depth` | integer | OPTIONAL | default: 0; max: 10 |
 | `task_id` | string/null | OPTIONAL; REQUIRED for ephemeral | non-null, non-empty for ephemeral |
 | `deployer_did` | string | OPTIONAL | W3C DID; displayed in consent UI |
 | `deployer_name` | string | OPTIONAL | maxLength: 128; displayed in UI |
 | `nonce` | string | REQUIRED | minLength: 22; cryptographically random |
 | `request_expires_at` | string | REQUIRED | ISO 8601 UTC; RECOMMENDED 15 min to 24 hours |
 | `callback_uri` | string | CONDITIONAL | REQUIRED for Web Redirect and QR flows; MUST use HTTPS |
 | `state` | string | OPTIONAL | maxLength: 512; echoed in GrantResponse |
 | `deployer_public_key` | object | OPTIONAL | JWK of deployer; the Principal Wallet SHOULD verify the deployer signature if present |

 The deployer MUST generate the agent's AID (by generating an Ed25519
 keypair and computing the AID) before constructing the GrantRequest,
 so that the resulting Principal Token correctly names the agent's AID
 in its `sub` field.

#### 4.5.3. Wallet Consent Requirements

 The Principal Wallet MUST implement the following requirements before
 signing any grant.

 **Nonce and expiry checks:** The Principal Wallet MUST check
 `request_expires_at` against the current clock. If expired, it MUST
 reject with `grant_request_expired` and MUST NOT show the consent UI.
 The Principal Wallet MUST maintain a record of seen `grant_request_id`
 values for at least 30 days and MUST reject replays with
 `grant_request_replayed`.

 **Mandatory display elements:** The consent UI MUST display ALL of the
 following before presenting the sign/decline choice:

 (1) Agent name (`agent_name`) and type (`agent_type`).
 (2) AI model - provider and model_id (e.g., "Anthropic - claude-
 sonnet-4-6").
 (3) Purpose - the `purpose` field verbatim.
 (4) Deployer identity - `deployer_name` and `deployer_did`; a clear
 "Deployer identity unverified" warning when `deployer_did` is
 absent.
 (5) All requested capabilities in the human-readable strings
 prescribed below.
 (6) Delegation validity - expiry date and time computed from
 `delegation_valid_for_seconds` (e.g., "Expires 21 June 2026 at
 10:00 UTC").
 (7) Sub-delegation notice - if `max_delegation_depth` > 0, a clear
 statement such as "This agent may create child agents of its own
 (up to depth N)".

 **Canonical human-readable capability strings** (wallets MUST use
 these strings, or accurate translations):

 | Scope | Human-readable display |
 |-------|------------------------|
 | `email.read` | "Read your email messages and metadata" |
 | `email.write` | "Draft email messages on your behalf" |
 | `email.send` | "Send email on your behalf" (append: "to up to N recipients per message" if `max_recipients_per_send` set) |
 | `email.delete` | "**Permanently delete** your email messages - this cannot be undone" |
 | `calendar.read` | "Read your calendar events" |
 | `calendar.write` | "Create and modify calendar events" |
 | `calendar.delete` | "**Delete** calendar events" |
 | `filesystem.read` | "Read files from: [list of allowed paths]" |
 | `filesystem.write` | "Write files to: [list of allowed paths]" |
 | `filesystem.execute` | "**Execute scripts and commands** on your system - HIGH RISK" |
 | `filesystem.delete` | "**Permanently delete** files - this cannot be undone" |
 | `web.browse` | "Browse public web content" |
 | `web.forms_submit` | "Submit forms to web services on your behalf" |
 | `web.download` | "Download files from the web" |
 | `transactions` | "**Make financial transactions** up to [max_single_transaction] [currency] each, up to [max_daily_total] [currency] per day" (append: "requiring your approval above [require_confirmation_above]" if set) |
 | `communicate.whatsapp` | "Send WhatsApp messages on your behalf" |
 | `communicate.telegram` | "Send Telegram messages on your behalf" |
 | `communicate.sms` | "Send SMS messages on your behalf" |
 | `communicate.voice` | "Make and receive phone calls on your behalf" |
 | `spawn_agents.create` | "Create child AI agents on your behalf (up to [max_concurrent] at a time)" |
 | `spawn_agents.manage` | "Manage (suspend, resume, update) your existing child AI agents" |

 The Principal Wallet MUST generate capability display text from the
 JSON `requested_capabilities` object — not from any deployer-supplied
 display string. The `purpose` field is displayed verbatim for context
 but MUST NOT override the capability list.

 Principal Wallets MUST visually distinguish destructive capabilities
 (`email.delete`, `filesystem.execute`, `filesystem.delete`,
 `transactions`, `communicate.*`) from read-only capabilities using a
 clear warning indicator.

 **Additional confirmation for destructive capabilities:** If any of
 the following are requested, the Principal Wallet MUST require an
 additional explicit confirmation step (e.g., typing "I confirm" or
 biometric authentication) beyond a single click:

 - `email.delete`
 - `filesystem.execute`
 - `filesystem.delete`
 - `transactions` with `max_single_transaction` > 0
 - Any `communicate.*` channel

 **Capability negotiation:** The principal MAY approve a strict subset
 of the requested capabilities. The Principal Wallet MUST NOT allow
 the principal to add capabilities not present in the GrantRequest.
 When a subset is approved, the GrantResponse `status` MUST be
 `"partial"`. Deployers MUST handle `"partial"` responses without
 assuming full approval.

#### 4.5.4. GrantResponse Object

 The GrantResponse is constructed and signed by the Principal Wallet
 after the principal completes (or declines) the signing ceremony.

 | Field | Type | Required | Constraints |
 |------------------------------------|---------|----------|-----------------------|
 | `grant_request_id` | string | REQUIRED | Echoed from GrantRequest; MUST match |
 | `nonce` | string | REQUIRED | Echoed; MUST match original nonce |
 | `state` | string | OPTIONAL | Echoed if present in GrantRequest |
 | `status` | string | REQUIRED | enum: `["approved", "rejected", "partial"]` |
 | `principal_id` | string | REQUIRED | W3C DID of the signing principal |
 | `principal_token` | string | CONDITIONAL | Compact JWT; REQUIRED when status is `"approved"` or `"partial"`; absent when `"rejected"` |
 | `signed_capability_manifest` | object | OPTIONAL | Signed Capability Manifest (RECOMMENDED - see Section 9.1 note) |
 | `approved_capabilities` | object | CONDITIONAL | REQUIRED when status `"approved"` or `"partial"` |
 | `approved_delegation_valid_for_seconds` | integer | CONDITIONAL | REQUIRED when status `"approved"` or `"partial"` |
 | `approved_max_delegation_depth` | integer | CONDITIONAL | REQUIRED when status `"approved"` or `"partial"` |
 | `rejection_reason` | string | OPTIONAL | maxLength: 256; only when `"rejected"` |
 | `signed_at` | string | REQUIRED | ISO 8601 UTC; actual signing time |

 **Deployer validation of GrantResponse:** Upon receipt the deployer
 MUST:

 1. Verify `grant_request_id` matches the original request.
 2. Verify `nonce` matches - mismatch MUST be treated as a forgery
 attempt and the response MUST be rejected.
 3. If `status` is `"rejected"`, halt. No agent is registered.
 4. Verify `signed_at` is plausible (not in future; not more than 24
 hours in past).
 5. Decode and verify the `principal_token` JWT signature against the
 `principal_id` DID's resolved public key.
 6. Verify the `principal_token` payload `sub` matches the agent's AID.
 7. Use `approved_capabilities` to construct the Capability Manifest -
 NOT the originally requested set.

 The Principal Wallet SHOULD sign the Capability Manifest on the
 principal's behalf during the signing ceremony and include it in
 `signed_capability_manifest`. This allows the deployer to use it
 directly in the Registration Envelope without a separate signing
 step. When the Principal Wallet does not support this, deployers MUST
 obtain the Capability Manifest signature through a separate mechanism
 and MUST document this limitation.

#### 4.5.5. Transport Bindings

 Implementations MUST support the Web Redirect Flow. Implementations
 SHOULD support at least one additional binding.

 **Web Redirect Flow.** The deployer serialises the GrantRequest to
 JSON, signs it with its Ed25519 key, and base64url-encodes the
 result. It then redirects the user agent to the Principal Wallet URI:

 EXAMPLE (informative):
```
 https://wallet.example.com/aip-grant?
 request=<base64url-signed-GrantRequest>
 &aip_version=0.3
```

 Or by reference:

 EXAMPLE (informative):
```
 https://wallet.example.com/aip-grant?
 request_uri=https://deployer.example.com/grants/gr:uuid
 &aip_version=0.3
```

 When `request_uri` is used, the Principal Wallet MUST fetch the
 GrantRequest over HTTPS and MUST verify the deployer's signature
 before displaying any content to the principal.

 After the principal signs, the Principal Wallet MUST deliver the
 GrantResponse:

 EXAMPLE (informative):
```
 POST <callback_uri>
 Content-Type: application/json

 {GrantResponse JSON}
```

 The `callback_uri` MUST be pre-registered by the deployer. Principal
 Wallets MUST NOT deliver GrantResponses to unregistered URIs.

 **QR Code / Proximity Flow.** For devices where the Principal Wallet
 is on a separate device:

 EXAMPLE (informative):
```
 aip-grant://v2?request_uri=https://deployer.example.com/grants/gr:uuid
```

 Or for offline scenarios:

 EXAMPLE (informative):
```
 aip-grant://v2?request=<base64url-GrantRequest>
```

 The Principal Wallet fetches, validates, and executes the ceremony;
 it MUST deliver the GrantResponse to `callback_uri`.

 **Server-to-Server Direct Flow.** For enterprise HSM-backed Principal Wallets
 where no human UI is displayed:

 EXAMPLE (informative):
```
 POST https://wallet.enterprise.example.com/v1/aip-grant
 Content-Type: application/json
 Authorization: Bearer <deployer-service-token>

 {GrantRequest JSON}

 HTTP 200 OK
 {GrantResponse JSON}
```

 This flow MUST only be used under explicit advance policy rules set
 by the principal (e.g., "auto-approve ephemeral agents from internal
 services with scopes ⊆ {email.read, web.browse}"). Policy rules are
 the organisation's responsibility; the flow mechanics are defined
 here.

#### 4.5.6. Principal Token Construction from Grant

 After the principal approves, the Principal Wallet MUST construct a
 Principal Token JWT (Section 4.2.4) with the following claims:

 | Claim | Value |
 |------------------------|-----------------------------------------------------|
 | `iss` | The principal's W3C DID (MUST equal `principal.id`) |
 | `sub` | The agent's AID (generated by deployer) |
 | `principal.type` | `"human"` or `"organisation"` per principal's DID |
 | `principal.id` | The principal's W3C DID |
 | `delegated_by` | `null` |
 | `delegation_depth` | `0` |
 | `max_delegation_depth` | `approved_max_delegation_depth` |
 | `issued_at` | Current UTC timestamp |
 | `expires_at` | `issued_at` + `approved_delegation_valid_for_seconds` |
 | `scope` | Array matching `approved_capabilities` |
 | `purpose` | The `purpose` from the GrantRequest |
 | `task_id` | The `task_id` from the GrantRequest (required for ephemeral) |

 The Principal Wallet MUST sign with the principal's DID private key.
 The JWT `alg` MUST be `"EdDSA"`.

 Before using the Principal Token, the deployer MUST:

 1. Verify the JWT signature against the principal's public key
 (resolved via DID method).
 2. Verify `sub` matches the agent's AID.
 3. Verify `principal.id` does NOT use the `did:aip` method.
 4. Verify `delegation_depth` is exactly 0.
 5. Verify `expires_at` is in the future.

#### 4.5.7. Sub-Agent Delegation Flow

 When a parent agent delegates to a child agent, the parent acts as
 the Principal Wallet. No human consent UI is required - the parent enforces
 scope inheritance (Section 8.2) programmatically.

 The parent MUST:

 1. Verify requested child capabilities are a strict subset of its own
 Capability Manifest (Rule D-1).
 2. Construct and sign the child's Principal Token with:
 - `iss`: the parent's AID (MUST equal `delegated_by`)
 - `sub`: the child's AID
 - `delegated_by`: the parent's AID
 - `delegation_depth`: parent's depth + 1
 - `max_delegation_depth`: ≤ parent's remaining depth
 - `scope`: the granted subset
 - `principal.id`: the root principal's DID (unchanged)
 - Signed with the parent's private key
 3. Construct the Registration Envelope for the child.
 4. Submit the Registration Envelope to the Registry.

#### 4.5.8. AIP-GRANT Error Codes

 | Code | Description |
 |-------------------------------|--------------------------------------|
 | `grant_request_expired` | `request_expires_at` has passed |
 | `grant_request_replayed` | `grant_request_id` seen before |
 | `grant_request_invalid` | GrantRequest malformed or signature failed |
 | `grant_rejected_by_principal` | Principal declined |
 | `grant_nonce_mismatch` | GrantResponse nonce does not match |
 | `grant_capability_exceeds_principal` | Requested capabilities exceed principal policy |

---

### 4.6. Chained Approval Envelopes

#### 4.6.1. Motivation: The Cascading Approval Problem

 A single human approval MUST be sufficient to authorise a
 pre-declared sequence of dependent agent actions that together
 constitute one logical transaction. Without this, multi-step agent
 workflows require the human to approve each step independently,
 eliminating the operational benefit of autonomous agents.

 The Chained Approval Envelope addresses this: the principal approves
 the complete workflow graph upfront — including all dependent actions
 — before any step executes. Each Relying Party independently verifies
 its specific step against the Registry without requiring a new human
 interaction.

 NOTE: For example, an agent places an order with an e-commerce
 platform (step 1), which triggers a payment processor to debit a
 bank account (step 2). These are legally distinct API calls at
 distinct Relying Parties. If each requires independent human
 approval, the workflow loses the benefit of automation. If the bank
 debit is implicit, the security model is broken — the principal
 never explicitly authorised the bank debit. The Approval Envelope
 allows a single human approval to authorise both steps while keeping
 each Relying Party's verification independent. This is analogous to
 a consumer approving a purchase: a single action implicitly
 authorises the complete chain of payment steps. AIP makes this chain
 explicit, auditable, and cryptographically bound.

#### 4.6.2. The Token-Expiry-While-Pending Problem

 A critical operational failure mode arises without Approval Envelopes
 in workflows that require human approval before execution:

 1. Agent orchestrates a Tier 2 workflow requiring human sign-off.
 2. Agent holds a Credential Token (TTL = 300s for Tier 2 scope).
 3. Human is unavailable for 30 minutes.
 4. Credential Token expires while approval is pending.
 5. Human approves - but no valid execution token exists.
 6. The agent cannot safely re-issue a new Credential Token without
 the human re-approving, because the original token context is
 lost.

 The Approval Envelope decouples the approval phase from the execution
 phase:

 - During the **approval-pending phase**, no execution Credential
 Token exists. The Envelope waits for the principal's signature
 without requiring any agent token to remain valid. The `approval_
 window_expires_at` field (which may span hours or days) is the
 only timer running.
 - Once approved, the executing agent requests fresh, short-lived
 **step-claim tokens** from the Registry for each step at execution
 time. These comply fully with normal TTL rules (300s for Tier 2).
 - No execution token ever needs to span the approval-pending window.

 This architecture correctly separates concerns: the human's approval
 is durable (stored in the Registry); the agent's execution authority
 is ephemeral (short-lived tokens per step).

#### 4.6.3. Approval Envelope Schema

 An Approval Envelope is submitted by the orchestrating agent to
 `POST /v1/approvals` (Section 15.4) and is then approved by the principal
 through their Principal Wallet. The Registry stores the envelope and enforces
 step ordering and spend status atomically.

 Canonical signing field order for `creator_signature`:
 `approval_id`, `created_by`, `principal_id`, `description`,
 `approval_window_expires_at`, `created_at`, `steps`,
 `compensation_steps`, `total_value`, `currency`, `creator_signature`.

 | Field | Type | Required | Constraints |
 |----------------------------|---------|----------|-------------------------------|
 | `approval_id` | string | REQUIRED | pattern: `^apr:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`; immutable |
 | `created_by` | string | REQUIRED | AID of orchestrating agent |
 | `principal_id` | string | REQUIRED | W3C DID of approving principal; MUST NOT be `did:aip` |
 | `description` | string | REQUIRED | minLength: 1; maxLength: 512; plain-language workflow description |
 | `approval_window_expires_at` | string | REQUIRED | ISO 8601 UTC; MUST be after `created_at`; RECOMMENDED maximum: 72 hours |
 | `created_at` | string | REQUIRED | ISO 8601 UTC |
 | `steps` | array | REQUIRED | minItems: 1; maxItems: 20; ordered forward execution steps |
 | `compensation_steps` | array | OPTIONAL | Compensation steps for SAGA rollback |
 | `total_value` | number | OPTIONAL | Total financial value; minimum: 0 |
 | `currency` | string | OPTIONAL | ISO 4217; pattern: `^[A-Z]{3}$` |
 | `creator_signature` | string | REQUIRED | base64url EdDSA of `created_by` AID's key |
 | `status` | string | READ-ONLY | Set by Registry; see Section 4.6.6 |
 | `principal_signature` | string | CONDITIONAL | base64url EdDSA; set by the Registry after principal approves via their Principal Wallet |

 `total_value` and `currency` MUST both be present or both absent.
 When present, `total_value` MUST equal the sum of `value` fields
 across all required forward steps. The Registry MUST enforce this
 constraint at submission time.

#### 4.6.4. Step Schema

 Each element in the `steps` array represents one atomic action at one
 Relying Party.

 | Field | Type | Required | Constraints |
 |----------------------|---------|----------|------------------------------------|
 | `step_index` | integer | REQUIRED | 1-based; unique within envelope; sequential |
 | `actor` | string | REQUIRED | AID of the agent executing this step |
 | `relying_party_uri` | string | REQUIRED | URI of the Relying Party |
 | `action_type` | string | REQUIRED | Application-defined action identifier; maxLength: 128 |
 | `action_hash` | string | REQUIRED | `sha256:<64-hex>`; see Section 4.6.7 for computation |
 | `description` | string | REQUIRED | minLength: 1; maxLength: 256; displayed to principal during approval |
 | `required` | boolean | REQUIRED | When false, step is optional; envelope can complete without it |
 | `triggered_by` | integer/null | REQUIRED | null for steps with no prerequisite; step_index of the prerequisite step otherwise |
 | `value` | number | OPTIONAL | Financial value of this step; minimum: 0 |
 | `currency` | string | OPTIONAL | ISO 4217; MUST match envelope `currency` when `total_value` is present |
 | `compensation_index` | integer/null | OPTIONAL | Index into `compensation_steps` array (0-based) of the compensation action for this step |
 | `status` | string | READ-ONLY | Set by Registry: `pending` \| `claimed` \| `completed` \| `failed` \| `compensated` \| `skipped` |
 | `claimed_at` | string | READ-ONLY | ISO 8601 UTC; set when claimed |
 | `completed_at` | string | READ-ONLY | ISO 8601 UTC; set when completed |

 The `triggered_by` field implements the SAGA DAG. A step with
 `triggered_by: null` is a root step - it may be claimed as soon as
 the envelope is approved. A step with `triggered_by: N` may only be
 claimed after step `N` has status `completed`. The Registry MUST
 enforce this ordering atomically (compare-and-swap on step status).

 Circular dependencies (step A triggered_by B, B triggered_by A) MUST
 be rejected by the Registry at submission time with
 `approval_envelope_invalid`.

 Multiple steps MAY share the same `triggered_by` value, enabling
 parallel execution paths. In this case all steps with the same
 prerequisite may be claimed concurrently once that prerequisite is
 completed.

#### 4.6.5. Compensation Step Schema

 Compensation steps define the SAGA rollback actions pre-authorised
 by the principal. If a forward step fails after earlier steps have
 completed, the compensation actions for those completed steps are
 executed without requiring a new human approval.

 | Field | Type | Required | Constraints |
 |----------------------|---------|----------|------------------------------------|
 | `compensation_index` | integer | REQUIRED | 0-based index; referenced by `steps[].compensation_index` |
 | `actor` | string | REQUIRED | AID of the agent executing the compensation |
 | `relying_party_uri` | string | REQUIRED | URI of the Relying Party |
 | `action_type` | string | REQUIRED | Application-defined; should describe the rollback |
 | `action_hash` | string | REQUIRED | `sha256:<64-hex>`; computation identical to Section 4.6.7 |
 | `description` | string | REQUIRED | Plain-language description of rollback action; displayed to principal during approval |
 | `status` | string | READ-ONLY | `pending` \| `claimed` \| `completed` \| `failed` |

 When the principal approves an Approval Envelope, they approve both
 the forward steps and all compensation steps. A compensation step
 carries the same weight of consent as a forward step - it was
 explicitly reviewed and signed by the principal.

#### 4.6.6. Approval Envelope Lifecycle

 The Registry maintains an Approval Envelope's lifecycle state and
 enforces valid transitions:

 Figure 3: Approval Envelope Lifecycle State Machine
```
 pending_approval ──────► approved ──────► executing ──────► completed
 │ │ │
 ▼ ▼ ▼
 rejected expired compensating ──► compensated
 │
 ▼
 failed
```

 Transition rules:

 - `pending_approval → approved`: Principal signs via Principal Wallet flow
 (Section 15.4). Registry stores `principal_signature` and sets
 `approved_at`.
 - `pending_approval → rejected`: Principal rejects.
 - `pending_approval → expired`: `approval_window_expires_at` passes
 without approval. The Registry MUST automatically transition to
 `expired` on or before the expiry time.
 - `approved → executing`: First step is claimed (Section 4.6.8). Automatic
 transition.
 - `executing → completed`: All `required: true` steps reach
 `completed` status.
 - `executing → compensating`: Any `required: true` step reaches
 `failed` status and at least one completed step has a
 `compensation_index`. The Registry MUST automatically trigger
 compensation.
 - `compensating → compensated`: All applicable compensation steps
 complete successfully.
 - `compensating → failed`: One or more compensation steps fail. This
 is a terminal failure state requiring manual intervention.
 - `completed`, `compensated`, `failed`, `rejected`, and `expired` are
 terminal states. No further transitions are permitted.

 The `executing`, `compensating`, `compensated`, and `failed` states
 MUST be set by the Registry based on step status changes. Agents
 MUST NOT attempt to set envelope-level status directly; they claim
 and complete individual steps.

#### 4.6.7. Action Hash Computation

 The `action_hash` in each step binds the principal's approval to the
 specific content of the action. An agent MUST NOT present an Approval
 Envelope step to execute a different amount, recipient, or action
 type than the principal approved.

 The `action_hash` MUST be computed as follows:

```
 action_hash = "sha256:" + LCHEX( SHA-256( JCS( action_parameters ) ) )
```

 Where:

 - `JCS( x )` denotes serialization of JSON value `x` per the JSON
   Canonicalization Scheme [RFC8785], producing a UTF-8 byte sequence
   with no BOM.
 - `SHA-256( b )` is the SHA-256 hash of byte sequence `b` per
   [FIPS-180-4].
 - `LCHEX( h )` is the lowercase hexadecimal encoding of hash `h`
   using digits `0-9` and `a-f` only.
 - `"sha256:"` is a literal 7-byte ASCII prefix.

 The resulting `action_hash` value MUST match the pattern
 `^sha256:[0-9a-f]{64}$`.

 Where `action_parameters` is a JSON object containing:

 | Field | Value |
 |------------------|----------------------------------------------------|
 | `approval_id` | The `approval_id` of the envelope |
 | `step_index` | The `step_index` of this step |
 | `actor` | The `actor` AID |
 | `relying_party_uri` | The `relying_party_uri` |
 | `action_type` | The `action_type` |
 | `parameters` | A JSON object with all action-specific parameters (e.g., `{"amount": 42.99, "currency": "GBP", "recipient": "amazon.co.uk"}`) |

 Implementations MUST use an RFC8785-conformant library for JCS
 serialization (per Section 2.1). The following language-native
 serializers are NOT RFC8785-conformant and MUST NOT be used
 directly for this computation: Python `json.dumps`, Go
 `encoding/json`, Rust `serde_json` (without explicit JCS mode).
 Using a non-conformant serializer produces silently incorrect
 hashes that will cause legitimate step claims to fail with
 `approval_step_action_mismatch` with no diagnostic indication of
 the root cause.

 NOTE (informative): Recommended RFC8785-conformant libraries:
 Go: `github.com/cyberphone/json-canonicalization`; Python: `jcs`
 (PyPI); Rust: `json-canon` crate; JavaScript: `canonicalize`
 (npm); Java: `json-canonicalization` (Cyberphone).

 Financial amounts and other numeric values in the `parameters`
 object MUST be represented as JSON numbers (not strings) so that
 RFC8785 §3.2.2 number canonicalization applies deterministically
 across implementations.

 The `parameters` object is application-defined. It MUST contain all
 values that are material to the action's effect and that the principal
 evaluated when approving. Implementations MUST document the
 `parameters` schema for each `action_type` they define.

 At step-claim time (Section 4.6.8), the claiming agent MUST present
 the `action_parameters` object. The Registry MUST recompute the hash
 and MUST reject any claim where the recomputed hash does not match
 the stored `action_hash`. This ensures the agent cannot execute a
 different action than the principal approved.

#### 4.6.8. Step Claim and Execution Protocol

 To execute a step, an agent follows this protocol:

 **Step 1 - Claim:** The agent calls
 `POST /v1/approvals/{id}/steps/{n}/claim` with:

 - A valid AIP Credential Token (standard TTL rules apply - 300s for
 Tier 2 scopes) in the `Authorization` header.
 - The `action_parameters` object in the request body.

 The Registry MUST atomically verify all of the following before
 granting the claim:

 a. Envelope status is `approved` or `executing`.
 b. `approval_window_expires_at` has not passed.
 c. The step's current status is `pending` (not claimed, completed,
 or failed). This MUST be checked atomically - two simultaneous
 claim requests for the same step MUST result in exactly one
 succeeding and one receiving `approval_step_already_claimed`.
 d. All steps whose `step_index` equals this step's `triggered_by`
 have status `completed`.
 e. The AID in the Credential Token's `iss` claim matches the step's
 `actor` field.
 f. The Credential Token passes the standard 12-step validation
 (Section 7.3).
 g. The recomputed action_hash from the presented `action_parameters`
 matches the stored `action_hash` for this step.

 If all checks pass, the Registry MUST atomically set the step status
 to `claimed`, set `claimed_at` to the current timestamp, and if the
 envelope was `approved`, transition it to `executing`.

 The Registry MUST return a **Step Execution Token** — a short-lived,
 step-bound Credential Token signed by the Registry's administrative
 key — that the agent presents to the Relying Party:

 EXAMPLE (informative):
```json
 {
 "iss": "<Registry AID>",
 "sub": "<actor AID>",
 "aud": "<relying_party_uri>",
 "iat": <now>,
 "exp": <now + 300>,
 "jti": "<UUID v4>",
 "aip_version": "0.3",
 "aip_scope": [...],
 "aip_chain": [...],
 "aip_approval_id": "<approval_id>",
 "aip_approval_step": <step_index>
 }
```

 The `aip_approval_id` and `aip_approval_step` claims in the Step
 Execution Token serve as proof that this step was approved as part of
 an Approval Envelope. The Relying Party MUST verify these claims by
 calling `GET /v1/approvals/{id}/steps/{n}` to confirm the step is in
 `claimed` status with a matching `actor`.

 **Step 2 - Execute:** The agent presents the Step Execution Token to
 the Relying Party and executes the action. The Relying Party validates
 the Step Execution Token using the standard 12-step algorithm PLUS the
 Approval Envelope step verification described above.

 **Step 3 - Complete or Fail:** After execution, the agent MUST call
 either `POST /v1/approvals/{id}/steps/{n}/complete` or
 `POST /v1/approvals/{id}/steps/{n}/fail`. Failure to call either
 within `step_claim_timeout_seconds` (RECOMMENDED: 600 seconds) MUST
 cause the Registry to automatically transition the step to `failed`
 and trigger compensation if applicable.

#### 4.6.9. SAGA Compensation Semantics

 When any `required: true` step transitions to `failed` after one or
 more earlier steps have status `completed`, the Registry MUST:

 1. Transition the envelope status to `compensating`.
 2. For every completed step that has a non-null `compensation_index`,
 trigger the corresponding compensation step by setting its status
 to `pending` in the `compensation_steps` array (in reverse
 `step_index` order - last completed first).
 3. Notify the orchestrating agent (`created_by`) of the compensation
 trigger via any available mechanism (webhook if registered, or
 polling via `GET /v1/approvals/{id}`).

 Compensation steps are executed using the same step-claim protocol
 (Section 4.6.8), with the same TTL rules and DPoP requirements, but against
 `POST /v1/approvals/{id}/compensation-steps/{n}/claim`.

 Because the principal pre-approved all compensation steps in the
 Approval Envelope, no additional human interaction is required for
 compensation. This is the core SAGA property: the human approved the
 complete workflow including its defined failure modes.

 If a compensation step itself fails, the envelope transitions to
 `failed` (terminal). This constitutes a SAGA failure requiring manual
 intervention outside the AIP protocol.

#### 4.6.10. Approval Envelope Validation Rules

 The Registry MUST reject an Approval Envelope at submission time if
 any of the following are true:

 1. `principal_id` begins with `did:aip:`.
 2. `steps` contains circular dependencies in `triggered_by` fields.
 3. `steps` contains duplicate `step_index` values.
 4. When `total_value` is present: the sum of `value` fields across all
 `required: true` steps does not equal `total_value`.
 5. When `total_value` is present: any step with a `value` field uses
 a `currency` different from the envelope's `currency`.
 6. `approval_window_expires_at` is in the past at submission time.
 7. `compensation_index` values in `steps` reference non-existent
 indices in `compensation_steps`.
 8. The `creator_signature` does not verify against `created_by`'s
 registered public key.
 9. The `created_by` agent is revoked.
 10. `steps` contains more than 20 elements.

 The Registry MUST also reject Approval Envelopes from agents whose
 Capability Manifest does not include `spawn_agents.create` or at
 minimum `transactions` capability relevant to the declared steps.

### 4.7. Capability Overlays

 A Capability Overlay is a signed restriction document stored in the
 Registry. It narrows an agent's effective capability set for
 operations within a specific engagement or issuer context.

 **Rule CO-1 (Attenuation Only):** An overlay MUST NOT expand any
 constraint value beyond what the base Capability Manifest permits.
 The effective capability set is always the intersection of the base
 manifest and all active overlays scoped to the engagement or issuer.

#### 4.7.1. Overlay Schema

 | Field | Type | Required | Constraints |
 |-------|------|----------|-------------|
 | `overlay_id` | string | REQUIRED | Pattern: `^co:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
 | `aid` | string | REQUIRED | The target agent's AID |
 | `engagement_id` | string | OPTIONAL | Pattern: `^eng:...` (UUID v4 with `eng:` prefix); links to Engagement Object (Section 4.8) |
 | `issued_by` | string | REQUIRED | DID of the overlay issuer; MUST be `did:web` or `did:aip` (MUST NOT be `did:key`) |
 | `overlay_type` | string | REQUIRED | MUST be `"restrict"` |
 | `issued_at` | string | REQUIRED | ISO 8601 UTC timestamp |
 | `expires_at` | string | REQUIRED | ISO 8601 UTC; MUST be strictly after `issued_at` |
 | `version` | integer | REQUIRED | Positive integer; monotonically increasing per `(aid, engagement_id, issued_by)` tuple |
 | `constraints` | object | REQUIRED | Uses the same schema as Capability Manifest `capabilities` sub-object |
 | `signature` | string | REQUIRED | Base64url EdDSA signature by `issued_by` over JCS canonical JSON [RFC8785] excluding the `signature` field |

#### 4.7.2. Overlay Rules

 1. **CO-1 (Attenuation Only):** For every field in `constraints`,
    the value MUST be equal to or more restrictive than the
    corresponding value in the base Capability Manifest. The Registry
    MUST reject overlays that violate CO-1 with
    `overlay_exceeds_manifest`.

 2. **CO-2 (Issuer DID Method):** The `issued_by` DID MUST use
    `did:web` or `did:aip`. Overlays signed by `did:key` MUST be
    rejected with `overlay_issuer_invalid`.

 3. **CO-3 (Version Monotonicity):** A new overlay for the same
    `(aid, engagement_id, issued_by)` tuple MUST have a strictly
    higher `version` than the current active overlay. The Registry
    MUST reject downgrades with `overlay_version_conflict`.

 4. **CO-4 (Expiry Handling):** Expired overlays MUST be treated as
    absent. When an overlay expires, the base Capability Manifest
    applies without restriction for that issuer/engagement context.

 5. **CO-5 (Engagement Termination):** If an Engagement Object
    (Section 4.8) associated with an overlay's `engagement_id` is
    terminated, all overlays for that engagement MUST be invalidated
    atomically by the Registry.

 6. **CO-6 (Multiple Overlays):** When multiple overlays apply to
    the same agent, the effective capability set is the intersection
    of ALL applicable overlays with the base manifest.

#### 4.7.3. Effective Capability Computation

 The effective capability set for a validation context is:

```
 effective = base_manifest.capabilities
 for each active_overlay in applicable_overlays:
     effective = intersect(effective, active_overlay.constraints)
```

 Where `intersect` applies per-field: boolean fields use AND (false
 wins); numeric limits use min(base, overlay); path arrays use set
 intersection; scope set to `false` removes that scope.

### 4.8. Engagement Objects

 An Engagement Object is a mutable Registry resource that models a
 multi-party engagement. It is the parent container for Capability
 Overlays (Section 4.7) scoped via `engagement_id`, Approval
 Envelopes (Section 4.6) scoped via `engagement_id`, and participant
 roster and approval gate state.

#### 4.8.1. Engagement Schema

 | Field | Type | Required | Constraints |
 |-------|------|----------|-------------|
 | `engagement_id` | string | REQUIRED | Pattern: `^eng:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
 | `title` | string | REQUIRED | maxLength: 256 |
 | `hiring_operator` | string | REQUIRED | DID; MUST be `did:web` or `did:aip` |
 | `deploying_principal` | string | REQUIRED | DID of the deploying principal |
 | `created_at` | string | REQUIRED | ISO 8601 UTC |
 | `expires_at` | string | REQUIRED | ISO 8601 UTC; MUST be after `created_at` |
 | `status` | string | REQUIRED | One of: `"proposed"`, `"active"`, `"suspended"`, `"completed"`, `"terminated"` |
 | `participants` | array | REQUIRED | Array of Participant objects |
 | `approval_gates` | array | OPTIONAL | Array of Approval Gate objects |
 | `change_log` | array | REQUIRED | Append-only array of Change Log Entry objects |
 | `hiring_operator_signature` | string | REQUIRED | Base64url EdDSA signature by `hiring_operator` |
 | `deploying_principal_signature` | string | REQUIRED | Countersignature by `deploying_principal` |
 | `version` | integer | REQUIRED | Monotonically increasing |

 **Participant object fields:** `aid` (REQUIRED), `role` (REQUIRED,
 maxLength: 64), `capability_overlay_id` (OPTIONAL), `added_at`
 (REQUIRED, ISO 8601), `added_by` (REQUIRED, DID), `removed_at`
 (OPTIONAL, ISO 8601).

 **Approval Gate object fields:** `gate_id` (REQUIRED, pattern:
 `^gate:[a-z0-9_-]+$`), `name` (REQUIRED, maxLength: 128),
 `required_approver` (REQUIRED, DID), `trigger` (REQUIRED, string),
 `status` (REQUIRED, one of: `"pending"`, `"approved"`,
 `"rejected"`), `approved_at` (OPTIONAL, ISO 8601).

#### 4.8.2. Change Log

 Each change log entry: `seq` (REQUIRED, monotonically increasing
 from 1), `timestamp` (REQUIRED, ISO 8601), `action` (REQUIRED),
 `actor` (REQUIRED, DID), `payload` (OPTIONAL, object), `signature`
 (REQUIRED, Base64url EdDSA by `actor` over JCS canonical JSON
 excluding `signature`).

 Defined actions: `engagement_created`, `engagement_countersigned`,
 `participant_added`, `participant_removed`,
 `participant_role_changed`, `gate_added`, `gate_approved`,
 `gate_rejected`, `engagement_suspended`, `engagement_resumed`,
 `engagement_completed`, `engagement_terminated`.

 The Registry MUST reject any request that modifies or deletes an
 existing change log entry. Only appends are permitted.

#### 4.8.3. Engagement Lifecycle

```
 proposed --> active --> completed
                |
                +--> suspended --> active (resumed)
                |
                +--> terminated
```

 - **proposed → active:** Requires both `hiring_operator_signature`
   and `deploying_principal_signature`.
 - **active → suspended / completed:** Hiring operator only.
 - **active/suspended → terminated:** Either party.

#### 4.8.4. Termination Cascade

 When an Engagement is terminated:

 1. The Registry MUST set `status: "terminated"` atomically.
 2. All Capability Overlays linked to this `engagement_id` MUST be
    invalidated (per Rule CO-5).
 3. All Approval Envelopes in `pending_approval`, `approved`, or
    `executing` status scoped to this `engagement_id` MUST be
    transitioned to `cancelled`.
 4. Subsequent Credential Token validation for operations scoped to
    this engagement MUST fail with `engagement_terminated`.

---

## 5. Registration Protocol

### 5.1. Registration Envelope

 An agent is registered by submitting a Registration Envelope to
 `POST /v1/agents`. The fields are defined in Section 4.2.5.

 The `principal_token` MUST have `delegation_depth` equal to 0 and
 `delegated_by` equal to null. The `sub` field of the decoded principal
 token payload MUST equal `identity.aid`.

### 5.2. Registration Validation

 The Registry MUST perform the following checks in order before
 accepting a Registration Envelope. The Registry MUST either accept
 all or reject all — partial registration MUST NOT be possible.

 Check 1. `identity` MUST be present and MUST be valid JSON
 conforming to the Agent Identity schema.

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

 The Registry MUST record the `delegated_by` field from the decoded
 `principal_token` payload (or the principal's DID if `delegated_by`
 is null) in the parent-child delegation index, for use in revocation
 propagation (Section 9.3).

### 5.3. Error Responses

 All AIP error responses MUST use the format defined in Section 13.1.
 Implementations MUST NOT return HTTP 200 for error conditions.

---

## 6. Agent Resolution

### 6.1. DID Resolution

 Every AID MUST have a corresponding W3C DID Document resolvable by
 any standard DID resolver. The DID Document is derived
 deterministically from the Agent Identity stored in the
 Registry.

 The Registry MUST generate and serve DID Documents from
 `GET /v1/agents/{aid}` when the `Accept: application/did+ld+json` or
 `Accept: application/did+json` header is present.

 AIP implementations MUST support DID resolution for at minimum
 `did:key` and `did:web` DID methods. Resolved DID Documents MAY be
 cached for a maximum of 300 seconds. If resolution fails or times
 out, implementations MUST treat the result as `registry_unavailable`
 and MUST reject the operation.

 If the AID has been revoked, the Registry MUST return
 `deactivated: true` in `didDocumentMetadata`, per [W3C-DID] Section 7.1.2.

### 6.2. DID Document Structure

 A conformant `did:aip` DID Document MUST include `@context`, `id`,
 `verificationMethod`, `authentication`, and `controller`. See the
 canonical example in the repository at
 `examples/latest/did-document.json`.

 A principal's DID Document that authorises agents for Tier 2
 operations MUST include an `AIPRegistry` service entry in its
 `service` array:

 ```json
 {
   "id": "did:web:acme.com#aip-registry",
   "type": "AIPRegistry",
   "serviceEndpoint": "https://registry.acme.com"
 }
 ```

 The `serviceEndpoint` MUST be an HTTPS URI pointing to the base URL
 of the authoritative AIP Registry for agents delegated by this
 principal. The `type` MUST be exactly `"AIPRegistry"` (case-
 sensitive).

 For principals using `did:key`: an `AIPRegistry` service entry
 cannot be declared (DID Key documents have no service array). Per
 Section 4.5, `did:key` principals MUST NOT authorise Tier 2
 operations.

 For principals using `did:web` or `did:aip`: the `AIPRegistry`
 service entry is REQUIRED when the principal authorises any agent
 with Tier 2 scopes. It is OPTIONAL for principals authorising only
 Tier 1 agents.

 The CRUD operations for `did:aip` are:

 | Operation | Mechanism |
 |------------|---------------------------------------------------|
 | Create | `POST /v1/agents` with Registration Envelope |
 | Read | `GET /v1/agents/{aid}` with DID Accept header |
 | Update | `PUT /v1/agents/{aid}` for key rotation only |
 | Deactivate | `POST /v1/revocations` with `full_revoke` object |

### 6.3. Registry Genesis

 Registry Genesis is the one-time initialisation procedure by which a
 new AIP Registry creates and persists its own `did:aip` Agent
 Identity (the Registry AID). It MUST be performed before the
 Registry serves any requests.

#### 6.3.1. Key Generation

 The Registry MUST generate a fresh Ed25519 keypair at first boot.
 The private key MUST be stored encrypted at rest (AES-256-GCM or
 equivalent). The public key is used to construct the Registry's DID
 Document and to sign CRL documents (Section 9.2) and Step Execution
 Tokens (Section 4.6.8).

#### 6.3.2. AID Construction

 The Registry MUST construct its AID using the `registry` namespace
 (Section 4.1):

```
 did:aip:registry:<32-hex-character unique-id>
```

 The `unique-id` MUST be generated as a cryptographically random
 32-character lowercase hexadecimal string. At most one Registry AID
 MUST be active per Registry deployment at any time.

#### 6.3.3. Self-Registration Exemption

 The Registry AID MUST NOT be created via `POST /v1/agents`. Instead,
 the Registry MUST persist its AID and keypair directly to its own
 data store during genesis. The following Registration Envelope
 checks (Section 5.2) are explicitly inapplicable to the Registry AID:

 - **Check 10** (`principal_token` validation) — the Registry has no
   human principal and MUST NOT carry a principal delegation chain.
 - **Check 4** (duplicate AID rejection) — genesis is idempotent; if
   a Registry AID already exists in the data store the existing record
   MUST be used and genesis MUST NOT overwrite it.

#### 6.3.4. Well-Known Publication

 The Registry MUST publish its DID Document and public key at:

```
 GET /.well-known/aip-registry
```

 The response MUST be a JSON object containing:

 | Field | Type | Required | Description |
 |-----------------|--------|----------|-----------------------------------------------|
 | `registry_aid` | string | REQUIRED | The Registry's `did:aip` AID |
 | `registry_name` | string | REQUIRED | Human-readable Registry name (maxLength: 128) |
 | `aip_version` | string | REQUIRED | The `aip_version` this Registry conforms to |
 | `public_key` | object | REQUIRED | JWK representation of the Registry's Ed25519 public key |
 | `endpoints` | object | REQUIRED | Map of service names to relative or absolute URI paths |
 | `signature` | string | REQUIRED | Base64url EdDSA signature of the canonical JSON (RFC 8785 JCS) of the document excluding the `signature` field |

 The `endpoints` object MUST include at minimum:

 | Key | Description |
 |---------------|----------------------------------------------|
 | `agents` | Base path for agent endpoints (e.g., `/v1/agents`) |
 | `crl` | CRL endpoint path (e.g., `/v1/crl`) |
 | `revocations` | Revocation submission path (e.g., `/v1/revocations`) |

 **Self-signature verification:** Relying Parties MUST verify the
 `signature` field against the `public_key` in the same document.
 This ensures the well-known document has not been tampered with in
 transit. The signature is computed over the RFC 8785 JCS canonical
 serialisation of the document with the `signature` field removed.

 **First-contact bootstrapping:** On first contact with a Registry,
 Relying Parties MUST:

 1. Fetch `/.well-known/aip-registry` over HTTPS.
 2. Verify the self-signature.
 3. Pin the `public_key` and `registry_aid` locally.
 4. On subsequent contacts, verify that the pinned key matches.

 Key rotation for Registry keys is an administrative operation that
 requires out-of-band communication to Relying Parties. A future AIP
 will define the Registry key rotation protocol.

 Validators bootstrapping trust in a Registry MUST fetch and pin the
 Registry's public key from this endpoint before processing any Step
 Execution Tokens or CRL documents signed by that Registry. Cached
 values MUST NOT be used beyond 300 seconds without revalidation.

#### 6.3.5. Single-Instance Constraint

 Each Registry deployment MUST have exactly one active Registry AID.
 Provisioning a second Registry AID within the same deployment
 MUST be treated as a fatal configuration error. Horizontal scaling
 and high-availability deployments MUST share a single Registry AID
 and keypair (stored in a shared secrets manager).

---

## 7. Credential Tokens

### 7.1. Token Structure

 An AIP Credential Token is transmitted as an HTTP Authorization
 header:

 EXAMPLE (informative):
```
 Authorization: AIP <token>
 X-AIP-Version: 0.3
```

 For interactions requiring Proof-of-Possession:

 EXAMPLE (informative):
```
 Authorization: AIP <token>
 DPoP: <dpop-proof>
 X-AIP-Version: 0.3
```

 The `X-AIP-Version` HTTP header MUST carry the full protocol version
 string, identical to the `aip_version` JWT claim (Section 4.2.3).
 For this specification, the value MUST be `"0.3"`. Implementations
 MUST reject requests where the `X-AIP-Version` header carries a
 version value that does not match a supported `aip_version`.

### 7.2. Token Issuance

 Implementations MUST enforce the following maximum token lifetimes:

 | Scope Category | Maximum TTL |
 |-----------------------------------------------------------|-------------------------|
 | All standard scopes (`email.*`, `calendar.*`, `web.*`, etc.) | 3600 seconds (1 hour) |
 | `transactions.*` or `communicate.*` | 300 seconds (5 minutes) |
 | `filesystem.execute` | 300 seconds (5 minutes) |
 | `spawn_agents.create` or `spawn_agents.manage` | 300 seconds (5 minutes) |

 When a token contains scopes from multiple categories, the most
 restrictive TTL applies. Zero-duration and negative-duration tokens
 (where `exp <= iat`) MUST be rejected.

### 7.3. Token Validation

 A Relying Party MUST execute the following 12 steps in order. The
 Relying Party MUST reject the token at the first step that fails.

 **Step 1 - Parse.** Parse as JWT. Fail: `invalid_token`.

 **Step 2 - Header.** Verify `typ` = `"AIP+JWT"` and `alg` is
 approved per Section 17.2. Fail: `invalid_token`.

 **Step 3 - Identify agent.** Extract `kid`. Retrieve the historical
 public key matching the full `kid` DID URL from the Registry.
 Fail: `unknown_aid`.

 **Step 4 - Signature.** Verify token signature. Fail: `invalid_token`.

 **Step 5 - Claims.**
 a) `iat` MUST NOT be in future (30s clock skew tolerance).
 b) `exp` MUST be strictly greater than `iat`. Fail: `invalid_token`.
 c) `exp` MUST be in future. Fail: `token_expired`.
 d) `aud` MUST match Relying Party identifier. Fail: `invalid_token`.
 e) `jti` MUST NOT have been seen for this issuer within the validity
 window. Fail: `token_replayed`.
 f) `aip_version` MUST be present and supported. Fail: `invalid_token`.

 **Step 6 - TTL.** Verify `exp - iat` ≤ maximum TTL for requested
 scopes (Section 7.2). Fail: `invalid_token`.

 **Step 6a - Registry Trust Anchoring (Tier 2 MUST; Tier 1 SHOULD).**
 1) Extract `principal_did` from `aip_chain[0].iss` (the root
    principal's DID).
 2) Resolve `principal_did` using the DID method's own resolution
    mechanism. The resolution MUST be independent of any agent-
    provided data.
 3) Locate a `service` entry with `type: "AIPRegistry"` in the
    resolved DID Document.
 4) Extract the `serviceEndpoint` URI.
 5) Verify that the Registry from which the Relying Party has been
    fetching revocation status and capability data for this token
    matches the `serviceEndpoint` URI (origin comparison per
    [RFC6454]).
 6) If `aip_registry` is present in the Credential Token and does
    not match the DID-Document-declared Registry, Fail:
    `registry_untrusted`.
 7) If the DID Document does not contain an `AIPRegistry` service
    entry and the token contains Tier 2 scopes, Fail:
    `registry_untrusted`.
 For Tier 1 operations, this step is RECOMMENDED but not required.
 Resolution failure: Fail: `registry_unavailable` for Tier 2.

 **Step 6b - Engagement validation (conditional).** If
 `aip_engagement_id` is present in the token:
 1) Fetch the Engagement Object from the Registry via
    `GET /v1/engagements/{aip_engagement_id}`.
 2) Verify the Engagement `status` is `active`. Fail:
    `engagement_terminated` if `completed` or `terminated`;
    `engagement_suspended` if `suspended`.
 3) Verify token `sub` appears in the Engagement's `participants`
    array with `status: "active"`. Fail:
    `engagement_participant_removed`.
 4) If the Engagement defines `approval_gates` with pending gates,
    verify the token's operation is not gated. Fail:
    `engagement_gate_pending`.

 **Step 7 - Revocation.** Query revocation status of `iss`. Fail:
 `agent_revoked`.

 **Step 8 - Delegation chain.** For each Principal Token at index `i`
 (from 0 to n-1):
 a) Valid JWT conforming to Principal Token schema.
 b) `delegation_depth` equals exactly `i`. Fail: `invalid_delegation_depth`.
 c) `delegation_depth` does not exceed root token's `max_delegation_depth`
 (default: 3 when absent). Fail: `invalid_delegation_depth`.
 d) Signature valid: resolve signing key from `aip_chain[i].iss`.
 For i=0, `iss` MUST equal `principal.id`; resolve the DID via its
 DID method. For i>0, `iss` MUST equal `delegated_by` (=
 `aip_chain[i-1].sub`); retrieve key from Registry.
 Fail: `delegation_chain_invalid` if `iss` constraint violated;
 `registry_unavailable` if key resolution fails.
 e) `delegated_by[i]` equals `sub[i-1]`. Fail:
 `delegation_chain_invalid`.
 f) Each `sub` AID not revoked. Fail: `agent_revoked`.
 g) No AID appears more than once. Fail: `delegation_chain_invalid`.
 h) `expires_at` strictly after `issued_at` and in future (30s
 tolerance). Fail: `chain_token_expired`.
 i) `principal.id` identical across all chain elements. Fail:
 `delegation_chain_invalid`.
 j) `principal.id` from `aip_chain[0]` does NOT begin with `did:aip:`.
 Fail: `delegation_chain_invalid`.

 **Step 8 Post-Check A.** `iss` MUST equal `aip_chain[n-1].sub`.
 Fail: `delegation_chain_invalid`.

 **Step 8 Post-Check B.** For single-element chains: `iss` MUST equal
 `sub`. Fail: `delegation_chain_invalid`.

 **Step 9 - Capability.** Fetch agent's Capability Manifest. For Tier
 2 operations: MUST be fetched fresh - cached manifests MUST NOT be
 used. For Tier 1: may be cached up to 60 seconds.
 a) Verify manifest `signature`. Fail: `manifest_invalid`.
 b) Verify manifest `expires_at` in future. Fail: `manifest_expired`.
 c) For delegated agents: verify scope inheritance up to
 `max_delegation_depth` ancestor fetches. Fail: `insufficient_scope`
 or `manifest_invalid`.
 d) Verify each scope in `aip_scope` per the exhaustive scope-to-
 manifest mapping (see full table in `schemas/v0.3/`). Fail:
 `insufficient_scope`.
 e) If a Capability Overlay exists for this agent (Section 4.7),
 compute the effective capability set by intersecting the base
 Capability Manifest with the overlay. Verify that each scope in
 `aip_scope` is present in the effective capability set. Fail:
 `insufficient_scope`. Verify the overlay signature. Fail:
 `overlay_signature_invalid`.

 **Step 10 - DPoP (conditional).** If any scope is `transactions`,
 `transactions.*`, `communicate.*`, `filesystem.execute`,
 `spawn_agents.create`, or `spawn_agents.manage`: verify
 DPoP proof per Section 17.3. Fail: `dpop_proof_required`.

 **Step 10a - Approval Envelope step verification (conditional).**
 If `aip_approval_id` and `aip_approval_step` are present in the
 token (Step Execution Token case): the Relying Party MUST call
 `GET /v1/approvals/{aip_approval_id}/steps/{aip_approval_step}` and
 verify: (i) step status is `claimed`; (ii) step `actor` matches
 token `sub`; (iii) step `relying_party_uri` matches the current
 request URL host; (iv) the recomputed action_hash matches. Fail:
 `approval_step_invalid`.

 **Step 11 - Tier 3 (conditional).** For Tier 3 enterprise deployments:
 verify mTLS client certificate maps to `iss`. Perform OCSP check.
 Fail: `invalid_token` or `agent_revoked` or `registry_unavailable`.

 **Step 12 - Accept.**

### 7.4. Token Refresh and Long-Running Tasks

#### 7.4.1. Agent Self-Refresh

 An AIP agent holds its own Ed25519 private key and MAY issue new
 Credential Tokens at any time, provided the Principal Token(s) in its
 delegation chain (`aip_chain`) remain valid. There is no refresh token
 in AIP - the agent's signing key IS the refresh credential.

 An agent self-refresh involves: issuing a new Credential Token with a
 new `jti`, a fresh `iat`, and a new `exp` within TTL limits.
 The `aip_chain` content remains unchanged until the Principal Tokens
 within it expire.

 Agents MUST NOT re-use the same `jti` when issuing a fresh token.
 Each issued Credential Token MUST have a unique `jti`.

#### 7.4.2. Pre-emptive Refresh Requirements

 Agents MUST implement pre-emptive refresh to avoid mid-task token
 expiry. An agent MUST begin issuing a replacement Credential Token
 before the current token expires:

 | Token TTL Category | Begin refresh when remaining TTL ≤ |
 |--------------------|-------------------------------------|
 | Standard (3600s) | 300 seconds (5 minutes) |
 | Sensitive (300s) | 30 seconds |

 Implementations MUST NOT wait for a token rejection (`token_expired`)
 before refreshing. Waiting for rejection creates a gap in execution
 continuity and may leave in-progress Tier 2 operations without valid
 authority.

 Relying Parties MUST NOT reject a token solely because a newer token
 exists for the same agent. Each token is independently valid for its
 own `iat` to `exp` window.

 For real-time streaming interactions (e.g., a long-running web
 socket), the agent SHOULD renegotiate the session with a fresh
 Credential Token before the current token's expiry rather than
 waiting for mid-stream rejection.

#### 7.4.3. Delegation Chain Expiry

 When a Principal Token in the `aip_chain` expires, the Credential
 Token becomes structurally invalid at validation Step 8h regardless
 of the Credential Token's own `exp`. This is because the delegation
 authority itself has lapsed.

 When a delegation chain expires:

 1. The agent MUST NOT issue new Credential Tokens referencing the
 expired `aip_chain` (even if the agent's own `exp` is still in the
 future).
 2. The agent MUST obtain a fresh delegation from its parent (or from
 the root principal for depth-0 agents) via the AIP-GRANT flow
 (Section 4.5) or sub-agent delegation flow (Section 4.5.7).
 3. Once a fresh delegation is established and registered, the agent
 may resume issuing Credential Tokens.

 Relying Parties that receive a token where Step 8h fails MUST return
 `chain_token_expired`. Agents receiving this error MUST treat it as
 `delegation_chain_refresh_required` - they must re-establish their
 delegation rather than merely refreshing their Credential Token.

 **Anticipatory chain refresh:** Agents SHOULD monitor the `expires_at`
 timestamps of all Principal Tokens in their `aip_chain`. When the
 nearest expiry is within 10% of the total delegation validity period
 (or 24 hours, whichever is smaller), the agent SHOULD proactively
 initiate a delegation renewal.

#### 7.4.4. Interaction with Approval Envelopes

 Approval Envelopes (Section 4.6) are specifically designed to decouple
 human approval timing from token TTL constraints. The following rules
 govern their interaction:

 1. An Approval Envelope's `approval_window_expires_at` is independent
 of any Credential Token TTL. Envelopes may remain in
 `pending_approval` status for hours while normal TTLs of 300s or
 3600s apply only at execution time.

 2. When an agent claims an Approval Step (Section 4.6.8), it MUST present a
 Credential Token that is valid at the time of the claim. The token
 TTL for a step-claim follows the same rules as for any other
 interaction involving those scopes (300s for Tier 2 scopes, 3600s
 for Tier 1).

 3. Long-running workflows where steps are separated by hours or days
 require the agent to issue a fresh Credential Token for each step
 claim. This is intentional - the agent's authority must be re-
 verified at each step, not just at envelope creation time.

 4. If an agent's delegation chain expires between envelope approval
 and step execution, the agent MUST renew its delegation (Section 7.4.3)
 before claiming any remaining steps. The Approval Envelope itself
 remains valid - only the execution credential needs renewal.

 5. An agent MUST NOT pre-issue step-claim Credential Tokens for all
 steps at envelope approval time. Tokens MUST be issued at execution
 time so that revocation checks (Section 7.3 Step 7) are performed against
 the current Registry state.

### 7.5. Token Exchange for MCP

#### 7.5.1. Overview

 An AIP agent MAY exchange its Credential Token for a scoped access
 token targeting a specific MCP server or OAuth-protected resource.
 The exchange is performed at the Registry's token endpoint
 (Section 15.5).

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

 Normative requirements:

 1. `grant_type` MUST be
    `urn:ietf:params:oauth:grant-type:token-exchange`.
 2. `subject_token` MUST be a valid AIP Credential Token.
 3. `subject_token_type` MUST be
    `urn:ietf:params:oauth:token-type:jwt`.
 4. `resource` MUST be present per RFC 8707 [RFC8707], identifying
    the target resource server.
 5. `scope` MUST use AIP scope URIs from the `urn:aip:scope:`
    namespace (Section 15.6). The requested scopes MUST be a subset
    of the Credential Token's `aip_scope`.
 6. DPoP proof [RFC9449] MUST be included, binding the exchange to
    the agent's key material.

#### 7.5.3. Exchange Validation

 The Registry (as OAuth AS) MUST:

 1. Validate the `subject_token` using the full 12-step algorithm
    (Section 7.3).
 2. Verify the DPoP proof binds to the agent's public key.
 3. Verify the requested `scope` is a subset of the
    `subject_token`'s `aip_scope` (attenuation only, never
    expansion).
 4. Verify the `resource` is a registered MCP server or resource.
    Fail: `invalid_target`.
 5. Issue an access token with:
    - `aud` set to the `resource` URI
    - `scope` set to the granted scopes
    - `sub` set to the agent's AID
    - `act.sub` set to the root principal's DID (actor chain per
      RFC 8693 §4.1)
    - TTL ≤ the remaining TTL of the `subject_token`
 6. The access token MUST be a JWT per RFC 9068 [RFC9068].

#### 7.5.4. Exchange Response

 EXAMPLE (informative):

```json
 {
   "access_token": "<JWT>",
   "token_type": "DPoP",
   "expires_in": 300,
   "scope": "urn:aip:scope:email.read urn:aip:scope:calendar.read",
   "issued_token_type": "urn:ietf:params:oauth:token-type:access_token"
 }
```

---

## 8. Delegation

### 8.1. Delegation Chain

 Every Credential Token MUST include a verifiable Principal Chain
 linking the acting agent to its root principal via the `aip_chain`
 array. The root principal MUST be a human or organisational entity
 identified by a W3C DID that does NOT use the `did:aip` method.

 The maximum delegation depth is 10 (hard maximum). The default
 `max_delegation_depth` MUST NOT exceed 3.

### 8.2. Capability Scope Rules

 Rules D-1 through D-5 are defined in Section 4.4.

 **Scope Inheritance Rule:** For each scope `s` granted to a child
 agent, `s` MUST be present in the parent's Capability Manifest AND
 all constraint values for `s` in the child's manifest MUST be ≤ the
 corresponding values in the parent's manifest.

 Implementations MUST enforce this rule at delegation time. Relying
 parties MUST independently verify this rule during validation at
 Step 9c.

### 8.3. Delegation Validation

 Ancestor Manifest Fetch Limits: implementations MUST NOT fetch more
 ancestor manifests than the `max_delegation_depth` value of the
 chain's root token (defaulting to 3). Ancestor manifests MAY be
 cached for a maximum of 60 seconds. If an ancestor manifest is
 unavailable, the Relying Party MUST return `manifest_invalid`.

---

## 9. Revocation

### 9.1. Revocation Object

 Revocation is performed by submitting a signed Revocation Object to
 `POST /v1/revocations`. The schema is defined in Section 4.2.6.

 **full_revoke** - Permanently revokes the AID.

 **scope_revoke** - Removes specific scopes from the Capability
 Manifest. Does NOT invalidate outstanding Credential Tokens. Effect is
 bounded by token TTLs. For immediate scope removal, issuers SHOULD
 use `full_revoke` and re-register.

 **delegation_revoke** - Invalidates delegation chains rooted at the
 target. Child agents lose authority; the target AID remains valid for
 direct principal interactions.

 **principal_revoke** - Issued by the root principal to revoke their
 entire authorisation of the target agent. Equivalent to `full_revoke`
 plus child propagation.

### 9.2. Certificate Revocation List (CRL)

 The Registry MUST expose a CRL at `GET /v1/crl`. The CRL MUST be
 updated within 15 minutes of a new Revocation Object being accepted.
 The CRL endpoint MUST be served from a CDN or distributed
 infrastructure.

### 9.3. Revocation Checking

 **Tier 1 — Bounded-staleness (threat-model declaration).**
 TTL ≤ 3600s. Validate against CRL at issuance time. CRL MUST be
 refreshed every 15 minutes.

 **Tier 2 — Real-time revocation (threat-model declaration).**
 Scopes: `transactions.*`, `communicate.*`, `filesystem.execute`,
 `spawn_agents.create`, `spawn_agents.manage`. TTL ≤ 300s. Real-time
 Registry check on EVERY request. MUST NOT cache revocation status.
 DPoP [RFC9449] MUST be verified. If Registry unreachable: MUST deny
 and return `registry_unavailable`.

 **Tier 3 — Enterprise / regulated (threat-model declaration).**
 MUST use mTLS. MUST support OCSP per [RFC6960]. Tier 3 supplements,
 not replaces, Tier 2.

 **Child Agent Propagation:** When the Registry processes a Revocation
 Object with `propagate_to_children: true`, the Registry MUST use its
 parent-child index (populated at registration time from `delegated_by`
 fields) to recursively revoke descendants within 15 seconds.

 Registries supporting RPNP (Section 9.4) MUST deliver revocation
 events to subscribers within 5 seconds of processing the Revocation
 Object.

 Replica Registries MUST synchronise within 45 seconds. Combined end-
 to-end propagation MUST NOT exceed 60 seconds.

 **Approval Envelope revocation interaction:** When an agent AID is
 revoked, the Registry MUST also transition all of that agent's
 Approval Envelopes in `pending_approval`, `approved`, or `executing`
 status to `failed`. Unclaimed steps for that actor MUST be marked
 `failed`. In-progress claims (status `claimed`) MUST be treated as
 failed; the Registry MUST initiate compensation if applicable.

### 9.4. Registry Push Notification Protocol (RPNP)

#### 9.4.1. Overview

 RPNP is an OPTIONAL Registry capability. When implemented:

 - Registry MUST deliver push events within 5 seconds of the
   triggering state change.
 - Push payloads MUST be signed by the Registry's administrative key.
 - Subscriber authentication MUST be verified at subscription time.

 Relying Parties that subscribe to RPNP receive push notifications
 for revocation events. For subscribing RPs, the effective revocation
 window is the RPNP delivery latency (at most 5 seconds) rather than
 the CRL refresh interval. Non-subscribing RPs continue to use CRL
 as specified above. RPNP does not replace CRL; it supplements it.

#### 9.4.2. Subscription

 A Relying Party subscribes by calling `POST /v1/subscriptions`
 (Section 15.8):

 | Field | Type | Required | Constraints |
 |---|---|---|---|
 | `subscriber_did` | string | REQUIRED | DID of the subscribing RP; MUST be `did:web` or `did:aip` |
 | `event_types` | array | REQUIRED | One or more of: `full_revoke`, `scope_revoke`, `delegation_revoke`, `engagement_participant_removed`, `engagement_gate_approved`, `engagement_terminated` |
 | `scope_filter` | string | REQUIRED | One of: `"aid"`, `"principal"`, `"all"` |
 | `targets` | array | CONDITIONAL | REQUIRED when `scope_filter` is `"aid"` or `"principal"` |
 | `webhook_uri` | string | REQUIRED | HTTPS URI; the RP's event receiver endpoint |
 | `hmac_secret_hash` | string | REQUIRED | SHA-256 hash of the shared HMAC secret (hex-encoded) |
 | `subscription_expires_at` | string | REQUIRED | ISO 8601 UTC; max 90 days from creation |

 The subscription request MUST be authenticated via DPoP proof
 binding `subscriber_did` to the request. The Registry MUST reject
 unsigned subscription requests with `subscription_auth_required`.

#### 9.4.3. Push Event Payload

 Push events are delivered as HTTP POST requests to the subscriber's
 `webhook_uri`. The request body is a compact-serialised JWT signed
 by the Registry's administrative key:

 JWT Header:

 | Field | Value |
 |-------|-------|
 | `typ` | `"AIP-RPNP+JWT"` |
 | `alg` | `"EdDSA"` |
 | `kid` | Registry AID key ID |

 JWT Payload:

 | Field | Type | Description |
 |-------|------|-------------|
 | `iss` | string | Registry AID |
 | `sub` | string | Affected AID or engagement ID |
 | `iat` | integer | Unix timestamp |
 | `jti` | string | UUID v4; unique event ID |
 | `event_type` | string | One of the subscribed event types |
 | `event_data` | object | Event-specific data |

 The request MUST include an `X-AIP-Signature` header containing
 `HMAC-SHA256(shared_secret, body)`. The subscriber MUST verify both
 the JWT signature (Registry key) and the HMAC (shared secret).

#### 9.4.4. Delivery Guarantees

 1. The Registry MUST deliver push events within 5 seconds of the
    triggering state change for all active subscribers.
 2. On delivery failure (non-2xx response or timeout), the Registry
    MUST retry with exponential backoff: 1s, 2s, 4s (3 attempts
    minimum).
 3. After 3 consecutive failures, the Registry MUST mark the
    subscription as `degraded` and MAY stop delivery attempts. The
    subscriber falls back to CRL.
 4. Subscribers MUST reject duplicate `jti` values within a
    60-second sliding window.

---

## 10. Principal Chain

 The `principal.id` field MUST be byte-for-byte identical in every
 Principal Token in the `aip_chain` array. Relying Parties MUST verify
 this. An intermediate agent MUST NOT change it, substitute its own
 AID, or modify the original principal DID in any way.

 Every element in `aip_chain` is a compact-serialised JWT whose
 payload conforms to the Principal Token schema (Section 4.2.4). Elements are
 ordered root-to-leaf. The maximum `aip_chain` length is 11.
 Implementations MUST reject tokens with `aip_chain` length
 exceeding 11.

 Cryptographic non-repudiation: Every Credential Token carries a
 delegation chain in which each link is signed by the delegating
 party's private key. Because `principal.id` is byte-identical across
 all chain elements and is bound to the signing key, every agent
 action is cryptographically attributable to the human or
 organisational principal that authorised it. This satisfies the
 non-repudiation requirement of [SP-800-63-4] Section 11.

---

## 11. Reputation and Endorsements

### 11.1. Endorsement Object

 Any Relying Party or agent MAY submit a signed Endorsement Object to
 the Registry after a completed interaction. The schema is in Section 4.2.7.

 The Registry MUST verify every submitted Endorsement Object signature.
 Only `success` and `partial` outcomes increment `endorsement_count`.
 `failure` increments `incident_count`.

 Completed Approval Envelope steps SHOULD generate Endorsement Objects.
 When an Approval Envelope reaches `completed` status, the orchestrator
 SHOULD submit an Endorsement Object for each agent that executed a
 step successfully.

### 11.2. Reputation Scoring

 The Registry MUST expose reputation data for every registered AID at
 `GET /v1/agents/{aid}/reputation`. Required fields: `registration_date`,
 `task_count`, `successful_task_count`, `endorsement_count`,
 `incident_count`, `revocation_history`, `last_active`.

 The Registry MAY expose a reference advisory score labelled
 `advisory_only: true`. Relying Parties MUST NOT treat it as
 normative. AIP standardises reputation inputs, not the scoring formula.

 Reputation Non-Transferability: Reputation is bound to a specific
 AID. Implementations MUST NOT transfer reputation from revoked to new
 AIDs. Endorsements from AIDs with current `full_revoke` or
 `principal_revoke` status MUST NOT be weighted.

---

## 12. Lifecycle States

 An AID has exactly two lifecycle states: `active` and `revoked`.
 AIP does not define an `inactive` status; the Dead Man's Switch
 mechanism (Section 17.8) uses `full_revoke`.

 An AID MUST remain valid until explicitly revoked. Revoked AIDs MUST
 NOT be reused. Key rotation preserves the AID but changes the active
 key. Outstanding tokens signed under the previous key remain valid
 until their `exp`.

 Ephemeral agents MUST have a non-null `task_id`. They MUST be
 explicitly revoked on task completion. The Registry SHOULD auto-revoke
 ephemeral agents when their stored `expires_at` passes.

---

## 13. Error Handling

### 13.1. Error Response Format

   EXAMPLE (informative):

```json
 {
 "error": "<error_code>",
 "error_description": "<human-readable description>",
 "error_uri": "https://provai.dev/errors/<error_code>"
 }
```

 Implementations MUST use exact string values for `error`.
 Implementations MUST NOT return HTTP 200 for error conditions.

### 13.2. Standard Error Codes

 | Error Code | HTTP | Description |
 |-----------------------------------|------|--------------------------------------|
 | `invalid_token` | 401 | Token malformed, invalid signature, or invalid claims |
 | `token_expired` | 401 | Token `exp` is in the past |
 | `token_replayed` | 401 | Token `jti` seen before within validity window |
 | `dpop_proof_required` | 401 | DPoP proof absent or invalid |
 | `delegation_chain_refresh_required` | 401 | Principal Token in chain has expired; agent must re-establish delegation |
 | `agent_revoked` | 403 | The AID has been revoked |
 | `insufficient_scope` | 403 | Operation not within granted scopes |
 | `invalid_delegation_depth` | 403 | `delegation_depth` mismatch or exceeds `max_delegation_depth` |
 | `chain_token_expired` | 403 | Principal Token in `aip_chain` expired |
 | `delegation_chain_invalid` | 403 | Structural error in delegation chain |
 | `manifest_invalid` | 403 | Capability Manifest signature failed or unavailable |
 | `manifest_expired` | 403 | Capability Manifest `expires_at` passed |
 | `approval_envelope_invalid` | 400 | Approval Envelope malformed, circular dependencies, or hash mismatch |
 | `approval_envelope_expired` | 403 | `approval_window_expires_at` has passed |
 | `approval_not_found` | 404 | Approval Envelope ID not found |
 | `approval_step_prerequisites_unmet` | 403 | `triggered_by` step not yet completed |
 | `approval_step_already_claimed` | 409 | Step already claimed by another actor |
 | `approval_step_action_mismatch` | 403 | Presented `action_parameters` hash does not match stored `action_hash` |
 | `approval_step_invalid` | 403 | Step Execution Token verification against Registry failed |
 | `grant_request_expired` | 400 | AIP-GRANT `request_expires_at` passed |
 | `grant_request_replayed` | 400 | AIP-GRANT `grant_request_id` seen before |
 | `grant_request_invalid` | 400 | GrantRequest malformed or signature failed |
 | `grant_rejected_by_principal` | 403 | Principal declined the grant |
 | `grant_nonce_mismatch` | 400 | GrantResponse nonce does not match |
 | `unknown_aid` | 404 | AID not registered in any accessible Registry |
 | `registry_unavailable` | 503 | Registry could not be reached |
 | `rate_limit_exceeded` | 429 | Rate limit for this operation exceeded; see Section 14 |
 | `revocation_stale` | 403 | Tier 2 operation with cached revocation status |
 | `dpop_required` | 401 | Tier 2 operation without DPoP proof |
 | `mtls_required` | 403 | Tier 3 operation without mTLS |
 | `invalid_scope` | 400 | Token contains retired bare `spawn_agents` scope |
 | `principal_did_method_forbidden` | 403 | Principal uses `did:key` for Tier 2 scope |
 | `identity_proofing_insufficient` | 403 | G3 identity proofing below requested `acr_values` |
 | `grant_not_found` | 404 | G1 `grant_id` not found or expired |
 | `grant_deployer_mismatch` | 403 | G1 `grant_id` does not match deployer |
 | `pkce_required` | 400 | G3 authorization request missing PKCE |
 | `registry_untrusted` | 403 | Registry does not match principal DID-Document-declared Registry |
 | `overlay_exceeds_manifest` | 400 | Overlay violates CO-1 attenuation rule |
 | `overlay_issuer_invalid` | 400 | Overlay issuer uses `did:key` |
 | `overlay_version_conflict` | 409 | Overlay version not strictly increasing |
 | `overlay_signature_invalid` | 400 | Overlay signature verification failure |
 | `engagement_terminated` | 403 | Engagement has been terminated or completed |
 | `engagement_suspended` | 403 | Engagement is currently suspended |
 | `engagement_participant_removed` | 403 | Agent removed from engagement |
 | `engagement_gate_pending` | 403 | Required approval gate not yet approved |
 | `engagement_not_found` | 404 | Engagement ID not found |
 | `engagement_countersign_required` | 400 | Missing required countersignature |
 | `change_log_immutable` | 400 | Attempt to modify change log entry |
 | `change_log_sequence_invalid` | 400 | Out-of-sequence change log append |
 | `subscription_auth_required` | 401 | RPNP subscription without DPoP |
 | `invalid_webhook_uri` | 400 | Webhook URI not HTTPS |
 | `subscription_limit_exceeded` | 429 | RPNP subscription limit reached |
 | `invalid_target` | 400 | Token exchange resource not registered |

### 13.3. Error Detail Types

 For `registry_unavailable` (503): SHOULD include `Retry-After` per
 [RFC9110].

 For `rate_limit_exceeded` (429): MUST include `Retry-After` per
 [RFC6585] Section 4 and rate limit headers per Section 14.1.

 For `delegation_chain_refresh_required` (401): the response SHOULD
 include an `error_description` indicating which delegation depth's
 Principal Token has expired, to help the agent identify which
 delegation level to renew.

---

## 14. Rate Limiting and Abuse Prevention

 Rate limiting protects the Registry from denial-of-service attacks,
 registration floods, and validation-driven key lookup storms. A
 public Registry that permits unrestricted write operations or
 validation-driven lookups is exploitable in ways that undermine the
 security guarantees of the entire ecosystem.

### 14.1. Rate Limit Response Format

 When rate limiting is applied, the Registry MUST return HTTP 429 with
 the following headers:

 | Header | Required | Description |
 |--------------------------|----------|-------------------------------------|
 | `Retry-After` | MUST | Seconds until the client may retry, or a HTTP-date per [RFC9110] |
 | `X-RateLimit-Limit` | SHOULD | The request limit for this window |
 | `X-RateLimit-Remaining` | SHOULD | Remaining requests in this window |
 | `X-RateLimit-Reset` | SHOULD | Unix timestamp when the window resets |
 | `X-RateLimit-Policy` | MAY | Human-readable description of the applicable policy |

 The response body MUST conform to the error response format (Section 13.1)
 with `error: "rate_limit_exceeded"` and a human-readable
 `error_description` identifying the rate-limited operation and the
 applicable window.

### 14.2. Per-Endpoint Rate Limit Categories

 The Registry MUST implement separate rate limit buckets for each of
 the following operation categories. The limits below are RECOMMENDED
 minimums; Registry operators MAY enforce stricter limits based on
 observed traffic patterns and threat models.

 **Category R1 - Registration writes** (`POST /v1/agents`):

 - Per-principal-DID: RECOMMENDED limit of 20 agent registrations per
 hour. This prevents a single compromised principal key from flooding
 the Registry with rogue agent registrations.
 - Per-source-IP: RECOMMENDED limit of 50 registrations per hour
 across all principals. This prevents registration floods from a
 single network origin, regardless of the principal DID presented.
 - Global: Registries SHOULD implement a global registration rate limit
 appropriate to their infrastructure capacity.

 **Category R2 - Key rotation writes** (`PUT /v1/agents/{aid}`):

 - Per-AID: RECOMMENDED limit of 10 key rotations per 24-hour window.
 Legitimate key rotation is infrequent; high frequency suggests
 automated abuse or a compromised orchestrator.

 **Category R3 - Revocation writes** (`POST /v1/revocations`):

 - Per-issuer-DID: RECOMMENDED limit of 100 revocations per hour.
 Higher limits are legitimate for enterprise orchestrators managing
 large ephemeral agent fleets. Registries MAY issue higher limits to
 verified principals.
 - Registries MUST apply special throttling to `propagate_to_children:
 true` revocations that would cascade to more than 100 descendants,
 as these trigger recursive Registry writes. A revocation that would
 cascade to more than 100 descendants SHOULD be queued and processed
 asynchronously, with the Registry returning HTTP 202 (Accepted) and
 a status URI rather than blocking on the full cascade.

 **Category R4 - Validation-driven key reads**
 (`GET /v1/agents/{aid}/public-key/{key-id}`,
 `GET /v1/agents/{aid}/revocation`):

 - Per-requesting-IP: RECOMMENDED limit of 1,000 requests per minute
 across all AIDs. Validation-driven reads are triggered by token
 verification; legitimate Relying Parties have bounded lookup rates.
 - Per-AID: RECOMMENDED limit of 200 reads per minute. A single AID
 being looked up 200 times per minute from varied IPs is likely the
 subject of a coordinated replay attack; rate limiting per AID
 allows the Registry to throttle targeted abuse.
 - Registries SHOULD offer API key authentication for Relying Parties
 whose legitimate validation rates exceed these limits (e.g.,
 high-traffic APIs that verify thousands of agent tokens per minute).

 **Category R5 - CRL reads** (`GET /v1/crl`):

 - The CRL endpoint MUST be served from a CDN or distributed
 infrastructure (Section 9.2). Direct-origin CRL reads SHOULD be rate
 limited per IP to 100 requests per minute to protect against CDN
 bypass attacks. CDN-served responses have no normative rate limit
 constraint.

 **Category R6 - Endorsement writes** (`POST /v1/endorsements`):

 - Per-from-AID: RECOMMENDED limit of 500 endorsements per hour. This
 prevents an AID from artificially inflating another AID's
 `endorsement_count` through automated submission.
 - Self-endorsement (`from_aid` == `to_aid`) MUST be rejected at the
 application layer before rate limits are checked.

 **Category R7 - Approval Envelope writes and step claims**
 (`POST /v1/approvals`, `POST /v1/approvals/{id}/steps/{n}/claim`):

 - Per-principal-DID: RECOMMENDED limit of 100 Approval Envelopes per
 hour. Approval Envelopes represent human-authorised workflows;
 high frequency is anomalous.
 - Per-actor-AID per envelope: step claims are naturally rate-limited
 by the sequential structure of the workflow. No additional rate
 limit is required for step claims within a single envelope.

### 14.3. Registration Abuse Prevention

 Beyond rate limiting, the Registry MUST implement the following
 structural checks to prevent registration abuse:

 **AID uniqueness enforcement:** The Registry MUST check AID uniqueness
 under a distributed lock or equivalent atomic mechanism. Two
 simultaneous registration requests for the same AID MUST result in
 exactly one succeeding and one receiving an appropriate error
 (Section 5.2 Check 4).

 **Principal delegation chain verification at registration:** The
 Registry MUST verify that the `principal_token` in the Registration
 Envelope was issued by a DID that is resolvable and has not been
 subjected to a `full_revoke` or `principal_revoke` RevocationObject
 in the Registry. A revoked principal MUST NOT be permitted to
 register new agents.

 **Registration flood from shared principals:** If a single
 principal DID registers more than 1,000 agents (across all time),
 the Registry SHOULD require the deployer to present proof of
 legitimate use (out-of-band, implementation-specific). This is a
 SHOULD, not a MUST, because legitimate orchestrator-heavy deployments
 may reach this threshold.

 **Public Registry challenge for unauthenticated deployers:** Registries
 that permit registration without deployer authentication (open
 Registries) SHOULD implement a lightweight proof-of-work or CAPTCHA
 mechanism for registrations where `deployer_did` is absent from the
 principal_token context.

### 14.4. Validation-Driven Lookup Limits

 Key lookup amplification occurs when an adversary presents many tokens
 with distinct `kid` values, forcing the Registry to perform a lookup
 for each. Mitigations:

 **Key version caching:** Relying Parties MUST cache resolved public
 keys for a given `kid` for up to 300 seconds (Section 6.1). Repeated
 validation of tokens with the same `kid` SHOULD NOT trigger repeated
 Registry lookups within the cache window.

 **Historical key depth limit:** Registries MAY reject requests for
 key versions older than a configurable retention window (RECOMMENDED:
 90 days past the key rotation date, since all tokens issued with that
 key must have expired within 3600s of rotation). This prevents
 adversaries from constructing tokens with ancient, never-rotated keys
 to force deep history lookups.

 **`kid` validation at the Relying Party:** Relying Parties MUST
 validate that the `kid` in the token header matches the pattern
 `^did:aip:[a-z][a-z0-9]*(-[a-z0-9]+)*:[0-9a-f]{32}#key-[1-9][0-9]*$`
 before performing any Registry lookup (Validation Step 3). Malformed
 `kid` values MUST be rejected with `invalid_token` without making a
 Registry call.

### 14.5. Approval Envelope Rate Limits

 Approval Envelope operations require specific abuse prevention because
 they involve asynchronous principal interactions and potential cascade
 effects.

 **Envelope submission rate:** Per Section 14.2, Category R7.

 **Pending envelope limit:** A Registry SHOULD enforce a maximum of
 1,000 `pending_approval` envelopes per principal DID at any time.
 Envelopes that expire transition to `expired` and free this quota.

 **Step claim timeout:** Step claims that are not completed or failed
 within 600 seconds MUST be automatically failed by the Registry
 (Section 4.6.8). This prevents a claimed step from blocking the workflow
 indefinitely due to a crashed or unresponsive agent.

 **Compensation cascade depth:** Compensation step execution is not
 rate-limited separately - it is a recovery mechanism whose scope is
 bounded by the number of forward steps (maximum 20). No additional
 rate limit is required for compensation.

### 14.6. Graduated Backoff Requirements

 Clients that receive HTTP 429 responses MUST implement exponential
 backoff with jitter. The minimum retry interval is the value in the
 `Retry-After` header. Clients MUST NOT retry before `Retry-After`
 expires.

 Implementations SHOULD use the following backoff formula:

```
 BACKOFF_BASE = 1         ; fixed exponential base, in seconds
 MAX_DELAY    = 3600      ; hard ceiling, in seconds

 computed_delay = min(BACKOFF_BASE * 2^attempt, MAX_DELAY)
 jitter         = random(0, BACKOFF_BASE)
 retry_delay    = max(computed_delay + jitter, Retry-After)
```

 The `Retry-After` value from the 429 response acts as a mandatory
 minimum: clients MUST NOT retry before `Retry-After` seconds have
 elapsed, even if `computed_delay + jitter` is smaller. When no
 `Retry-After` header is present, clients MUST treat it as 0 and
 rely solely on the exponential formula.

 Clients that continue to receive HTTP 429 after 5 exponential backoff
 attempts MUST cease retrying for a minimum of 1 hour and SHOULD alert
 an operator. Persistent rate limiting at this scale indicates either
 a misconfigured client or a sustained attack pattern.

 Registries MUST track clients that consistently exceed rate limits and
 MAY temporarily block their source IPs or API keys after sustained
 abuse. Blocking decisions are implementation-specific and are not
 normatively constrained by this specification.

---

## 15. Registry Interface

### 15.1. Required Endpoints

 A conformant AIP Registry MUST implement the following HTTP endpoints:

 | Method | Path | Description |
 |--------|------|-------------|
 | `POST` | `/v1/agents` | Register a new AID (Registration Envelope) |
 | `GET` | `/v1/agents/{aid}` | Retrieve Agent Identity or DID Document |
 | `PUT` | `/v1/agents/{aid}` | Key rotation only |
 | `GET` | `/v1/agents/{aid}/public-key` | Current public key (JWK) |
 | `GET` | `/v1/agents/{aid}/public-key/{key-id}` | Historical key version |
 | `GET` | `/v1/agents/{aid}/capabilities` | Current Capability Manifest |
 | `PUT` | `/v1/agents/{aid}/capabilities` | Replace Capability Manifest |
 | `GET` | `/v1/agents/{aid}/revocation` | Revocation status |
 | `POST` | `/v1/revocations` | Submit RevocationObject |
 | `GET` | `/v1/crl` | Certificate Revocation List |
 | `GET` | `/v1/agents/{aid}/reputation` | Reputation data |
 | `POST` | `/v1/endorsements` | Submit Endorsement Object |
 | `POST` | `/v1/grants` | Submit G1 grant (Section 4.5) |
 | `GET` | `/v1/grants/{grant_id}` | Retrieve grant status |
 | `PUT` | `/v1/agents/{aid}/overlays` | Submit Capability Overlay (Section 4.7) |
 | `GET` | `/v1/agents/{aid}/overlays` | Retrieve current overlay |
 | `POST` | `/v1/engagements` | Create Engagement Object (Section 4.8) |
 | `GET` | `/v1/engagements/{id}` | Retrieve Engagement Object |
 | `PUT` | `/v1/engagements/{id}` | Update Engagement (append change log) |
 | `POST` | `/v1/subscriptions` | Create RPNP subscription (Section 9.4) |
 | `DELETE`| `/v1/subscriptions/{id}` | Cancel RPNP subscription |
 | `GET` | `/v1/scopes` | Scope Map registry (Section 15.6) |
 | `POST` | `/v1/oauth/authorize` | G3 authorization endpoint (Section 15.5) |
 | `POST` | `/v1/oauth/token` | G3 token endpoint / token exchange (Section 15.5) |
 | `GET` | `/.well-known/oauth-authorization-server` | AS Metadata [RFC8414] |

### 15.2. AID URL Encoding

 In all path parameters, the `did:aip:` prefix and colons MUST be
 percent-encoded per [RFC3986]:

   EXAMPLE (informative):

```
 did:aip:personal:9f3a1c82b4e6d7f0a2b5c8e1d4f7a0b3
 → /v1/agents/did%3Aaip%3Apersonal%3A9f3a1c82b4e6d7f0a2b5c8e1d4f7a0b3
```

### 15.3. Response Format

 All Registry responses MUST use `Content-Type: application/json`.
 All timestamps MUST be in ISO 8601 UTC format.

### 15.4. Approval Envelope Endpoints

 A conformant AIP Registry MUST implement the following additional
 endpoints for Approval Envelopes:

 | Method | Path | Description |
 |--------|------|-------------|
 | `POST` | `/v1/approvals` | Submit Approval Envelope for approval |
 | `GET` | `/v1/approvals/{id}` | Retrieve Approval Envelope with step statuses |
 | `POST` | `/v1/approvals/{id}/approve` | Principal approves (wallet call; sets `principal_signature`) |
 | `POST` | `/v1/approvals/{id}/reject` | Principal rejects |
 | `POST` | `/v1/approvals/{id}/steps/{n}/claim` | Claim step for execution; returns Step Execution Token |
 | `POST` | `/v1/approvals/{id}/steps/{n}/complete` | Mark step completed |
 | `POST` | `/v1/approvals/{id}/steps/{n}/fail` | Mark step failed; triggers compensation |
 | `GET` | `/v1/approvals/{id}/steps/{n}` | Get step status (used by Relying Parties for Step Execution Token verification) |
 | `POST` | `/v1/approvals/{id}/compensation-steps/{n}/claim` | Claim compensation step |
 | `POST` | `/v1/approvals/{id}/compensation-steps/{n}/complete` | Mark compensation step completed |
 | `POST` | `/v1/approvals/{id}/compensation-steps/{n}/fail` | Mark compensation step failed |

 **`POST /v1/approvals` validation:** The Registry MUST perform all
 checks defined in Section 4.6.10 before accepting an Approval Envelope. The
 Registry MUST return HTTP 201 with the stored envelope (including the
 Registry-assigned `status: "pending_approval"`) on success.

 **`POST /v1/approvals/{id}/approve` flow:** This endpoint is called
 by the Principal Wallet after the principal completes the signing
 ceremony. The request body MUST contain the `principal_signature`
 (base64url EdDSA signature of the envelope's `approval_id`, signed
 by the `principal_id`'s private key). The Registry MUST verify this
 signature before transitioning the envelope to `approved`.

 **Atomicity requirement for step claim:** The Registry MUST implement
 step-claim operations atomically (e.g., using optimistic locking or
 a distributed lock) to prevent two actors from claiming the same step
 simultaneously. Only one claim MUST succeed; the other MUST receive
 `approval_step_already_claimed`.

 **Step Execution Token format:** The Step Execution Token returned by
 `POST .../steps/{n}/claim` is a JWT signed by the Registry's
 administrative key with the claims described in Section 4.6.8. Its TTL
 MUST comply with normal TTL rules (Section 7.2) for the scopes involved.

### 15.5. OAuth 2.1 Authorization Server

 A conformant AIP Registry supporting G3 grants MUST implement an
 OAuth 2.1 Authorization Server [RFC6749] with the following
 requirements:

 1. The authorization endpoint MUST be published in the Registry's
    well-known configuration at
    `/.well-known/oauth-authorization-server` per [RFC8414].
 2. PKCE [RFC7636] with `code_challenge_method: "S256"` is REQUIRED
    for all authorization requests.
 3. The `scope` parameter MUST use AIP scope URIs from the
    `urn:aip:scope:` namespace (Section 15.6).
 4. The token endpoint MUST return a signed Principal Token (not a
    standard OAuth access token) as the `access_token` value, with
    `token_type: "AIP+JWT"`.
 5. The token response MUST include `acr` and `amr` claims reflecting
    the authentication performed.
 6. The authorization server MUST support the `acr_values` parameter
    to declare minimum identity-proofing requirements.
 7. DPoP [RFC9449] MUST be supported on the token endpoint.

 The token endpoint also serves RFC 8693 [RFC8693] token exchange
 requests (Section 7.5).

 **Well-known metadata additions:** The `/.well-known/aip-registry`
 response MUST also include:

 | Field | Type | Description |
 |-------|------|-------------|
 | `grant_tiers_supported` | array | Supported grant tiers: `["G1", "G2", "G3"]` |
 | `acr_values_supported` | array | Supported `acr` values |
 | `amr_values_supported` | array | Supported `amr` values |
 | `oauth_authorization_server` | string | URI of the OAuth AS metadata document (present only if G3 supported) |
 | `identity_proofing_required_for_tier2` | boolean | Whether this Registry requires G3 for Tier 2 operations |

### 15.6. Scope Map

 All AIP capability scopes MUST be representable as URIs in the
 `urn:aip:scope:` namespace:

```
 scope_string → urn:aip:scope:<scope_string>
```

 Examples: `email.read` → `urn:aip:scope:email.read`,
 `spawn_agents.create` → `urn:aip:scope:spawn_agents.create`.

 When used in OAuth `scope` parameters, the URI form MUST be used.
 Within AIP Credential Tokens (`aip_scope` array), the short string
 form remains canonical.

 A conformant AIP Registry MUST implement `GET /v1/scopes` returning
 a JSON object mapping scope strings to metadata:

 | Field | Type | Description |
 |-------|------|-------------|
 | `uri` | string | Full `urn:aip:scope:` URI |
 | `description` | string | Human-readable description |
 | `tier` | integer | Tier classification (1, 2, or 3) |
 | `destructive` | boolean | Whether the scope requires additional confirmation per Section 4.5.3 |
 | `constraint_schema` | object/null | JSON Schema fragment for scope-specific constraints |

### 15.7. Engagement Endpoints

 A conformant AIP Registry supporting Engagement Objects
 (Section 4.8) MUST implement:

 | Method | Path | Description |
 |--------|------|-------------|
 | `POST` | `/v1/engagements` | Create Engagement Object |
 | `GET` | `/v1/engagements/{id}` | Retrieve Engagement Object |
 | `PUT` | `/v1/engagements/{id}` | Update Engagement (append change log entry) |

 **Create validation:** The Registry MUST verify the initiator's
 DID signature, validate that all referenced participant AIDs exist
 and are not revoked, and assign `status: "active"` with
 `seq_number: 1`.

 **Update validation:** The Registry MUST verify the submitter is an
 active participant, the change log entry's `seq_number` is exactly
 `current_max + 1`, and the entry signature is valid. The Registry
 MUST reject modifications to existing entries with
 `change_log_immutable`.

### 15.8. RPNP Subscription Endpoints

 A conformant AIP Registry supporting RPNP (Section 9.4) MUST
 implement:

 | Method | Path | Description |
 |--------|------|-------------|
 | `POST` | `/v1/subscriptions` | Create RPNP subscription |
 | `GET` | `/v1/subscriptions/{id}` | Retrieve subscription status |
 | `DELETE` | `/v1/subscriptions/{id}` | Cancel subscription |

 Subscription creation MUST be authenticated via DPoP. The
 `webhook_uri` MUST use HTTPS. The Registry MUST reject non-HTTPS
 URIs with `invalid_webhook_uri`.

---

## 16. Versioning and Compatibility

 AIP follows Semantic Versioning. Before v1.0, MINOR versions MAY
 include breaking changes. v0.2 and v0.3 are partially compatible:
 validators SHOULD accept `aip_version: "0.2"` tokens with the
 following caveats:

 - `aip_version: "0.2"` tokens may contain the bare `spawn_agents`
   scope. Validators SHOULD treat this as `spawn_agents.create` for
   backward compatibility but MUST log a deprecation warning.
 - `aip_version: "0.2"` Registration Envelopes do not include
   `grant_tier`. Validators SHOULD treat absent `grant_tier` as
   `"G2"` during the transition period.
 - `aip_version: "0.2"` Principal Tokens do not include `acr`/`amr`
   claims. Validators MUST treat their absence as non-applicable.
 - Validators receiving `aip_version: "0.2"` from agents that should
   be on v0.3 SHOULD log a warning.
 - Step 6a (Registry Trust Anchoring) MAY be skipped for
   `aip_version: "0.2"` tokens.

 Breaking changes from v0.2:

 - `aip_version` is now `"0.3"` for conforming implementations.
 - `X-AIP-Version: 0.3` replaces `X-AIP-Version: 0.2`.
 - The bare `spawn_agents` scope is retired; use
   `spawn_agents.create` and `spawn_agents.manage` (Section 3).
 - Registration Envelopes MUST include `grant_tier` (Section 4.5).
 - Principal DID Documents for Tier 2 agents MUST include an
   `AIPRegistry` service entry (Section 6.2).
 - The `/.well-known/aip-registry` response MUST include
   `signature`, `registry_name`, and `endpoints` (Section 6.3.4).
 - §14.6 backoff formula corrected (Section 14.6).

 Implementations MUST NOT silently accept tokens from unsupported
 versions without logging a version warning.

### 16.1. Tier Conformance

 | Tier | Revocation | DPoP | mTLS | `grant_tier` | Principal DID |
 |------|------------|------|------|-------------|---------------|
 | 1 | CRL (15 min) | NOT REQUIRED | NOT REQUIRED | G1 or G2 | Any |
 | 2 | Real-time | REQUIRED | NOT REQUIRED | G2 or G3 | `did:web` or `did:aip` |
 | 3 | Real-time + OCSP | REQUIRED | REQUIRED | G3 | `did:web` or `did:aip` |

---

## 17. Security Considerations

### 17.1. Threat Model

 Assets: Agent private keys; Credential Tokens; Capability Manifests;
 Delegation Chains; Revocation Records; Principal Identity; Approval
 Envelopes.

 Threat actors: T1 (External Attacker), T2 (Compromised Agent),
 T3 (Malicious Sub-Agent), T4 (Rogue Registry), T5 (Insider Principal).

 Key threat scenarios and mitigations:

 **TS-1 (Bearer Token Theft):** DPoP (Section 17.3), short TTLs (Section 7.2), TLS.

 **TS-2 (Capability Escalation via Delegation):** Scope intersection
 rule (Section 8.2), independent verification at Step 9c.

 **TS-3 (Revocation Suppression):** Short TTLs; multiple channels;
 signed Revocation Objects.

 **TS-4 (Principal Impersonation):** Root Principal Token signed by
 principal key (Step 8d); `principal.id` consistency (Step 8i).

 **TS-5 (Token Replay):** `jti` UUID v4; (`iss`, `jti`) replay cache
 (Section 17.5); DPoP per-request binding.

 **TS-6 (Delegation Depth Exhaustion):** `max_delegation_depth` hard
 cap of 10; default of 3.

 **TS-7 (Registry Unavailability Attack):** Short TTLs; MUST NOT fall
 back to stale cache for Tier 2 (Section 9.3); rate limits (Section 14).

 **TS-8 (Root Principal Key Compromise):** Rotate principal DID key;
 issue `full_revoke` for all affected agents; re-register under new key.

 **TS-9 (Approval Envelope Manipulation):** `action_hash` binding (Section 4.6.7)
 prevents substitution of action parameters after principal approval.
 `creator_signature` prevents tampering with envelope structure. The
 Registry enforces step ordering atomically. See Section 17.9 for full
 Approval Envelope threat analysis.

 **TS-10 (Grant Ceremony Spoofing):** GrantRequest signature by deployer
 (Section 4.5.5); Principal Wallet-generated capability display from JSON (Section 4.5.3),
 not deployer-supplied text; nonce binding prevents replay.

 **TS-11 (Registration Flood):** Per-principal and per-IP registration
 rate limits (Section 14.3); principal revocation check at registration time.

 **TS-12 (Orchestrator Compromise Cascade).** A compromised
 orchestrator with `spawn_agents.create` capability uses its TTL
 window to register child agents before revocation propagates. Each
 child may itself hold `spawn_agents.create`, creating a
 self-replicating delegation tree. *Mitigation:*
 `spawn_agents.create` is Tier 2 (Section 3), requiring real-time
 revocation check, DPoP, and 300s max TTL. Child propagation via
 `propagate_to_children: true` (Section 9.3) revokes the entire
 subtree.

 **TS-13 (Capability Overlay Injection).** An attacker attempts to
 submit a forged Capability Overlay to the Registry, expanding an
 agent's effective permissions beyond the base Capability Manifest.
 *Mitigation:* Rule CO-1 (Section 4.7) enforces attenuation only —
 the Registry rejects any overlay that expands beyond the base
 manifest. Overlay signature verification against the issuer's DID
 key prevents forgery. The `issued_by` DID must be `did:web` or
 `did:aip` (not `did:key`), ensuring issuer identity is verifiable
 and rotatable.

 **TS-14 (Engagement State Tampering).** An attacker attempts to
 modify a completed change log entry in an Engagement Object to
 retroactively alter the participant roster or approval gate status.
 *Mitigation:* The change log is append-only with monotonic sequence
 numbers (Section 4.8). Each entry is independently signed by the
 actor's DID key. The Registry rejects modifications with
 `change_log_immutable`. Auditors can reconstruct and verify the
 full engagement history from the signed change log.

### 17.2. Cryptographic Requirements

 Mandatory-To-Implement (MTI):

 | Operation | Algorithm | Specification | Status |
 |------------------------|-----------------|---------------|--------|
 | Signing / Verification | Ed25519 (EdDSA) | [RFC8037] | MUST |
 | Hashing | SHA-256 | [FIPS-180-4] | MUST |
 | Key representation | JWK | [RFC7517] | MUST |
 | Key exchange (future) | X25519 | [RFC7748] | SHOULD |

 Optional suites: ES256 (ECDSA P-256) per [RFC7518] for WebAuthn
 compatibility; RS256 (RSA-PKCS1) per [RFC7518] for legacy enterprise
 only - MUST NOT be the sole supported algorithm; RSA keys MUST be at
 least 2048 bits.

 Prohibited: `none`, `HS256/384/512`, `RS512`, `MD5`, `SHA-1`.

 The `alg` header MUST be explicitly specified. Implementations MUST
 NOT infer algorithm from context. Unsupported `alg` MUST return
 `invalid_token`.

 AIP satisfies NIST SP 800-63-4 [SP-800-63-4] AAL2: (1) bound
 cryptographic authenticator (Ed25519 key registered in Registry);
 (2) DPoP cryptographic authentication protocol; (3) `htu` claim
 provides phishing resistance.

### 17.3. Proof-of-Possession (DPoP)

 Required for `transactions.*`, `communicate.*`, and
 `filesystem.execute`. DPoP proofs MUST always use `EdDSA` (Ed25519)
 regardless of the Credential Token's `alg`. Relying Parties MUST
 reject DPoP proofs with any `alg` other than `EdDSA`.

 **DPoP Proof Header:**

   EXAMPLE (informative):

```json
 {
 "typ": "dpop+jwt",
 "alg": "EdDSA",
 "jwk": {
 "kty": "OKP",
 "crv": "Ed25519",
 "x": "<base64url public key, no padding>",
 "kid": "<DID URL matching the Credential Token kid>"
 }
 }
```

 **DPoP Proof Payload:**

   EXAMPLE (informative):

```json
 {
 "jti": "<UUID v4 - unique per request>",
 "htm": "<HTTP method, uppercase>",
 "htu": "<scheme + host + path; no query or fragment>",
 "iat": "<Unix timestamp, within 30 seconds of server time>",
 "ath": "<BASE64URL(SHA-256(ASCII(header.payload.signature)))>"
 }
```

 The `ath` computation MUST exactly follow [RFC9449] Section 4.2: hash the
 full compact JWT string `header.payload.signature` as ASCII bytes,
 no whitespace, no scheme prefix.

 **Relying Party DPoP validation steps:** (1) Verify `DPoP` header
 present. (2) Verify `alg` is `EdDSA`. (3) Verify `jwk.kid` matches
 Credential Token `kid`; retrieve key from Registry. (4) Verify `htm`
 (case-sensitive uppercase). (5) Verify `htu` (no query or fragment).
 (6) Verify `iat` within 30 seconds. (7) Check DPoP `jti` replay cache
 keyed by (`kid`, `jti`). (8) Verify `ath`. (9) Verify signature.

 Fail: `dpop_proof_required` (HTTP 401).

 DPoP nonce support: Relying Parties SHOULD implement per [RFC9449] Section 8.
 Nonces SHOULD expire after 60 seconds.

### 17.4. Key Management

 Private keys MUST NOT be stored in plaintext on disk, transmitted in
 any protocol message, or included in logs. Private keys SHOULD be
 stored in HSM, secure enclave, or OS-level keychain.

 Key rotation MUST: generate new keypair; increment `version`; include
 `previous_key_signature` signed by retiring key (using canonical field
 order); submit to Registry; retain retiring key until outstanding
 tokens expire.

 On suspected key compromise: immediately revoke with
 `reason: "key_compromised"`; register new AID with new keypair;
 re-establish delegations.

### 17.5. Token Security

 All tokens MUST be transmitted over TLS 1.2 or higher (TLS 1.3
 RECOMMENDED). MUST NOT transmit over unencrypted HTTP.

 JTI replay cache: keyed by (`iss`, `jti`); window at least max TTL
 for served scopes; shared cache required for distributed deployments.

 Audience validation: MUST validate `aud` claim. Mismatch MUST return
 `invalid_token`.

 Token Binding Prohibition: MUST NOT bind Credential Tokens to TLS
 sessions. DPoP is the required binding mechanism.

### 17.6. Delegation Chain Security

 Default `max_delegation_depth` MUST NOT exceed 3. Hard cap of 10.
 Circular delegation MUST be detected and rejected.

 Ephemeral agents MUST have non-null `task_id`. Registry SHOULD auto-
 revoke via `full_revoke` when `expires_at` passes.

### 17.7. Registry Security

 All write operations MUST be authenticated. Revocation `issued_by`
 MUST be verified as in the target's delegation chain. Internally
 generated Revocation Objects (propagation, auto-revoke) MUST be
 signed by the Registry's administrative key, whose public key MUST
 be published in the Registry's well-known configuration.

 Registry read endpoints MUST target 99.9% uptime. CRL MUST be served
 from CDN. See Section 14 for rate limiting requirements.

 Multi-Registry: revocation MUST be submitted to the authoritative
 Registry. Replicas MUST sync within 45 seconds. Replicas that cannot
 meet this SLA MUST NOT serve revocation status for Tier 2 operations.

 Relying Parties MUST NOT trust the `aip_registry` claim in a
 Credential Token as the sole indicator of Registry authority. For
 Tier 2 operations, the authoritative Registry MUST be independently
 verified via the root principal's DID Document (Step 6a,
 Section 7.3). The `aip_registry` claim is a convenience for Tier 1
 Relying Parties and an early-exit optimisation; it is never
 authoritative.

### 17.8. Revocation Security

 Every Revocation Object MUST be signed. Unsigned or invalidly signed
 objects MUST be rejected.

 Dead Man's Switch (Optional): Registry MAY issue `full_revoke` with
 `reason: "other"` for agents that fail to submit a signed heartbeat
 within a configured window (RECOMMENDED: 24 hours). MUST be
 explicitly configured by the principal.

 Revocation timing attack: short sensitive-scope TTLs (max 300s) limit
 the exploitation window. Tier 2 real-time checks eliminate the CRL
 window. Registry SHOULD support webhook subscriptions for relying
 parties requiring immediate notification.

### 17.9. Approval Envelope Security

 **Action hash integrity (TS-9a):** The `action_hash` binds the
 principal's approval to specific action parameters. An agent
 MUST NOT change the amount, recipient, or action type after the
 principal has signed without invalidating the hash check at claim
 time. The Registry MUST reject any claim where the recomputed hash
 does not match - this check is the critical enforcement point.

 **Double-spend prevention:** The Registry's atomic step-claim
 operation (Section 15.4) ensures that each step can be claimed by exactly
 one actor exactly once. Distributed Registry deployments MUST use
 distributed locking or equivalent mechanisms for step claims.

 **Envelope replay prevention:** The `approval_id` is a UUID v4
 unique per envelope. Registries MUST reject duplicate `approval_id`
 values at submission time.

 **Approval window expiry:** Envelopes that expire in
 `pending_approval` status cannot be approved after `approval_window_
 expires_at`. This prevents stale approvals from accumulating in the
 Registry and being activated long after the principal's intent has
 been expressed.

 **Compensation pre-authorization:** The fact that compensation steps
 are pre-approved by the principal in the Approval Envelope creates a
 legal and cryptographic record that the principal knew and consented
 to the rollback mechanism before any step executed. This is stronger
 than a "refund might occur" disclosure - it is specific, action-bound,
 and signed.

 **Step Execution Token scope:** Step Execution Tokens are bound to a
 specific `approval_id` and `step_index`. They MUST NOT be usable for
 any purpose other than the specific step claim. Relying Parties MUST
 verify `aip_approval_id` and `aip_approval_step` when present.

 **Threat: Rogue orchestrator creates envelope without principal
 intent.** Mitigation: The `principal_signature` on the envelope is
 collected via the Principal Wallet consent flow (Section 15.4, `POST .../approve`),
 which MUST display all steps and compensation steps to the principal
 before signing. A rogue orchestrator can submit the envelope but
 cannot forge the principal's approval signature.

### 17.10. Privacy Considerations

 `principal.id` in Principal Tokens may be linkable to a real person.
 Implementations SHOULD use pairwise DIDs (e.g., `did:peer`) per
 service.

 Approval Envelopes stored in the Registry contain detailed workflow
 descriptions. Principals SHOULD be informed that envelope content
 (including step descriptions) is visible to the Registry operator and
 potentially to the Relying Parties that verify steps.

 Registries MUST NOT expose raw interaction logs. Only aggregated
 reputation fields (Section 11.2) MUST be exposed.

 AID correlation: persistent AIDs enable cross-service correlation.
 Principals who wish to prevent correlation SHOULD use separate AIDs
 per Relying Party. Ephemeral agents inherently limit correlation to
 one task.

 Registry Data Retention: Registries MUST provide a mechanism for
 principals to request deletion of an AID's reputation and endorsement
 data, subject to applicable law. Core identity records MAY be
 retained for audit purposes.

---

## 18. IANA Considerations

 This document defines the `did:aip` DID method, submitted for
 registration with the W3C DID Method Registry per [W3C-DID] Section 9.

 The `AIP+JWT` token type is used in the `typ` header of AIP
 Credential Tokens. The `AIP` HTTP Authorization scheme is used in
 `Authorization: AIP <token>`. Neither is registered with IANA in
 this draft.

---

## 19. Normative References

 [RFC2119] Bradner, S., "Key words for use in RFCs", BCP 14, March 1997.

 [RFC3986] Berners-Lee et al., "URI Generic Syntax", STD 66, January 2005.

 [RFC5234] Crocker & Overell, "ABNF", STD 68, January 2008.

 [RFC5280] Cooper et al., "X.509 PKI Certificate Profile", May 2008.

 [RFC6585] Nottingham & Fielding, "Additional HTTP Status Codes", April 2012.

 [RFC7515]  Jones, M., Bradley, J., and N. Sakimura, "JSON Web
            Signature (JWS)", RFC 7515, DOI 10.17487/RFC7515,
            May 2015, <https://www.rfc-editor.org/info/rfc7515>.

 [RFC7517] Jones, M., "JSON Web Key (JWK)", May 2015.

 [RFC7518] Jones, M., "JSON Web Algorithms (JWA)", May 2015.

 [RFC7519]  Jones, M., Bradley, J., and N. Sakimura, "JSON Web
            Token (JWT)", RFC 7519, DOI 10.17487/RFC7519,
            May 2015, <https://www.rfc-editor.org/info/rfc7519>.

 [RFC7748] Langley et al., "Elliptic Curves for Security", January 2016.

 [RFC8032]  Josefsson, S. and I. Liusvaara, "Edwards-Curve Digital
            Signature Algorithm (EdDSA)", RFC 8032,
            DOI 10.17487/RFC8032, January 2017,
            <https://www.rfc-editor.org/info/rfc8032>.

 [RFC8037] Liusvaara, I., "CFRG Elliptic Curves for JOSE", January 2017.

 [RFC8174] Leiba, B., "Ambiguity of Uppercase in RFC 2119", BCP 14, May 2017.

 [RFC8259] Bray, T., "JSON Data Interchange Format", STD 90, December 2017.

 [RFC8785]  Rundgren, A., Jordan, B., and S. Erdtman, "JSON
            Canonicalization Scheme (JCS)", RFC 8785,
            DOI 10.17487/RFC8785, June 2020,
            <https://www.rfc-editor.org/info/rfc8785>.

 [RFC9110]  Fielding, R., Ed., Nottingham, M., Ed., and J. Reschke,
            Ed., "HTTP Semantics", STD 97, RFC 9110,
            DOI 10.17487/RFC9110, June 2022,
            <https://www.rfc-editor.org/info/rfc9110>.

 [RFC9449]  Fett, D., Campbell, B., Bradley, J., Lodderstedt, T.,
            Jones, M., and D. Waite, "OAuth 2.0 Demonstrating
            Proof of Possession (DPoP)", RFC 9449,
            DOI 10.17487/RFC9449, September 2023,
            <https://www.rfc-editor.org/info/rfc9449>.

 [W3C-DID]  Sporny, M., Longley, D., Sabadello, M., Reed, D.,
            Steele, O., and C. Allen, "Decentralized Identifiers
            (DIDs) v1.0", W3C Recommendation, July 2022,
            <https://www.w3.org/TR/did-core/>.

 [RFC6454]  Barth, A., "The Web Origin Concept", RFC 6454,
            December 2011.
            <https://www.rfc-editor.org/info/rfc6454>

 [RFC6960]  Santesson, S., Myers, M., Ankney, R., Malpani, A.,
            Galperin, S., and C. Adams, "X.509 Internet Public Key
            Infrastructure Online Certificate Status Protocol -
            OCSP", RFC 6960, June 2013.
            <https://www.rfc-editor.org/info/rfc6960>

 [RFC7636]  Sakimura, N., Ed., Bradley, J., and N. Agarwal,
            "Proof Key for Code Exchange by OAuth Public Clients",
            RFC 7636, September 2015.
            <https://www.rfc-editor.org/info/rfc7636>

 [RFC8176]  Jones, M., Hunt, P., and A. Nadalin, "Authentication
            Method Reference Values", RFC 8176, June 2017.
            <https://www.rfc-editor.org/info/rfc8176>

 [RFC8414]  Jones, M., Sakimura, N., and J. Bradley, "OAuth 2.0
            Authorization Server Metadata", RFC 8414, June 2018.
            <https://www.rfc-editor.org/info/rfc8414>

 [RFC8693]  Jones, M., Nadalin, A., Campbell, B., Bradley, J., and
            C. Mortimore, "OAuth 2.0 Token Exchange", RFC 8693,
            January 2020.
            <https://www.rfc-editor.org/info/rfc8693>

 [RFC8707]  Campbell, B., Bradley, J., and H. Tschofenig, "Resource
            Indicators for OAuth 2.0", RFC 8707, February 2020.
            <https://www.rfc-editor.org/info/rfc8707>

 [RFC9068]  Bertocci, V., "JSON Web Token (JWT) Profile for
            OAuth 2.0 Access Tokens", RFC 9068, October 2021.
            <https://www.rfc-editor.org/info/rfc9068>

 [RFC9728]  Jones, M., Parecki, A., and F. Skokan, "OAuth 2.0
            Protected Resource Metadata", RFC 9728, December 2024.
            <https://www.rfc-editor.org/info/rfc9728>

 [FIPS-180-4]
            National Institute of Standards and Technology,
            "Secure Hash Standard (SHS)", FIPS PUB 180-4,
            DOI 10.6028/NIST.FIPS.180-4, August 2015,
            <https://doi.org/10.6028/NIST.FIPS.180-4>.

---

## 20. Informative References

 [RFC4122] Leach et al., "UUID URN Namespace", July 2005.

 [RFC6749]  Hardt, D., Ed., "The OAuth 2.0 Authorization
            Framework", RFC 6749, DOI 10.17487/RFC6749,
            October 2012,
            <https://www.rfc-editor.org/info/rfc6749>.

 [RFC9562] Davis et al., "Universally Unique IDentifiers (UUIDs)", May 2024.

 [MCP]      Anthropic, "Model Context Protocol Specification",
            2024, <https://spec.modelcontextprotocol.io>.

 [SP-800-207]
            Rose, S., Borchert, O., Mitchell, S., and S. Connelly,
            "Zero Trust Architecture", NIST Special Publication
            800-207, DOI 10.6028/NIST.SP.800-207, August 2020,
            <https://doi.org/10.6028/NIST.SP.800-207>.

 [SP-800-63-4]
            Temoshok, D., Fenton, J., Choong, Y., Lefkovitz, N.,
            Regenscheid, A., and J. Richer, "Digital Identity
            Guidelines", NIST Special Publication 800-63-4
            (2nd Public Draft), July 2025,
            <https://doi.org/10.6028/NIST.SP.800-63-4.2pd>.

 [SAGA] Garcia-Molina & Salem, "Sagas", SIGMOD 1987.
 Informative reference for the SAGA compensation pattern in Section 4.6.9.

 [OWASP-LLM]
            OWASP Foundation, "OWASP Top 10 for Large Language Model
            Applications".
            <https://owasp.org/www-project-top-10-for-large-language-model-applications/>

---

## Acknowledgements

 AIP builds directly on the work of the W3C DID Working Group,
 IETF OAuth Working Group, and NIST NCCoE AI Agent Identity and
 Authorization Concept Paper (2026).

---

## Authors' Addresses

 Paras Singla
 Independent / ProvAI
 GitHub: @itisparas

 ProvAI
 https://provai.dev
 Email: spec@provai.dev
 Repository: https://github.com/provai-dev/aip-spec

---

*AIP Specification v0.2 - Standards Track Draft*
*Released under CC0 1.0 Universal - No rights reserved*
*Provai - https://provai.dev*
---

## Appendix A: Changes from Version 0.1

   This appendix is informative.

   This version addresses four operational and security additions relative
   to v0.1:

   - **Section 4.5 — AIP-GRANT Principal Authorization Protocol.** Defines
     the standardised ceremony by which a human principal reviews, consents
     to, and cryptographically authorises an agent delegation. Analogous to
     the OAuth 2.0 Authorization Code Flow.

   - **Section 4.6 — Chained Approval Envelopes.** Defines a workflow-level
     authorisation primitive. A single human approval covers a pre-declared
     sequence of dependent agent actions, including SAGA compensation steps.
     Addresses the cascading-approval problem and the token-expiry-while-
     pending problem for Tier 2 workflows.

   - **Section 7.4 — Token Refresh and Long-Running Tasks.** Specifies when
     and how agents re-issue Credential Tokens, pre-emptive refresh
     requirements, and handling of delegation chain expiry.

   - **Section 14 (revised) — Rate Limiting and Abuse Prevention.** Defines
     per-endpoint rate limit categories, required response headers, anti-
     abuse rules for registration and validation-driven lookups, and
     graduated backoff requirements.

## Appendix B: Changes from Version 0.2

   This appendix is informative.

   v0.3 introduces the following changes relative to v0.2. Items marked
   **(breaking)** are not backward compatible.

   **Breaking changes:**

   - **(breaking) §3 — Tiers reframed as threat-model declarations.**
     Tier 1 (bounded-staleness), Tier 2 (real-time revocation), Tier 3
     (enterprise/regulated). Each Tier now enumerates its security
     property declarations rather than just listing scopes.

   - **(breaking) §3, §4.5.3, §7.2 — `spawn_agents` scope retired.**
     Replaced by `spawn_agents.create` and `spawn_agents.manage`, both
     classified as Tier 2 with 300s max TTL and DPoP requirement.

   - **(breaking) §4.5 — Three-tier grant model.** AIP-GRANT
     restructured into G1 (Registry-Mediated), G2 (Direct Deployer),
     and G3 (Full Ceremony with OAuth 2.1). Registration Envelopes MUST
     include `grant_tier`. `did:key` principals forbidden for Tier 2.

   - **(breaking) §6.2 — AIPRegistry service entry.** Principal DID
     Documents authorising Tier 2 agents MUST include an `AIPRegistry`
     service entry.

   - **(breaking) §6.3.4 — Well-known schema extended.** The
     `/.well-known/aip-registry` response MUST include `signature`,
     `registry_name`, and `endpoints` fields.

   - **(breaking) §7.1 — Version header.** `X-AIP-Version` updated
     from `"0.2"` to `"0.3"`.

   **Additive changes:**

   - **§1.2 — MCP integration note.** Informative note clarifying
     AIP's relationship with Model Context Protocol.

   - **§4.2.3 — New claims.** `aip_approval_step` (integer) and
     `aip_engagement_id` (string) added to Credential Token schema.

   - **§4.2.4 — Principal Token claims.** `acr` and `amr` claims
     added for G3 identity proofing. `iss` field added.

   - **§4.7 — Capability Overlays.** New section defining context-
     specific capability attenuation with Rules CO-1 through CO-6.

   - **§4.8 — Engagement Objects.** New section defining multi-party
     engagement lifecycle, append-only change log, and approval gates.

   - **§7.3 — Validation steps.** Step 6a (Registry Trust Anchoring),
     Step 6b (Engagement validation), and Step 9e (Overlay application)
     added.

   - **§7.5 — Token Exchange.** New section for RFC 8693 token exchange
     with DPoP binding, enabling AIP-to-OAuth bridging for MCP.

   - **§9.4 — RPNP.** Registry Push Notification Protocol for near-
     real-time event delivery (5s SLA).

   - **§13.2 — Error codes.** 26 new error codes for all v0.3 features.

   - **§14.6 — Backoff formula corrected.** `BACKOFF_BASE` separated
     from `Retry-After`; jitter bounded by `BACKOFF_BASE`.

   - **§15.5 — OAuth 2.1 AS.** Authorization server interface for G3.

   - **§15.6 — Scope Map.** `urn:aip:scope:` URI namespace and
     `GET /v1/scopes` endpoint.

   - **§15.7 — Engagement Endpoints.** CRUD for Engagement Objects.

   - **§15.8 — RPNP Endpoints.** Subscription management.

   - **§16.1 — Tier Conformance table.** Maps Tiers to required
     security properties.

   - **§17.1 — Threat scenarios.** TS-12 (orchestrator cascade),
     TS-13 (overlay injection), TS-14 (engagement tampering).

   - **§19 — References.** 10 new normative references (RFC 6454,
     6960, 7636, 8176, 8414, 8693, 8707, 9068, 9728; RFC 8785
     already present). 1 new informative reference (OWASP LLM Top 10).
