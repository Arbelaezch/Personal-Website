#!/usr/bin/env bash
# The same checks CI runs (.github/workflows/main.yml), against SQLite, so no MySQL or .env is needed.
#   scripts/test.sh                          uses env/bin/python at the repo root
#   PYTHON=/path/to/python scripts/test.sh   use another interpreter
set -euo pipefail
cd "$(dirname "$0")/../website"
PY="${PYTHON:-../env/bin/python}"

export DJANGO_ALLOWED_HOSTS="www.christiandonovan.ca christiandonovan.ca localhost 127.0.0.1 [::1]"
export SECRET_KEY="test-only-secret-key-not-used-anywhere-else-0123456789-abcdefghij"
export DEBUG=1 DEV_DB_ENGINE=django.db.backends.sqlite3 DEV_DB_NAME=:memory:
export DEV_DB_HOST= DEV_DB_USER= DEV_DB_PASSWORD= DEV_DB_PORT=

echo "== migrations are committed"
"$PY" manage.py makemigrations --check --dry-run

echo "== deployment settings (production-like, must be warning-free)"
DEBUG=0 PROD_DB_ENGINE=django.db.backends.sqlite3 PROD_DB_NAME=:memory: \
  "$PY" manage.py check --deploy --fail-level WARNING

echo "== static files collect with the production storage (a reference to a missing file fails here)"
STATIC_CHECK_DIR="$(mktemp -d)"
trap 'rm -rf "$STATIC_CHECK_DIR"' EXIT
STATIC_ROOT_OVERRIDE="$STATIC_CHECK_DIR" "$PY" manage.py collectstatic --noinput -v0

echo "== tests"
"$PY" manage.py test --noinput
