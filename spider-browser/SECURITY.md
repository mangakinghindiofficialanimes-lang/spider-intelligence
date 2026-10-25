# Spider Browser security and privacy checklist

## Implemented in the prototype

- Desktop website windows run with context isolation, sandboxing, Node integration disabled, and web security enabled.
- The desktop opener accepts HTTP and HTTPS only, rejects URL credentials, and blocks unsafe schemes.
- New windows are intercepted and validated before a new managed window is created.
- Browser permissions (including geolocation and notifications) are denied by default.
- A small hostname blocklist blocks a handful of known advertising and tracking domains.
- The web UI does not send entered text to a server or an AI provider.

## Known gaps — do not call this production-ready

- The hostname list is small and does not provide strong/comprehensive ad blocking. It is not a substitute for EasyList, EasyPrivacy, or a maintained ad-blocking engine.
- The desktop UI does not yet connect its buttons to the Electron preload bridge; this needs a platform-specific renderer adapter and tests.
- The Android-facing page opens websites in the system browser. It cannot filter the system browser's network traffic or render every website inside itself.
- There is no AI browsing backend, page extraction, citation pipeline, credential vault, extension system, tab manager, or automated security test suite yet.
- Persistent partition data is used by the desktop scaffold; a visible clear-history/site-data control must be added before release.
- The prototype does not prevent fingerprinting, all tracking, malicious downloads, deceptive content, or screen capture.

## Required before a public release

1. Use a maintained ad-blocking library/filter engine. Verify its Electron API, licensing, update behavior, memory use, and test coverage before integration.
2. Download and update filter lists safely: HTTPS only, integrity validation, bounded size, last-known-good rollback, and no remote code execution.
3. Add tests for URL parsing, IDN/Unicode hostnames, redirects, pop-ups, blocked requests, filter exceptions, and Electron permission policy.
4. Add a per-site allowlist and visible blocked-request count without exposing sensitive full URLs in logs.
5. Add a clear browsing-data action that clears cookies, cache, local storage, and history with confirmation.
6. Keep AI credentials server-side. Ask before sending page text to external models, submitting forms, downloading files, or performing account actions.
7. Treat web page text as untrusted input. Ignore page instructions that try to override system rules, reveal secrets, or trigger unrelated tools.
8. Run dependency scanning and an Electron security review; test on current Windows and Android devices.
