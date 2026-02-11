#!/usr/bin/env bash
set -e

URL=${1:-http://localhost:8080}
TIMEOUT=${2:-60}

echo "Attend que l'application soit disponible sur $URL ..."

for ((i=0; i<TIMEOUT; i++)); do
  if curl -fsS "$URL" >/dev/null; then
    echo "Application disponible"
    exit 0
  fi
  sleep 1
done

echo "Timeout: l'application ne répond pas"
exit 1
