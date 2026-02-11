#!/usr/bin/env bash
set -e

TARGET=${1:-http://host.docker.internal:8080}
REPORT_DIR=${2:-rapports}

mkdir -p "$REPORT_DIR"

echo "Lancement du scan OWASP ZAP sur $TARGET"

docker run --rm -t \
  -v "$(pwd)/$REPORT_DIR:/zap/wrk" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t "$TARGET" \
  -r zap.html \
  -J zap.json \
  -x zap.xml

echo "Scan ZAP terminé. Rapports dans $REPORT_DIR/"
