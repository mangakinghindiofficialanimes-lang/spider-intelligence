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
  navigationHint.textContent = "Opening " + url + " in your system browser. This web preview cannot embed every website.";
  window.open(url, "_blank", "noopener,noreferrer");
});

blockerToggle.addEventListener("change", () => {
  blockerStatus.textContent = blockerToggle.checked
    ? "Blocking enabled in the desktop scaffold. This web preview cannot filter requests made by your system browser."
    : "Blocking disabled in the desktop scaffold. Existing browser tabs may need to be reloaded.";
});

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
