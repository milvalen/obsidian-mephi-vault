---
title: "Service logs, metrics and health"
type: lecture
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Service logs, metrics and health

[System Administration](system-administration.md) · [Service lifecycle](systemd-service-lifecycle.md)

English summary or worked reasoning based on owner-supplied Section 4.4 material dated 2026-10-11 at 03:48. Original text and example log transcripts are not retained. Official references were consulted on 2026-10-11. Course examples are not student measurements; commands below were not executed.

## Running versus healthy

Process existence does not prove successful requests, sufficient resources or correct behavior. Logs describe events; metrics describe measured state over time. Request probes and application-specific checks provide additional evidence. These are complementary sources, not the only possible means of observation.

The supplied material identifies this section as the end of the mandatory course content before integrated deployment practice. That is reported course context; no completion or assessment result is recorded.

## Where logs actually go

A systemd service's stdout/stderr commonly go to journald, but unit output settings can redirect them. Journald also accepts other sources such as kernel events and syslog. It stores structured entries in journal files rather than plain line-oriented logs. [journald service](https://manpages.debian.org/testing/systemd/systemd-journald.service.8.en.html).

Fields include message, priority, timestamps, process identity and unit information. `journalctl` renders them as text or structured output; APIs and other tools can read the journal too. Do not use `cat` or text `grep` as a substitute for decoding raw journal files. Text filtering can follow `journalctl` output. [Journal fields](https://manpages.debian.org/testing/systemd/systemd.journal-fields.7.en.html).

```sh
sudo journalctl -u my-app.service -f
sudo journalctl -u my-app.service --since "10 minutes ago" --no-pager
sudo journalctl -u my-app.service -u nginx.service --since today --no-pager
sudo journalctl -u my-app.service -p err --since today --no-pager
```

`-f` follows new entries. Multiple units support timeline correlation; `-p err` selects error and more severe priorities. Application text containing the word “error” is not necessarily assigned that journal priority, so start investigations without a priority restriction. [journalctl](https://manpages.debian.org/testing/systemd/journalctl.1.en.html).

Persistence depends on `Storage` configuration: journals can be volatile under `/run/log/journal` or persistent under `/var/log/journal`. Retention and rate limits can remove or suppress evidence. [journald configuration](https://manpages.debian.org/testing/systemd/journald.conf.5.en.html).

For the attached Docker wrapper in [Section 4.3](systemd-service-lifecycle.md), application output can reach journald through the attached client. Docker's own logging driver is separate; do not assume every detached container's output appears under the wrapper's unit.

## Nginx access and error logs

Logging destinations and formats are configurable. Package installations often use `/var/log/nginx/`; official Nginx container images route access/error output to stdout/stderr for Docker collection. [Docker logging guidance](https://docs.docker.com/engine/logging/).

Typical `combined` access fields are:

| Field | Interpretation |
| --- | --- |
| Remote address | Peer address as interpreted by configuration |
| Literal `-` | Placeholder; not a retrieved remote logname |
| Remote user | HTTP-authenticated user, when available |
| Local time | Request timestamp with offset |
| Request | Method, target and protocol rendering |
| Status | Response status |
| Body bytes sent | Bytes excluding response headers |
| Referer / User-Agent | Client-provided headers |

The supplied example adds a final X-Forwarded-For field; it is not part of Nginx's default `combined` format. Access logging can be disabled, conditional or buffered. Peer and forwarded addresses require a trusted proxy configuration before being treated as original-client identity. [Nginx access logging](https://nginx.org/en/docs/http/ngx_http_log_module.html).

Error logs record configured severity levels, not one mandatory entry per failed request. A missing static file can generate a filesystem-open error, but an upstream application's 404 need not create the same error entry. [Nginx error logging](https://nginx.org/en/docs/ngx_core_module.html#error_log).

```sh
sudo tail -F /var/log/nginx/access.log
sudo tail -F /var/log/nginx/error.log
```

These examples assume real files at those paths. `tail -F` follows by name and retries across replacement during rotation. [GNU tail manual](https://manpages.debian.org/testing/coreutils/tail.1.en.html).

## Resource trends

| Command | What it contributes | Interpretation limit |
| --- | --- | --- |
| `uptime` | Uptime and 1/5/15-minute load averages | Load is not CPU percentage |
| `free -h` | RAM/swap snapshot, including available memory | Host totals do not show every container limit |
| `df -h` | Filesystem space use | Does not directly measure a disk's health |

Linux load averages include runnable tasks and tasks in uninterruptible sleep, often waiting for I/O. Relate load to CPU count and workload rather than declaring a fixed universal threshold. [uptime](https://manpages.debian.org/testing/procps/uptime.1.en.html). `available` estimates RAM usable for new work without swapping; cached memory is not automatically a leak. [free](https://manpages.debian.org/testing/procps/free.1.en.html). [df reference](https://manpages.debian.org/testing/coreutils/df.1.en.html).

Timestamp repeated observations. A rising trend can reveal resource pressure; a single post-crash snapshot cannot reconstruct the peak. Inspect inode availability with `df -i` when writes fail despite apparent free space.

## Recall and limits

1. Why can `active (running)` coexist with failed HTTP requests?
2. Why might journal priority filtering miss an application's error message?
3. How can volatile storage erase earlier-boot evidence?
4. Which access-log dash is a literal format placeholder?
5. Why does an application 404 not imply a missing static file?
6. Why is load average different from CPU utilization?

No logging destinations or current resource usage were verified on the practice VM. Continue with [the nighttime-crash investigation](practice/nighttime-service-crashes.md).
