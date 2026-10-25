const address = document.querySelector("#address");
const navigateForm = document.querySelector("#navigate-form");
const navigationHint = document.querySelector("#navigation-hint");
const blockerToggle = document.querySelector("#blocker-toggle");
const blockerStatus = document.querySelector("#blocker-status");
const researchForm = document.querySelector("#research-form");
const researchPrompt = document.querySelector("#research-prompt");
const researchResult = document.querySelector("#research-result");
const askBeforeActions = document.querySelector("#ask-before-actions");
const minimizeData = document.querySelector("#minimize-data");
const privacyStatus = document.querySelector("#privacy-status");
const clearDemo = document.querySelector("#clear-demo");
const backButton = document.querySelector("#back-button");
const forwardButton = document.querySelector("#forward-button");
const reloadButton = document.querySelector("#reload-button");
const desktopBridge = window.spiderDesktop;

function normalizeAddress(value) {
  const input = value.trim();
  if (!input) return null;
  if (/^(javascript|data|file|vbscript):/i.test(input)) return null;
  const candidate = /^[a-z][a-z0-9+.-]*:\/\//i.test(input)
    ? input
    : (/^[\w.-]+\.[a-z]{2,}([/:?#]|$)/i.test(input) ? "https://" + input : "https://www.google.com/search?q=" + encodeURIComponent(input));
  try {
    const url = new URL(candidate);
    if (!["http:", "https:"].includes(url.protocol)) return null;
    return url.href;
  } catch {
    return null;
  }
}

navigateForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const url = normalizeAddress(address.value);
  if (!url) {
    navigationHint.textContent = "Please enter a valid HTTP(S) website or search query.";
    return;
  }
  if (desktopBridge?.openUrl) {
    navigationHint.textContent = "Opening in Spider Browser desktop window…";
    desktopBridge.openUrl(url).then((result) => {
      navigationHint.textContent = result?.ok ? "Opened in Spider Browser desktop window." : (result?.error || "Could not open this address.");
    }).catch(() => { navigationHint.textContent = "Could not open this address."; });
  } else {
    navigationHint.textContent = "Opening " + url + " in your system browser. This web preview cannot embed every website.";
    window.open(url, "_blank", "noopener,noreferrer");
  }
});

blockerToggle.addEventListener("change", async () => {
  if (desktopBridge?.setBlocking) {
    try {
      const result = await desktopBridge.setBlocking(blockerToggle.checked);
      blockerStatus.textContent = result?.ok ? (blockerToggle.checked ? "Blocking enabled. Reload open pages to apply." : "Blocking disabled. Reload open pages to apply.") : (result?.error || "Could not change blocking state.");
    } catch { blockerStatus.textContent = "Could not change blocking state."; }
  } else {
    blockerStatus.textContent = blockerToggle.checked
      ? "Blocking setting selected. This web preview cannot filter requests made by your system browser."
      : "Blocking setting disabled for a future desktop session; this preview cannot filter system-browser traffic.";
  }
});

async function navigateDesktop(direction) {
  if (!desktopBridge?.navigate) {
    navigationHint.textContent = "Back, forward, and reload controls work in the desktop app; this web preview uses your system browser.";
    return;
  }
  try {
    const result = await desktopBridge.navigate(direction);
    navigationHint.textContent = result?.ok ? "Browser navigation updated." : (result?.error || "No active browser page.");
  } catch { navigationHint.textContent = "Browser navigation failed."; }
}
backButton.addEventListener("click", () => navigateDesktop("back"));
forwardButton.addEventListener("click", () => navigateDesktop("forward"));
reloadButton.addEventListener("click", () => navigateDesktop("reload"));

researchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const prompt = researchPrompt.value.trim();
  if (!prompt) return;
  researchResult.textContent = "Draft plan (local demo only): search for reliable sources about “" + prompt.slice(0, 180) + "”, compare at least two independent sources, note publication dates, and return a cited summary. No page content is being fetched and no AI service was contacted.";
});

function updatePrivacyStatus() {
  const actions = askBeforeActions.checked ? "confirmation required" : "confirmation disabled in this demo";
  const data = minimizeData.checked ? "minimize data enabled" : "minimize data disabled";
  privacyStatus.textContent = "Sensitive actions: " + actions + "; " + data + ". Settings are not persisted.";
}
askBeforeActions.addEventListener("change", updatePrivacyStatus);
minimizeData.addEventListener("change", updatePrivacyStatus);
clearDemo.addEventListener("click", () => {
  researchPrompt.value = "";
  researchResult.textContent = "Spider will show its research plan here.";
  address.value = "";
  navigationHint.textContent = "Demo text cleared. Browser history in your system browser is unaffected.";
  updatePrivacyStatus();
});
