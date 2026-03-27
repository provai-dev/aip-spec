# AIP Versioning Policy

## 1. Version Format

AIP uses Semantic Versioning: `MAJOR.MINOR.PATCH`

The current canonical specification is `docs/aip-spec.md`. The preamble of
that file states the current version. Frozen snapshots of each released version
live at `spec/vMAJOR.MINOR/` and `docs/aip-spec-vMAJOR.MINOR.md`.

---

## 2. AIP Numbers vs. Spec Versions

AIP numbers (e.g., AIP-0004) and spec version numbers (e.g., v0.2) are
independent identifiers.

- **AIP numbers** identify proposals. They are sequential, permanent, and never
  reused — even if a proposal is rejected or withdrawn.
- **Spec versions** identify releases of `docs/aip-spec.md`. A single spec
  version may incorporate multiple accepted AIPs.

Multiple AIPs may land in one spec version. The `docs/aip-spec.md` preamble
includes a "Changes in this version" section listing which AIPs were
integrated. The `AIP_INDEX.md` records the spec version in which each AIP was
integrated.

---

## 3. What Triggers a New Version

### PATCH (e.g., v0.1.0 → v0.1.1)

- One or more Errata issues resolved with no change to normative behaviour
- Clarifications that do not alter what implementations MUST do
- Broken links, formatting, editorial corrections
- Schema `$id` version is **unchanged**
- All existing valid tokens, registrations, and delegation chains remain valid

### MINOR (e.g., v0.1 → v0.2)

- One or more Accepted AIPs that add new normative requirements or new
  optional schema fields
- All changes are backwards-compatible: existing valid tokens, registrations,
  delegation chains, and revocations remain valid
- Implementations MAY ignore unknown optional fields

### MAJOR (e.g., v0.x → v1.0, or v1.x → v2.0)

- One or more Accepted AIPs with breaking changes: at least one of —
  - Existing valid tokens become invalid under the new version
  - An existing required field is removed or its type changes
  - An algorithm step is changed in a way that alters its output
  - A key format is deprecated and removed
  - The DID method syntax changes incompatibly
- Schema `$id` versions **MUST** be bumped on breaking changes
- A full migration guide is required in CHANGELOG.md

---

## 4. Cutting a New Version

A version is cut by the Editor body by opening a PR that:

1. Updates the version number in the `docs/aip-spec.md` preamble
2. Adds a "Changes in this version" section listing integrated AIPs
3. Creates a frozen snapshot: `spec/vMAJOR.MINOR/` (copies of spec source files)
4. Generates `docs/aip-spec-vMAJOR.MINOR.md` as a versioned RFC snapshot
5. Updates `AIP_INDEX.md` with the spec version column for integrated AIPs
6. Adds a CHANGELOG.md entry (see § 7)

The version-cut PR requires at least two Editor approvals. Declaration of v1.0
stability requires a two-thirds super-majority per GOVERNANCE.md § 6.

---

## 5. Immutability Rule

Once a version is released, `spec/vMAJOR.MINOR/` and
`docs/aip-spec-vMAJOR.MINOR.md` are **immutable**. They MUST NOT be modified
for any reason. Any correction requires a new version.

`docs/aip-spec.md` always reflects the latest version but is not authoritative
for a specific released version. Implementations MUST pin to a specific version
snapshot.

---

## 6. Pre-1.0 Rules

Before v1.0:
- MINOR versions MAY include breaking changes
- Stability is not guaranteed
- Implementations SHOULD NOT ship production systems against pre-1.0 versions
  without explicit acknowledgement that breaking changes may occur at any MINOR
  increment

v1.0 signals: two independent conforming implementations exist, a conformance
test suite is published, and the Editor body has declared the specification
stable by super-majority vote.

---

## 7. CHANGELOG.md

Every version MUST include a CHANGELOG.md entry with:

```markdown
## v<MAJOR.MINOR[.PATCH]> — YYYY-MM-DD

### Integrated AIPs
- AIP-XXXX: <title>
- AIP-YYYY: <title>

### Breaking Changes
- [none] or [description]

### Migration Guide
- [none required] or [step-by-step instructions]

### Errata Fixed
- [list of errata issue numbers and descriptions]
```

---

## 8. Version Negotiation for Implementations

The AIP Credential Token MUST include an `aip_version` claim indicating the
spec version under which the token was produced (e.g., `"0.1"`).

Validators SHOULD accept tokens from any spec version they support. Validators
MUST reject tokens from versions with breaking changes relative to their
supported version unless they implement explicit version negotiation.

A future AIP will define a formal version negotiation mechanism (e.g.,
`aip-version-min` / `aip-version-max` fields in the Capability Manifest).
Until that AIP is accepted, validators MAY use any implementer-defined
negotiation strategy but MUST NOT silently accept tokens from unsupported
versions.

---

## 9. Compatibility Table

Implementations are encouraged to publish a compatibility table in their
documentation:

| AIP Spec Version | Supported | Notes |
|-----------------|-----------|-------|
| v0.1 | Yes | |
| v0.2 | Planned | |

---

## 10. Deprecation Policy

- Deprecated features MUST be documented in the spec with the version in which
  they were deprecated
- Deprecated features MUST continue to be supported for at least one MINOR
  version after deprecation
- Removal is only permitted in a MAJOR version bump
