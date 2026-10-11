---
title: "Container images, lifecycle and data"
type: concept
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Container images, lifecycle and data

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

The agent wrote this study note from the Module 3 review that the owner supplied on 2026-10-11 at 01:38. Official documents give additional information. The exact course sections and software versions are unknown. The agent did not recover the original lecture or do the example procedures. The vault does not store the original text. The agent read the official references on 2026-10-11.

## Image and container

An image is immutable content plus runtime configuration. A new build creates new image content. A tag can refer to a different image after an update. A container is an instance of an image and can be created, running, exited or removed. Multiple containers can use the same image independently. [Image fundamentals](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/).

Linux containers share the kernel of the environment running the engine. Namespaces isolate views of resources. Cgroups govern resource accounting and limits. A VM has a guest kernel. Docker Desktop usually runs Linux containers in a Linux VM. See the comparison in [Module 3 review](module-3-review.md).

## Lifecycle example

Example commands, not a recorded deployment:

```sh
docker run -d --name study-web -p 127.0.0.1:8080:80 nginx:stable
docker ps
docker ps -a
docker logs study-web
docker stop study-web
docker start study-web
```

`run` creates and starts a container. `ps` lists running containers, while `ps -a` also shows stopped ones. The mapping exposes container port 80 at host loopback port 8080. A foreground process exiting normally ends the container. Detached mode does not keep a finished process alive. [Container run reference](https://docs.docker.com/engine/containers/run/).

## Data lifetime

A stopped container keeps its writable layer. Container removal discards that layer. Named volumes have a lifecycle separate from individual containers.

Bind mounts expose a specified host path. Use a volume or bind mount for data that must remain after container replacement. Neither automatically supplies a backup. [Docker volumes](https://docs.docker.com/engine/storage/volumes/).

## Common mistakes and recall

Keep these differences clear:

- A host port is not a container port.
- A stopped container is not a removed container.
- An immutable image does not make application data persistent. `localhost` inside a container refers to that container's network context.

1. Why can two containers share an image but store different changes?
2. What survives stop, and what can be lost on removal?
3. Where should database data live if the container is replaceable?

Continue with [Dockerfiles](dockerfile-and-build-cache.md) and [Compose](docker-compose.md).
