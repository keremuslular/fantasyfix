# FantasyFix

Browser extension for Chrome, Firefox and Safari (Mac + iPhone/iPad) that fixes missing matchups, game status and past-day stats on ESPN Fantasy.

## What it does

In some places, ESPN's CDN answers the fantasy site's requests to `site.api.espn.com` with **403 Access Denied**. ESPN serves the same data at `site.web.api.espn.com`, which isn't blocked.

The extension contains **one redirect rule** ([extension/rules.json](extension/rules.json)): any request to `https://site.api.espn.com/...` is sent to `https://site.web.api.espn.com/...` instead. That's all it does.

- No JavaScript, no background script, no popup.
- Permissions: `declarativeNetRequest` plus access to `*.espn.com` (browsers require host access for redirects).
- It doesn't read pages, cookies or data, and it sends nothing anywhere.

## Layout

```
extension/          the extension (shared by every browser)
  manifest.json
  rules.json        the one redirect rule
  icons/
safari/FantasyFix/  Xcode project: Safari app + extension for macOS and iOS (uses extension/ directly)
tools/
  package.sh        builds dist/fantasyfix-<version>.zip for Chrome / Firefox
  test-chrome.mjs   loads ESPN Fantasy in headless Chrome with/without the extension
  make_icons.py     draws the icons
```

## Chrome (and Edge, Brave, Arc)

Install for yourself:
1. Open `chrome://extensions` and turn on **Developer mode** (top right).
2. Click **Load unpacked** and pick the `extension` folder.

Share with the league: `bash tools/package.sh`, then upload `dist/fantasyfix-<version>.zip` to the [Chrome Web Store developer dashboard](https://chrome.google.com/webstore/devconsole) ($5 one-time fee) as **Unlisted**. Only people with the link can find it.

## Firefox

Install for yourself (temporary, until Firefox restarts): `about:debugging` → **This Firefox** → **Load Temporary Add-on** → pick `extension/manifest.json`.

Permanent and shareable: upload the same zip at [addons.mozilla.org/developers](https://addons.mozilla.org/developers/) (free). Choose **On your own** to get a signed `.xpi` you can send to people directly, or list it publicly.

## Safari (Mac, iPhone, iPad)

Open `safari/FantasyFix/FantasyFix.xcodeproj`. The team (`2CVT63B2DP`) and bundle ID (`com.keremuslular.FantasyFix`) are already set.

**Mac:** run the **FantasyFix (macOS)** scheme once, then go to Safari → Settings → Extensions, tick **FantasyFix**, and allow it on espn.com.

**iPhone / TestFlight:**
1. Create the app in [App Store Connect](https://appstoreconnect.apple.com) → Apps → **+** → New App, platform iOS (add macOS too if you want Mac Safari via TestFlight). Bundle ID `com.keremuslular.FantasyFix`, any unique name (e.g. "FantasyFix – Stats Fix").
2. In Xcode, pick the **FantasyFix (iOS)** scheme and **Any iOS Device**, then Product → **Archive** → Distribute App → **TestFlight & App Store**.
3. In App Store Connect → TestFlight: create an **external** group, add the build, fill in the short Beta App Review info, and turn on the **public link**. Send that link to the league.
4. Each person installs it and then follows the steps the app shows:
   - Settings → Apps → Safari → Extensions → **FantasyFix** → on.
   - Permissions: **espn.com** → **Allow**.
   - Use **fantasy.espn.com in Safari** (the extension can't change the ESPN app).

TestFlight builds expire after 90 days. Upload a new build (bump the build number) before then.

## Changing the extension

Edit `extension/`, bump `version` in `manifest.json`, then:
- Chrome: reload on `chrome://extensions`, or upload a new zip.
- Firefox: upload a new zip.
- Safari: bump `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION` in Xcode and archive again.

Test against the real site: `node tools/test-chrome.mjs` (without) and `node tools/test-chrome.mjs --with-extension`.
