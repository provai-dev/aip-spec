---
AIP: 0008
Title: Engagement Objects — multi-party versioned engagement lifecycle
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 4.8, 7.3, 13.2, 15.7
Requires: 0007
Supersedes: ~
---

# AIP-0008: Engagement Objects — multi-party versioned engagement lifecycle

## Abstract

This proposal introduces the Engagement Object (§4.8) — a first-class
Registry resource that models multi-party, multi-week engagements with
participant rotation, approval gates, and a signed append-only change
log. Engagement Objects are the parent container for Approval Envelopes
and Capability Overlays, resolving the tension between AIP's token-centric
cryptographic non-repudiation and the operational need for mutable
engagement state.

## Motivation

v0.2 Approval Envelopes (§4.6) were designed for single-transaction
workflows: immutable post-signing, 20-step maximum, no participant
rotation. Production agentic pipelines run for days or weeks, requiring:

1. **Participant rotation** — replacing an agent mid-engagement without
   revoking the entire principal chain.
2. **Approval gates** — blocking downstream execution until a named
   operator signs off at a checkpoint.
3. **Cross-operator hire formalisation** — a structured, auditable record
   when a hiring operator engages an external agent.
4. **Mutable engagement scope** — scope that narrows over time via
   Capability Overlays (AIP-0007) linked to the engagement.

The Credential Token carries immutable delegation chains; the Registry
carries mutable current state. Engagement Objects formalise the mutable
layer.

Closes #12

## Terminology

**Engagement Object** — A Registry-stored resource representing a
multi-party engagement with a defined lifecycle, participant roster,
approval gates, and an append-only signed change log.

**Change Log Entry** — An append-only, individually-signed record of a
state mutation within an Engagement Object. Each entry has a monotonic
sequence number.

**Approval Gate** — A named checkpoint within an Engagement that blocks
downstream execution until a designated approver signs off.

**Participant Rotation** — The act of adding or removing an agent from
an Engagement's participant roster via a signed change log entry,
without revoking the delegation chain.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §4.8 Engagement Objects (new section)

#### 4.8.1. Overview

An Engagement Object is a mutable Registry resource that models a
multi-party engagement. It is the parent container for:
- Capability Overlays (AIP-0007) scoped via `engagement_id`
- Approval Envelopes (§4.6) scoped via `engagement_id`
- Participant roster and approval gate state

All mutations to an Engagement Object are recorded as signed change log
entries. The change log is append-only and forms an auditable history.

#### 4.8.2. Engagement Schema

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `engagement_id` | string | REQUIRED | Pattern: `^eng:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |
| `title` | string | REQUIRED | maxLength: 256 |
| `hiring_operator` | string | REQUIRED | DID of the hiring operator; MUST be `did:web` or `did:aip` |
| `deploying_principal` | string | REQUIRED | DID of the deploying principal whose agents participate |
| `created_at` | string | REQUIRED | ISO 8601 UTC |
| `expires_at` | string | REQUIRED | ISO 8601 UTC; MUST be after `created_at` |
| `status` | string | REQUIRED | One of: `"proposed"`, `"active"`, `"suspended"`, `"completed"`, `"terminated"` |
| `participants` | array | REQUIRED | Array of Participant objects (see below) |
| `approval_gates` | array | OPTIONAL | Array of Approval Gate objects (see below) |
| `change_log` | array | REQUIRED | Array of Change Log Entry objects; append-only |
| `hiring_operator_signature` | string | REQUIRED | Base64url EdDSA signature by `hiring_operator` over JCS canonical JSON of the engagement (excluding signatures and change_log) |
| `deploying_principal_signature` | string | REQUIRED | Base64url EdDSA countersignature by `deploying_principal` |
| `version` | integer | REQUIRED | Monotonically increasing; incremented on each change log append |

**Participant object:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `aid` | string | REQUIRED | The participant agent's AID |
| `role` | string | REQUIRED | maxLength: 64; application-defined role label |
| `capability_overlay_id` | string | OPTIONAL | Reference to an active Capability Overlay |
| `added_at` | string | REQUIRED | ISO 8601 UTC |
| `added_by` | string | REQUIRED | DID of the actor who added this participant |
| `removed_at` | string | OPTIONAL | ISO 8601 UTC; set when participant is removed |

**Approval Gate object:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `gate_id` | string | REQUIRED | Pattern: `^gate:[a-z0-9_-]+$` |
| `name` | string | REQUIRED | maxLength: 128 |
| `required_approver` | string | REQUIRED | DID of the required approver |
| `trigger` | string | REQUIRED | Condition that activates the gate (application-defined) |
| `status` | string | REQUIRED | One of: `"pending"`, `"approved"`, `"rejected"` |
| `approved_at` | string | OPTIONAL | ISO 8601 UTC; set when approved |

#### 4.8.3. Change Log

Each change log entry has:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `seq` | integer | REQUIRED | Monotonically increasing from 1 |
| `timestamp` | string | REQUIRED | ISO 8601 UTC |
| `action` | string | REQUIRED | One of the defined action types (see below) |
| `actor` | string | REQUIRED | DID of the actor performing the change |
| `payload` | object | OPTIONAL | Action-specific data |
| `signature` | string | REQUIRED | Base64url EdDSA signature by `actor` over JCS canonical JSON of the entry excluding `signature` |

**Defined action types:**

| Action | Payload | Who may issue |
|--------|---------|---------------|
| `engagement_created` | (none) | Hiring operator |
| `engagement_countersigned` | (none) | Deploying principal |
| `participant_added` | `{ aid, role }` | Hiring operator or deploying principal |
| `participant_removed` | `{ target_aid, reason, effective_at }` | Hiring operator |
| `participant_role_changed` | `{ target_aid, new_role }` | Hiring operator |
| `gate_added` | Approval Gate object | Hiring operator |
| `gate_approved` | `{ gate_id }` | Required approver for that gate |
| `gate_rejected` | `{ gate_id, reason }` | Required approver |
| `engagement_suspended` | `{ reason }` | Hiring operator |
| `engagement_resumed` | (none) | Hiring operator |
| `engagement_completed` | (none) | Hiring operator |
| `engagement_terminated` | `{ reason }` | Hiring operator or deploying principal |

**Append-only invariant:** The Registry MUST reject any request that
modifies or deletes an existing change log entry. Only appends are
permitted. Violation attempts MUST return `change_log_immutable`.

**Sequence invariant:** Each new entry's `seq` MUST equal
`previous_entry.seq + 1`. The Registry MUST reject out-of-sequence
appends with `change_log_sequence_invalid`.

#### 4.8.4. Engagement Lifecycle

```
 proposed --> active --> completed
                |
                +--> suspended --> active (resumed)
                |
                +--> terminated
```

- **proposed → active:** Requires both `hiring_operator_signature` and
  `deploying_principal_signature`. The Registry transitions to `active`
  when both signatures are present.
- **active → suspended:** Hiring operator may suspend. All Approval
  Envelope execution within the engagement is paused.
- **suspended → active:** Hiring operator resumes.
- **active → completed:** Hiring operator marks complete. No further
  Approval Envelope execution. Overlays are retained for audit.
- **active/suspended → terminated:** Either party may terminate.
  Triggers cascade (see §4.8.5).

#### 4.8.5. Termination Cascade

When an Engagement is terminated:

1. The Registry MUST set `status: "terminated"` atomically.
2. All Capability Overlays linked to this `engagement_id` MUST be
   invalidated (per AIP-0007 Rule CO-5).
3. All Approval Envelopes in `pending_approval`, `approved`, or
   `executing` status scoped to this `engagement_id` MUST be
   transitioned to `cancelled`.
4. Subsequent Credential Token validation for operations scoped to this
   engagement MUST fail with `engagement_terminated`.

### §4.6 Approval Envelope — New Optional Field

Add `engagement_id` as an optional field in the Approval Envelope
schema:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `engagement_id` | string | OPTIONAL | Pattern matching Engagement Object ID; links the envelope to an engagement |

When present, the Registry MUST verify that the Engagement is in
`active` status before accepting the Approval Envelope.

### §4.2.3 Credential Token — New Optional Claim

Add `aip_engagement_id` as an optional claim:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `aip_engagement_id` | string | OPTIONAL | Pattern matching Engagement Object ID; present when the token is scoped to an engagement |

### §7.3 Validation — New Step

Insert after Step 6a (Registry Trust Anchoring):

> **Step 6b — Engagement validation (conditional).** If
> `aip_engagement_id` is present in the Credential Token:
>
> 1. Fetch the Engagement Object from
>    `GET /v1/engagements/{aip_engagement_id}`.
> 2. Verify `status` is `"active"`. Fail: `engagement_terminated` if
>    terminated/completed, `engagement_suspended` if suspended.
> 3. Verify the token's `sub` (agent AID) is in the `participants`
>    array with `removed_at` null. Fail:
>    `engagement_participant_removed`.
> 4. Verify all approval gates with `trigger` matching the current
>    operation context are in `approved` status. Fail:
>    `engagement_gate_pending`.

### §13.2 Error Codes — New Entries

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `engagement_terminated` | 403 | Engagement has been terminated or completed |
| `engagement_suspended` | 403 | Engagement is currently suspended |
| `engagement_participant_removed` | 403 | Agent has been removed from the engagement |
| `engagement_gate_pending` | 403 | Required approval gate has not been approved |
| `engagement_not_found` | 404 | Engagement ID not found |
| `engagement_countersign_required` | 400 | Engagement missing required countersignature |
| `change_log_immutable` | 400 | Attempt to modify existing change log entry |
| `change_log_sequence_invalid` | 400 | Change log sequence number out of order |

### §15.7 Engagement Endpoints (new section)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/engagements` | Create engagement (hiring operator) |
| `GET` | `/v1/engagements/{id}` | Retrieve engagement with current state |
| `POST` | `/v1/engagements/{id}/countersign` | Deploying principal countersigns |
| `POST` | `/v1/engagements/{id}/delta` | Append change log entry |
| `GET` | `/v1/engagements/{id}/changelog` | Retrieve full change log |
| `POST` | `/v1/engagements/{id}/gates/{gate_id}/approve` | Approve gate |
| `POST` | `/v1/engagements/{id}/gates/{gate_id}/reject` | Reject gate |

**`POST /v1/engagements` validation:**
1. Verify `hiring_operator_signature` against `hiring_operator` DID.
2. Set initial `status: "proposed"`.
3. Return 201 with the engagement awaiting countersignature.

**`POST /v1/engagements/{id}/delta` validation:**
1. Verify the change log entry `signature` against the `actor` DID.
2. Verify the `actor` has authority for the specified `action` (per
   the "Who may issue" table in §4.8.3).
3. Verify `seq` monotonicity.
4. Apply the state change atomically.
5. If the action is `engagement_terminated`, execute the termination
   cascade (§4.8.5).

### Normative Requirements

1. Engagement Objects MUST require dual signatures (hiring operator +
   deploying principal) before becoming active.
2. The change log MUST be append-only with monotonic sequence numbers.
3. Each change log entry MUST be independently signed by the actor.
4. Engagement termination MUST cascade to overlays and approval
   envelopes.
5. Credential Tokens scoped to an engagement MUST be validated against
   the engagement's current participant roster and gate status.
6. The Registry MUST reject change log modifications.

### Failure Conditions

See §13.2 new error codes above.

### Schema Changes

Create `spec/v0.3/schemas/engagement-object.schema.json` with the
fields defined in §4.8.2.

## Security Considerations

**Change log integrity:** Each entry is independently signed. Verifiers
can reconstruct the full engagement history and detect any tampering.
The `seq` field prevents reordering attacks.

**Countersignature requirement:** Prevents unilateral engagement creation.
Neither the hiring operator nor the deploying principal can establish an
engagement alone.

**Termination cascade:** Ensures all associated resources (overlays,
approval envelopes) are atomically invalidated. Prevents stale
authorizations persisting after engagement ends.

**Participant removal atomicity:** When a participant is removed via
change log, the Registry atomically marks `removed_at`. Subsequent
Credential Token validation rejects the removed participant before
any operation executes.

**Approval gate trust:** Gate approval is signed by the designated
approver's DID key. A compromised agent cannot approve its own gates.

**RPNP integration:** Engagement state changes (participant rotation,
gate approval, termination) are natural RPNP event types (see AIP-0009).
Subscribing Relying Parties receive near-real-time notification.

## Backwards Compatibility

Fully backwards compatible. Engagement Objects are a new feature.
Existing tokens without `aip_engagement_id` skip Step 6b entirely.
Approval Envelopes without `engagement_id` continue to function
independently.

## Test Vectors

This proposal requires no new cryptographic test vectors. Conformance
tests should verify:

1. An engagement missing the countersignature remains in `proposed`.
2. A token with `aip_engagement_id` for a terminated engagement is
   rejected.
3. A token for a removed participant is rejected.
4. A change log entry with wrong `seq` is rejected.
5. A change log modification attempt is rejected.
6. Termination cascades to overlays and approval envelopes.

## Implementation Guidance

**For hiring operators:** Create an Engagement when onboarding external
agents. Add participants via signed change log entries. Use approval
gates to control phase transitions. Link Capability Overlays via
`engagement_id` for scope narrowing.

**For deploying principals:** Countersign engagements to activate them.
Monitor the change log for participant removals affecting your agents.

**For Registry implementers:** Store the change log as an append-only
ledger. Index by `(engagement_id, seq)` for efficient retrieval.
Implement the termination cascade atomically (transaction-level
consistency).

## Alternatives Considered

**Extend Approval Envelopes for multi-week workflows.** Rejected
because Approval Envelopes are immutable post-signing and capped at
20 steps. They are the wrong primitive for evolving multi-week
engagements.

**Use Capability Overlays alone without an engagement container.**
Rejected because overlays address scope narrowing but not participant
rotation, approval gates, or auditable engagement lifecycle.

**Token-only model (no Registry state).** Rejected because participant
rotation requires mutable state that tokens cannot carry. The
Engagement Object resolves the token-vs-registry tension as a
"both/and" design.

## References

### Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.
              <https://www.rfc-editor.org/info/rfc2119>

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119
              Key Words", BCP 14, RFC 8174, May 2017.
              <https://www.rfc-editor.org/info/rfc8174>

   [RFC8785]  Rundgren, A., Jordan, B., and S. Erdtman, "JSON
              Canonicalization Scheme (JCS)", RFC 8785, June 2020.
              <https://www.rfc-editor.org/info/rfc8785>

### Informative References

   AIP-0007 — Capability Overlays (engagement-scoped overlay linkage).
   AIP-0009 — RPNP (engagement events as notification types).

## Acknowledgements

Design informed by production operator feedback on multi-week editorial
pipelines in [w3c/did-use-cases#155](https://github.com/w3c/did-use-cases/issues/155).

## Changelog

- 2026-04-12 — Initial draft.
