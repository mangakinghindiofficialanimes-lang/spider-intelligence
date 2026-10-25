# Spider Browser privacy architecture

Branding: **Spider Browser by Spider AI**  
Project identity / responsibility label: **spider-apis**  
Intended website domain: **spiderapis.com** (not yet verified as owned, registered, or deployed)

## Privacy promise we can honestly make

Spider Browser should minimize data collection and offer private sessions, but must never promise that nobody can observe internet activity. Private mode mainly controls local browser data. The network provider can still observe connection metadata; websites can identify logged-in users and may use IP addresses or fingerprinting. HTTPS protects page contents in transit but does not hide all connection metadata.

## Planned private session behavior

- Keep private session cookies, cache, local storage, and session state in a separate non-persistent browser session.
- Close all private windows and destroy the private session when the user ends the session.
- Do not write visited URLs, page contents, searches, or private-session identifiers to Spider server logs.
- Do not send page contents to AI providers unless the user explicitly starts an AI action and is shown what data will be shared.
- Keep normal browsing history separate from private sessions.
- Add a visible "End private session and clear data" action.
- Avoid analytics and advertising SDKs by default; disclose any future telemetry clearly and make it opt-in.
- Avoid saving passwords or payment details into AI prompts or page summaries.
- Ensure crash reporting, error logs, and diagnostics redact URLs, query strings, tokens, and page text.

## Network privacy limitations

- HTTPS encrypts the contents of traffic in transit but generally does not conceal every destination-related detail from the network provider.
- Private browsing does not make the user anonymous to websites or their internet provider.
- A VPN changes which network operator can observe some connection metadata; it does not make the user untrackable and moves trust to the VPN provider.
- DNS-over-HTTPS can protect DNS queries from some local-network observers, but it does not hide the destination from every party or solve browser fingerprinting.
- No privacy feature can guarantee that every tracker, fingerprinting method, or network observer is defeated.

## Ad and tracker blocking

The current prototype uses a small illustrative host list only. Before calling it strong protection, integrate a maintained, compatible filter engine and lists, verify license terms, validate updates, and provide per-site exceptions. Blocking must be visible and user-controlled.

## AI browsing protections

- Treat page text, downloaded files, and page instructions as untrusted data.
- Do not let a page override system rules, request hidden credentials, or authorize unrelated actions.
- Ask for explicit confirmation before submitting forms, sending messages, purchasing, deleting data, changing account settings, or downloading executable files.
- Limit page size, redirects, runtime, and tool permissions.
- Keep model API keys on the server in a secret manager; never ship provider secrets in the browser bundle.
- Disclose the AI provider and data categories before page text is sent to an external provider.

## Domain and deployment status

The intended domain is `spiderapis.com`; this repository does not prove domain ownership, DNS configuration, or deployment. Before publishing:
1. Confirm the domain is owned and accessible by the project maintainer.
2. Host the static site on a trusted HTTPS-capable host.
3. Configure DNS and TLS with the host's documented instructions.
4. Publish a privacy policy and contact/security reporting address before collecting any user data.
5. Do not collect account details or user browsing data until retention, access control, deletion, and incident-response policies exist.
