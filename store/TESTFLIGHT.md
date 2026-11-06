# TestFlight (iPhone / iPad Safari)

## 1. Create the app (once)

App Store Connect → Apps → **+** → New App
- Platform: **iOS**
- Name: **FantasyFix** (must be unique on the App Store; if taken: "FantasyFix – Stats Fix")
- Primary language: English
- Bundle ID: **com.keremuslular.FantasyFix**
- SKU: `fantasyfix`
- User access: Full Access

## 2. Upload a build

```bash
bash tools/upload-ios.sh
```

The build shows up under **TestFlight** after processing (5–15 minutes). Export compliance is answered automatically (the app declares it uses no non-exempt encryption).

## 3. Try it yourself first (internal testing, no review)

TestFlight → **Internal Testing** → **+** → create a group (e.g. "Me"), add yourself, add the build. Install it from the TestFlight app on your iPhone.

## 4. Share with the league (external testing, needs a short beta review)

TestFlight → **External Testing** → **+** → group "League" → add the build. App Store Connect then asks for the following.

**Test Information** (TestFlight → Test Information):
- **Beta App Description:**
  > FantasyFix is a Safari extension that fixes ESPN Fantasy pages where opponents, game status and past-day stats fail to load. In some regions ESPN's stats server (site.api.espn.com) answers the fantasy site with "Access Denied"; ESPN serves the same data at site.web.api.espn.com, and FantasyFix sends those requests there instead. It collects no data. Independent project, not affiliated with ESPN.
- **Feedback email:** your email
- **Marketing URL / Privacy Policy URL:** optional for TestFlight (leave empty)

**Beta App Review Information:**
- Contact: your name, phone, email
- **Sign-in required:** No
- **Review notes:**
  > The app itself only shows setup instructions; the functionality is the Safari Web Extension. To review: install, then Settings → Apps → Safari → Extensions → FantasyFix → turn on, and allow it on espn.com. Open https://fantasy.espn.com in Safari. The extension rewrites requests from site.api.espn.com to site.web.api.espn.com (ESPN's own alternate stats host). It does not collect data, make its own network requests, or modify page content. The effect is only visible in regions where site.api.espn.com is blocked; elsewhere pages simply load as normal.

**What to Test** (shown to testers, per build):
> Turn on the extension (Settings → Apps → Safari → Extensions → FantasyFix, allow espn.com), then open your league on fantasy.espn.com in Safari. Opponents, game times and yesterday's stats should all show up.

Submit for review (usually within a day). Once approved: External group → **Public Link** → enable → copy the link.

## 5. Message for the league

> ESPN Fantasy on iPhone missing opponents / game times / stats? Install this:
> 1. Open this link on your iPhone and install TestFlight if asked: <PUBLIC LINK>
> 2. Install **FantasyFix** from TestFlight
> 3. Settings → Apps → Safari → Extensions → **FantasyFix** → turn on, and set **espn.com** to **Allow**
> 4. Use **fantasy.espn.com in Safari** (the ESPN app itself can't be fixed)
>
> Chrome/Firefox on a computer: <store links>

## Notes

- TestFlight builds expire after **90 days**. Run `bash tools/upload-ios.sh` again before then; new builds of the same version usually skip review.
- Up to 10,000 external testers via the public link.
