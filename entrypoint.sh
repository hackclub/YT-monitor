#!/usr/bin/env bash
set -euo pipefail

# Install dependencies if not present (works in some container setups)
if [ -f requirements.txt ]; then
  pip install --no-cache-dir -r requirements.txt || true
fi

# Run DB init (idempotent)
if [ -n "${DATABASE_URL:-}" ]; then
  echo "Running DB init..."
  python init_db.py || echo "init_db.py failed (continuing): $?"
else
  echo "DATABASE_URL not set; skipping DB init"
fi

# If arguments provided, run them instead of default web server
if [ $# -gt 0 ]; then
  echo "Running: $@"
  exec "$@"
fi

# Default: start the web app
exec python web.py
