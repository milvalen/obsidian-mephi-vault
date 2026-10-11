---
title: "Docker Compose services, readiness and persistence"
type: concept
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Docker Compose services, readiness and persistence

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

The agent wrote this study note from the Module 3 review that the owner supplied on 2026-10-11 at 01:38. Official documents give additional information. The exact course sections and software versions are unknown. The agent did not recover the original lecture or do the example procedures. The vault does not store the original text. The agent read the official references on 2026-10-11.

## Declarative application model

Compose describes services, networks and volumes together. A service is a configuration for containers. It is not itself an image or a single fixed container. `compose.yaml` is the preferred filename. [Compose CLI](https://docs.docker.com/reference/cli/docker/compose/).

## Study example

This example shows a database and a client. It shows a readiness check and persistent storage. The agent did not execute the example:

```yaml
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: study
      POSTGRES_PASSWORD: "${STUDY_DB_PASSWORD:?Set a local study password}"
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U study"]
      interval: 5s
      timeout: 3s
      retries: 10
  client:
    image: postgres:17
    command: ["pg_isready", "-h", "db", "-U", "study"]
    depends_on:
      db:
        condition: service_healthy
volumes:
  db-data:
```

The client executes one check and exits. It is not a persistent application. Supply the local password outside files tracked by Git. The volume path is specific to PostgreSQL image version 17. Later major versions can use different paths. [Official PostgreSQL image documentation](https://github.com/docker-library/docs/blob/master/postgres/README.md).

## Network and startup

The client reaches `db` by service name on the shared network. No host database port is needed for this connection. [Compose networking](https://docs.docker.com/compose/how-tos/networking/).

Short-form dependencies order startup. `service_healthy` also waits for a configured health check. This does not guarantee every query succeeds later. Applications still need retries and reconnect logic. [Startup order](https://docs.docker.com/compose/how-tos/startup-order/).

## Lifecycle commands

`docker compose config` resolves and validates the configuration. Its output can show supplied values. Examine this output before publication.

`docker compose up -d` creates or starts services. `ps` shows their state. `logs` helps identify the cause of an exit.

`docker compose down` removes service containers and project networks. Adding `-v` also removes declared named volumes and anonymous volumes. External volumes remain untouched. See [Compose config](https://docs.docker.com/reference/cli/docker/compose/config/) and [Compose down](https://docs.docker.com/reference/cli/docker/compose/down/).

## Recall

1. Why is `db:5432` different from a host port mapping?
2. What changes when `service_healthy` is used?
3. Why does the example client exit?
4. How can a volume survive container replacement?
