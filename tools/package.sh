#!/usr/bin/env bash
# Builds dist/fantasyfix-<version>.zip (the same zip works for Chrome Web Store and Firefox Add-ons).
set -euo pipefail
cd "$(dirname "$0")/.."
VERSION=$(python3 -c 'import json; print(json.load(open("extension/manifest.json"))["version"])')
mkdir -p dist
OUT="dist/fantasyfix-$VERSION.zip"
rm -f "$OUT"
(cd extension && zip -qrX "../$OUT" . -x "*.DS_Store" "_metadata/*")
echo "$OUT"
