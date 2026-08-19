# Rework by Rampjet

Marketing site for Rework — a fixed-price, two-day website rebuild for
industrial companies. Static HTML/CSS, no build step and no JavaScript.

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
No JavaScript, and the motion stops under `prefers-reduced-motion`.

Regenerate a shot with `tools/capture-site.py` (needs Chrome and Pillow):

    python3 tools/capture-site.py https://www.flextram.com/ \
        --out img/after-flextram-full --video-time 35.6 --hide .calc-toast

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
- `--width` sets the written width (default 1200). The script prints the
  finished dimensions — copy them into the `<img width height>` attributes so
  the pane reserves the right space while loading.

For an archived page, use the Wayback `if_` suffix so the archive's toolbar
and donation banner are not baked in:

    https://web.archive.org/web/20240907221802if_/https://www.flextram.com/

Two failure modes worth recognising, since both look like a broken capture
rather than a broken script. A blank white hero means the video did not
composite; that is what tile-zero-before-any-scrolling and `--video-time`
exist to prevent. A page whose logo and nav vanish is usually the same thing:
white text over a hero that failed to paint.
