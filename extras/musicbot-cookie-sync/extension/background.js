// Polls a local server every ~30s; when it says it needs fresh cookies,
// reads the current cookies for a configured domain out of this Chrome
// profile and pushes them up as a Netscape-format cookies.txt body.
//
// Configure the target server origin and cookie domain via the extension's
// options page (defaults: http://127.0.0.1:8999 and youtube.com).

const DEFAULTS = {
  serverOrigin: "http://127.0.0.1:8999",
  cookieDomain: "youtube.com",
};

const POLL_ALARM = "cookie-sync-poll";
const POLL_PERIOD_MINUTES = 0.5; // 30 seconds (chrome.alarms minimum granularity)

chrome.alarms.create(POLL_ALARM, { periodInMinutes: POLL_PERIOD_MINUTES });
chrome.runtime.onInstalled.addListener(() => {
  chrome.alarms.create(POLL_ALARM, { periodInMinutes: POLL_PERIOD_MINUTES });
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === POLL_ALARM) {
    pollAndSync().catch((err) => console.error("cookie-sync poll failed", err));
  }
});

async function getSettings() {
  const stored = await chrome.storage.sync.get(DEFAULTS);
  return { ...DEFAULTS, ...stored };
}

async function pollAndSync() {
  const { serverOrigin, cookieDomain } = await getSettings();

  let needsRefresh = false;
  try {
    const res = await fetch(`${serverOrigin}/needs-refresh`);
    if (!res.ok) return;
    const data = await res.json();
    needsRefresh = !!data.needsRefresh;
  } catch (err) {
    // Server isn't running / not reachable right now -- that's fine, just skip.
    return;
  }

  if (!needsRefresh) return;

  const cookies = await chrome.cookies.getAll({ domain: cookieDomain });
  const body = toNetscape(cookies);

  try {
    await fetch(`${serverOrigin}/cookies`, {
      method: "POST",
      headers: { "Content-Type": "text/plain" },
      body,
    });
    console.log(`cookie-sync: pushed ${cookies.length} ${cookieDomain} cookies`);
  } catch (err) {
    console.error("cookie-sync: failed to push cookies", err);
  }
}

function toNetscape(cookies) {
  const lines = [
    "# Netscape HTTP Cookie File",
    "# https://curl.haxx.se/rfc/cookie_spec.html",
    "# This is a generated file! Do not edit.",
    "",
  ];
  for (const c of cookies) {
    const includeSubDomain = c.domain.startsWith(".") ? "TRUE" : "FALSE";
    const secure = c.secure ? "TRUE" : "FALSE";
    const expiry = c.expirationDate ? Math.trunc(c.expirationDate).toString() : "0";
    lines.push([c.domain, includeSubDomain, c.path, secure, expiry, c.name, c.value].join("\t"));
  }
  lines.push("");
  return lines.join("\n");
}
