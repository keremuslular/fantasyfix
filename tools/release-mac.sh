#!/usr/bin/env bash
# Mac Safari app releases.
#   tools/release-mac.sh download   Developer ID signed + notarized zip in dist/ (for direct download)
#   tools/release-mac.sh appstore   upload to App Store Connect (Mac App Store / TestFlight)
# Uses the Xcode-signed-in account and Apple's cloud-managed certificates; no passwords needed here.
# The build number is the current UTC time, so every build is unique.
set -euo pipefail
MODE="${1:-}"
[[ "$MODE" == download || "$MODE" == appstore ]] || { echo "usage: $0 download|appstore"; exit 1; }

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/safari/FantasyFix"
BUILD=$(date -u +%Y%m%d%H%M)
WORK="${TMPDIR:-/tmp}/fantasyfix-mac-$BUILD"
mkdir -p "$WORK" "$ROOT/dist"
VERSION=$(python3 -c 'import json; print(json.load(open("'"$ROOT"'/extension/manifest.json"))["version"])')

if [[ "$MODE" == download ]]; then METHOD=developer-id; else METHOD=app-store-connect; fi
cat > "$WORK/ExportOptions.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>method</key><string>$METHOD</string>
  <key>destination</key><string>upload</string>
  <key>teamID</key><string>2CVT63B2DP</string>
  <key>signingStyle</key><string>automatic</string>
  <key>manageAppVersionAndBuildNumber</key><false/>
</dict>
</plist>
EOF

echo "Archiving $VERSION ($BUILD)..."
xcodebuild archive -scheme FantasyFix -destination "generic/platform=macOS" -archivePath "$WORK/FantasyFix.xcarchive" \
  -allowProvisioningUpdates MARKETING_VERSION="$VERSION" CURRENT_PROJECT_VERSION="$BUILD" -quiet

echo "Exporting ($METHOD) and uploading to Apple..."
xcodebuild -exportArchive -archivePath "$WORK/FantasyFix.xcarchive" -exportOptionsPlist "$WORK/ExportOptions.plist" \
  -exportPath "$WORK/export" -allowProvisioningUpdates

if [[ "$MODE" == appstore ]]; then
  echo "Uploaded $VERSION ($BUILD). It appears in App Store Connect after processing (usually 5–15 minutes)."
  exit 0
fi

echo "Waiting for notarization (usually 1–10 minutes)..."
for i in $(seq 1 60); do
  if xcodebuild -exportNotarizedApp -archivePath "$WORK/FantasyFix.xcarchive" -exportPath "$WORK/notarized" >/dev/null 2>&1; then
    break
  fi
  [[ $i == 60 ]] && { echo "Notarization not finished after 30 minutes. Re-run: xcodebuild -exportNotarizedApp -archivePath $WORK/FantasyFix.xcarchive -exportPath $WORK/notarized"; exit 1; }
  sleep 30
done

APP="$WORK/notarized/FantasyFix.app"
xcrun stapler validate "$APP"
spctl --assess --type execute --verbose=2 "$APP"
OUT="$ROOT/dist/FantasyFix-$VERSION-mac.zip"
rm -f "$OUT"
ditto -c -k --keepParent "$APP" "$OUT"
echo "Done: $OUT"
