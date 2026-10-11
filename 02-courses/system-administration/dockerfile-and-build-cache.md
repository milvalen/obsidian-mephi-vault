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

The agent wrote this study note from the Module 3 review that the owner supplied on 2026-10-11 at 01:38. Official documents give additional information. The exact course sections and software versions are unknown. The agent did not recover the original lecture or do the example procedures. The vault does not store the original text. The agent read the official references on 2026-10-11.

## Build-time versus runtime

A Dockerfile describes image construction. `FROM` selects a base. `WORKDIR` sets the working directory. `COPY` copies build-context files. `RUN` executes during the build.

`CMD` supplies the default runtime command or arguments. `ENTRYPOINT` specifies the executable entry point. In exec form, `CMD` can supply default arguments. A runtime override depends on their combination. `EXPOSE` documents a port but does not publish it. [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

## Minimal study example

Suppose an existing directory contains `index.html` and this `Dockerfile`:

```dockerfile
FROM nginx:stable
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
```

The example inherits the base image's startup configuration. Build and run commands are example:

```sh
docker build -t study-web:demo .
docker run -d --name study-web-demo -p 127.0.0.1:8081:80 study-web:demo
```

The final `.` is the build context. `COPY` resolves its source from that context. The `-t` flag names the resulting image. The agent did not deploy this example.

## Cache reasoning

A builder can reuse a step when its instruction and relevant inputs match. Changing a copied file invalidates that step and normally the following steps. Put stable dependency inputs before frequently edited application files. For example, use this order:

1. Copy the dependency manifest.
2. Install the dependencies.
3. Copy the application code.

With this order, a code-only change can reuse the dependency installation step.

`RUN` cache checks do not inspect remote repositories for newly published packages. A cached install command can therefore reuse old results. Cache reuse and current dependencies are different requirements. [Cache invalidation](https://docs.docker.com/build/cache/invalidation/).

## Common mistakes and recall

`CMD` does not run at build time. Adding `EXPOSE` does not make a host port reachable. Tags such as `stable` can change. To repeat a build, select a version or digest limit. See [registries](image-registries.md).

1. What does the build context control?
2. Which step runs before any container exists?
3. Why place dependency manifests before application source?
4. Why can an unchanged install command reuse stale content?
