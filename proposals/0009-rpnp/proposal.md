---
AIP: 0009
Title: Registry Push Notification Protocol (RPNP)
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 9.3, 9.4, 15.8
Requires: 0002
Supersedes: ~
---

# AIP-0009: Registry Push Notification Protocol (RPNP)

## Abstract

This proposal introduces the Registry Push Notification Protocol (RPNP)
— an optional webhook subscription mechanism (§9.4, §15.8) that delivers
near-real-time revocation and engagement events to subscribing Relying
Parties. RPNP collapses the effective revocation window from ~16 minutes
(CRL cache) to at most 5 seconds for subscribers, without replacing the
existing CRL model for non-subscribers.

## Motivation

v0.2 §9.3 gives Tier 1 a 15-minute CRL refresh window plus a 60-second
manifest cache — approximately 16 minutes of exposure after revocation.
The spec has no push mechanism. For production cross-operator scenarios
where a hiring operator revokes an agent mid-engagement, this window is
operationally unacceptable.

RPNP provides an opt-in push layer. Non-subscribing Relying Parties
continue using CRL as specified. Subscribing RPs receive signed push
events within 5 seconds of a revocation or engagement state change.

Closes #10

## Terminology

**RPNP (Registry Push Notification Protocol)** — A webhook-based
subscription mechanism for receiving near-real-time event notifications
from an AIP Registry.

**RPNP Subscriber** — A Relying Party that has registered a webhook
endpoint with the Registry to receive push notifications.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §9.3 Revocation Checking — RPNP Cross-Reference

Add the following to §9.3 after the Tier-specific paragraphs:

> Relying Parties that subscribe to RPNP (§9.4) receive push
> notifications for revocation events. For subscribing RPs, the
> effective revocation window is the RPNP delivery latency (at most 5
> seconds) rather than the CRL refresh interval. Non-subscribing RPs
> continue to use CRL as specified above. RPNP does not replace CRL;
> it supplements it.
>
> Registries that implement RPNP and cannot meet the 5-second delivery
> SLA for a given subscriber MUST NOT serve revocation status for Tier 2
> operations to that subscriber via the push channel.

### §9.4 Registry Push Notification Protocol (new section)

#### 9.4.1. Overview

RPNP is an OPTIONAL Registry capability. When implemented:

- Registry MUST deliver push events within 5 seconds of the triggering
  state change.
- Push payloads MUST be signed by the Registry's administrative key.
- Subscriber authentication MUST be verified at subscription time.

#### 9.4.2. Subscription

A Relying Party subscribes by calling `POST /v1/subscriptions`:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `subscriber_did` | string | REQUIRED | DID of the subscribing RP; MUST be `did:web` or `did:aip` |
| `event_types` | array | REQUIRED | One or more of: `full_revoke`, `scope_revoke`, `delegation_revoke`, `engagement_participant_removed`, `engagement_gate_approved`, `engagement_terminated` |
| `scope_filter` | string | REQUIRED | One of: `"aid"` (per-agent), `"principal"` (all agents under a principal), `"all"` (all events) |
| `targets` | array | CONDITIONAL | REQUIRED when `scope_filter` is `"aid"` or `"principal"`; array of AID or principal DID strings |
| `webhook_uri` | string | REQUIRED | HTTPS URI; the RP's event receiver endpoint |
| `hmac_secret_hash` | string | REQUIRED | SHA-256 hash of the shared HMAC secret (hex-encoded) |
| `subscription_expires_at` | string | REQUIRED | ISO 8601 UTC; max 90 days from creation |

The subscription request MUST be authenticated via DPoP proof binding
`subscriber_did` to the request. The Registry MUST reject unsigned
subscription requests with `subscription_auth_required`.

#### 9.4.3. Push Event Payload

Push events are delivered as HTTP POST requests to the subscriber's
`webhook_uri`. The request body is a compact-serialised JWT signed by
the Registry's administrative key:

**JWT Header:**
| Field | Value |
|-------|-------|
| `typ` | `"AIP-RPNP+JWT"` |
| `alg` | `"EdDSA"` |
| `kid` | Registry AID key ID |

**JWT Payload:**
| Field | Type | Description |
|-------|------|-------------|
| `iss` | string | Registry AID |
| `sub` | string | Affected AID or engagement ID |
| `iat` | integer | Unix timestamp |
| `jti` | string | UUID v4; unique event ID |
| `event_type` | string | One of the subscribed event types |
| `event_data` | object | Event-specific data (revocation reason, engagement delta, etc.) |

**HMAC transport verification:** The request MUST include an
`X-AIP-Signature` header containing `HMAC-SHA256(shared_secret, body)`.
The subscriber MUST verify both the JWT signature (Registry key) and
the HMAC (shared secret).

#### 9.4.4. Delivery Guarantees

1. **SLA:** The Registry MUST deliver push events within 5 seconds of
   the triggering state change for all active subscribers.
2. **Retry:** On delivery failure (non-2xx response or timeout), the
   Registry MUST retry with exponential backoff: 1s, 2s, 4s (3
   attempts minimum).
3. **Degradation:** After 3 consecutive failures, the Registry MUST
   mark the subscription as `degraded` and MAY stop delivery attempts.
   The subscriber falls back to CRL.
4. **Replay prevention:** Subscribers MUST reject duplicate `jti` values
   within a 60-second sliding window.
5. **Ordering:** Events for the same `sub` (agent or engagement) MUST
   be delivered in causal order. Cross-agent events have no ordering
   guarantee.

#### 9.4.5. Subscription Management

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v1/subscriptions/{id}` | Retrieve subscription status |
| `DELETE` | `/v1/subscriptions/{id}` | Unsubscribe |
| `GET` | `/v1/subscriptions` | List subscriber's active subscriptions |

Subscriptions expire at `subscription_expires_at`. The subscriber MUST
renew before expiry to maintain push delivery.

### §15.8 RPNP Endpoints (new section)

Add to the Registry Interface:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/subscriptions` | Create RPNP subscription |
| `GET` | `/v1/subscriptions` | List active subscriptions (filtered by subscriber DID) |
| `GET` | `/v1/subscriptions/{id}` | Retrieve subscription |
| `DELETE` | `/v1/subscriptions/{id}` | Delete subscription |

### §15.1 Well-Known Configuration — RPNP Advertisement

Add to the `/.well-known/aip-registry` response:

| Field | Type | Description |
|-------|------|-------------|
| `rpnp_supported` | boolean | Whether this Registry implements RPNP |
| `rpnp_sla_seconds` | integer | Maximum delivery latency (MUST be ≤ 5 when `rpnp_supported` is true) |

### Normative Requirements

1. Registry support for RPNP is OPTIONAL (SHOULD for production
   Registries).
2. When RPNP is implemented, the 5-second delivery SLA is MUST.
3. Push payloads MUST be signed by the Registry's administrative key.
4. Subscription requests MUST be authenticated via DPoP.
5. Subscribers MUST verify both JWT signature and HMAC.
6. Subscribers MUST reject duplicate `jti` within 60 seconds.

### Failure Conditions

| Condition | Error Code | HTTP Status |
|-----------|-----------|-------------|
| Subscription request without DPoP authentication | `subscription_auth_required` | 401 |
| Invalid webhook URI (not HTTPS) | `invalid_webhook_uri` | 400 |
| Subscription target AID not found | `agent_not_found` | 404 |
| Subscription limit exceeded | `subscription_limit_exceeded` | 429 |

### Schema Changes

Create `spec/v0.3/schemas/rpnp-subscription.schema.json` and
`spec/v0.3/schemas/rpnp-event.schema.json`.

## Security Considerations

**Webhook authentication:** Dual-layer (JWT signature + HMAC) prevents
both payload tampering and endpoint spoofing. The HMAC secret is never
transmitted in plaintext; only its SHA-256 hash is stored.

**Subscription hijacking:** DPoP-authenticated subscription requests
prevent an attacker from subscribing a victim's webhook endpoint.

**Replay prevention:** The `jti` + 60-second window prevents replayed
push events from triggering duplicate revocation actions.

**Delivery failure fallback:** Degraded subscriptions fall back to CRL.
RPNP is a supplement, not a replacement; the system degrades gracefully.

## Backwards Compatibility

Fully backwards compatible. RPNP is optional. Non-subscribing RPs are
unaffected. The CRL model continues to function as specified in v0.2.

## Test Vectors

This proposal requires no new cryptographic test vectors.

## Implementation Guidance

Registries implementing RPNP should use a message queue (e.g., Redis
Streams, Kafka) to buffer events and ensure the 5-second SLA under
load. The webhook delivery should be asynchronous from the revocation
write path.

## Alternatives Considered

**WebSocket-based streaming.** Rejected for operational complexity;
webhooks are simpler to deploy and operate across network boundaries.

**Server-Sent Events (SSE).** Rejected because SSE requires long-lived
connections; webhooks work with standard HTTP infrastructure.

**Reduce CRL refresh interval.** Rejected because it shifts load to the
CRL CDN without providing near-real-time delivery.

## References

### Normative References

   [RFC2119]  <https://www.rfc-editor.org/info/rfc2119>
   [RFC8174]  <https://www.rfc-editor.org/info/rfc8174>
   [RFC9449]  <https://www.rfc-editor.org/info/rfc9449>

### Informative References

   AIP-0002 — Tier threat-model declarations (RPNP delivery bound).
   AIP-0008 — Engagement Objects (engagement events as RPNP types).

## Changelog

- 2026-04-12 — Initial draft.
