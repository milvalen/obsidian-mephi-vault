---
title: Nginx web serving and reverse proxying
type: lecture
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Nginx web serving and reverse proxying

[System Administration](system-administration.md) · [Request path](module-4-request-path.md) · [Routing exercise](practice/nginx-two-app-routing.md) · [TLS setup](tls-certificates-and-nginx.md) · [systemd lifecycle](systemd-service-lifecycle.md) · [WAF inspection](waf-modsecurity-and-crs.md)

## Course context

This consolidates overlapping material supplied on 2026-10-11 at 02:41 and 02:42. It follows the Module 4 request-path introduction. The supplied material references container sections 3.3–3.4 and a later section 4.3; the exact number of this section is unconfirmed. Original text is not retained. The earlier submission also describes ungraded self-checks; no student answers or score are recorded.

## Static and dynamic content

Static content is prepared content served from files, such as HTML, CSS, JavaScript and images. Dynamic responses are produced by application logic and may use a database. This describes how content is produced, not a guarantee that every request recomputes it: caching can reuse dynamic responses. Static serving also involves processing such as path selection, permissions and headers.

Nginx can serve files directly or pass a request to an upstream application. An HTTP reverse proxy fronts servers; a forward proxy acts for clients. Neither role automatically implies anonymity. [Nginx beginner's guide](https://nginx.org/en/docs/beginners_guide.html).

## Why place a proxy before an application?

A proxy can centralize TLS termination, static serving, compression and upstream selection. Nginx uses event-driven connection processing rather than requiring a dedicated worker for each connection. The C10K problem concerns scaling to around ten thousand concurrent connections, not a strict protocol threshold. Nginx was created by Igor Sysoev and first publicly released in 2004. [Nginx overview](https://nginx.org/en/), [connection processing](https://nginx.org/en/docs/events.html).

A proxy does not make application restarts automatically seamless. Availability still depends on healthy upstreams, connection handling and retry behavior; a single unavailable upstream can produce errors.

## Host Nginx forwarding to a container

Illustrative HTTP server block, included inside the main configuration's `http` context:

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}
```

`proxy_pass` selects the upstream. [Proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass). A top-level HTTP `server` belongs inside `http`; `location` belongs inside `server` or, where permitted, another `location`. A standalone `location` file included directly in `http` is invalid. [HTTP core contexts](https://nginx.org/en/docs/http/ngx_http_core_module.html#location).

For host-installed Nginx, an illustrative container launch is:

```sh
docker run -d -p 127.0.0.1:8080:8080 --name my-app my-script
```

This assumes image `my-script` exists and the application accepts connections on container port 8080 through its container interface. Binding only to container loopback can prevent access through publication. Host loopback publication keeps the upstream port from ordinary direct external access. The supplied `-p 8080:8080` form instead publishes broadly by default. [Docker port publishing](https://docs.docker.com/engine/network/port-publishing/).

If Nginx runs in another container, its `127.0.0.1` points to itself; use a shared network and the application's service name instead. See [Compose networking](docker-compose.md).

## Configuration placement

On Debian/Ubuntu packages, a site can live in `/etc/nginx/sites-available/my-app` and be enabled by a link in `/etc/nginx/sites-enabled/`:

```sh
sudo ln -s /etc/nginx/sites-available/my-app /etc/nginx/sites-enabled/my-app
```

The main configuration's `include` directives determine what is actually loaded. A directory name alone does not activate files. Removing the enabled link leaves the source configuration available; applying that change requires a reload. [Ubuntu Nginx guide](https://ubuntu.com/server/docs/how-to/web-services/install-nginx/).

The supplied material describes `/etc/nginx/conf.d/*.conf` as the common RHEL-family layout. Verify the installed `/etc/nginx/nginx.conf` rather than assuming the Debian directory convention applies to Fedora.

## Validation and graceful reload

```sh
sudo nginx -t
sudo systemctl reload nginx
```

Run the reload only after the test succeeds. `nginx -t` checks syntax and attempts to open referenced files; it does not reload the running service. A missing semicolon can fail parsing, but exact error text depends on context. A passing test does not prove upstream reachability or correct routing. [Nginx command-line reference](https://nginx.org/en/docs/switches.html).

On a normal reload, the master validates and attempts to apply the new configuration. If it cannot apply it, Nginx retains the old configuration. On success, new workers use the new configuration while old workers finish existing requests. This differs from stopping the service and attempting a fresh start with invalid configuration. Testing before reload remains useful, but the supplied claim that an invalid reload necessarily stops every site is too strong. [Nginx process control](https://nginx.org/en/docs/control.html).

## Recall and self-check answers

1. Which directive selects the upstream? `proxy_pass`.
2. What does `nginx -t` check? Configuration syntax and access to referenced files, without reloading.
3. Why use available/enabled site directories? To separate stored configurations from enabled ones through links, where that package layout is configured.
4. Why can a proxy still return errors during an application restart?
5. Why does host loopback publication differ from container loopback binding?

These are explanatory answers, not a recorded student attempt. The supplied learning targets progress from static/dynamic understanding to proxy configuration and explaining validation and event-driven architecture.

## Verification limits

Official references were consulted on 2026-10-11. Nginx is not available on the agent's PATH; examples have not undergone `nginx -t` or live proxy testing. No container or server configuration was changed. The note remains a draft.
