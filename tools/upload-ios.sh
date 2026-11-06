#!/usr/bin/env bash
# Archives the iOS Safari app and uploads it to App Store Connect (TestFlight).
# Needs: Xcode signed in to the developer account, and the app created in App Store Connect
# with bundle ID com.keremuslular.FantasyFix.
# The build number is the current UTC time, so every upload is unique.
set -euo pipefail
cd "$(dirname "$0")/../safari/FantasyFix"

BUILD=$(date -u +%Y%m%d%H%M)
ARCHIVE="${TMPDIR:-/tmp}/FantasyFix-iOS-$BUILD.xcarchive"
EXPORT_OPTIONS="${TMPDIR:-/tmp}/FantasyFix-ExportOptions.plist"

cat > "$EXPORT_OPTIONS" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>method</key><string>app-store-connect</string>
  <key>destination</key><string>upload</string>
  <key>teamID</key><string>2CVT63B2DP</string>
  <key>signingStyle</key><string>automatic</string>
  <key>uploadSymbols</key><true/>
  <key>manageAppVersionAndBuildNumber</key><false/>
</dict>
</plist>
EOF

echo "Archiving build $BUILD..."
xcodebuild archive -scheme "FantasyFix (iOS)" -destination "generic/platform=iOS" \
  -archivePath "$ARCHIVE" -allowProvisioningUpdates CURRENT_PROJECT_VERSION="$BUILD" -quiet

echo "Uploading to App Store Connect..."
xcodebuild -exportArchive -archivePath "$ARCHIVE" -exportOptionsPlist "$EXPORT_OPTIONS" \
  -exportPath "${TMPDIR:-/tmp}/FantasyFix-export-$BUILD" -allowProvisioningUpdates

echo "Uploaded build $BUILD. It appears in App Store Connect → TestFlight after processing (usually 5–15 minutes)."
