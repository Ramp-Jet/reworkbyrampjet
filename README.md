# Ramp/Jet — reworkbyrampjet.com

Marketing site for Ramp/Jet: systems for owner-operated industrial companies.
Static HTML/CSS with one small shared script, no build step. Deploys to
reworkbyrampjet.com via GitHub Pages from `main` — **a push to `main` is a
production deploy.**

Read **BUILD.md** before changing anything. It covers the voice rules, the
design system, what's still placeholder, and the two class-name traps that
have bitten this codebase before.

## Layout

    index.html            house page
    reach/  run/          product pages
    tools/  insights/     content sections
    advisors/             advisor page, printable sheet, and PDF (footer-only)
    assets/site.css       shared stylesheet
    assets/site.js        email assembly (keeps addresses out of the source)
    _config.yml           keeps BUILD.md / README.md off the published site

## Local preview

    python3 -m http.server 8000
