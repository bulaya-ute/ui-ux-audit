# Evidence tiers and severity

Findings are only as strong as their evidence. Every finding carries a tier;
severity is capped by tier. This is what keeps the report trusted across
repeat audits.

## Evidence tiers

| Tier | Meaning | How to obtain |
|---|---|---|
| **T0s** (on-screen) | What a user actually sees is wrong | Screenshot from the running app / browser tab (browser tools), full viewport |
| **T0m** (measured) | A tool measured the failure | better-design `inspect-spacing` (DOM), computed contrast values, viewport math |
| **T1** (code) | The defect is deterministic in code | file:line + the exact construct; grep-verified repeat counts |
| **T2** (inferred) | Pattern suggests a defect | Cross-file heuristics; naming; convention mismatch |

## Severity caps by tier

| Tier | Max severity |
|---|---|
| T0s | Blocker |
| T0m | Major (up to Blocker when outcome-visible) |
| T1  | Blocker when the failure is unguarded by construction (e.g. no error branch at all) |
| T2  | **Minor (Probable)** — never a blocker |

Rule of thumb: same construct found once with T2 and once verified T1 → the
finding is T1 everywhere it recurs (cite the strongest instance, list repeat
sites compactly).

## Severity ladder

- **Blocker** — a user-visible failure in a primary path reachable today
  (broken entry point, no failure state on a data screen, blown-out overlay,
  unreachable content).
- **Major** — degrades a primary flow or materially raises error-rate/cost
  (contrast, target size, dead ends, irrevocable-without-confirm, clipping).
- **Minor** — polish with real consequences if deferred long (icon labels,
  spacing rhythm, terminology).
- **Probable** — T2 only; needs a check the auditor couldn't run. State what
  would confirm it.

## Profile calibration

`profiles.md` overrides severities (tighten/relax) and validity. Calibration
goes: default (checks.csv) → profile adjustment → evidence tier cap → final.
Record any profile override in the journal (that's the calibration history).

## Counting discipline

Blockers are rare by design. If an audit yields >3 blockers, suspect either a
real systemic break (fine — group them under one systemic finding with repeat
sites) or over-eagerness (recheck tiers). A good audit ends with findings the
user would have missed, not findings they'd contest.
