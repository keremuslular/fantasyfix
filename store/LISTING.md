# Store listing (copy and paste)

Upload file: `dist/fantasyfix-<version>.zip` (run `bash tools/package.sh`).
Images in this folder: `icon-128.png`, `screenshot-1280x800.png`, `promo-440x280.png`.

---

## Shared text

**Name:** FantasyFix

**Short description / summary** (Chrome max 132 chars, Firefox max 250):

> Fixes missing matchups, game status and stats on ESPN Fantasy by loading ESPN's stats from its working server.

**Full description:**

> Seeing blank opponents, missing game times or empty past-day stats on ESPN Fantasy? In some regions ESPN's stats server (site.api.espn.com) refuses requests from the fantasy site with "Access Denied", so parts of your matchup and roster pages never load.
>
> ESPN serves exactly the same data from another address (site.web.api.espn.com) that isn't blocked. FantasyFix sends the fantasy site's stats requests there instead, and everything shows up again.
>
> • Brings back opponents, game status and past-day stats on matchup, roster and player pages
> • Works on fantasy.espn.com. Nothing to set up: install it and reload the page
> • Uses ESPN's own data. Nothing is changed, added or sent anywhere else
> • No account, no tracking, no analytics, no data collected
>
> How it works: the extension changes one thing, the hostname of requests to ESPN's stats API, from site.api.espn.com to site.web.api.espn.com.
>
> FantasyFix is an independent project and is not affiliated with or endorsed by ESPN.

---

## Chrome Web Store

Dashboard: https://chrome.google.com/webstore/devconsole (one-time $5 developer registration)

**Store listing tab**
- Category: **Lifestyle → Entertainment** (closest fit; there is no Sports category)
- Language: English
- Store icon: `icon-128.png`
- Screenshot: `screenshot-1280x800.png`
- Small promo tile: `promo-440x280.png`
- Homepage / support URL: optional (leave empty, or your GitHub repo if you publish one)

**Privacy practices tab**
- **Single purpose:**
  > Fixes ESPN Fantasy pages that fail to load stats by sending their requests for ESPN's stats API (site.api.espn.com) to ESPN's alternate stats address (site.web.api.espn.com).
- **declarativeNetRequest justification:**
  > Used for a single static redirect rule that changes the hostname of requests to site.api.espn.com to site.web.api.espn.com. No other rules, no blocking, no header changes.
- **Host permission justification** (`*://*.espn.com/*`):
  > Browsers only allow redirect rules for sites the extension has access to. The rule applies to ESPN's stats API on espn.com, and a small content script on fantasy.espn.com makes the same hostname change for browsers that don't apply redirect rules (Safari). No other sites are accessed.
- **Remote code:** No, I am not using remote code.
- **Data usage:** tick nothing (it collects no user data), then tick all three certifications:
  - I do not sell or transfer user data to third parties, outside of the approved use cases
  - I do not use or transfer user data for purposes that are unrelated to my item's single purpose
  - I do not use or transfer user data to determine creditworthiness or for lending purposes
- Privacy policy URL: not required when no data is collected. If the form insists, host `PRIVACY.md` (e.g. as a GitHub Gist) and paste its link.

**Distribution tab**
- Visibility: **Public** (anyone can find it) or **Unlisted** (only people with the link). Unlisted is fine for the league; Public helps others with the same problem.
- Regions: all regions.

Review usually takes from a few hours to a few days.

---

## Firefox Add-ons (addons.mozilla.org)

Dashboard: https://addons.mozilla.org/developers/addon/submit/distribution (free, Firefox account needed)

1. **How to distribute:** "On this site" (listed on addons.mozilla.org).
2. Upload `dist/fantasyfix-<version>.zip`. It should pass validation with no errors.
3. **Source code:** answer **No**. Nothing is minified, bundled or generated; the files in the zip are the source.
4. **Describe add-on:**
   - Name: FantasyFix
   - Add-on URL: `fantasyfix` (if taken, `fantasyfix-espn`)
   - Summary: the short description above
   - Description: the full description above
   - Category: **Other**
   - Support email: your choice
   - License: **MIT** (or "All Rights Reserved" if you don't want others reusing it)
   - Privacy policy: leave off (it collects nothing; the manifest already declares `data_collection_permissions: none`)
5. **Notes to reviewer:**
   > Single-purpose add-on. rules.json contains one declarativeNetRequest redirect rule (host transform site.api.espn.com → site.web.api.espn.com). inject.js runs on fantasy.espn.com in the page context and makes the same hostname change in fetch/XMLHttpRequest (needed for Safari, which shares this code). No remote code, no data collection, no network calls of its own. To test: open https://fantasy.espn.com in a region where site.api.espn.com returns 403 and compare player opponent/game-status columns with and without the add-on.
6. After submitting, add `screenshot-1280x800.png` on the listing's **Images** page.

Listed add-ons are usually reviewed within a day or two (sometimes automatically approved within minutes).

---

## Releasing an update

1. Change files in `extension/`, bump `version` in `extension/manifest.json`.
2. `bash tools/package.sh`
3. Chrome: dashboard → Package → Upload new package → Submit for review.
4. Firefox: dashboard → Upload new version.
