---
AIP: 0017
Title: Add new normative references for v0.3
Author(s): Paras Singla <paras@provai.dev> (@itisparas)
Status: Draft
Type: Standards Track
Created: 2026-04-12
Last-Call-Ends: ~
Spec-Section: 19
Requires: 0005, 0006, 0009, 0010
Supersedes: ~
---

# AIP-0017: Add new normative references for v0.3

## Abstract

This proposal adds normative references to §19 for all new RFCs and
standards cited by v0.3 proposals, ensuring every normative citation
in the spec has a corresponding entry in the references section.

## Motivation

v0.3 proposals cite RFCs not present in v0.2's §19: RFC 6960 (OCSP),
RFC 7636 (PKCE), RFC 8176 (AMR), RFC 8414 (AS Metadata), RFC 8693
(Token Exchange), RFC 8707 (Resource Indicators), RFC 8785 (JCS),
RFC 9068 (JWT Profile), and RFC 9728 (Protected Resource Metadata).

## Terminology

This proposal introduces no new terms.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

## Specification

### §19 References — New Normative Entries

Add the following to the normative references:

```
[RFC6454]  Barth, A., "The Web Origin Concept", RFC 6454,
           December 2011.
           <https://www.rfc-editor.org/info/rfc6454>

[RFC6960]  Santesson, S., Myers, M., Ankney, R., Malpani, A.,
           Galperin, S., and C. Adams, "X.509 Internet Public Key
           Infrastructure Online Certificate Status Protocol - OCSP",
           RFC 6960, June 2013.
           <https://www.rfc-editor.org/info/rfc6960>

[RFC7636]  Sakimura, N., Ed., Bradley, J., and N. Agarwal, "Proof
           Key for Code Exchange by OAuth Public Clients", RFC 7636,
           September 2015.
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

[RFC8785]  Rundgren, A., Jordan, B., and S. Erdtman, "JSON
           Canonicalization Scheme (JCS)", RFC 8785, June 2020.
           <https://www.rfc-editor.org/info/rfc8785>

[RFC9068]  Bertocci, V., "JSON Web Token (JWT) Profile for OAuth 2.0
           Access Tokens", RFC 9068, October 2021.
           <https://www.rfc-editor.org/info/rfc9068>

[RFC9728]  Jones, M., Parecki, A., and F. Skokan, "OAuth 2.0
           Protected Resource Metadata", RFC 9728, December 2024.
           <https://www.rfc-editor.org/info/rfc9728>
```

### §19 References — New Informative Entry

```
OWASP LLM Top 10 — OWASP Foundation, "OWASP Top 10 for Large
           Language Model Applications".
           <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
```

### Normative Requirements

1. Every RFC cited normatively in the spec MUST have a corresponding
   entry in §19.
2. Reference entries MUST follow IETF citation format.

### Failure Conditions

No new error codes.

### Schema Changes

No schema changes.

## Security Considerations

This proposal introduces no new threat vectors. It is a references-only
change.

## Backwards Compatibility

Fully backwards compatible. References are non-normative metadata.

## Test Vectors

This proposal requires no new test vectors.

## References

### Normative References

   [RFC2119]  <https://www.rfc-editor.org/info/rfc2119>
   [RFC8174]  <https://www.rfc-editor.org/info/rfc8174>

## Changelog

- 2026-04-12 — Initial draft.
