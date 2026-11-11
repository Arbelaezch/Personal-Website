# nginx on the server (`meditations`)

Everything here is the live configuration, versioned. `install.sh` copies it to `/etc/nginx`,
runs `nginx -t` and reloads (it restores a backup if the test fails). Nothing is edited by hand
on the server any more: change the files here, then `sudo ./install.sh`.

```
nginx.conf                       main file (TLS 1.2+ only; includes conf.d and sites-enabled)
conf.d/00-global.conf            server_tokens off, gzip, rate-limit zones (perip, login)
snippets/security-headers.conf   HSTS, nosniff, Permissions-Policy  (include in every server AND in
                                 locations that use add_header)
snippets/proxy-app.conf          proxy headers; OVERWRITES X-Forwarded-For
snippets/cloudflare-real-ip.conf real client IP behind Cloudflare (regenerate: ./refresh-cloudflare-ips.sh)
sites-available/000-catch-all    default_server on 80/443: unknown Host -> connection closed (444),
                                 unknown TLS name -> handshake refused
sites-available/christiandonovan.ca
templates/app-site.conf.template starting point for a new site
```

## Adding a new site (e.g. an app in Docker)
1. App listens on loopback only (`127.0.0.1:PORT`) or a unix socket. Never publish it on `0.0.0.0`
   (Docker bypasses UFW).
2. DNS and certificate:
   - **DNS-only domain:** `sudo certbot certonly --nginx -d app.example.com`
   - **Cloudflare-proxied domain** (e.g. `callback.modularmonolith.ca`): create a Cloudflare *Origin CA*
     certificate, save as `/etc/ssl/cloudflare/<domain>.pem` / `.key` (key mode 600), set SSL mode to
     *Full (strict)*, and add `include /etc/nginx/snippets/cloudflare-real-ip.conf;` to the server block.
3. `cp templates/app-site.conf.template sites-available/<domain>`, replace the `@@PLACEHOLDERS@@`.
4. `sudo ./install.sh` (it also enables the new file).
5. Test: `curl -sI https://<domain>/`; unknown hosts must still be refused (see below).

## Checks
```bash
sudo nginx -t
curl -sI https://christiandonovan.ca/ | grep -i -E 'strict-transport|x-content-type|permissions-policy|^server'
curl -s -o /dev/null -w '%{http_code}\n' -H 'Host: nope.invalid' http://127.0.0.1/       # empty reply (444)
curl -sk --resolve nope.invalid:443:127.0.0.1 https://nope.invalid/ ; echo "exit $?"      # handshake refused
sudo certbot renew --dry-run
```

## Notes
- HSTS is 180 days without `includeSubDomains`/`preload`; raise it deliberately later.
- Rate limits: `perip` 30 r/s (burst 60) for general browsing, `login` 10 r/min (burst 5) for login forms.
  Exceeded requests get HTTP 429.
- Rolling back: `/root/nginx-backup-<timestamp>` (printed by `install.sh`), or `git revert` and re-run it.
