# Spider Browser (prototype)

Spider Browser is the first browser module for Spider Intelligence. This branch adds an Android-friendly browser-control UI, a desktop Electron browser-window scaffold, privacy defaults, and a domain-based ad/tracker blocking MVP.

## Current status

**Prototype, not a production-ready browser.** The web UI is a control panel, not a full browser engine. On Android, opening a URL hands it to the system browser for now; a website cannot safely embed every site because many sites block framing. The desktop scaffold opens websites in isolated Electron windows and applies a small bundled host blocklist. That blocklist is not equivalent to EasyList/EasyPrivacy and will miss many ads.

## Features in this milestone

- Mobile-first Spider Browser dashboard with address/search field, AI research panel mockup, blocker toggle, and privacy controls.
- Desktop Electron scaffold with context isolation, sandboxing, no Node integration in page renderers, safe HTTP(S)-only navigation, and default-deny browser permissions.
- Request blocking for a small set of known advertising/tracking hostnames.
- Documentation for the next milestone: maintained filter lists, filter updates, exception management, real AI backend, Android-native browser engine, and automated security tests.

## Run the web prototype

Open `index.html` in a browser or serve this directory with any static web server. The prototype UI can launch URLs in the system browser and simulate AI research responses locally; it does not yet connect to Spider Core or an LLM.

## Run the desktop scaffold

Requires Node.js 22+ and a supported desktop OS.

```sh
cd spider-browser/desktop
npm install
npm start
```

This starts the Electron control window. Use **Open in desktop browser** to open a separate managed website window. The current blocklist is deliberately small and should be expanded only with a proper filter engine and tests. Review the security notes before exposing this to real users.

## Roadmap

1. Replace the small host list with a maintained filter engine and EasyList/EasyPrivacy-compatible rules, including safe list updates and per-site exceptions.
2. Add browser tabs, history/bookmarks, downloads UI, and session-clear controls.
3. Connect the AI panel to Spider Core through a server-side API; use explicit allowlists, timeouts, page-size caps, citations, and user approval before form submission or other sensitive actions.
4. Add a real Android app/browser engine if full in-app page rendering is required. The web interface alone cannot act as a full Android browser.
5. Add tests for URL validation, blocked hosts, permissions, external-window handling, and prompt-injection resistance.
6. Run dependency scanning, Electron security review, and manual testing before production release.

## Privacy defaults

- Do not save page contents or prompts to a server in this prototype.
- Browser permission prompts default to deny in the desktop scaffold.
- Do not enter passwords or payment details into the AI research panel.
- AI must treat webpage content as untrusted data, never as instructions to ignore Spider's safety policy.
- Never commit API keys. Any provider keys belong in a server-side secret manager.
