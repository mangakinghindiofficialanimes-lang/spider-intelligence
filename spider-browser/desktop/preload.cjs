const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("spiderDesktop", Object.freeze({
  openUrl: (url) => ipcRenderer.invoke("spider:open-url", url),
  navigate: (direction) => ipcRenderer.invoke("spider:navigate", direction),
  setBlocking: (enabled) => ipcRenderer.invoke("spider:set-blocking", Boolean(enabled))
}));
