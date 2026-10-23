---
title: Nginx web serving and reverse proxying
type: lecture
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-23
course: System Administration
---
# Nginx web serving and reverse proxying

[System Administration](system-administration.md) · [Request path](module-4-request-path.md) · [Routing exercise](practice/nginx-two-app-routing.md) · [TLS setup](tls-certificates-and-nginx.md) · [systemd lifecycle](systemd-service-lifecycle.md) · [WAF inspection](waf-modsecurity-and-crs.md)

## Course context

This note combines repeated material that the owner supplied on 2026-10-11 at 02:41 and 02:42. It follows the Module 4 request-path introduction. The supplied material references container sections 3.3–3.4 and a later section 4.3. The exact number of this section is unconfirmed.

The vault does not store the original text. The earlier submission also describes ungraded self-checks. No student answers or score are recorded.

The owner supplied this section again on 2026-10-23.
The existing note retains the earlier source dates and distinguishes source examples from agent execution.

## Static and dynamic content

Static content is prepared content served from files, such as HTML, CSS, JavaScript and images. Application logic produces dynamic responses. It can use a database. This distinction describes content production. A cache can reuse a dynamic response without new application calculations. Static serving also involves processing such as path selection, permissions and headers.

Nginx can serve files directly or pass a request to an upstream application. An HTTP reverse proxy accepts requests for servers. A forward proxy sends requests for clients. Neither role automatically hides a participant's identity. [Nginx beginner's guide](https://nginx.org/en/docs/beginners_guide.html).

## Why place a proxy before an application?

A proxy can supply TLS termination, static file service, compression, and upstream selection in one place. Nginx uses event-driven connection processing. It does not require a separate worker for each connection.

The C10K problem concerns scaling to around ten thousand concurrent connections, not a strict protocol threshold. Igor Sysoev created Nginx. Its first public release was in 2004. [Nginx overview](https://nginx.org/en/), [connection processing](https://nginx.org/en/docs/events.html).

A proxy does not guarantee continuous service during application restarts. Availability still depends on healthy upstreams, connection handling and retry behavior. A single unavailable upstream can produce errors.

## Host Nginx forwarding to a container

Example HTTP server block, included inside the main configuration's `http` context:

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}
```

`proxy_pass` selects the upstream. [Proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass). A top-level HTTP `server` belongs inside `http`. `location` belongs inside `server` or, where permitted, another `location`. A standalone `location` file included directly in `http` is invalid. [HTTP core contexts](https://nginx.org/en/docs/http/ngx_http_core_module.html#location).

For host-installed Nginx, an example container launch is:

```sh
docker run -d -p 127.0.0.1:8080:8080 --name my-app my-script
```

This assumes image `my-script` exists and the application accepts connections on container port 8080 through its container interface. Binding only to container loopback can prevent access through publication. Host loopback publication keeps the upstream port from ordinary direct external access. The supplied `-p 8080:8080` form instead publishes broadly by default. [Docker port publishing](https://docs.docker.com/engine/network/port-publishing/).

If Nginx runs in another container, its `127.0.0.1` points to that container. Use a shared network. Select the application by its service name. See [Compose networking](docker-compose.md).

## Configuration placement

Debian and Ubuntu packages can store a site in `/etc/nginx/sites-available/my-app`. A link in `/etc/nginx/sites-enabled/` enables it:

```sh
sudo ln -s /etc/nginx/sites-available/my-app /etc/nginx/sites-enabled/my-app
```

The main configuration's `include` directives select the files that Nginx loads. A directory name alone does not activate files. If you remove the enabled link, the source configuration remains. Reload Nginx to apply the change. [Ubuntu Nginx guide](https://ubuntu.com/server/docs/how-to/web-services/install-nginx/).

The supplied material describes `/etc/nginx/conf.d/*.conf` as the common RHEL-family layout. Verify the installed `/etc/nginx/nginx.conf` rather than assuming the Debian directory convention applies to Fedora.

## Validation and graceful reload

```sh
sudo nginx -t && sudo systemctl reload nginx
```

Run the reload only after the test succeeds. `nginx -t` checks syntax and attempts to open referenced files. It does not reload the running service. A missing semicolon can fail parsing, but exact error text depends on context. A passing test does not prove upstream reachability or correct routing. [Nginx command-line reference](https://nginx.org/en/docs/switches.html).

On a normal reload, the master validates and attempts to apply the new configuration. If it cannot apply it, Nginx keeps the old configuration. After a successful reload, new workers use the new configuration. Old workers finish existing requests.

A fresh start after a full stop is different. Invalid configuration can prevent that start. Test before a reload. An invalid reload does not necessarily stop every site, as the supplied material claimed. [Nginx process control](https://nginx.org/en/docs/control.html).

## Practical limits

A public port 8080 can permit direct access that bypasses the host proxy.
Use the loopback publication above when only host Nginx needs the application port.
The application still needs an appropriate listener inside its container.

A valid configuration can route to the wrong application or an unavailable port.
Check both upstream endpoints before testing their public routes.
Use the [routing exercise](practice/nginx-two-app-routing.md) to distinguish location matching from URI replacement.
Do not infer successful deployment from syntax validation alone.

## Recall and self-check answers

1. Which directive selects the upstream? `proxy_pass`.
2. What does `nginx -t` check? Configuration syntax and access to referenced files, without reloading.
3. Why use available/enabled site directories? To separate stored configurations from enabled ones through links, where that package layout is configured.
4. Why can a proxy still return errors during an application restart?
5. Why does host loopback publication differ from container loopback binding?

These are explanatory answers, not a recorded student attempt. The supplied learning targets progress from static/dynamic understanding to proxy configuration and explaining validation and event-driven architecture.

## Verification limits

The agent read the official references on 2026-10-11. The agent's PATH contains no Nginx binary. The agent did not execute `nginx -t` or a live proxy test. The agent did not change a container or server configuration. The note remains a draft.


## Additional source check, 2026-10-23

The agent reread official Nginx location, proxy, and reload documentation, plus Docker port-publication guidance.
These references support the routing and reload qualifications above.
This source check does not establish a completed lab or repeat the earlier environment check.
