# ui-ux-audit knowledge journal

Newest first. One entry per audit session or KB change. This file is the
narrative diff of the knowledge base; `checks.csv`/`profiles.md` are the state.

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
