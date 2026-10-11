---
title: "Image registries, tags and distribution"
type: concept
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Image registries, tags and distribution

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

The agent wrote this study note from the Module 3 review that the owner supplied on 2026-10-11 at 01:38. Official documents give additional information. The exact course sections and software versions are unknown. The agent did not recover the original lecture or do the example procedures. The vault does not store the original text. The agent read the official references on 2026-10-11.

## Naming and identity

A registry stores and serves image content. A repository groups image references within that registry. A tag is a readable reference that can move. A digest identifies content.

An explicit reference has the form `HOST[:PORT]/NAMESPACE/IMAGE[:TAG]`. Docker defaults to Docker Hub when a registry is omitted. [Image tagging](https://docs.docker.com/reference/cli/docker/image/tag/).

## Distribution workflow

Assume `study-web:demo` already exists locally, and an example registry is reachable with valid authentication and TLS:

```sh
docker tag study-web:demo registry.example.com/study/web:demo
docker login registry.example.com
docker push registry.example.com/study/web:demo
```

The hostname is example and is not a configured service. Tagging creates a local reference. Pushing transfers content and requires upload permission. Do not put passwords into tracked scripts. [Image push](https://docs.docker.com/reference/cli/docker/image/push/).

On another engine, pulling the same reference retrieves the image:

```sh
docker pull registry.example.com/study/web:demo
```

A later pull of a mutable tag can select different content. A pull with `IMAGE@sha256:DIGEST` selects specified content. Replace the placeholder with the digest of the required image. Digest pinning does not by itself show publisher trust. [Image pull](https://docs.docker.com/reference/cli/docker/image/pull/).

## Reachability and common errors

`localhost:5000/study/web:demo` addresses a registry in the engine's loopback network context. Another machine's `localhost` does not reach the first machine. Use a reachable registry host and the correct port. Registry transport settings, authentication and image names are separate concerns.

An image on one engine is not automatically available to another engine. A local tag is not an upload. A tag named `latest` is not a promise of the most recent semantic version.

## Recall

1. How do registry, repository, tag and digest differ?
2. Which step actually uploads content?
3. What breaks when a localhost reference is reused on another machine?
4. Why can a tag change while an image's content remains immutable?

Related: [Dockerfiles](dockerfile-and-build-cache.md) and [Compose](docker-compose.md).
