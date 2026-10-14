# UI/UX Audit — LusakaCity Admin Web + Marketing Site (2026-10-14)

Fingerprints:
- **Admin web** (`lusaka_ride_web`): surface web-desktop · profile `admin-data-dense` · suite: sibling of the two Flutter apps + marketing site — **suite policy NOT declared (DECISION)** · audience staff · input pointer+keyboard · evidence: T1 code + T0s live + T0m DOM (49 rects), light-theme variant unverified (see finding 9)
- **Marketing site** (`lusaka-ride-web`): web · `marketing-landing` · suite member (brand-aligned to LrBrand by construction ✓ token-exact) · anonymous · evidence: T0s (full-page capture) + T0m (DOM contrast probes on 4 pairs, 34 rects, wireframes in `audits/2026-10-14/`)

Totals: **9 findings** (0 Blocker · 4 Major · 5 Minor) · 3 DECISIONS · healthy rows balanced at the bottom.

---

## Findings — Admin web

### A1 · MAJOR · V-2 state-holes: empty-state copy misleads when no filters are set (T0s)
`/bookings` on an empty DB shows *"No bookings match the current filters."* with **zero active filters** — the message concretely misleads an operator debugging their own filters. The component also lacks a *true-empty* branch distinct from *filtered-no-results* (table-anatomy A8), and offers no guidance CTA.
**Fix**: branch on active-filter count — true-empty: "No bookings yet; bookings appear once passengers reserve seats." + link to itineraries; filtered: current copy + a **Clear filters** action. One component change in `DataTable`'s empty branch.

### A2 · MAJOR · A-2 semantics: sortable headers without `aria-sort` (T1: 0 occurrences in `DataTable.tsx` for `aria-sort`, plus live `th[aria-sort]` all null with sortable columns shipped)
Screen-reader users cannot tell which column drives order or its direction. All management tables feed on this component, so every table inherits it.
**Fix**: header sort buttons set `aria-sort="ascending|descending|none"` on the `th`, plus an sr-only "sorted ascending/descending" cue. (~5 line component change.)

### A3 · MAJOR · N-3 sidebar-collapsibility: the collapse control claims to collapse but doesn't (T0m: class flips `sidebar--open` → `sidebar--collapsed`, width 232px → 213px, labels unchanged)
On an `admin-data-dense` profile the collapse affordance exists (good) but produces no icon-rail — operators on small screens gain only 19px; the affordance doesn't deliver the promise. (T0s screenshot stored.)
**Fix**: at `sidebar--collapsed` render icon-only rail (~64px, labels hidden with `title` tooltips), persist the choice.

### A4 · MAJOR · X-1 suite policy undefined → app family tokens drift (T2 probable + T0s evidence)
The admin login carries brand green (`#0F7A3E`-family visual) with slate-dark body tokens (`#262D38` etc.), while the mobile apps and marketing site run the exact **LrBrand green500 `#207C3C`/green600 `#1A6634` + `#F9F9F9` neutrals**. No suite policy is declared anywhere (`unified` vs `themed-variants`), so this drift has no owner today.
**Fix (DECISION first, then change)**: declare the suite policy; minimum: map the admin's green and neutrals onto LrBrand tokens (log-in panel + primary CTAs) — a one-file token change; the slate *dark* palette itself can stay as a themed-variant if documented.

### A5 · MINOR · L-2 fixed-size truncation without compensation (T0s)
Sidebar user chip truncates ("System Admin…") with no `title`/tooltip/full-view fallback.
**Fix**: `title` attribute + the profile modal already contains the full name.

### A6 · MINOR · A-2 spacer columns leak unnamed `<th>` into the accessibility tree (T0m: 4 `<th>` with empty text in the audit)
Spacer/alignment columns (checkbox + actions + sort-row alignment) expose empty headers; screen readers announce empty columns; also `scope="col"` hygiene.
**Fix**: mark structural spacers as `scope="col"` with sr-only labels ("Actions", "Selection") or `aria-hidden` + `scope="presentation"`.

### Healthy (checked, good)
Sticky table header ✓ · eligibility-aware bulk selection w/ bulk bar ✓ (code) · CSV export ✓ · column show/hide with user persistence ("Showing all columns") ✓ · per-column filter operator chips + global search ✓ (T7 work) · mobile drawer breakpoint implementation in `index.css` ≈ correct N-1 grammar ✓ · login autofill (`autocomplete=email/current-password`) ✓ · stale-board items actually *fixed* (Approvals endpoints now real) ✓ · CSV-export + sort without state loss confirmed by code reading ✓.

**Not checked / can't verify this session**: loading-state branch render (DB seeded empty; skeleton code present but unrendered), Route Simulator page, printer/export outputs.

---

## Findings — Marketing site

### M1 · MINOR · A-2 semantics: demo route mock leaks fake operational data to assistive tech (T1: code + T0s)
The hero's mock seat-map ("8/9 seats left", "YOU", "K25.00", "Your seat: here") is real DOM that screen readers will announce as product data — a public landing shouldn't read invented availability to a blind visitor.
**Fix**: wrap the mock card in `aria-hidden="true"` (and same for the drivers' manifest mock) with a one-line `p`-tag description ("Illustration of seat availability") for context.

### M2 · MINOR · C-3 conflicting utilities on the same element (T1: `text-amber-700 text-[#7a4d00]` on the seats chip — the arbitrary value silently wins)
Two text colors on one element is a maintenance trap (theme-driven tint changes silently lose).
**Fix**: keep one source (`text-[#7a4d00]`) or define `amber-ink` token in `@theme` and drop the duplicate.

### M3 · MINOR · C-1 repeated inline SVG ×3 (T1: identical check-circle SVG pasted in the trust row)
**Fix**: extract one `<Check />` component (footprint: 3 lines).

### M4 · PROBABLE · L-5 multi-width (T2 this session — viewport resize unavailable in the audit harness)
Layout is Bootstrap-style `md:`-gated single-column at small widths by construction, but no under-420px capture exists yet.
**Fix**: capture 320/375px on a phone (the user's device or devtools) and check the hero mock card and footer at small width; promote the rule after one real capture.

### M5 · MINOR · V-1 borderline (healthy with headroom note) (T0m: hero accent `#4EBB78` over gradient ≈ 3.6:1)
Passes AA for its 48px semibold size (3:1 large-text), but the margin is one theme tweak from failing.
**Fix (optional)**: use `green200` (`#7ED2A0`) in that span for ~5:1 headroom — zero visual character loss.

### Healthy (checked, good)
Skip-link ✓ · visible focus ring ✓ · reduced-motion guards ✓ (`anim-rise` + scroll) · semantic `<details>` FAQ ✓ · `autocomplete`-free public forms n/a · single canonical object naming across sections (Riverside → Prospect consistent in both mocks) ✓ · `og:*` ✓ · `favicon.svg` ✓ · footer year auto ✓ · tokens byte-aligned to the apps' LrBrand palette ✓ (X-1 clean on this member).

**DECISIONS needed** (user judgment, not auto-fixable):
- Suite policy: declare `unified` vs `themed-variants` for {admin web, passenger app, driver app, marketing} — A4's minimum move follows from it.
- Contact mailboxes (`support@lusakaride.co.zm`, `drivers@lusakaride.co.zm`) — confirm they exist before launch (W-2/DECISION).
- "Request the beta APK" → becomes a Play/Release link when the store listing lands (W-3 corollary: the CTA should name what happens next).

---

## Suggested corrections queue (recommended order)

1. **A1** empty-state branch + copy (10 min) · **A2** `aria-sort` (15 min)
2. **A4** suite-policy DECISION → token alignment (30 min incl. decision)
3. **M2 + M3 + M1** marketing hygiene trio (20 min total)
4. **A3** icon-rail implementation (1–2 h; affects Shell CSS only)
5. **M4** real phone-width captures (5 min on a phone)

---

## Mobile-leg addendum (2026-10-14 night, live app run)

Run at 375×812 desktop-window instances of both Flutter apps (audit harness,
`AUDIT_WINDOW_CONTROLS=true`), driving the live audit DB (`lusakaride-audit-pg`)
through `gnome-window-control`. Passenger leg went: OTP login (masked
971••••567, mock OTP) → profile setup → home → From/To pickers → search.

### T7 incident (server regression caught live)

First search tap returned the app's error screen **behind** a "Route search
could not be completed" state — server logs showed `GET /api/itineraries?
boardingLocationId=…&alightingLocationId=…` → **500**.
`ItineraryService.ListAsync` filtered with `StopIds.Contains` directly on the
JSON column — plan-translator-untranslatable after a recent regression, i.e.
the T7 area bit again. **Fix applied** (filter in memory after
materialization; commit on server `audit/ux-1014`), API restarted, verified:
same query now 200 `{"items":[],"totalCount":0}`.

### V-8 candidate · stale-count-beside-error (observed on passenger app)

With the (pre-fix) server 500 up, the search screen paired **"0 routes
found"** with the error panel — a count from the previous run beside
"Could not load routes". Fix shipped on passenger `audit/ux-1014`
(`f00e05b`): count blanked while `_error != null`. Candidate until the
corrected flow is re-verified live.

### P-4 candidate · permission-ask-context-gated (observed)

Location-permission nudge appeared as its own step in passenger onboarding
(pre-login capture, night-1014 evidence). Proposed rule: ask for
permissions **at the moment of need**, with one-line justification tied to
the action the user is already taking — never as an orphan pre-flight step.

### A7 · MAJOR · L-2 native-input-intrinsic-width (fixed & verified)

`CompareFilter` side-by-side min/max (auditor found on Passengers
Joined/Rating columns, dev-server capture):
~53px per input clips native date inputs to an unreadable squished-calendar
("dc📅") and number placeholders to "M⇅". **Fix**: stack the between pair
vertically (web `audit/ux-1014` `10fda22`). Verified by DOM probe: all four
between inputs at 120–123px, clipped count 0 (was 4). Promoted KB rule
**L-6**, `established`.

### Audit-harness learnings (for the skill, not the product)

- Sub-pixel field clicks: click the element's vertical **center**; a click
  1px above a field's top edge silently does nothing.
- Two 375×859 Flutter windows overlapped at (773,127)/(823,177): clicks
  computed from one window's frame can land on the other's pixels when it
  is stacked on top. Tile/offset windows apart before driving.
- Flutter **desktop** windows drive fine via real input where Flutter-web
  synthetic semantics resisted; screenshot-driven feedback each step is the
  reliable loop when row heights shift between captures.
