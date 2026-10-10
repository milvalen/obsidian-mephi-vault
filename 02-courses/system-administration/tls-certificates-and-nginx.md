---
title: "TLS certificates and Nginx HTTPS"
type: lecture
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# TLS certificates and Nginx HTTPS

[System Administration](system-administration.md) · [Nginx reverse proxy](nginx-reverse-proxy.md)

English summary of owner-supplied Section 4.3 material dated 2026-10-11 at 02:52, with official-reference corrections. Original text is not retained. Commands are proposed study examples, not completed work or a recorded student attempt. References were consulted on 2026-10-11.

## Trust, encryption and identity

TLS protects traffic while certificate authentication helps establish server identity. Public trust requires a valid chain to an accepted trust anchor, appropriate validity and usage, and a matching service identity. A self-signed certificate is signed by its own private key; it can be trusted explicitly in a controlled environment but is not automatically trusted by browsers.

Equal subject and issuer names indicate a self-issued certificate, not conclusive proof of a valid self-signature. Modern hostname verification uses Subject Alternative Name (SAN), rather than relying on CN alone. See [the request-path note](module-4-request-path.md#tls-and-certificate-identity) and [OpenSSL certificate tools](https://docs.openssl.org/master/man1/openssl-x509/).

## Local study certificate

The following example uses `my-app.test` as a local study name. It is not a public domain or configured service. Arrange local name resolution separately. In an empty disposable directory:

```sh
umask 077
openssl req -x509 -noenc -days 365 -newkey rsa:2048 \
  -keyout my-app.key -out my-app.crt \
  -subj "/CN=my-app.test" -addext "subjectAltName=DNS:my-app.test"
chmod 600 my-app.key
chmod 644 my-app.crt
openssl x509 -in my-app.crt -noout -subject -issuer -dates -ext subjectAltName
```

`-x509` creates a certificate instead of a CSR; `-newkey` creates a key pair; `-noenc` leaves the private key unencrypted. The supplied `-nodes` spelling is deprecated in OpenSSL 3 in favor of `-noenc`. `-days` sets the requested lifetime. Explicit permissions avoid assuming every environment creates identical file modes. [OpenSSL req](https://docs.openssl.org/master/man1/openssl-req/).

Keep the private key outside the vault and accessible only to the necessary privileged service context. The certificate is public. Install the files at the paths used by Nginx only as a separate, deliberate setup step; no files were generated or installed here.

## HTTPS and the HTTP entry point

Illustrative blocks inside the existing `http` context, after certificate installation:

```nginx
server {
    listen 80;
    server_name my-app.test;
    return 308 https://my-app.test$request_uri;
}

server {
    listen 443 ssl;
    server_name my-app.test;
    ssl_certificate /etc/ssl/certs/my-app.crt;
    ssl_certificate_key /etc/ssl/private/my-app.key;

    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}
```

The certificate/key directives enable TLS on the SSL listener. Nginx must be able to read both files. This setup terminates client TLS at Nginx and uses HTTP for the loopback upstream. A plain port-80 listener in the TLS block does not redirect by itself; the separate block makes that policy explicit. Routing and firewall access remain separate requirements. [Nginx HTTPS guide](https://nginx.org/en/docs/http/configuring_https_servers.html).

Run `sudo nginx -t` before `sudo systemctl reload nginx`. A certificate path or permission error can fail validation. A normal failed reload retains the previous configuration; a failed fresh start is different. See [Nginx validation and reload](nginx-reverse-proxy.md#validation-and-graceful-reload).

## Public certificates and changing lifetime rules

ACME automates proof of identifier control and certificate issuance. Let's Encrypt supports publicly validatable domain names and, since January 2026, public IP certificates with short lifetimes. A private-only name or loopback address is not made publicly validatable by this feature. The supplied statement that issuance always requires an owned domain is therefore outdated. [Let's Encrypt IP certificate announcement](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability).

As checked on 2026-10-11, Let's Encrypt documents a default 90-day lifetime and optional 6-day certificates. Automate renewal for the chosen profile. [Lifetime documentation, updated 2026-07-22](https://cps.root-x1.letsencrypt.org/ca/docs/cert-lifetimes/).

CA/Browser Forum rules limit newly issued publicly trusted subscriber certificates to 200 days from 2026-03-15. The supplied 398-day figure is historical, not the current general ceiling. This rule is distinct from a locally trusted self-signed lab certificate's selected lifetime. [Current baseline requirements](https://cabforum.org/working-groups/server/baseline-requirements/requirements/).

## Recall and limits

1. How can encryption work while the browser rejects certificate trust?
2. Why must the certificate include the intended name in SAN?
3. Why are equal subject and issuer names insufficient to prove a self-signature?
4. What redirects HTTP to HTTPS in the example?
5. What must be automated for a short-lived public certificate?

No certificate, HTTPS listener or ACME issuance was tested. Draft status remains.
