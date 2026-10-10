---
title: "Dockerfiles and build caching"
type: concept
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Dockerfiles and build caching

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

Reconstructed study note based on the owner's Module 3 review supplied on 2026-10-11 at 01:38, supplemented by official documentation. This is not a recovered lecture transcript. Exact course section mapping and environment versions are unconfirmed. Examples are illustrative and have not been run; original source text is not stored. Official references were consulted on 2026-10-11.

## Build-time versus runtime

A Dockerfile describes image construction. `FROM` selects a base; `WORKDIR` sets the working directory; `COPY` copies build-context files; `RUN` executes during the build. `CMD` supplies the default runtime command or arguments. `ENTRYPOINT` defines the executable entry point; exec-form `CMD` can supply its defaults. A runtime override depends on their combination. `EXPOSE` documents a port but does not publish it. [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

## Minimal study example

Suppose an existing directory contains `index.html` and this `Dockerfile`:

```dockerfile
FROM nginx:stable
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
```

The example inherits the base image's startup configuration. Build and run commands are illustrative:

```sh
docker build -t study-web:demo .
docker run -d --name study-web-demo -p 127.0.0.1:8081:80 study-web:demo
```

The final `.` is the build context; `COPY` resolves its source from that context. The `-t` flag names the resulting image. This example has not been deployed.

## Cache reasoning

A builder can reuse a step when its instruction and relevant inputs match. Changing a copied file invalidates that step and normally the following steps. Put stable dependency inputs before frequently edited application files. For example, copying a dependency manifest, installing dependencies, and then copying application code can reuse installation after a code-only edit.

`RUN` cache checks do not inspect remote repositories for newly published packages. A cached install command can therefore reuse old results. Cache efficiency and obtaining fresh dependencies are separate requirements. [Cache invalidation](https://docs.docker.com/build/cache/invalidation/).

## Common mistakes and recall

`CMD` does not run at build time. Adding `EXPOSE` does not make a host port reachable. Tags such as `stable` can change; choose version or digest constraints deliberately when reproducing builds. See [registries](image-registries.md).

1. What does the build context control?
2. Which step runs before any container exists?
3. Why place dependency manifests before application source?
4. Why can an unchanged install command reuse stale content?
