# ui-ux-audit knowledge journal

Newest first. One entry per audit session or KB change. This file is the
narrative diff of the knowledge base; `checks.csv`/`profiles.md` are the state.

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
