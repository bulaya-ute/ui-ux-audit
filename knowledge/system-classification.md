# System fingerprint — multi-dimensional classification

Before rule application, the auditor fingerprints the **system** along
multiple dimensions. The fingerprint decides *which rules matter and how
they bind* — the same UI pattern is judged against the class the system
claims to be in, not against a universal ideal.

## The fingerprint axes

| Axis | Values (typical) | Determines |
|---|---|---|
| **Surface** | phone-mobile · tablet · web-desktop · tablet-web · kiosk · watch · tv | Layout expectations, target sizes, input vocabulary |
| **App-kind** | see `profiles.md` (task / glance / data-dense / marketing / dev-tool) | Which profile calibrates severity |
| **Suite membership** | standalone · sibling-suite (multiple apps, one platform or family) | Whether cross-app consistency rules apply at all |
| **Sibling design-system policy** | `unified` (tokens identical) · `themed-variants` (same system, per-app accent swaps — "same skeleton, swapped primary/secondary") · `independent` (deliberate divergence) | Whether X-1/X-2 are defects or intended design. **The policy must be explicit** — asked from the owner or evidenced in-theme — never assumed |
| **Primary audience** | riders · drivers · admins · public/anonymous | Copy reading level, trust signals |
| **Input primary** | touch one-handed · touch two-handed · pointer+keyboard · voice | Target sizes, hover-dependent patterns |
| **Motion tolerance** | standard · reduced-required (safety/medical) · latency-bound | A-4 application |
| **Evidence surface available** | running app · live DOM · code only | Which evidence tiers are reachable |

## Sibling suites (the multi-app case)

When the fingerprint shows a **sibling suite**, three consistency rules
activate — but ONLY within the declared policy:

- **X-1 token drift** (`unified` only): the same color *role* resolving to
  different values across sibling apps (e.g. one app's page background is
  `#F9F9F9` and its sibling's is `#E4F7EC` for the same role) — a defect in
  `unified`, *intended variety* in `themed-variants` (but then it must be a
  documented role mapping, not an accident), and ignored in `independent`.
- **X-2 component parity** (`unified`/`themed-variants`): shared components
  (cards, pickers, dialogs) must keep the same structure across siblings —
  same anatomy, same interaction grammar — differing only by the declared
  theme axes. Structure drift (an overlay picker in one app, a stock
  dropdown in its sibling) is a defect at Major under the first two
  policies.
- **X-3 cross-app language**: the same action/object named the same way in
  every sibling ("Book" means booking a seat in all apps; "trip" vs "ride"
  used consistently). Copy drift across a suite confuses the whole product
  family, not just an app.

Audit practicalities: fingerprinting a suite means diffing theme/token files
across sibling repositories (Flutter `lr_theme.dart` ↔ sibling
`lr_theme.dart`; tokens/`@theme` blocks in web repos) — line-diff them and
catalogue which deltas are *role mapping* (policy-consistent) vs *drift*
(nobody decided).

## Class-fit deviation (the meta-check)

Once classified, the analysis itself changes stance: **audit the system for
fitness to its class** (see `knowledge/profiles.md`), and flag
*class-fit deviations*:

- a task app behaving like an admin console (density above profile),
- an in-vehicle surface hiding depth or using hover-only affordances,
- a marketing page demanding app-like dense data reading,
- data-dense admin restricting itself to phone-scale patterns (7-element
  screens) that cripple professional throughput.

These deviations are the most valuable findings an auditor can surface —
report them as `Class-fit` findings with the axis that's violated.

## Volatile axes (record, don't lecture)

Some axes change during a session (window resize, tablet rotation, dark-mode
switch). The protocol: audit the **dominant claimed surface first**, then spot
check the volatile ones (`L-5` responsive-break-frame) — never litigate an
orientation choice as a defect.
