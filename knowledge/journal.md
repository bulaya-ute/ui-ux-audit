# ui-ux-audit knowledge journal

Newest first. One entry per audit session or KB change. This file is the
narrative diff of the knowledge base; `checks.csv`/`profiles.md` are the state.

## 2026-10-14 · Exemplar batch 2 — web systems sweep (7 systems, 5 landed)

**Method**: same skill, pattern-harvest stance; screenshots (T0s) +
`browser.evaluate` structural probes + code-level reads via GitHub API (T1,
cal.com). Deferred with reasons: Airbnb (bot-walled the search route), Polar
(Shopify migrated their docs; old Polaris routes 404), Design-for-Driving
(public URLs dead — need the alternate Google surface), Figma community
clones / app-store screens (next epoch; native-mobile internals).

### Systems landed
- **Stripe** (`stripe.com`) — live hero *metric-as-trust* ("Global GDP running
  on Stripe: 1.731…%"), restrained dual CTA, logo wall. Marketing-landing
  corroboration: evidence-in-copy beats claims.
- **Linear** — captured mid-entrance-animation (black hero → content animates
  in): a deliberate brand choice but also a caution that animation-first
  heroes resist audit evidence; their skip-link + nav survived capture.
- **Grafana Play** — (a) boot sequence: generic spinner → **branded logo**
  boot state (zero blank screen); candidate **V-7 boot-state-branded**;
  (b) their 404 lands as a *structured recovery page*: heading + explanation
  + primary "Back to Home" + secondary "Community Help" + toast — direct
  corroboration for the new flow rule below; (c) dashboards list: scope
  chips (tag/owner), visibility toggles, folder tree.
- **cal.com** — the 404 page itself converts: "The username /hari is still
  **available**" with a register CTA embedding the subject of the miss.
  Code-level harvest (T1): `packages/ui/components` ships `EmptyScreen`
  (headline+description+CTA contract, dashed border), `Skeleton`, `Loader`,
  `errorBoundary` — **state-hole prevention as reusable primitives**, not
  per-screen patches.
- **Plausible (live demo)** — honest dark data-dense: 6 KPI tiles with delta
  arrows, chart, segmented bottom tables, live presence dot (81), date-range
  + filter in one header row. Notable policy: **delta coloring is
  direction-based** (green ↑/red ↓), so bounce-rate *improving* renders red
  — a conscious system decision. Candidate **X-5 delta-color-policy**:
  systems must document goodness-based vs direction-based sequenced colors.
- **Bolt** — ride-domain giant's landing: minimal white page, ONE vivid green
  CTA ("Get Bolt") weight-differentiated against a grey tonal sibling
  ("Get Bolt Food") — multi-product weight grammar, and brand-green in the
  wild confirming our palette choice reads serious.

### Promotions & seeds
- **PROMOTED → established: V-5 skeleton-in-place** — corroborated Booking.com
  study-1 (T0s) + cal.com `Skeleton`/`Loader` primitives (T1).
- **NEW established: F-9 not-found-offers-recovery** — two independent
  exemplars (Grafana 404 recovery page + cal.com 404→conversion). Not-found
  is never a dead end: explain, offer primary + secondary recovery paths,
  and where possible turn the miss into value.
- **NEW candidates: V-7 boot-state-branded** (Grafana boot sequence),
  **X-5 delta-color-policy** (Plausible direction-based coloring).
- Kept `candidate` (single corroboration each, from study 1): F-6
  search-context-persistence, W-3 cta-names-missing-input, A-5
  filter-count-preview, W-4 auth-gate-dismissable, A-6
  hierarchical-orientation, W-5 trust-signals-near-cta.

**Provenance**: screenshots in `docs/img/exemplar-{stripe,calcom-404,
grafana-boot-spinner,grafana-404-recovery,grafana-dashboards-list,
plausible-live-dashboard,bolt-home}.jpg` (13 images total now).

---

## 2026-10-14 · Exemplar study 1 — Booking.com (public booking flow)

**Method**: skill applied as-pattern-harvest, not defect-hunt. Fingerprint:
phone/web · passenger-task analog · standalone · anonymous audience · touch.
Evidence: T0s screenshots (4, in `docs/img/`), T0m DOM-rect harvest (121
layout rects, property-card anatomy: consistent 729×274 cards), browser-find
probes. Pages: home gate → results (25 cards, Lusaka) → property page.

**Patterns observed worth encoding (candidates):**

1. **F-6 `search-context-persistence`** (`candidate`) — the search criteria
   bar (destination/dates/occupancy chips) stays visible AND editable on both
   results and property pages; refining never loses the result context.
2. **W-3 `cta-names-missing-input`** (`candidate`) — when a prerequisite
   isn't set yet, the card CTA literally names what's missing ("Select
   dates") instead of a generic action that would dead-end.
3. **V-5 `skeleton-in-place`** (`candidate`) — partial-data rails render
   visible skeleton bars while loading, never blank panels (review breakdown
   on the property page).
4. **A-5 `filter-count-preview`** (`candidate`) — each filter shows the
   current result count it would produce (59, 49, 138…) — actuation honesty.
5. **W-4 `auth-gate-dismissable`** (`candidate`) — the sign-in promo is a
   closable modal offered once, never forced; browsing continues ( contra
   forced-gates our apps must avoid).
6. **A-6 `hierarchical-orientation`** (`candidate`) — breadcrumb chain on
   deep pages (Home → Zambia → Lusaka Province → Lusaka → property) plus
   in-page section tabs with counts ("Guest reviews (295)").
7. **W-5 `trust-signals-near-cta`** (`candidate`) — review count + rating
   band sit adjacent to the price/CTA cluster, not in a distant stats page.

**Notes**: `per night` / price-basis labeling was present in body text
(W-family already covered by W-2 drift? No — seed a rule only if it repeats
in another exemplar; held as observation). Wishlist heart button 36×36 sits
at ≥8px from the CTA cluster — the relational target rule (T-1) holding on
a world-class site. Left with back-stack intact via breadcrumbs + tabs; no
dead ends encountered.

**Status**: all 7 seeded `candidate`; promote on next corroboration (second
exemplar or in-product recurrence). Screenshots stored under repo
`docs/img/exemplar-*.jpg` as the public-facing evidence set.

---

## 2026-10-14 · KB v1.1 — system fingerprint, overrides, wireframes, consent

**Source**: user requirements for the public release — five structural
additions, plus two rule families:

- **System fingerprint** added as a Phase-1 pre-requisite
  (`knowledge/system-classification.md`): surface / app-kind / suite policy /
  audience / input / motion / evidence-surface axes; the analysis stance is
  now *fitness to class*, with Class-fit findings (X-4) as first-class output.
- **Override layer** added (`knowledge/overrides.md`): installed users get the
  shipped base verbatim; their reshaping happens via disable/override/exempt/
  new-rule entries in user-overrides files that resolve last and survive
  updates. Authors correct the base via journal `supersedes` only.
- **Wireframe extraction** added as supporting evidence
  (`references/wireframe.md` + `scripts/wireframe.py`, DOM-rect → ASCII,
  tested on synthetic input). Supporting tier: `L-*` findings only;
  Flutter wireframing is stage-2 (screenshot-read method until tooling lands).
- **Consent principle** added for screen capture of user machinery; public
  web pages opened in-session remain default-allowed.
- **Multi-size evidence** added to Phase 2 (realistic widths: 320/375/430,
  ~768, 1440/1728; maps to new rule **L-5 responsive-break-frame**,
  `candidate` until a real multi-width audit runs).
- **Suite rules seeded**: X-1 token drift (defect only under a declared
  `unified` policy), X-2 component parity, X-3 cross-app language, X-4
  class-fit deviation (`established` — they operationalize the fingerprint).

Promotion notes: X-1..X-4 established because they *define* the analysis;
L-5/A-4/T-2 stay `candidate` until observed in-product.

---

## 2026-10-14 · KB seeded (v1)

**Source**: assessment of the Odysseus report
("UI Design Principles and Practices Across System Types") + installation's
own campaign backlog (LusakaRide 2026-09→10), cross-checked against
ui-ux-pro-max data (which the auditor skill deliberately does not duplicate).

**Established rules imported (28)**: C-1..C-3, L-1..L-4, V-1..V-4, P-1..P-3,
T-1, A-1..A-3, F-1..F-5, W-1..W-2. Several came directly from LusakaRide
findings that recurred across two+ audits/files — e.g. C-1/C-2 (driver's
inline `_LocationPicker` + its dead mirror `location_picker_field.dart`),
P-1 (the OverlayPortal/Positioned giant-panel family of fixes), V-2
(state-holes found across passenger screens), F-1 (splash-404 entry-point fix).

**Adopted knowledge upgrades (from the assessment, marked `adapted`)**:
- **T-1 rewritten**: relational target rule (24 css px + spacing, no overlap)
  now the *floor*; 44pt/48dp stays as the practical primary-action
  recommendation — supersedes the absolutist single-number reading.
- **A-4** seeded as `candidate` (reduced-motion guards) — first audit to find
  it in-product promotes it to established.
- **T-2** seeded as `candidate` (in-motion target sizing for driver-glance) —
  calibrate on the driver app audit.
- **Profiles seeded** with the attention-budget frame (driver-glance gets
  tightened glare/motion rules; admin-data-dense explicitly relaxes density).
  All exception lines are provisional until the first real audits correct them
  (that IS the calibration loop).

**Held out deliberately** (candidate backlog, NOT yet rules): condition-based
testing disciplines (real-lighting/weak-Wi-Fi checks), VUI dialogue patterns,
companion-device handoff pattern — none have evidence in-product yet; they
promote when a real audit touches that territory.
---

## 2026-10-14 · Portals batch pt3 — Ant Design Pro + Plausible theme policy

**Ant Design Pro** (preview, light): KPI-tile grammar captured (title/value/
delta chips + mini bar + sparkline), medal-chip ranked lists, icon-rail with
hover-expand, floating settings drawer. **Delta finding**: its chips render
red-up/green-down ("周同比 12%▲ red") — the Chinese-market convention
(red = up/good) — a *third, culturally opposed* policy instance for X-5
delta-color-policy: the rule's core claim ("document your policy") now spans
direction-based (Plausible, Tabler) AND market-convention (Ant Pro) systems.
Drawer harvest (T0s: exemplar-antpro-settings-drawer.jpg): self-service
chrome configurator — nav modes (left/split/right), content width++
流式/固定, fixed-header/menu toggles, primary palette swatches — a strong
exemplar that N-3 sidebar-collapsibility decisions can be USER-configurable.
Failed dark-switch attempt documented (image-card picker not script-clickable;
drawer grammar evidence retained). Primary color rolled to orange mid-study —
the template state, not a defect claim.

**Plausible theme policy solved**: `prefers-color-scheme` matched → html
class flips to `dark` automatically (`schemeDark: true`, class
`h-full plausible dark`) — study 1's dark rendering was OS-responsive, not a
locked theme. Corroborates V-1 (both themes first-class) and adds nuance to
X-5 (policy interactions with responsive theming).

Skips this stretch: none new (airbnb/polaris/design-for-driving previously
logged; hay matches team preference to not force).

**KB effect**: none structural; X-5 gains locale-awareness nuance. Rule count
unchanged at 39. Evidence: 2 new screenshots in docs/img.
---

## 2026-10-14 · REAL AUDIT 1 — LusakaRide admin web + marketing site (calibration)

Full two-system audit per the six-phase protocol (REPORT.md + wireframes +
JSON in audits/2026-10-14/). Artifacts centralized in the skill repo instead
of the audited private repos — deliberate deviation for a private codebase,
revisit if in-repo trend tracking becomes valuable.

**Findings**: admin 6 (3 Major: V-2 empty-copy case, A-2 no aria-sort,
N-3 non-collapsing collapse; 1 X-1 probable suite drift; 2 Minor) · marketing
5 (M1 fake-data-to-AT Major→Minor after profile calibration: public page,
single-visit comprehension cost; C-1/C-3 Minor; L-5 Probable; one borderline
AA-large healthy-with-headroom). 0 Blockers — correct for a codebase that
already went through T7 + campaigns.

**Tooling lessons (the adaptive loop in action)**:
- **Contrast probes must alpha-blend through the ancestor chain** — the first
  probe ignored (a) bg gradients (backgroundImage ≠ backgroundColor) and
  (b) fractional alpha layers, false-failing the CTA band (2.12 fake) and
  mangling the seats chip (20.08 fake). Manual blend math corrected both:
  chip ≈ 7.4:1 PASS, band ≈ 6.5:1 PASS, hero accent ≈ 3.6:1 (AA-large pass,
  thin margin). Promote to candidates: **T0m probe correctness rules** —
  journal only, implementation detail for the next audit agent.
- **React SPA clicks**: synthetic `el.click()` didn't drive the sidebar
  collapse reliably; the ref-based click path did — evidence acquisition
  should prefer ref clicks for SPA state changes (journal note).

**Profile experiences**:
- `admin-data-dense` confirmed: density and structure handled well; the
  failures were *state copy*, *semantics*, and *affordance promises* — the
  exact triad the profile tightens.
- `marketing-landing`: token cleanliness high (built with the KB in mind);
  the residual findings are the AT-leak class (M1) and micro-hygiene —
  matches expectations for a fresh KB-informed build: the loop works.

**Stale-board discipline validated**: two previously "known" issues
(Approvals dead endpoints, duplicated pagination after T7) did NOT resurface
— re-verifying before citing prevented resurrecting fixed defects.
