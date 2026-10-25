const { app, BrowserWindow, ipcMain, session, shell } = require("electron");
const path = require("node:path");
const { URL } = require("node:url");

const blockedHosts = new Set([
  "doubleclick.net",
  "googlesyndication.com",
  "googleadservices.com",
  "adservice.google.com",
  "adnxs.com",
  "adsrvr.org",
  "adform.net",
  "scorecardresearch.com",
  "outbrain.com",
  "taboola.com",
  "quantserve.com",
  "hotjar.com",
  "pixel.facebook.com",
  "connect.facebook.net"
]);

let controlWindow;
let activePageWindow;

function safeHttpUrl(raw) {
  try {
    const url = new URL(raw);
    if (url.protocol !== "https:" && url.protocol !== "http:") return null;
    if (!url.hostname || url.username || url.password) return null;
    return url.href;
  } catch {
    return null;
  }
}

function isBlockedHost(hostname) {
  const host = hostname.toLowerCase().replace(/\.$/, "");
  for (const blocked of blockedHosts) {
    if (host === blocked || host.endsWith("." + blocked)) return true;
  }
  return false;
}

function installRequestBlocking(ses) {
  ses.webRequest.onBeforeRequest({ urls: ["http://*/*", "https://*/*"] }, (details, callback) => {
    let blocked = false;
    try {
      blocked = isBlockedHost(new URL(details.url).hostname);
    } catch {
      blocked = false;
    }
    callback({ cancel: blocked });
  });
}

function makePageWindow(url) {
  const safeUrl = safeHttpUrl(url);
  if (!safeUrl) throw new Error("Only valid HTTP(S) URLs are allowed.");
  const page = new BrowserWindow({
    width: 1180,
    height: 820,
    show: true,
    title: "Spider Browser",
    webPreferences: {
      session: session.fromPartition("persist:spider-browser", { cache: true }),
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true,
      allowRunningInsecureContent: false
    }
  });
  activePageWindow = page;
  const ses = page.webContents.session;
  installRequestBlocking(ses);
  ses.setPermissionRequestHandler((_webContents, _permission, callback) => callback(false));
  ses.setPermissionCheckHandler(() => false);
  page.webContents.setWindowOpenHandler(({ url: target }) => {
    const checked = safeHttpUrl(target);
    if (checked) makePageWindow(checked);
    else shell.beep();
    return { action: "deny" };
  });
  page.webContents.on("will-navigate", (event, target) => {
    if (!safeHttpUrl(target)) event.preventDefault();
  });
  page.on("closed", () => {
    if (activePageWindow === page) activePageWindow = null;
  });
  page.loadURL(safeUrl);
  return page;
}

function createControlWindow() {
  controlWindow = new BrowserWindow({
    width: 1000,
    height: 760,
    minWidth: 340,
    minHeight: 560,
    title: "Spider Browser",
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });
  controlWindow.loadFile(path.join(__dirname, "..", "index.html"));
  controlWindow.webContents.setWindowOpenHandler(() => ({ action: "deny" }));
}

app.whenReady().then(() => {
  createControlWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createControlWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

ipcMain.handle("spider:open-url", (_event, raw) => {
  const checked = safeHttpUrl(String(raw || ""));
  if (!checked) return { ok: false, error: "Only valid HTTP(S) URLs are allowed." };
  makePageWindow(checked);
  return { ok: true };
});

ipcMain.handle("spider:navigate", (_event, direction) => {
  if (!activePageWindow || activePageWindow.isDestroyed()) return { ok: false, error: "No active browser page." };
  const contents = activePageWindow.webContents;
  if (direction === "back" && contents.canGoBack()) contents.goBack();
  else if (direction === "forward" && contents.canGoForward()) contents.goForward();
  else if (direction === "reload") contents.reload();
  else return { ok: false, error: "Navigation action is unavailable." };
  return { ok: true };
});
