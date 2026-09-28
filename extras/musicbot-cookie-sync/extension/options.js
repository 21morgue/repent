const DEFAULTS = {
  serverOrigin: "http://127.0.0.1:8999",
  cookieDomain: "youtube.com",
};

async function load() {
  const settings = { ...DEFAULTS, ...(await chrome.storage.sync.get(DEFAULTS)) };
  document.getElementById("serverOrigin").value = settings.serverOrigin;
  document.getElementById("cookieDomain").value = settings.cookieDomain;
}

async function save() {
  const serverOrigin = document.getElementById("serverOrigin").value.trim() || DEFAULTS.serverOrigin;
  const cookieDomain = document.getElementById("cookieDomain").value.trim() || DEFAULTS.cookieDomain;

  await chrome.storage.sync.set({ serverOrigin, cookieDomain });

  // Request the extra host permission for the configured server origin so
  // fetch() to it isn't blocked (only 127.0.0.1/localhost are granted at
  // install time; anything else needs an explicit runtime grant).
  try {
    const url = new URL(serverOrigin);
    await chrome.permissions.request({ origins: [`${url.origin}/*`] });
  } catch (err) {
    console.warn("cookie-sync: could not request host permission", err);
  }

  const status = document.getElementById("status");
  status.textContent = "Saved.";
  setTimeout(() => (status.textContent = ""), 1500);
}

document.addEventListener("DOMContentLoaded", load);
document.getElementById("save").addEventListener("click", save);
