# Rework by Rampjet

Marketing site for Rework — a fixed-price, two-day website rebuild for
industrial companies. Static HTML/CSS, no build step, and no build-time or
third-party JavaScript. The one script on the page is about 1KB inline, and
only upgrades the contact form; everything else is HTML and CSS.

- `index.html` — homepage
- `rework-advisor-one-pager.html` — one-pager for M&A advisors
- `fonts/` — self-hosted woff2 (Archivo, IBM Plex Sans, IBM Plex Mono)
- `img/` — the before/after screenshots in the proof section
- `tools/` — the script that captures those screenshots
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

## Before / after screenshots

The proof section shows two real pages scrolling in place: the client's old
site and the rebuilt one. Each is a single full-page screenshot, clipped to a
16:10 window and panned top to bottom with a CSS `object-position` animation.
No JavaScript involved, and the motion stops under `prefers-reduced-motion`.

Regenerate a shot with `tools/capture-site.py` (needs Chrome and Pillow):

    python3 tools/capture-site.py https://www.fluidtechllc.com/ \
        --out img/after-fluidtech-full

It drives headless Chrome and stitches viewport-sized tiles. Tiles rather
than one tall capture because Chrome's `captureBeyondViewport` will not
composite video or fixed backgrounds — a hero video comes out blank — and a
`100vh` hero stretches to fill whatever height you ask for.

Useful flags:

- `--video-time` holds a background video on one frame. Without it you get
  whatever frame playback happened to be on, which on a dark reel is usually
  unreadable at pane size.
- `--hide` removes overlays before the shot: cookie banners, marketing
  popups. Repeatable.
- `--eval` runs arbitrary JavaScript before the shot, for whatever the other
  flags do not cover. The Fluid Tech before-shot uses it to swap the page's
  YouTube embed for a still: the archive cannot replay third-party video, so
  it otherwise captures as a black slab that reads as a broken screenshot
  rather than as the page a visitor actually saw.
- `--width` sets the written width (default 1200). The script prints the
  finished dimensions — copy them into the `<img width height>` attributes so
  the pane reserves the right space while loading.

For an archived page, use the Wayback `if_` suffix so the archive's toolbar
and donation banner are not baked in:

    https://web.archive.org/web/20250429143453if_/https://www.fluidtechllc.com/

Two failure modes worth recognising, since both look like a broken capture
rather than a broken script. A blank white hero means the video did not
composite; that is what tile-zero-before-any-scrolling and `--video-time`
exist to prevent. A page whose logo and nav vanish is usually the same thing:
white text over a hero that failed to paint.

Archived pages are also just inconsistent. Successive captures of the same
Wayback snapshot came back 4957, 5281, 5903 and 6044 pixels tall as different
stylesheets and images made it out of the archive. It is worth taking two or
three and comparing them: the giveaway for a run that missed its CSS is
content sitting flush against the viewport edge instead of inside the page's
container.

## Contact form

The form in the booking section posts to Formspree. It is a plain HTML form
first: with no JavaScript it posts, and Formspree's `_next` field sends the
browser back to `thanks.html` rather than leaving people on Formspree's own
confirmation page.

The inline script upgrades that. It intercepts the submit, posts the same
form with `Accept: application/json` so Formspree answers instead of
redirecting, and swaps the form for a confirmation in place — no navigation,
no page load. If the request fails for any reason, including a non-2xx
response, it calls `form.submit()` and lets the browser do it the ordinary
way, so a message is never lost to a failed fetch.

That means the confirmation exists twice, once inline and once as
`thanks.html`, and both need editing if the wording changes. Keeping the
plain-post path is what makes the form work in a browser with JavaScript
turned off, and what catches the case where Formspree is reachable by
navigation but the fetch fails.
