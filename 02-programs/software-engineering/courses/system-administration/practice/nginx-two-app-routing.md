---
title: "Practice: route legacy and new applications with Nginx"
type: problem
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Practice: route legacy and new applications with Nginx

[System Administration](../system-administration.md) · [Nginx concepts](../nginx-reverse-proxy.md)

## Task summary and assumptions

Route `/legacy/` to an older application and other paths under `/` to a new application. This English summary is based on material supplied at 02:41 and repeated at 02:42 on 2026-10-11. The vault does not store the original text. The student did not supply an attempt.

This solution uses these assumptions:

- Nginx operates on the host.
- The legacy application listens on host loopback port 8081.
- The legacy application expects root-relative request paths.
- The new application listens on port 8080. These port choices are example, not measured or assigned course values. The agent did not start or test either application.

## Suggested configuration

Include this server block within the existing `http` context:

```nginx
server {
    listen 80;

    location = /legacy {
        return 308 /legacy/$is_args$args;
    }

    location ^~ /legacy/ {
        proxy_pass http://127.0.0.1:8081/;
    }

    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}
```

The exact match handles the slashless entry point. `^~ /legacy/` reserves that prefix against later regex locations. `/` supplies the fallback. A plain `location /legacy/` also works if no competing regex location exists. A prefix `/legacy` would also match `/legacy-other`, which is usually unintended. [Location selection](https://nginx.org/en/docs/http/ngx_http_core_module.html#location).

## The two different trailing slashes

| Configuration inside `/legacy/` | Request | Upstream URI |
| --- | --- | --- |
| `proxy_pass http://127.0.0.1:8081/;` | `/legacy/items?x=1` | `/items?x=1` |
| `proxy_pass http://127.0.0.1:8081;` | `/legacy/items?x=1` | `/legacy/items?x=1` |

A URI in `proxy_pass` replaces the matched location prefix. Omitting that URI preserves the path in this simple configuration. Choose based on the upstream's expected path. A slash in `location` defines a prefix boundary. A slash after the upstream port controls URI rewriting. The two slashes have different functions.

An incorrect choice can produce application 404s. [proxy_pass semantics](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass).

## Application integration gap

Prefix stripping handles incoming request paths, but does not automatically make application-generated links, redirects or cookie paths use `/legacy/`. Configure the application's external base path. If necessary, change the response paths. Otherwise a legacy HTML page can point at `/assets/...`, which reaches the new application's fallback. This is a consequence of the proposed routing, not an observed failure.

## Proposed checks

First execute `sudo nginx -t`. If the test succeeds, reload Nginx. After deployment, inspect responses and upstream logs:

| Request | Expected destination or behavior |
| --- | --- |
| `/` | New application at port 8080 |
| `/legacy` | 308 redirect to `/legacy/` |
| `/legacy?x=1` | Redirect preserving `x=1` |
| `/legacy/` | Legacy application, URI `/` |
| `/legacy/items?x=1` | Legacy application, URI `/items?x=1` |
| `/legacy-other` | New application |

These expectations derive from the configuration. They are not runtime results. Check method handling with the actual applications. Check query strings, assets, redirects, and cookies. The example uses plain HTTP. TLS, authentication and domain selection are separate configuration work.

## Recall and verification limits

1. Which slash controls request-prefix stripping?
2. Why can `/legacy` be a broader match than intended?
3. What must change if the legacy application expects `/legacy/items`?
4. Why can incoming routing work while generated asset URLs fail?

The agent read the official references on 2026-10-11. The agent did not execute a Nginx syntax or runtime check. The Nginx binary is not available in the agent environment. This is an agent-written worked solution, not completed student practice.
