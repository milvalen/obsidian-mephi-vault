---
title: "Docker Compose services, readiness and persistence"
type: concept
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Docker Compose services, readiness and persistence

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

Reconstructed study note based on the owner's Module 3 review supplied on 2026-10-11 at 01:38, supplemented by official documentation. This is not a recovered lecture transcript. Exact course section mapping and environment versions are unconfirmed. Examples are illustrative and have not been run; original source text is not stored. Official references were consulted on 2026-10-11.

## Declarative application model

Compose describes services, networks and volumes together. A service is a configuration for containers; it is not itself an image or a single fixed container. `compose.yaml` is the preferred filename. [Compose CLI](https://docs.docker.com/reference/cli/docker/compose/).

## Study example

This hypothetical database/client setup illustrates readiness and persistent storage; it has not been run:

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

The one-shot client exits after its check; it is not a persistent application. The local password value is supplied outside tracked files. The volume path is specific to PostgreSQL image version 17; later major versions can use different paths. [Official PostgreSQL image documentation](https://github.com/docker-library/docs/blob/master/postgres/README.md).

## Network and startup

The client reaches `db` by service name on the shared network. No host database port is needed for this connection. [Compose networking](https://docs.docker.com/compose/how-tos/networking/).

Short-form dependencies order startup. `service_healthy` also waits for a configured health check; this does not guarantee every query succeeds later. Applications still need retries and reconnect logic. [Startup order](https://docs.docker.com/compose/how-tos/startup-order/).

## Lifecycle commands

`docker compose config` resolves and validates configuration; interpolation can reveal supplied values, so do not publish its output blindly. `docker compose up -d` creates or starts services; `ps` reports state and `logs` helps diagnose exits. `docker compose down` removes service containers and project networks; adding `-v` also removes declared named volumes and anonymous volumes. External volumes remain untouched. See [Compose config](https://docs.docker.com/reference/cli/docker/compose/config/) and [Compose down](https://docs.docker.com/reference/cli/docker/compose/down/).

## Recall

1. Why is `db:5432` different from a host port mapping?
2. What changes when `service_healthy` is used?
3. Why does the example client exit?
4. How can a volume survive container replacement?
