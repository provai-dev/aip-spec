# Implementer Walkthrough

This walkthrough gives implementers a narrow, non-normative path through one AIP flow using the repository's existing examples and schemas.

The draft remains the source of truth. If this guide appears to conflict with `draft.xml`, `sections/`, `schemas/`, or `examples/`, treat the draft sources as authoritative and file an issue.

## Flow Covered

This walkthrough follows a G2 Direct Deployer grant flow:

1. An agent deployer prepares an agent identity and requested capabilities.
2. The deployer sends a GrantRequest to the principal wallet.
3. The principal wallet returns a GrantResponse with a principal token.
4. The deployer constructs a capability manifest from the approved capabilities.
5. The deployer submits a Registration Envelope to the registry.

Related draft source:

- `sections/12-grant.xml`
- `sections/06-registration.xml`
- `sections/17-registry.xml`

Related examples:

- `examples/grant-request.json`
- `examples/grant-response.json`
- `examples/capability-manifest.json`
- `examples/registration-envelope.json`

Related schemas:

- `schemas/grant-request.schema.json`
- `schemas/grant-response.schema.json`
- `schemas/capability-manifest.schema.json`
- `schemas/registration-envelope.schema.json`

## Step 1: Prepare The Agent Identity

Before constructing the GrantRequest, the deployer prepares the agent identity and key material needed for the agent's AID.

In the example set, the same AID appears across the grant and registration artifacts:

```text
did:aip:personal:9f3a1c82b4e6d7f0a2b5c8e1d4f7a0b3
```

Implementation check:

- the AID in `grant-request.json` should match the `principal_token.sub` value in `grant-response.json`
- the same AID should appear in the registration envelope identity and capability manifest

If an implementation cannot determine when or how to compute the AID, file an implementation report.

## Step 2: Construct The GrantRequest

The GrantRequest describes what the deployer wants the principal to approve.

Inspect:

- `examples/grant-request.json`
- `schemas/grant-request.schema.json`

Important fields for implementers:

- `grant_request_id`: stable request identifier
- `agent_aid`: the target agent identity
- `requested_capabilities`: requested authorization surface
- `purpose`: text the wallet should display to the principal
- `delegation_valid_for_seconds`: requested validity period
- `max_delegation_depth`: requested sub-delegation depth
- `nonce`: replay protection
- `callback_uri`: where the wallet posts the result in the Web Redirect binding
- `state`: deployer state value for request correlation

Implementation check:

- validate the example with `make validate-examples`
- preserve `nonce` and `state` so they can be checked when the GrantResponse returns
- treat the example signatures as placeholders, not production signatures

## Step 3: Process The GrantResponse

The principal wallet returns a GrantResponse after approval, partial approval, or denial.

Inspect:

- `examples/grant-response.json`
- `schemas/grant-response.schema.json`

Important fields for implementers:

- `grant_request_id`: must match the original request
- `nonce`: must match the original request
- `state`: should match deployer state
- `status`: indicates approval state
- `principal_id`: identifies the approving principal
- `principal_token`: compact JWT naming the authorized agent
- `approved_capabilities`: capabilities approved by the principal
- `approved_delegation_valid_for_seconds`: approved validity period
- `approved_max_delegation_depth`: approved delegation depth

Implementation check:

- reject mismatched `grant_request_id`, `nonce`, or `state`
- verify the principal token according to the draft
- do not assume `approved_capabilities` equals `requested_capabilities`
- handle partial approval explicitly

If status handling is unclear for a real implementation, file an implementation report before proposing a draft change.

## Step 4: Build The Capability Manifest

The deployer uses approved capabilities to construct the capability manifest.

Inspect:

- `examples/capability-manifest.json`
- `schemas/capability-manifest.schema.json`

Important fields for implementers:

- `manifest_id`: manifest identifier
- `aid`: the authorized agent identity
- `granted_by`: principal or grant authority
- `issued_at` and `expires_at`: manifest timing
- `capabilities`: approved capability set
- `signature`: production deployments must replace placeholder signatures

Implementation check:

- derive capabilities from `approved_capabilities`, not from the original request alone
- keep manifest expiry consistent with the grant response
- verify whether the draft gives enough detail for canonical signing in your implementation context

## Step 5: Submit The Registration Envelope

The registration envelope combines the agent identity, capability manifest, principal token, and grant tier.

Inspect:

- `examples/registration-envelope.json`
- `schemas/registration-envelope.schema.json`

Important fields for implementers:

- `identity`: agent identity object
- `capability_manifest`: authorization surface
- `principal_token`: token returned by the principal wallet
- `grant_tier`: grant model used for registration

Implementation check:

- the identity AID, manifest AID, and principal token subject should refer to the same agent
- the principal token should bind the authorization to the principal and agent
- the registry submission should not rely on the non-standard `_comment`, `_notes`, or decoded helper fields used in examples

## Local Validation

Run:

```bash
make validate-examples
```

For draft text changes, also run:

```bash
make validate
make html
make text
```

## What To Report

Implementation reports are especially useful when this walkthrough exposes:

- fields whose timing or trust boundary is unclear
- capabilities that are hard to map into real product permissions
- partial approval behavior that is hard to implement
- signature or canonicalization ambiguity
- registry submission details that are underspecified
- lifecycle, revocation, or expiry questions

Use [IMPLEMENTATION-REPORTS.md](IMPLEMENTATION-REPORTS.md) and the `Implementation Report` issue template.
