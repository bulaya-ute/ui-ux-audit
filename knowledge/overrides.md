# Override protocol — how users reshape the knowledge base

The shipped knowledge base (`checks.csv`, `profiles.md`) is the **opus
excellence baseline** the skill's authors publish; on install every user gets
it verbatim. Users then adapt it to their product — WITHOUT editing shipped
files — via the override layer. This keeps updates safe: the base can be
updated upstream while user intent survives.

## The layers (reading order)

1. **Base** — `checks.csv` / `profiles.md` (shipped, versioned, IDs stable).
2. **User overrides** — loaded if present:
   - User-global: `<skill-dir>/user-overrides.md` (survives skill updates).
   - Project-local: `<repo>/audits/overrides.md` (per-product intent).
3. **Audit-time calibration** — Phase-1 fingerprint + user corrections,
   recorded in the journal (ephemeral until promoted into an override file).

**Override resolves last and wins.** The journal records what overrode what.

## Override grammar (plain markdown, grep-able)

```markdown
### override: T-1 · project passenger-app · 2026-10-15
severity: Minor            # instead of Major
because: >-
  This app is an in-office kiosk variant; targets stay 24css but pilots
  showed 40dp fine for the primary CTA which is always full-width.
review-by: 2027-01         # optional expiry so overrides don't fossilize
```

```markdown
### disable: W-2 terminology-drift · reason: brand naming is in flux
### exempt: L-3 density-above-profile · context: roster screen in driver-glance
### new-rule: C-4 · domain reuse · name "prefab-widget-missing"
   ...full rule body, severity default, applicability...
```

- **override** = change severity/meaning for a context
- **disable** = rule doesn't apply here (must give a reason)
- **exempt** = scoped to named screens/contexts only
- **new-rule** = user-authored rule (gets a `u-` prefixed ID in reports; the
  author may later promote it into the base and rename the ID)

Every override: `id + scope + because (+ optional review-by)`. Overrides
without reasons are rejected by the auditor at read time — intent must be
recordable, otherwise the knowledge base quietly rots.

## Author-side flow (what the skill's authors do)

1. Audit real systems (target projects AND public exemplars) per the
   protocol.
2. Journal findings; flag issues in the base itself as the authors (base
   corrections go through the journal as `supersedes` entries and land in
   `checks.csv` with stable IDs).
3. Push a new base release; user overrides (separate files) survive.

## Update safety

- Base IDs are never renumbered; retired IDs stay retired (journal notes).
- New base versions may introduce rules an override disables — that's
  allowed and requested behavior; the report shows `(rule disabled by
  override)` transparency lines for disabled/exempted rules so reviewers can
  see what the user chose not to audit.
