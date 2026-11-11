#!/usr/bin/env bash
# Install this directory's nginx config onto the server, safely.
#   sudo ./install.sh
# 1. backs up /etc/nginx   2. copies nginx.conf, conf.d/, snippets/, sites-available/ and enables every
# site in sites-available/ (removing the stock "default" site)   3. nginx -t   4. reload.
# If the test fails the backup is restored and nothing is reloaded.
set -euo pipefail

[ "$(id -u)" -eq 0 ] || { echo "run as root: sudo $0"; exit 1; }
SRC="$(cd "$(dirname "$0")" && pwd)"
NGX=/etc/nginx
BACKUP=/root/nginx-backup-$(date +%Y%m%d-%H%M%S)

cp -a "$NGX" "$BACKUP"
echo "backup: $BACKUP"

restore() { echo "!! restoring $BACKUP"; rm -rf "$NGX"; cp -a "$BACKUP" "$NGX"; exit 1; }

install -m 644 "$SRC/nginx.conf" "$NGX/nginx.conf"
install -m 644 "$SRC"/conf.d/*.conf "$NGX/conf.d/"
install -d "$NGX/snippets"
install -m 644 "$SRC"/snippets/*.conf "$NGX/snippets/"
for f in "$SRC"/sites-available/*; do
  name=$(basename "$f")
  install -m 644 "$f" "$NGX/sites-available/$name"
  ln -sfn "$NGX/sites-available/$name" "$NGX/sites-enabled/$name"
done
rm -f "$NGX/sites-enabled/default"

nginx -t || restore
systemctl reload nginx
echo "nginx reloaded. Check: curl -sI https://<site>/ ; backup kept at $BACKUP"
