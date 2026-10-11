---
title: "Practice: investigate recurring nighttime service crashes"
type: problem
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Practice: investigate recurring nighttime service crashes

[System Administration](../system-administration.md) · [Logs and metrics](../service-logs-and-metrics.md)

The owner supplied the Section 4.4 material on 2026-10-11 at 03:48. This page gives an English summary or a suggested solution. The vault does not store the original text or log transcripts. The agent read the official references on 2026-10-11. The examples are not student measurements. The agent did not execute the commands.

## Task and status

Example scenario: a service failed twice overnight during one week without an obvious external trigger. Choose useful evidence and explain why HTTP access logs may be less informative than service logs and memory observations. No actual crash times, logs, metric samples or student attempt have been supplied. This is an agent-written investigation plan, not a diagnosis.

## Investigation sequence

1. Record the exact event times and timezone.
2. Identify the affected unit or container.
3. Check for a host reboot.
4. Check for an operator restart or scheduled restart.
5. Keep evidence from before and after each failure.
6. Examine the complete service records: exception messages, exit code, termination signal, failed dependency, and restart attempts. A manager state of “running” after recovery does not show why the previous process ended.
7. Examine kernel records for out-of-memory kills, storage errors, and other events in the same time interval. A SIGKILL or exit code 137 alone does not prove an OOM kill.
8. Compare memory availability, swap use, load, filesystem space, and inode counts over time. Current readings are a starting point, not historical evidence.
9. Compare proxy errors and request traffic with the failure interval. Check scheduled maintenance if timing repeats. Nighttime occurrence alone does not identify a cause.

Example queries, with the actual interval chosen for the incident:

```sh
sudo journalctl -u my-app.service --since yesterday --until today --no-pager
sudo journalctl -k --since yesterday --until today --no-pager
sudo journalctl --list-boots
uptime
free -h
df -h
df -i
```

`yesterday` and `today` select midnight boundaries in the local time context. Use explicit timestamps for a real incident. For an earlier boot, select the relevant boot rather than relying on the current kernel journal. Available history depends on retention. [journalctl](https://manpages.debian.org/testing/systemd/journalctl.1.en.html).

## Why memory and service evidence come first

A memory leak, cgroup memory limit or system-wide pressure can terminate a process even when few HTTP requests occur. Unit and kernel records may identify the termination and restart sequence. After a restart, `free -h` can look normal because the process released its memory. Repeated samples before failure are more useful.

For a Docker workload, inspect its limits and actual state as well as host memory. `docker inspect my-app` can expose container state and configuration. Redact sensitive environment values before sharing. [Docker inspect](https://docs.docker.com/reference/cli/docker/inspect/).

Access logs describe requests and responses, not memory allocation or every process failure. A quiet service can crash without a revealing access entry. Traffic increases or upstream errors can help compare demand with failure. Thus, access logs still supply useful evidence.

## Hypotheses and discriminating evidence

| Hypothesis | Evidence that would support it | What would not suffice |
| --- | --- | --- |
| Memory exhaustion | OOM records naming the process/cgroup plus memory trends | Exit code 137 alone |
| Application defect | Exception or abort preceding termination | A generic proxy 502 |
| Storage pressure | Failed writes, full filesystem or exhausted inodes | A healthy disk-space reading after cleanup |
| Scheduled activity | Timer/maintenance events aligned with both failures | Both failures being at night |
| Traffic pressure | Request-rate increase aligned with resource pressure | A high load snapshot without timing |

This table is diagnostic reasoning. No hypothesis has been confirmed. See [logs and metrics](../service-logs-and-metrics.md) for field meanings and observation limits.

## Next evidence and recall

Record the actual interval, unit termination result, relevant kernel events and available resource samples. Then state the strongest supported explanation and what remains unknown. Do not turn a plan into a completed lab record.

1. What evidence distinguishes OOM termination from another SIGKILL?
2. Why can post-restart memory look healthy?
3. What can access logs show, and what can they not show?
4. How would you compare the two failure windows consistently?

The agent did not execute commands against a service. The agent did not investigate a real incident. This note remains a draft.
