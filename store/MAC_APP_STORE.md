# Mac App Store (Safari extension)

## 1. Create the app in App Store Connect (once)

Apps → **+** → New App
- Platform: **macOS**
- Name: **FantasyFix** (if taken: "FantasyFix – Stats Fix")
- Primary language: English (U.S.)
- Bundle ID: **com.keremuslular.FantasyFix**
- SKU: `fantasyfix-mac`
- User access: Full Access

## 2. Upload a build

```bash
bash tools/release-mac.sh appstore
```

Appears under the app's **Build** section after processing (5–15 minutes).

## 3. Listing (App Store tab → macOS App → 1.0)

**Screenshots (16:10):** `store/screenshot-mac-2880x1800.png`

**Promotional text** (170 max, can be changed anytime without review):
> Blank opponents, missing game times or empty stats in your fantasy basketball league? FantasyFix brings them back in Safari.

**Description:**
> FantasyFix is a Safari extension for fantasy sports players whose league pages show blank opponents, missing game times or empty past-day stats.
>
> In some regions the stats server that ESPN Fantasy uses (site.api.espn.com) answers with "Access Denied", so parts of the matchup and roster pages never load. The same data is served from another ESPN address (site.web.api.espn.com) that isn't blocked. FantasyFix sends those requests there instead, and everything shows up again.
>
> • Brings back opponents, game status and past-day stats
> • Works on fantasy.espn.com in Safari. Turn it on once and reload the page
> • Changes nothing else: no ads, no tracking, no data collected
>
> How to set it up:
> 1. Open FantasyFix once
> 2. Safari → Settings → Extensions → turn on FantasyFix
> 3. Allow it on espn.com, then reload fantasy.espn.com
>
> FantasyFix is an independent project and is not affiliated with, endorsed by or sponsored by ESPN.

**Keywords** (100 max, comma separated, no spaces needed; no trademarks):
> fantasy,basketball,stats,matchup,roster,league,hoops,safari,extension,fix,scores,game,sports

**Support URL:** `https://fantasyfix.keremuslular.com/` (Cloudflare, see wrangler.jsonc)
**Marketing URL:** optional, same as support
**Copyright:** `2026 Kerem Uslular`

**App Information tab**
- Subtitle (30 max): `Fantasy stats fix for Safari`
- Category: Primary **Sports**, Secondary **Utilities**
- Content rights: "Does not contain, show, or access third-party content" → **No, it does not**. (It only changes request addresses; it doesn't show ESPN content itself.)
- Age rating: answer **None / No** to everything → 4+

**App Privacy tab**
- Privacy Policy URL: `https://fantasyfix.keremuslular.com/privacy`
- Data collection: **No, we do not collect data from this app** → "Data Not Collected"

**Pricing and Availability**
- Price: Free
- Availability: all countries (or at least the ones your league is in)

## 4. App Review Information

- Sign-in required: **No**
- Notes:
  > FantasyFix is a Safari Web Extension; the app window only explains how to enable it. To review: open the app, then Safari → Settings → Extensions → enable FantasyFix and allow it on espn.com. Open https://fantasy.espn.com in Safari.
  >
  > What it does: rewrites requests from site.api.espn.com to site.web.api.espn.com (ESPN's own alternate stats host, serving identical data). In some countries site.api.espn.com returns 403 Access Denied to the fantasy site, so player opponents, game status and stats don't load; the extension fixes that. Outside those countries the pages already work, so the effect is not visible there. To see the rewrite, open Safari's Web Inspector → Network on fantasy.espn.com: requests go to site.web.api.espn.com.
  >
  > The extension collects no data, makes no network requests of its own, shows no ads and does not change page content. It is an independent project, not affiliated with ESPN.

Then **Add for Review** → **Submit to App Review**. Typical review: 1–2 days.

## Risks to know about

- **Naming another company (guideline 5.2):** the description names ESPN to explain what it fixes, and the disclaimer says it isn't affiliated. The app name, subtitle, icon and keywords don't use ESPN. If review objects, reword to "a popular fantasy sports site" and resubmit.
- **"Minimum functionality" (guideline 4.2):** single-purpose extensions are allowed; the review notes explain what it does and how to verify it.
