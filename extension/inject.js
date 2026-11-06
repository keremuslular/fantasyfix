// Runs inside fantasy.espn.com pages and sends the page's requests for ESPN's stats API
// (site.api.espn.com, blocked in some regions) to site.web.api.espn.com, which serves the
// same data. Nothing else is read, changed or sent anywhere.
// (Chrome and Firefox also do this with the redirect rule in rules.json; Safari needs this script.)
(() => {
  const FROM = "site.api.espn.com";
  const TO = "site.web.api.espn.com";

  const fix = (value) => {
    try {
      const url = new URL(String(value), location.href);
      if (url.hostname !== FROM) return null;
      url.hostname = TO;
      return url.href;
    } catch {
      return null;
    }
  };

  const originalFetch = window.fetch;
  window.fetch = function (input, init) {
    if (input instanceof Request) {
      const fixed = fix(input.url);
      if (fixed) input = new Request(fixed, input);
    } else {
      const fixed = fix(input);
      if (fixed) input = fixed;
    }
    return originalFetch.call(this, input, init);
  };

  const originalOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method, url, ...rest) {
    return originalOpen.call(this, method, fix(url) ?? url, ...rest);
  };
})();
