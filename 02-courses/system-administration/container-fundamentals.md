---
title: "Container images, lifecycle and data"
type: concept
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Container images, lifecycle and data

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

Reconstructed study note based on the owner's Module 3 review supplied on 2026-10-11 at 01:38, supplemented by official documentation. This is not a recovered lecture transcript. Exact course section mapping and environment versions are unconfirmed. Examples are illustrative and have not been run; original source text is not stored. Official references were consulted on 2026-10-11.

## Image and container

An image is immutable content plus runtime configuration. Building again creates new image content; a tag can be moved to point at a different image. A container is an instance of an image and can be created, running, exited or removed. Multiple containers can use the same image independently. [Image fundamentals](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/).

Linux containers share the kernel of the environment running the engine. Namespaces isolate views of resources; cgroups govern resource accounting and limits. A VM has a guest kernel. Docker Desktop commonly runs Linux containers in a Linux VM. See the comparison in [Module 3 review](module-3-review.md).

## Lifecycle example

Illustrative commands, not a recorded deployment:

```sh
docker run -d --name study-web -p 127.0.0.1:8080:80 nginx:stable
docker ps
docker ps -a
docker logs study-web
docker stop study-web
docker start study-web
```

`run` creates and starts a container. `ps` lists running containers, while `ps -a` also shows stopped ones. The mapping exposes container port 80 at host loopback port 8080. A foreground process exiting normally ends the container; detached mode does not keep a finished process alive. [Container run reference](https://docs.docker.com/engine/containers/run/).

## Data lifetime

Stopping a container retains its writable layer; removing the container discards that layer. Named volumes have a lifecycle separate from individual containers. Bind mounts expose a specified host path. Use either deliberately for data that must outlive container replacement; neither is automatically a backup. [Docker volumes](https://docs.docker.com/engine/storage/volumes/).

## Common mistakes and recall

Do not confuse host ports with container ports, a stopped container with a removed one, or image immutability with persistent application data. `localhost` inside a container refers to that container's network context.

1. Why can two containers share an image but store different changes?
2. What survives stop, and what can be lost on removal?
3. Where should database data live if the container is replaceable?

Continue with [Dockerfiles](dockerfile-and-build-cache.md) and [Compose](docker-compose.md).
