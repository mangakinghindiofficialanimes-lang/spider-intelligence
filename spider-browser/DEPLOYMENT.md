# Deploying Spider Browser and spiderapis.com

## Current state

The website is source code in this repository. It is not automatically live at `spiderapis.com`. Domain ownership, DNS, TLS, and hosting must be configured by the maintainer.

## Publish the static landing page

A static host such as GitHub Pages or Netlify can serve `spider-browser/website/` as a landing page. The browser prototype itself lives at `spider-browser/index.html`. Keep the static site separate from any authenticated API backend.

## Connect the domain

1. Confirm you control `spiderapis.com` through your domain registrar.
2. Create a site/project on the chosen host and deploy the contents of `spider-browser/website/`.
3. Add `spiderapis.com` and, if desired, `www.spiderapis.com` in the host's domain settings.
4. Apply only the DNS records provided by the host. Do not guess A, AAAA, or CNAME values.
5. Enable HTTPS/TLS in the host dashboard and wait until its certificate is active.
6. Verify the apex domain, www redirect, mobile layout, and security headers.

## Before public launch

- Publish a real privacy policy, terms, contact details, and security reporting route.
- Do not publish secrets or model provider keys in static frontend files.
- Do not connect private browsing to analytics or request logging without a clear reason and transparent consent.
- Use a separate backend host for AI tasks; enforce authentication, rate limits, request-size caps, URL allowlists/SSRF protections, and server-side secrets.
- Test accessibility, dependency vulnerabilities, URL validation, and ad-blocking filter updates.
- Explain clearly that private mode is not total anonymity and does not prevent all ISP or website observation.
