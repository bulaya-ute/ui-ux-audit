# Flow protocol — mapping flows before judging them

You cannot flag "poor flow" without having *drawn* the flow. This protocol
turns a fuzzy flow review into a graph + coverage audit. Output: a compact
flow map (text, not a diagram tool) + coverage matrix + findings.

## 1. Enumerate entry points (with code evidence)

- **First-run / signed-out paths**: splash → routing decision → sign-in →
  first content. What happens if the session is half-dead (401 mid-flow)?
- **App deep links & notifications**: intent filters / route defs; notification
  payloads → which screen, with what invalid-id fallback?
- **Error recovery routes**: after a 401/403/404, where does the user land?
  Forced-logout modals?
- **In-app entries**: tabs, cards, cards' empty states, FABs — list them all;
  every entry is a promise that the destination is usable *from this state*.

Signal Grep (Flutter): route tables (`GoRoute`, custom `NavigationController`
push calls), `Navigator.push(`/`AppGlobals.nav.push` sites, notification
payload handlers. (React): `createBrowserRouter`/`<Route>` defs,
`navigate(` sites, notification/redirect handlers.

## 2. Trace the happy path, then perturb it

For the flow's primary job (e.g. passenger booking):

happy: search → select departure → seat/fare confirm → pay/skip → success

Perturbations to trace one by one (each is a row in the coverage matrix):
- **It's full**: waitlist offered? FIFO promotion explained?
- **It's gone**: route/departure removed mid-flow (stale list) — how does the
  user find out? (F-5: the detail screen must *say*, not 404-crash)
- **Session breaks**: 401 mid-flow → re-auth → return to the same step or
  data loss?
- **Network breaks**: submit fails → retry preserves input + no double charge
  (idempotency-ish UX).
- **Back mid-flow**: back at each step — honest navigation (confirm-on-dirty),
  not a silent loss.
- **Recentration**: user backgrounds the app during an expiring step (OTP,
  hold expires) — recoverable with explaination?

## 3. Coverage matrix (output artifact)

For each screen in the flow, mark coverage of:
`loading · empty · error+retry · permission-denied · stale-refresh ·
success · undo/exit`

Any `GAP` in the matrix is a `V-2` candidate (state-holes). A screen with
happy-path-only coverage is the highest-yield finding class in real apps.

## 4. Flow graph (output artifact)

Compact text graph with edges labeled by condition:

```
[Home: search] --routes found--> [Detail]
[Detail] --booked--> [Confirm(code)] --> back to Home(list refresh)
[Detail] --no routes--> [Empty(try again)]  ← must offer exit
[401 anywhere] --> [Sign-in] --resumed--> <same step or home — WHICH?>
```

Findings read off the graph: dead ends (`F-2`), inconsistent back behavior
(`F-3`), entry-point gaps (`F-1`), object-name drift along edges (`F-5`).

## 5. Flow-specific severities

A broken *happy path* entry (F-1) is Blocker. Broken *perturbation* path ≥
Major when the perturbation is plausible monthly for the target user. Broken
*edge-case* paths (deep-concurrency races) are Minor/Probable unless they lose
work or money — those are Major/Blocker (data/money loss is always elevated).

## 6. Cross-screen consistency sweep (last pass — cheap, high-yield)

- Object names: list row vs detail title vs confirmation copy vs notification.
- Dates/times: `07:30` vs `"morning"` vs raw ISO — one format per flow.
- Primary action: same placement/shape/color on every step of the flow.
- Back: label ("Back" vs route name), and *does* back cancel pending work?
- Error copy style: consistent voice (see W-1; the campaign's descriptive
  errors standard).

## Output discipline

The flow map + coverage matrix live at the top of the report (or an appendix
for long flows). Every flow finding references the edge or matrix row that
exposes it — "flow says A→B on full; code says A→B' is unreachable" — not
just a screen-local complaint.
