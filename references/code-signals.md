# Code signals — per-stack defect patterns

Static signals that map to KB rules. Grep snippets are starting points, not
verdicts — every hit needs reading before it becomes a finding (T1 requires
the construct confirmed, not a keyword). Signal can be used to *hypothesize*
(T2), then confirm by reading.

---

## Flutter (passenger/driver apps)

### C-1 inline-duplicated-component / C-3 literals
- Repeated widget instantiations at call sites: grep the screen file for
  repeated `Padding(` + `Container(` + `Text(` groups, or identical list-item
  builders copy-pasted across two screens.
- Two sibling screens that build the same object-card each with their own
  private `_Card`-ish class. (Experienced: driver/ad and passenger both had
  per-app copies of widgets — per-*repo* copies are convention and fine;
  per-*file* or per-*class* duplication is the C-1 defect.)
- Hint strings, radii (`circular(12)`, `circular(14)`, `circular(16)` mixed
  for the same element class) → C-3.

### C-2 dead-code-copy
- `grep -rn "class <Name>" lib/` where the class appears in one file only and
  the file has zero imports. (Experienced: driver `location_picker_field.dart`
  duplicated the live inline picker, zero usages.)

### L-1 rhythm / L-2 clipping
- `grep -n "EdgeInsets.fromLTRB(1[379]" -r lib/` and similar non-4/8 values.
- `SizedBox(height: <literal>)` chains vs theme spacing constants.
- Fixed `height:` on `Container(`/`SizedBox(` wrapping `Text` without
  `maxLines` → clipping risk with long strings/self-translations.

### V-2 state-holes
- `await ApiClient...` followed by `if (!mounted) return;` then *only* a
  success branch — no `isSuccessful == false` UI, no empty-list branch.
- `ListView(children: data.map(...))` with no `data.isEmpty` alternative →
  blank screen on truly-empty data.
- `ref.watch(provider)` screens that never render `AsyncError`.

### P-1 overlay/positioning hazards
- `OverlayEntry(` used directly (raw overlay) instead of `OverlayPortal` with
  constrained `Positioned` roots.
- `Positioned(` inside `TextFieldTapRegion`/other ParentData-consuming
  wrappers (the "Incorrect use of ParentDataWidget" giant-panel bug class).
- `CompositedTransformFollower(` without a cap on BOTH axes when the anchor
  box is near an edge.
- Any overlay panel measuring anchor size from `context.findRenderObject()`
  *inside* `overlayChildBuilder` (resolves to the overlay, not the field —
  the documented crash root).

### P-2 sticky/safe areas
- `bottomNavigationBar`/`persistentFooter` + `CustomScrollView`/`ListView`
  without bottom padding inset.
- `SafeArea(` missing on full-bleed app-bar-less screens; `MediaQuery.viewInsets`
  unused where a keyboard opens over fixed CTAs.

### T-1/T-2 targets
- `IconButton(iconSize: <20)` + no `visualDensity`/`padding` → 40px targets;
  `GestureDetector` on small `Icon(` without a wrap.
- Adjacent `InkWell(...)` rows/buttons inside tight `<8px` gaps.
- Driver screens (profile `driver-glance`): anything tappable <48dp.

### A-1..A-3
- Status/badge widgets whose *only* difference between states is color.
- `Icon(` inside `IconButton/InkWell` where `<icon>` has no
  `semanticLabel`, or `Icon(..., size: 20)` in `icon:` role inside
  `IconButton` with `tooltip: null`.
- `TextField` without `validator`/label hook, custom widgets with no
  `Semantics` even when composing interactive parts.
- Animations (`AnimatedContainer`, custom tweens, page transitions) without
  `MediaQuery.of(context).disableAnimations` check (A-4).

### F-flow pertinents in code
- `Navigator.push` chains where the pushed screen can finish without a way
  back (`Navigator.pushReplacement` after mutating state = possible dead end).
- `showDialog` paths that don't `dismissLast()` on error branches (leaked
  dialog over failed submit — historically a real LusakaRide bug class).
- Submit handlers catching failures that don't reset `setState(submitting…)`.
- Screen-level `&(dispose)` missing subscription/focus/controller → leaked
  resources over flow repeats.

---

## React / TS (admin web `lusaka_ride_web`, marketing site)

### C-1 / C-3
- Repeated identical JSX blocks (3+ lines copied across table pages:
  filter toolbar chunks, pagination footers, confirm dialogs).
- Duplicated inline style objects: `style={{...}}` with same object shape
  repeated; magic pixel paddings; `className` strings re-composed per page.
- Hand-rolled pagination patterns (the admin app has one duplicated 3×) —
  classic C-1.

### L-1 / L-2
- Tailwind arbitrary values (`px-[13px]`, `w-[547px]`) sprinkled where tokens
  exist; text containers with `overflow-hidden` and no truncate.
- Grid gaps drifting (`gap-2` vs `gap-3`) across equivalent sections.

### V-1 / V-2
- Text on tinted brand surfaces without contrast check (e.g. slate text on
  `bg-brand-50`).
- `data.length &&` guard with no `data.length === 0` branch → empty
  containers instead of empty states; `isLoading` branch missing on async
  tables; catch that only `console.error`s.

### P-1 / P-3
- `position: absolute` with magic offsets inside flow containers (mentor
  modals over relative parents missing → off-screen banners, a recurring
  real finding class).
- `z-50`/`z-[999]` stacking collisions; full-screen `pointer-events-none`
  overlays; `Modal` without focus trap / Escape handling.

### A-*
- Interactive `<div onClick>` (re: no button role/tabindex); icon-only
  buttons with `aria-label` missing; headings skipping levels.
- `useEffect` scroll/animation without `prefers-reduced-motion`.

### F-*
- Route tables containing dead routes / dead links (from old screens);
  `Link href` targets missing; buttons with `disabled` logic flipped.
- Forms: no `noValidate`-consistent inline errors; multi-step where step N
  doesn't restore step N-1 state on back.

---

## Cross-stack reading order (audit hygiene)

1. Route/screen inventory first (so you know the app's real shape).
2. Then grep the highest-signal tables above for the file set.
3. Then read (not skim) the 3–5 screens that anchor the flow.
4. Then apply severity.md calibration + report.

Anti-pattern to avoid: grep-driven findings dumps. Signals generate
*hypotheses*; the report cites *read and confirmed* evidence only.
