---
title: System Administration
type: course
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-26
---
# System Administration

[Courses](../courses.md) · [Home](../../../../README.md)

The owner named this field of study on 2026-10-11. The official course title and syllabus remain unknown.

## Course context

The semester, instructor, course code, and prerequisites are unknown.

## Syllabus and sources

The owner supplied RPM and digital signature material on 2026-10-11 at 01:33. The owner supplied a Module 3 summary on 2026-10-11 at 01:38. The owner supplied a Module 4 introduction on 2026-10-11 at 02:33. The owner did not supply the full syllabus, textbooks, or official course title. See [Sources](../../../../05-sources/sources.md).

## Lectures and concepts

- [Optional observability: eBPF and OpenTelemetry](ebpf-and-opentelemetry.md) — ungraded demonstration and evidence limits.

- [WAF, ModSecurity and OWASP CRS](waf-modsecurity-and-crs.md) — ungraded demonstration, HTTP inspection and anomaly scoring.
- [Service logs, metrics and health](service-logs-and-metrics.md) — Section 4.4 journald, Nginx logs and resource trends.
- [TLS certificates and Nginx HTTPS](tls-certificates-and-nginx.md) — Section 4.3 certificate trust, lab generation and HTTPS setup.
- [systemd service lifecycle and container supervision](systemd-service-lifecycle.md) — Section 4.3 units, dependencies, enable/start and PID 1.
- [Nginx web serving and reverse proxying](nginx-reverse-proxy.md) — static/dynamic content, proxy configuration, package layouts and graceful reload.
- [Module 4: the path from browser to service](module-4-request-path.md) — ports, listening addresses, DNS, HTTP, TLS and layered diagnosis.
- [Module 3 review: software delivery and storage](module-3-review.md) — packages, containers, Compose, registries, RAID and LVM.
- [RPM packages and digital signatures](rpm-and-digital-signatures.md) — RPM structure, spec files, GPG and APT/DNF verification.

## Reconstructed Module 3 topics

- [Software delivery, dependencies and archives](software-delivery.md)
- [APT and DNF package management](apt-and-dnf.md)
- [Container images, lifecycle and data](container-fundamentals.md)
- [Dockerfiles and build caching](dockerfile-and-build-cache.md)
- [Docker Compose services, readiness and persistence](docker-compose.md)
- [Image registries, tags and distribution](image-registries.md)
- [RAID layouts, capacity and Linux mdadm](raid-and-mdadm.md)
- [LVM allocation and filesystem growth](lvm-and-filesystem-growth.md)

These notes reconstruct topics named in the supplied review. They do not claim to reproduce missing course lectures or unseen test questions.

## Problems and laboratories

- [Practice: recurring nighttime crashes](practice/nighttime-service-crashes.md) — proposed evidence collection and hypothesis testing. No actual crash reported.
- [Practice: route legacy and new applications](practice/nginx-two-app-routing.md) — worked configuration and slash behavior. Not deployed.
- [Practice: RAID 1 with loop devices](practice/raid1-loop-devices.md) — owner-reported array inspection.

The reported `/dev/md0` RAID 1 array has 499 MiB capacity. Both `/dev/loop0` and `/dev/loop1` are active. No devices failed. The owner did not report formatting or mounting.

Use the [problem template](../../../../90-templates/problem.md) or [lab template](../../../../90-templates/lab.md). Preserve attempts and distinguish reported observations from independently verified results.

## Review and assessment

The supplied material describes the RPM block as an ungraded demonstration. The Module 3 summary refers to a final module test in Section 6. The owner did not supply its questions, grading rules, or date. General assessment requirements and deadlines remain unknown. Recall questions are included in the note. Record actual attempts with the [review template](../../../../90-templates/review.md).

## Connections

Add links to related notes after you add material.

## Open questions

- What is the official course title and syllabus?
- Which materials and assessment requirements apply?
