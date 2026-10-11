---
title: "systemd service lifecycle and container supervision"
type: lecture
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# systemd service lifecycle and container supervision

[System Administration](system-administration.md) · [Nginx reverse proxy](nginx-reverse-proxy.md) · [Logs and metrics](service-logs-and-metrics.md)

The owner supplied the Section 4.3 material on 2026-10-11 at 02:52. This English summary includes corrections from official references. The vault does not store the original text. The commands are study examples. The agent did not do these procedures. The agent read the references on 2026-10-11.

## Terminal commands and managed services

A foreground process can depend on its terminal session. Terminal closure does not stop every program. The Docker daemon manages the earlier `docker run -d` container. Its terminal can close without a container stop.

Docker can manage restarts itself. A systemd wrapper is an alternative when its lifecycle integration is needed. Do not combine competing Docker restart policies and an external restart manager. [Docker restart guidance](https://docs.docker.com/engine/containers/start-containers-automatically/).

## PID 1 and namespaces

PID 1 is the init process in a PID namespace. systemd usually has this role on a host. A container can use an application or a small init process instead. A subreaper can collect the exit status of orphan processes. If no subreaper applies, the namespace init does this task.

Host init termination and container init termination have different scope. If a container namespace's init exits, the kernel terminates other processes in that namespace. This does not cause a host-wide kernel panic. [PID namespaces](https://manpages.debian.org/testing/manpages/pid_namespaces.7.en.html).

Inspect the environment with `ps -p 1 -o pid,comm,args` or `cat /proc/1/status`. A course example is not a new local observation.

## Example Docker wrapper

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

`After` sets the order of start jobs. It does not start Docker by itself. `Requires` adds the dependency. With ordering, a failed dependency activation prevents this start. Neither directive proves application readiness or guarantees recovery after every Docker daemon restart.

`WantedBy` provides enablement information. [Unit dependencies](https://manpages.debian.org/testing/systemd/systemd.unit.5.en.html).

The attached Docker client is the service's main process. Docker and its runtime manage the container processes. `Restart=on-failure` responds to qualifying service failures, not every clean exit or failed HTTP check. `ExecStop` clearly requests container shutdown. Client exit status and daemon interruptions need runtime testing before assuming full container supervision. [Service semantics](https://manpages.debian.org/testing/systemd/systemd.service.5.en.html).

Write each directive on a separate line in its section. Do not use a semicolon in place of unit-file line breaks. The unit is a study example, not a deployed service.

## Load, enable, start and inspect

After you install the unit at `/etc/systemd/system/my-app.service`, use these commands:

```sh
sudo systemctl daemon-reload
sudo systemctl enable my-app.service
sudo systemctl start my-app.service
systemctl status my-app.service
systemctl is-enabled my-app.service
journalctl -u my-app.service -n 50 --no-pager
```

`daemon-reload` reloads manager configuration, not application configuration. `enable` installs the correct links for target activation. It does not start the unit immediately. `start` activates it now without enabling future boot activation. `enable --now` combines them.

`status` reports manager state, main PID and recent logs, not always application health. A stop does not disable the unit. A disable command does not stop the unit unless you request a stop. [systemctl](https://manpages.debian.org/testing/systemd/systemctl.1.en.html).

## Recall and limits

1. Why does a detached Docker container not need an open SSH session?
2. How do `After` and `Requires` differ?
3. What is the main process of this wrapper, and why does that matter?
4. What does `Restart=on-failure` leave uncovered?
5. How do enablement, immediate start and application readiness differ?
6. Why does losing PID 1 inside a container differ from losing host init?

The agent did not install, enable, or start a service for this note. The note does not copy the supplied course test results or identify them as student evidence. The agent could not retrieve the freedesktop manuals. The agent used the linked systemd manuals on the Debian website instead. This note remains a draft.
