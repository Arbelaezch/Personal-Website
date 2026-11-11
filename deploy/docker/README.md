# Docker on the server (`meditations`)

Docker 29.x with Compose v5 (callback needs v2.24.4+). Config here is the live config.

## Rules for every app
1. **Publish ports on loopback only**, behind nginx: `ports: ["127.0.0.1:3000:3000"]`. The daemon default
   (`"ip": "127.0.0.1"` in `daemon.json`) makes a bare `3000:3000` loopback too, but write the address anyway.
   Docker adds its own iptables rules, so **UFW does not protect published container ports**.
2. Databases, Redis and workers publish **nothing** (talk over the compose network).
3. Logs rotate at 10 MB x 3 files per container (daemon default). Keep apps logging to stdout/stderr.
4. Use `restart: unless-stopped` for services that must survive a reboot.
5. Do not put service accounts in the `docker` group; membership is root-equivalent.
6. Check after any change: `sudo ./check-ports.sh`

## Install / update (as root)
```bash
install -m 644 daemon.json /etc/docker/daemon.json
systemctl restart docker        # only when no important container is running
install -m 644 docker-prune.service docker-prune.timer /etc/systemd/system/
systemctl daemon-reload && systemctl enable --now docker-prune.timer
```

## Cleanup
`docker-prune.timer` runs weekly (Sun ~04:30): dangling images and build cache older than 7 days only.
Stopped containers and volumes are never removed automatically; clean those by hand
(`docker ps -a`, `docker volume ls`, `docker system df`). Disk budget: keep `/` under about 85% used.
