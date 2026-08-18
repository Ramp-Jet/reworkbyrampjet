# Rework by Rampjet

Marketing site for Rework — a fixed-price, two-day website rebuild for
industrial companies. Static HTML/CSS, no build step and no JavaScript.

- `index.html` — homepage
- `rework-advisor-one-pager.html` — one-pager for M&A advisors
- `fonts/` — self-hosted woff2 (Archivo, IBM Plex Sans, IBM Plex Mono)
- `CNAME` — custom domain for GitHub Pages

## Local preview

Any static server from the repo root, e.g.:

    python3 -m http.server 4321

Then open http://localhost:4321/

## Fonts

Fonts are self-hosted rather than loaded from Google, so the page makes no
third-party requests. The two variable fonts are subset to the axis ranges the
site actually uses (Archivo `wght 700-900` / `wdth 78-90%`, IBM Plex Sans
`wght 400-600`), which cuts the downloaded font payload by about a third.
Regenerating them requires `fonttools`; the ranges are recorded in the
`@font-face` block in `index.html`.
