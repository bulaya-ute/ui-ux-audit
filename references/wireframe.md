# Wireframe extraction — shape/position evidence for layout critique

A wireframe (structure-only map: containers, order, relative size and
alignment of components — no styling, no images) is the strongest common
ground for *layout choice* critique. This skill can generate one from:

- **Live DOM** (web): element bounding boxes via the in-session browser →
  ASCII rect map (script below).
- **Screenshots** (any surface, incl. Flutter apps/Android): the auditor
  *reads* the screenshot and hand-draws the wireframe as text — subjective
  but real; tier it as T0s evidence with the attached image.
- **Flutter widget tree** (stage-2, not yet automated): via DevTools
  render-tree export. Until tooling lands, use the screenshot route.

Generation is **optional evidence work** — never require every audit to
produce one; it earns its cost on layout-heavy claims (L-*, P-*, alignment,
density, whitespace rhythm) and on cross-screen comparative audits (does
screen B's anatomy differ from screen A's?).

## DOM extraction recipe (web)

1. Open the page in the in-session browser → `browser.tabs.open`.
2. Collect rect data with an in-page script (via the browser's evaluate
   capability), restricted to *layout-bearing* elements (skip leaf text
   nodes; include section headers, cards, CTAs, navs, footers):

```js
() => {
  const sel = 'header,nav,main,footer,section,article,aside,[class*=card],' +
              '[class*=container],button,a,form,input,select,textarea,h1,h2,h3';
  return [...document.querySelectorAll(sel)].slice(0, 220).map(el => {
    const r = el.getBoundingClientRect();
    return { tag: el.tagName.toLowerCase(), cls: (el.className+'').slice(0,40),
             x: Math.round(r.x), y: Math.round(r.y + window.scrollY),
             w: Math.round(r.width), h: Math.round(r.height) };
  }).filter(b => b.w > 8 && b.h > 8);
}
```

3. Pipe the JSON to the bundled renderer:

```bash
python3 scripts/wireframe.py boxes.json --width 80 > wireframe.txt
```

4. Critique the wireframe in a **separate reasoning pass** — first draw, then
   judge: order/alignment/whitespace rhythm/visual entry path. Do not let
   the critique reuse the extraction's structural assumptions.

## Renderer contract

`scripts/wireframe.py`: JSON in (list of `{tag, cls, x, y, w, h}` sorted by
y), ASCII out — non-overlapping boxes drawn as `┌─┐││└─┘` rectangles scaled
to `--width` columns with optional `--height` rows cap; boxes labeled with
tag + (clipped) class. Reads stdin if no file. It is a *layout projection*,
not documentation of pixel truth — state that in any report using it.

## Caveats (why we tier wireframes)

- DOM rects exclude scrollbar effects, pseudo-elements, and
  shadow-DOM internals unless measured on the right roots.
- A wireframe proves *structure*, not *appearance*: color/contrast/typography
  findings must still cite actual rendering.
- For Flutter (or anything without DOM rects) screenshot-derived wireframes
  are a *reading aid*; keep the screenshot as the citable evidence and the
  wireframe as an illustration of the reading.
- Wireframe passes are currently graded as **supporting evidence for L-*
  findings only** (never the sole basis for a Blocker).
