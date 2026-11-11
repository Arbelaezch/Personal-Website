#!/usr/bin/env bash
# Fail if any container publishes a port on a non-loopback address.
# Docker adds its own iptables rules, so a port published on 0.0.0.0 is reachable from the
# internet even if UFW says it is closed. Run:  sudo ./check-ports.sh
set -euo pipefail
bad=0
while IFS=$'\t' read -r name ports; do
  [ -z "$ports" ] && continue
  # entries look like "127.0.0.1:3000->3000/tcp, 0.0.0.0:80->80/tcp, [::]:80->80/tcp"
  if echo "$ports" | tr ',' '\n' | sed 's/^ *//' | grep -E -- '->' | grep -q -v -E '^(127\.0\.0\.1|\[::1\]):'; then
    echo "NOT LOOPBACK: $name  $ports"; bad=1
  fi
done < <(docker ps --format '{{.Names}}\t{{.Ports}}')
[ "$bad" -eq 0 ] && echo "ok: every published port is bound to loopback (or nothing is published)"
exit "$bad"
