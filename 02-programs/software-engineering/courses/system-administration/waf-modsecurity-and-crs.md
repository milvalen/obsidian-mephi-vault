---
title: WAF, ModSecurity and OWASP CRS
type: lecture
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-11
course: System Administration
tags:
  - security
  - http
  - waf
---
# WAF, ModSecurity and OWASP CRS

[System Administration](system-administration.md) · [Nginx reverse proxy](nginx-reverse-proxy.md) · [Logs and metrics](service-logs-and-metrics.md)

## Course context

The owner supplied this material on 2026-10-11 at 04:47. This page gives an English summary. The material describes an ungraded demonstration that is not required for passing the course. Its exact section number is unknown.

It references reverse proxying in Section 4.2 and RPM packaging in Section 3.7. The vault does not store the original text or log transcripts. The student did not report a demonstration.

## Inspection at the HTTP boundary

A web application firewall inspects HTTP transactions, including request targets, headers and supported body content. A network firewall typically controls lower-layer traffic using addresses, protocols and ports. A reverse-proxy integration can inspect traffic before forwarding it to the application. A separate WAF proxy can provide the same boundary.

Inspection requires readable HTTP content. The TLS endpoint must decrypt HTTPS traffic before this inspection. Direct access to an unprotected upstream can bypass the intended boundary. Response inspection can also occur after the application has handled a request.

A WAF adds defense in depth. It does not repair vulnerable application code or guarantee detection of every attack. Request inspection is not source-code review. Engines can evaluate rules, transformations and other detection logic rather than only matching literal text strings. [ModSecurity engine](https://github.com/owasp-modsecurity/ModSecurity).

## Engine versus rule set

| Component | Role |
| --- | --- |
| ModSecurity | Inspection engine and rule language |
| Web-server connector | Integrates the engine with the server, such as Nginx |
| OWASP Core Rule Set (CRS) | Maintained generic detection rules used by a compatible engine |

ModSecurity v3 separates the engine library from its web-server connector. CRS includes coverage for common threats such as SQL injection, cross-site scripting and file/path attacks. Package availability and compatibility depend on the distribution, server and engine versions. Do not assume every distribution ships the same Nginx module. [ModSecurity project](https://github.com/owasp-modsecurity/ModSecurity).

## Anomaly scoring

In CRS anomaly-scoring mode, detection rules add scores and a separate evaluation decides whether to block. The policy compares the total score with a threshold. It can block when the score equals or exceeds that threshold.

The documented default inbound threshold is 5. A critical match usually adds 5. Thus one rule match can already reach the threshold. Multiple matches are not a requirement. CRS evaluates request and response scores separately. Response blocking does not mean the request never reached the application.

Synthetic example with threshold 5:

| Matching-rule contributions | Total | Score-based decision in blocking mode |
| --- | --- | --- |
| None | 0 | Pass this evaluation |
| One contribution of 3 | 3 | Pass this evaluation |
| Contributions of 3 and 2 | 5 | Block |
| One contribution of 5 | 5 | Block |

This calculation shows the documented model. It does not describe measured requests.

Detection-only mode records findings without enforcing the same blocking action. Other engine rules or policy decisions can also affect a transaction. [CRS anomaly scoring](https://coreruleset.org/docs/2-how-crs-works/2-1-anomaly_scoring/).

## Deployment and tuning

The project provides prebuilt images through `owasp/modsecurity-crs`, including documented server/engine variants. Select a compatible maintained image variant. Select an explicit tag or digest. Configure the backend. Check the enforcement and log settings.

A mutable image tag alone does not show which CRS version was used. [Official CRS container project](https://github.com/coreruleset/modsecurity-crs-docker).

A package or supported image can avoid managing a custom source build, but neither removes the need to understand updates, connectors, configuration and application compatibility. The agent did not download an image or start a container for this note.

Legitimate requests can resemble attacks and trigger false positives. Compare rule IDs, matched variables, scores, and transaction data. Understand the application input before you add an exclusion. Limit each exclusion to the necessary scope.

Broadly raising thresholds or disabling rules can hide real attacks. An allowed request is not proof that the application is safe. [CRS tuning guidance](https://coreruleset.org/docs/2-how-crs-works/2-3-false-positives-and-tuning/).

## Reported demonstration and evidence limits

The supplied material describes a normal request returning 200 and an SQL-injection-shaped query returning 403, with a libinjection-related detection and anomaly-threshold event. These are course-reported outcomes, not a live check by the owner or agent. The owner did not supply the exact image version, configuration, rule IDs, or score.

A 403 alone does not show that a WAF blocked the request. Applications and other proxy policies can return it too. To validate a local demonstration, use this procedure:

1. Compare the WAF audit event with the request and upstream observations.
2. Identify inbound blocking or response blocking.
3. Record the image version.
4. Record the effective policy. Do not infer vulnerability in the upstream from the presence of an attack-shaped test input.

## Recall and learning targets

Minimum: explain the WAF boundary and its defense-in-depth role.

Core: distinguish ModSecurity, its connector and CRS, and explain the benefit and limits of prebuilt deployment.

Advanced: explain score totals, thresholds, false positives, and why one match can cause a block. The student did not report completion.

1. Why does a WAF not replace fixing an application vulnerability?
2. Which component executes rules, and which supplies the generic rule set?
3. With threshold 5, can one match cause blocking?
4. Why does a response-side block not prove the request was stopped before execution?
5. What evidence ties a 403 to a specific WAF decision?
6. How can direct upstream access defeat the intended inspection boundary?

## Verification limits

The agent read the official project references on 2026-10-11. The agent did not deploy a WAF, send a test request, or inspect runtime logs. Distribution, image version and teaching-environment configuration remain unknown. The note remains a draft.
