# App-kind profiles — severity calibration table

Profiles encode the *context of use*: attention budget, motor condition, and
environment. They adjust the default severity in `checks.csv` — and, in some
cases, flip validity ("this is fine here, wrong there"). When a real audit
finds the profile itself wrong, that correction is a **profile exception**
recorded under the profile below AND journaled.

The frame: each profile sets (a) attention budget, (b) motor condition,
(c) environment, (d) allowed-pattern exceptions, (e) tightened rules.

---

## passenger-task
Everyday mobile app, one-handed use, on the move but seated-ish: attention
MEDIUM; motor precision GOOD but one-handed; connectivity variable.
- Tightened: `L-3` (density ≤ ~7 interactive elements on prime screens),
  `T-1` (44pt/48dp practical floor for primary actions), `W-1` (descriptive
  errors — riders act on them alone).
- Standard: `V-*`, `P-*`, `F-*`.
- Exceptions: none yet. *(first calibration pending)*

## driver-glance
Driver app, used in-and-around a vehicle: attention LOW and fragmented by
driving; hand may be off-screen; glare and windscreen direct-sun; interruptions
frequent. UI must survive being *missed*.
- Tightened: `T-2` (≥48dp for any action available while the vehicle may be
  in motion; larger still on primary), `L-3` (one primary action; feed-style
  layouts), `V-1` (contrast checked at simulated-glare: dark text on white
  fields reads close to illegible at sun angles), `F-2` (no dead ends — a
  driver tapping the wrong thing must always land somewhere recoverable),
  `W-1` (errors must say exactly what to do next; recovery time is safety).
- Exceptions: **data density may rise on stop-screen views** (manifests,
  rosters) — dense lists are legitimate when the vehicle is stationary. In-
  motion screens keep the glance rules. (provisional — calibrate)

## admin-data-dense
Admin web console (React), DOM pointer + keyboard, large screen: attention
HIGH; motor precision HIGH. The point is throughput, not minimalism.
- Relaxed: `L-3` density rules don't apply to tables (dense rows are the
  point); `T-1` never shrinks targets below 24 css px but 44pt is not
  required for row-scoped actions; multi-step flows may use drawers instead
  of full screens.
- Tightened: `C-1` (duplication across the 7 management tables grows into
  drift fast), `V-1` both themes (dark mode is a first-class surface),
  `F-5` (object naming across list→detail→bulk action).
- Exceptions: stacked filters and operator UIs are allowed if they don't
  hide results; empty states may be plain text with a link (not cards).

## marketing-landing
Public site (one-pager, static): attention MEDIUM-HIGH, cursor or touch,
motivated visitor. Honesty and clarity outrank novelty; performance is part
of UX (every 100 kB of JS is a conversion tax).
- Tightened: `L-2` (no clipping at 320px / 1440px), `V-1` (contrast on tinted
  brand surfaces), `A-4` (reduced-motion fallbacks), `W-2` (claims must match
  the actual product — marketing copy that over-promises is a W-2 defect).
- Exceptions: none yet.

## dev-tool (default when nothing else fits)
Dashboards/simulators/internal tooling: attention HIGH, precision HIGH,
tolerant of density; but correctness of states and copy matters most.
- Tightened: `V-2` state holes (an internal tool with a missing error branch
  silently corrupts work), `W-1` (only place where "display raw error" is
  acceptable).
- Exceptions: none yet.

---

## Composing a new profile (when none fits)
Ask: device? attention? motor condition? environment (motion/light/network)?
Then propose: tightened rules (2–4), relaxed rules (with reasons), exception
lines. The user accepts it → it lands in this table with a `calibrate` note
and a journal entry. That is the skill's most important adaptive loop.
