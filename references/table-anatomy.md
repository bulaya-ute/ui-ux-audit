# Table anatomy — "tables done right" checklist

Tables are the highest-stakes component in data portals: they are *the*
product for management systems. This checklist reads top-to-bottom for any
table audit; each item cites KB rules it feeds. Order matters: structural
items (A) grossly outrank niceties (C).

## A. Structure & mechanics

| Check | Looks for | Feeds |
|---|---|---|
| A1 column purpose | every column earns its width; ID/identifier columns available but not mandatory-visible (user-toggleable) | C-1 |
| A2 sticky header | header row visible on scroll; sticky first column (or a sane alternative) when the table scrolls horizontally | P-2 |
| A3 row selection mechanics | checkboxes uniformly enabled/disabled per row eligibility; disabled rows SAY WHY (the eligibility-aware pattern); select-all scope shown ("all N on this page" vs "N total") | C-1/F-1 |
| A4 bulk action bar | appears only with selection ≥1; shows count; destructive bulk = confirm | F-4 |
| A5 sorting | header affordance visible + state (asc/desc arrow), server-side when paged, survives filter changes | F-3 |
| A6 filter/sort/paginate interplay | changing a filter resets page to 1 (classic bug); applied filters visible as removable chips; count updates | F-3/V-2 |
| A7 pagination | for server-paged: totals shown, page size controlled, jump-to-page for big data; for client-tables: virtualization beyond ~200 rows | L-2 |
| A8 empty/loading/error | distinct treatments: loading (skeleton rows/ shimmer, not a spinner GIF), empty (guidance + create CTA), error (retry, keep filters); **no-results-after-filter counts separately from true-empty** ("no results for 'x' — clear filters") | V-2 |

## B. Interaction & access

| Check | Looks for | Feeds |
|---|---|---|
| B1 keyboard | tab reaches rows/checkboxes in DOM order; header sort via keyboard; Enter opens row; escape closes column menus | A-3 |
| B2 density control | comfort/compact toggle where data-heavy; row height ≥ semantically sufficient; touch mode for tablets | T-1/L-3 |
| B3 row actions | primary visible × secondary in overflow (⋯) menu — consistently positioned last visible column; row click ≠ destructive | F-4 |
| B4 column config | show/hide + reorder persisted per user (server or localStorage), reset available | C-1/F-3 |
| B5 responsive strategy | explicit: horizontal scroll (min-width table) vs stacked cards below a width breakpoint — decided per table class, not per accident; sticky action column survives the scroll | L-5 |
| B6 export | export visible where data is the point (CSV/PDF); respects current filters; export of filtered set obvious | F-1 |

## C. Polish

| Check | Looks for | Feeds |
|---|---|---|
| C1 alignment | numbers right-aligned with identical decimal treatment; text left; status centered w/ color+icon (A-1) | L-4/A-1 |
| C2 typography | tabular-nums for figures; dates in ONE format, sortable representation once sorted | W-2/L-4 |
| C3 link/row affordance | hover/press states; row hover reveals actions affordance | V-4 |
| C4 theming | borders, zebra, hover, selection, focus all verified in BOTH themes; dark tables lose hairlines (=the classic breakage) | V-1 |
| C5 load-of-large-data | skeletons-in-place for header+rows; never a blank grid | V-2/V-5 |

## Responsive chrome grammar (feeds N-rules)

Width-driven chrome decisions observed in portals worth copying:

- **≥1280px**: sidebar expanded OR icon-rail; table gets full width; top bar carries context + avatar.
- **~1024–1280**: icon-rail sidebar; secondary nav moves into top bar sections; drawer used for detail panes (master–detail remains).
- **<1024**: sidebar → hidden behind hamburger drawer; top app bar gains the primary nav; table switches per B5; detail opens as **modal/sheet** (never side-by-pane).
- **Modals vs drawers**: drawers for *contextual, side-by-side, low-stakes* detail (preview, edit metadata); modals for *focused, state-changing* decisions (confirm, create) and on small screens (no room for side-by-side).
- **Top app bars**: carry global search + identity + master actions; NEVER transport row-level actions.

Every violation maps: chrome-above-content overlaps → P-2; unusable table at
phone width → L-5; a drawer that should have been a modal (or vice versa) →
N-2; hidden hamburger with no drawer content → F-2.
