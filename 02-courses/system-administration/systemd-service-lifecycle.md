---
title: "systemd service lifecycle and container supervision"
type: lecture
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# systemd service lifecycle and container supervision

[System Administration](system-administration.md) · [Nginx reverse proxy](nginx-reverse-proxy.md) · [Logs and metrics](service-logs-and-metrics.md)

English summary of owner-supplied Section 4.3 material dated 2026-10-11 at 02:52, with official-reference corrections. Original text is not retained. Commands are proposed study examples, not completed work or a recorded student attempt. References were consulted on 2026-10-11.

## Terminal commands and managed services

A foreground process can depend on terminal/session behavior, but terminal closure does not universally stop every program. In particular, the earlier `docker run -d` container is managed by the Docker daemon and does not require the launching terminal to remain open. Docker can manage restarts itself; a systemd wrapper is an alternative when its lifecycle integration is needed. Do not combine competing Docker restart policies and an external restart manager. [Docker restart guidance](https://docs.docker.com/engine/containers/start-containers-automatically/).

## PID 1 and namespaces

PID 1 is the init process in a PID namespace. systemd commonly occupies this role on a host; a container may instead run an application or a small init process. Orphan reaping can be handled by a subreaper, otherwise by the namespace init. Host init termination and container init termination have different scope: when a container namespace's init exits, the kernel terminates remaining processes in that namespace; this is not a host-wide kernel panic. [PID namespaces](https://manpages.debian.org/testing/manpages/pid_namespaces.7.en.html).

Inspect the actual environment with `ps -p 1 -o pid,comm,args` or `cat /proc/1/status`; no supplied course example is treated as a new local observation.

## Illustrative Docker wrapper

Assume a rootful Docker service and an existing stopped container named `my-app`, with Docker restart policy disabled. This unit neither builds an image nor creates the container. Confirm the installed Docker executable path before using it.

```ini
[Unit]
Description=Study application container
Requires=docker.service
After=docker.service

[Service]
Type=simple
ExecStart=/usr/bin/docker start -a my-app
ExecStop=/usr/bin/docker stop -t 10 my-app
Restart=on-failure
RestartSec=5
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
```

`After` orders start jobs; it does not pull in Docker on its own. `Requires` adds the dependency; with ordering, a failed dependency activation prevents this start. Neither directive proves application readiness or automatically guarantees recovery after every Docker daemon restart. `WantedBy` provides enablement information. [Unit dependencies](https://manpages.debian.org/testing/systemd/systemd.unit.5.en.html).

The attached Docker client is the service's main process; the container's processes are managed by Docker and its runtime. `Restart=on-failure` responds to qualifying service failures, not every clean exit or failed HTTP check. `ExecStop` explicitly requests container shutdown. Client exit status and daemon interruptions need runtime testing before assuming full container supervision. [Service semantics](https://manpages.debian.org/testing/systemd/systemd.service.5.en.html).

Each directive belongs on its own line in its section. A semicolon cannot be used as a general substitute for unit-file line breaks. The unit is a study example, not a deployed service.

## Load, enable, start and inspect

After deliberately installing a unit at `/etc/systemd/system/my-app.service`:

```sh
sudo systemctl daemon-reload
sudo systemctl enable my-app.service
sudo systemctl start my-app.service
systemctl status my-app.service
systemctl is-enabled my-app.service
journalctl -u my-app.service -n 50 --no-pager
```

`daemon-reload` reloads manager configuration, not application configuration. `enable` installs the appropriate links for target activation; it does not start the unit immediately. `start` activates it now without enabling future boot activation. `enable --now` combines them. `status` reports manager state, main PID and recent logs, not necessarily application health. Stopping a unit does not disable it; disabling it does not stop it unless requested. [systemctl](https://manpages.debian.org/testing/systemd/systemctl.1.en.html).

## Recall and limits

1. Why does a detached Docker container not need an open SSH session?
2. How do `After` and `Requires` differ?
3. What is the main process of this wrapper, and why does that matter?
4. What does `Restart=on-failure` leave uncovered?
5. How do enablement, immediate start and application readiness differ?
6. Why does losing PID 1 inside a container differ from losing host init?

No service was installed, enabled or started for this note. The supplied course's test results are not copied or adopted as student evidence. Upstream freedesktop manual retrieval failed; the linked Debian-hosted systemd manual pages were used instead. Draft status remains.
