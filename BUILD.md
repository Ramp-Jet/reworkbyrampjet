# Ramp/Jet — Web Build Reference (reworkbyrampjet.com)

> Onboarding doc for the Ramp/Jet site at **reworkbyrampjet.com**. Read this first if you're picking up the project in a new chat.
>
> **History:** this site lived at rampjet.ai until Sept 2026, in `Ramp-Jet/reworkbyrampjet`. It moved here wholesale when rampjet.ai became a single holding page for a different offering. The Rework product site that previously occupied this domain was retired at the same time. This repo is `Ramp-Jet/reworkbyrampjet`.

---

## What it is

A single-file marketing site for **Ramp/Jet**, which builds the operating systems that owner-operated industrial companies run on when the owner isn't in the room — the website, the demand engine behind it, and the quoting/tracking/follow-up work that still lives in spreadsheets and memory.

**Buyer:** owner-operated industrial companies, roughly $5–50M — machine shops, fabricators, distributors, contract manufacturers, specialty suppliers. The defining condition: *the owner is still the system.*

**Three products, à la carte or together:**

| Product | Slot | Customer's sentence | Price shape |
|---|---|---|---|
| Rework | The website | "Our site doesn't look like the work we do." | $2,000 one-time (+ Maintain $200/mo) |
| Reach | The demand engine | "We get leads and nobody follows up." | Monthly |
| Run | Operations | "Quotes wait on me." | Per project, fixed price, scoped first |
| The Full Build | All three, one plan | — | One build price + Reach monthly |

**The territory claim.** Everything from the first search to the ERP. It stops where the ERP starts, and "ERP" is always glossed so QuickBooks-and-a-whiteboard counts.

> **History:** until Aug 2026 this was an AI-search-visibility site for mid-market B2B ("Be the answer when buyers ask AI"). That positioning is gone. Any doc, asset, or copy referencing AI search, citations, flywheel cycles, or "websurfaces" is stale.

---

## File layout

```
~/Desktop/RampJetHomePage/
├── index.html           ← the entire site (one self-contained file)
├── favicon.svg          ← flywheel mark, transparent, theme-aware
├── favicon-32.png       ← 32px fallback
├── favicon-16.png       ← 16px fallback (simplified ring)
├── apple-touch-icon.png ← 180px, opaque steel
├── CNAME                ← reworkbyrampjet.com
└── BUILD.md             ← this file
```

No build step. No bundler, no framework. Vanilla HTML + inline `<style>` + a small inline `<script>`. `index.html` is ~970 lines.

**Deploy:** GitHub Pages from `main` → **reworkbyrampjet.com**. A push to `main` is a production deploy. Branch for anything unfinished.

---

## Local dev

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`. Any static server works.

⚠️ **Browsers cache this aggressively.** If you see stale content, append a query string (`?v=2`) or hard-reload. A plain reload on `/` will happily serve you the old page.

---

## Open items — start here

Known-unfinished work, most consequential first. Details are in the sections below.

| # | Item | Notes |
|---|---|---|
| 1 | **`/advisors` doesn't exist; the footer link points at `#`** | It's the *only* public doorway to advisor content, and it goes nowhere. the design doc §6 has the full spec: move the Rework page's advisor section, Transfer Packet, confidentiality/fee notes and the two advisor FAQ items there, largely as written. This is the one page where exit and sale language is allowed — see §6 before writing any of it. Keep it out of the header nav; footer link only. |
| 2 | **Reach reads `from $750/mo` and is not in the structured data** | Resolved Aug 2026: Run's `from $3,500` was confirmed real and now carries a `priceSpecification` (minPrice 3500) in the JSON-LD and a figure in `llms.txt`. Reach was softened to a floor rather than confirmed, so it is deliberately absent from both — machine-readable price gets quoted back as fact without the page's context. When Reach firms up, add its `priceSpecification` and a figure to `llms.txt`. |
| 3 | **No proof/testimonial section** | Removed rather than ship the doc's illustrative quotes as real. the design doc §4.8 specifies one; add it back when there are genuine statements or screenshots. |
| 4 | **Product pages don't exist** | Nav and footer point at on-page anchors (`#rework`, `#reach`, `#run`). When `/rework` etc. ship, the anchors move with them. Template is the design doc §5. |

### Before you push

`main` is the GitHub Pages source — **a push to `main` deploys to reworkbyrampjet.com**. Branch for anything unfinished.

⚠️ **The GitHub repo is public.** `_config.yml` keeps `BUILD.md` off the published site, but that is not the same as private — anything committed here is readable by anyone at `raw.githubusercontent.com`. **The design document is deliberately not in this repo** for that reason: it carries exit/sale-prep positioning and unpublished prices. It lives at `~/Desktop/rampjet-design-doc.md`; ask Joseph for a copy. Don't commit it back in.

---

## The through-line

Three beats, in this order, and the page depends on all three:

1. **Hero** — *"Systems for the half that runs on memory."* Names the problem as a category, not a complaint.
2. **Absence check** — *"One day, someone else runs this."* The emotional turn. Succession, illness, or just a vacation all have one requirement: whatever lives only in your head doesn't transfer.
3. **Territory map** — *"Everything up to the ERP."* Bounds the promise so the rest reads as concrete rather than consulting.

### Exit / sale language is banned here

Per the design doc §1, the house page **never** says exit, sale, sell, buyer (as acquirer), valuation, or transaction. That content belongs on `/advisors`, reached from a footer link only. Public framing is *"runs without you"* and *"transferable."*

The absence check deliberately uses **illness / family / time-off** and never sale. Owners get defensive at "what happens when you sell" — you lose them before the argument lands.

```bash
# before shipping, confirm the house page stays clean:
grep -niE '\bexit\b|\bsale\b|\bsell\b|valuation|transaction|acquir' index.html
```

Two hits for "buyer" in the territory map are fine — that's *your customer's* buyer ("A buyer searches").

---

## Voice

**The voice guide is the authority: `~/Desktop/rampjet-voice-guide.md` ("The Honest Mechanic", locked v1, Aug 2026).** Not in this repo — §1 is marked private and §8 rule 2 concerns the advisor channel, and this repo is public. Ask Joseph for a copy. It carries an audit procedure; run it on any new page before shipping.

The short version: the honest mechanic across the counter. Tells you what needs fixing **and what doesn't**. Prices like a parts list, never "let's talk" where a number would do. Outcome before technology. **Readiness, never selling** — "ready for whoever comes next", never "sell". Rampjet does not build new systems; it writes down and gets running the ones you have.


Plain, short, shop-floor. Sentences an owner would say out loud. Concrete over abstract.

**Avoid anywhere:** infrastructure, modernize, digital transformation, AI (as a headline or selling point), automation platform, solution, seamless, leverage, empower. The buyer fears rip-and-replace; every section should read as *"we connect what you have."*

The one intentional exception: the don't-do list says `No "digital transformation"` — quoting the phrase to reject it.

---

## Design system

Work-order / spec-sheet aesthetic. No border-radius anywhere. No drop shadows except the hard orange offset. No gradients. No icons beyond the arrow glyph and the ✕ in the don't-do list.

### Tokens

```css
--steel:#0E1013; --steel-2:#1B1F23; --steel-3:#262B31;
--paper:#F9F6F1; --bone:#ECEAE4; --ink:#14171A;
--mute:#6B7076; --mute-lt:#A9AEB3;
--orange:#e94b35; --orange-dk:#bd3420; --orange-lt:#f26550;
```

**On the orange.** `--orange` is the brand's bright accent, carried over from the previous site — not the muted `#C2603F` in the design doc. `--orange-dk` is **text-only** (spec-sheet "does not include" rows, card CTA links) and is darkened to `#bd3420` so it clears WCAG AA on both bone and paper; at the bright orange's natural dark shade it measured 4.24:1, under the 4.5 threshold. **Every fill, bar, and swatch uses the full `--orange`.**

⚠️ **Known issue:** white text on orange buttons is 3.80:1 — below AA for 14px text. The design doc's original orange was also failing (4.17:1). Fixing it means darkening the button fill, which fights the brand accent. Left as-is deliberately.

### Type

- **Display:** Archivo 800/900, uppercase, `letter-spacing:-.01em`, `line-height:1.02`. H1 `clamp(44px,6vw,76px)`, H2 `clamp(32px,4.4vw,56px)`.
- **Body:** IBM Plex Sans. 17–19px, `#3A3F44` for paragraphs on light (not pure ink).
- **Spec/label:** IBM Plex Mono, 11–13px, uppercase, wide tracking. `.spec.on` is the orange eyebrow above every H2.
- **Stamp:** Space Mono — work-order numbers, "Op 10" labels, rotated tags.

Loaded from Google Fonts. No other typefaces.

### Components

- **Work-order card** (`.order`, `.sheet`) — paper, 2px ink border, `box-shadow:10px 10px 0 var(--orange)`, bone header strip with mono title + document number, dashed row dividers, rotated `.stamp` tag. Used twice: the hero order form and the absence check.
- **Spec sheet** (`.card`) — bone, 1px border, reversed ink header bar, mono key/value rows.
- **Op routing** (`.route`/`.op`) — stages split by 2px ink rules, `Op 10 / 20 / 30` stamps, arrow glyph overlapping the divider.
- **Buttons** (`.btn`, `.btn.ghost`) — solid orange, mono 600 uppercase, no radius.

---

## Page sections, top to bottom

| # | Section | Selector / id | Ground |
|---|---|---|---|
| 1 | Hero + order form | `.hero` | steel |
| 2 | Absence check | `.risk` `#handoff` | steel-2 |
| 3 | Territory map | `.map` `#map` | bone |
| 4 | Who this is for | `.who` | paper |
| 5 | The system (flywheel) | `.system` `#system` | steel |
| 6 | Three products | `.products` — `#rework` `#reach` `#run` | paper |
| 7 | What we don't do | `.dont` | steel |
| 8 | The Full Build | `.full` `#full` | paper |
| 9 | Book the call | `.final` `#book` | paper |

Nav links target `#map`, `#rework`, `#reach`, `#run`, `#full` — all on this page. **When product pages exist**, these become `/rework`, `/reach`, `/run` and the anchors move with them.

Dark bands alternate deliberately: hero and absence check are adjacent but use `--steel` and `--steel-2` so they read as different rooms rather than one long slab.

---

## Interactive pieces

All vanilla JS at the bottom of the file, progressive enhancement, no dependencies.

### 1. Order form (`#order`)

Three checkbox line items. `#tot` and `#totbtn` update live:

| Checked | Total text | Button |
|---|---|---|
| none | "Nothing checked yet. Start with the one that hurts." | Book a call |
| one | "*Product*, *shape*. Scoped and priced on the call." | Start with *Product* |
| two | "*A* + *B*. Scoped and priced on the call." | Book a call |
| all three | "That's The Full Build…" | Talk Full Build |

The selection is also written to the hidden `#cta-items` field, so the booking form reports which products someone checked.

### 2. Absence check (`#absence`)

Five concrete "you're out three weeks" items. It **counts the gap, not the wins** — that's where the moment is:

- 0 checked → "Nothing checked yet."
- 1–4 → "**N of 5** still wait on one person. Those are the ones we build."
- 5 → "**All five.** Rare — and worth protecting."

The all-five case matters: an owner who genuinely has this handled walks away feeling seen rather than sold to. Don't remove it.

### 3. Booking form (`#cta-form`)

Posts to Formspree (`f/xojryrdy`) via `fetch`, shows `#thanks` or `#form-error` inline. Honeypot `_gotcha` field. Error path points at the address assembled by `assets/site.js`.

---

## The flywheel animation

Lives in **section 5**, not the hero. Single closed clockwise loop, four nodes, 7.2s cycle.

```
                Calibrate (12 o'clock)
                     ●
                   ╱   ╲
        Ramp ●───╱       ╲───● Tune (3 o'clock)
    (9 o'clock)  ╲       ╱
                   ●───╯
                Jet (6 o'clock)
```

### Geometry

- **viewBox** `0 0 480 480`; loop circle centered (260,240), r=160, drawn as one `<circle>` with `stroke-dasharray="4 6"`
- **Ramp** (100,240) · **Calibrate** (260,80) · **Tune** (420,240) · **Jet** (260,400)

### Timing chain

| Time | Event |
|---|---|
| 0 → 4.4s | Satellites assemble at Ramp; first packet stream starts |
| 3.564s | Cal flashes on first impact; first Cal→Jet packet emerges |
| 3.71s | Packet passes Tune; needle does its first tick |
| 4.374s | Slot 1 lights at Jet |
| 5.274 → 10.674s | Slots 2–8 light at 0.9s intervals |
| 10.674s | Ring full; return packet leaves Jet |
| 11.574s | Return packet reaches Ramp; ring resets; next cycle |

CSS-first — `@keyframes`, `offset-path`, `animation-delay`. No JS timing.

### Two things to know before touching it

1. **It's recolored for a dark ground.** Calibrate, Tune, and Jet's ring are `#F9F6F1` (were `#1a1a1a`); the Tune needle inverted to `#0E1013`; the loop's dotted circle sits at 0.65 opacity. If you ever move this back onto a light background, invert those again.
2. **The reduced-motion fallback is load-bearing.** The global `@media (prefers-reduced-motion:reduce){*{animation:none!important}}` would leave `.ramp-visual` stuck at `opacity:0` — the whole graphic invisible. An explicit block pins it to a readable static state (feelers extended, satellites and slots visible, packets hidden). Don't delete it.

The **RAMP / CALIBRATE / TUNE / JET** text labels were removed on purpose. The old names are product names no longer.

---

## Favicon

The flywheel rebuilt as clean vector geometry (not traced from a render): 24-dot ring, four nodes in the same clock positions.

- **Transparent background.** The Ramp aura is translucent orange at 18% rather than solid pink, so it works on any backdrop.
- **`favicon.svg` is theme-aware** — the two ink nodes would vanish on a dark tab bar, so it carries its own `@media (prefers-color-scheme:dark){.ink{fill:#F9F6F1}}`.
- **`favicon-16.png` is simplified** to a 16-dot ring. At 16px each of 24 dots lands on under a pixel and the ring turns to mush.
- **`apple-touch-icon.png` is opaque steel.** iOS composites transparent touch icons onto flat black. Since it had to be opaque, it uses the site's steel with light nodes.

PNG fallbacks exist because **Safari doesn't support SVG favicons**. They can't respond to theme, so Safari-in-dark-mode keeps dark nodes.

---

## Accessibility

- Checkboxes are real `<input type="checkbox">` inside `<label>`; the visual is CSS on top.
- `:focus-visible` — 3px orange outline, 3px offset, on every interactive element.
- Reduced motion respected everywhere; see the flywheel note above.
- Check every change at **390px and 1280px**. The territory map's mobile collapse and the two work-order cards are the most likely to break.

The territory map collapses at ≤980px to a linear list via CSS `order`, with each claim ahead of the stages it covers: Rework, stage 1, stage 2, Reach, stage 3, stage 4, Run, stage 5, stage 6, ERP.

**Rework spans stages 1–2, not just stage 2.** the design doc §4.2 leaves stage 1 ("a buyer searches") unclaimed with a "Not ours" cell; that cell is gone, because Rework also covers content and social work that acts before anyone reaches the site. The page doesn't name those modules — the claim bar is the only place it shows.

---

## Not real yet

- **Reach `$750/mo` and Run `from $3,500`** are the design doc's `[PLACEHOLDER]` values, rendering as live prices. Rework's $2,000 is real.
- **There is no proof/testimonial section.** It was removed rather than ship the design doc's illustrative quotes as if they were real. the design doc §4.8 still specifies one; add it back when there are genuine customer statements or screenshots (a follow-up log, a quote that used to take a day).
- **No mobile nav menu.** `.nav ul` is `display:none` under 820px with no hamburger; only the wordmark and Book-a-call button show.
- **Product pages, `/advisors`, and the "Also from Rampjet" strip** don't exist yet.
- Footer's "For advisors" link points at `#`.

---

## Where the spec lives

**The design document** (`~/Desktop/rampjet-design-doc.md`, kept outside the repo) — the full spec: information architecture, product page templates for Reach and Run, the advisor page, design tokens, and the open decisions list. It is the source of truth for anything this file doesn't cover. Where the two disagree about *this page*, BUILD.md describes what actually shipped; the design doc describes what was specified.

Three places this build knowingly departs from it:

1. **The orange.** the design doc §3.1 specifies `#C2603F`; we kept the brighter `#e94b35` from the previous site.
2. **The flywheel section.** Not in the spec at all — added to give the animation a home.
3. **The absence check.** Not in the spec. It implements the succession through-line, staying inside the §1 rule that keeps sale language off the house page.
4. **Four copy edits** made after a coherence read, so the design doc's verbatim copy no longer matches the page:
   - §4.5's `No AI as a headline` → **`No AI for its own sake`**. The original is a copywriting rule from §1 published as a customer promise; an owner reading it asks "headline of *what*?"
   - Reach's §4.4 P1 lost its closing sentence, *"The system watches what works and adjusts."* It was the only unfalsifiable claim on a page that otherwise commits to checkable numbers — and it sat one section above a list that swears off exactly that. Not replaced: the preceding sentence already opens "You see…", so a concrete substitute collided.
   - The absence check's fourth item was *"The job that shipped Tuesday gets invoiced."* Invoicing is past the ERP line, so the section was promising work the territory map says we never do.
   - `Start where it hurts` (products intro) → `Start with the one you'd fix first`, so "hurts" lands twice rather than three times.

The HTML mock the build derives from (`rampjet-homepage.html`) is **not** in the repo, deliberately: GitHub Pages serves every file at the domain root, so a second homepage would go live at `reworkbyrampjet.com/rampjet-homepage.html`. It's in the original delivery zip if you need it.

### Publishing note

Everything in this repo is served publicly unless excluded. `BUILD.md` was reachable at `reworkbyrampjet.com/BUILD.md` until `_config.yml` was added; that file's `exclude:` list now keeps the internal docs out of the built site. **Add any new internal doc to that list.**
