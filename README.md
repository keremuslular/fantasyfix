# FantasyFix

Browser extension for Chrome, Firefox and Safari (Mac) that fixes missing matchups, game status and past-day stats on ESPN Fantasy.

## What it does

In some places, ESPN's CDN answers the fantasy site's requests to `site.api.espn.com` with **403 Access Denied**. ESPN serves the same data at `site.web.api.espn.com`, which isn't blocked.

The extension sends every request for `https://site.api.espn.com/...` to `https://site.web.api.espn.com/...` instead, in two small parts:

- [extension/rules.json](extension/rules.json): one browser redirect rule. Chrome and Firefox use this.
- [extension/inject.js](extension/inject.js): about 30 lines that run on `fantasy.espn.com` and swap the hostname in the page's own `fetch`/`XMLHttpRequest` calls. Safari needs this: it loads the redirect rule, but in testing (Safari 27) it never applied it.

Nothing else:
- Permissions: `declarativeNetRequest` plus access to `*.espn.com`.
- It doesn't read cookies or page content, and it sends nothing anywhere.

## Layout

```
extension/          the extension (shared by every browser)
  manifest.json
  rules.json        redirect rule (Chrome, Firefox)
  inject.js         hostname swap inside fantasy.espn.com pages (needed for Safari)
  icons/
safari/FantasyFix/  Xcode project: Mac app that carries the Safari extension (uses extension/ directly)
docs/               website for GitHub Pages: downloads, support, privacy policy
store/              store listing text (LISTING.md), privacy policy, screenshot, promo tile, icon
  screenshot.html   source for the screenshot / promo images (rendered with headless Chrome)
tools/
  package.sh        builds dist/fantasyfix-<version>.zip for Chrome / Firefox
  release-mac.sh    Mac app: notarized download zip, or App Store upload
  test-chrome.mjs   loads ESPN Fantasy in headless Chrome with/without the extension
  make_icons.py     draws the icons
```

## Publishing

Everything the Chrome Web Store and Firefox Add-ons forms ask for (texts, permission justifications, images) is in [store/LISTING.md](store/LISTING.md).

## Chrome (and Edge, Brave, Arc)

Install for yourself:
1. Open `chrome://extensions` and turn on **Developer mode** (top right).
2. Click **Load unpacked** and pick the `extension` folder.

Share with the league: `bash tools/package.sh`, then upload `dist/fantasyfix-<version>.zip` to the [Chrome Web Store developer dashboard](https://chrome.google.com/webstore/devconsole) ($5 one-time fee) as **Unlisted**. Only people with the link can find it.

## Firefox

Install for yourself (temporary, until Firefox restarts): `about:debugging` → **This Firefox** → **Load Temporary Add-on** → pick `extension/manifest.json`.

Permanent and shareable: upload the same zip at [addons.mozilla.org/developers](https://addons.mozilla.org/developers/) (free). Choose **On your own** to get a signed `.xpi` you can send to people directly, or list it publicly.

## Safari (Mac)

Safari extensions ship inside a small Mac app: `safari/FantasyFix/FantasyFix.xcodeproj` (team `2CVT63B2DP`, bundle ID `com.keremuslular.FantasyFix`, macOS 13+). It uses the files in `extension/` directly.

- **Direct download:** `bash tools/release-mac.sh download` builds, signs with Developer ID, notarizes and writes `dist/FantasyFix-<version>-mac.zip`. Share it (e.g. as a GitHub Release asset).
- **Mac App Store:** `bash tools/release-mac.sh appstore` uploads a build to App Store Connect. Listing text, screenshots and review notes: [store/MAC_APP_STORE.md](store/MAC_APP_STORE.md).

Users open the app once, then Safari → Settings → Extensions → tick **FantasyFix** and allow it on espn.com.

No iPhone version: on phones people use the ESPN app, which an extension can't change.

## Website

`docs/` is a small static site (download links, setup steps, support, privacy policy) meant for GitHub Pages. The Mac App Store requires its support and privacy URLs.

## Changing the extension

Edit `extension/`, bump `version` in `manifest.json`, then:
- Chrome: reload on `chrome://extensions`, or upload a new zip.
- Firefox: upload a new zip.
- Safari: `bash tools/release-mac.sh download` and/or `appstore` (the app version follows manifest.json; build numbers are automatic).

Test against the real site: `node tools/test-chrome.mjs` (without) and `node tools/test-chrome.mjs --with-extension`.
