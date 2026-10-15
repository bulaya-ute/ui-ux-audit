# WORKSTATE — LusakaRide Mobile/Full Audit Night (2026-10-14 →)

**Mission**: full ui-ux-audit of the two mobile Flutter apps (run on Linux desktop, multi-size),
fix what's found, along with pending fixes from the earlier web/marketing audit. The user
is asleep; blanket permissions granted (see PERMISSIONS). Work autonomously; update this
file continuously so context compaction never loses state.

## PERMISSIONS (granted 2026-10-14, before user sleep)
- Full audit of mobile apps, run as Linux apps at multiple screen sizes.
- Control the user's computer (browsers: firefox + chromium available).
- Checkout dev/new branches in ALL repos; on testing branches: modify/commit/push freely.
- Containerized DB that is easily discarded/reset.
- Fix all issues seen; keep working until the system is complete.
- Make decisions for LusakaRide.
- IMPORTANT: audit repo (public) may hold evidence screenshots — mask personal data (phone numbers etc).

## DECISIONS MADE (recorded)
1. **Suite policy: `unified`** — one design system (LrBrand tokens) across admin web,
   marketing, both mobile apps. Admin gets LrBrand greens (login panel + accents);
   slate dark neutrals stay as admin's documented variant.
2. **Audit DB**: separate container `lusakaride-audit-pg` (port 5433, db `lusakaride_audit`)
   — dev DB untouched; reset = stop/rm/rerun (server auto-migrates + seeds).
3. **API on 5287** pointed at the audit DB for this session via
   `ConnectionStrings__Default` env override (Host=localhost;Port=5433).
4. **Branches**: `audit/ux-1014` off develop in passenger/driver/admin-web;
   off main in marketing. Commits push to these audit branches only; merges to
   develop/main are tomorrow's user-facing decision (or my call if they said fix).
5. **Multi-size harness in apps**: `window_manager`-based size presets driven by
   `--dart-define=AUDIT_WINDOW_CONTROLS=true` (guarded, so normal builds unaffected).
   Presets: 360×720, 375×812, 414×896, 768×1024, 1024×700.
6. **Screenshots path**: try gnome Shell Screenshot DBus / grim; else Flutter VM-service
   screenshot; last resort: window-positioned crops. Evidence → audits repo `docs/img/`.
7. Smart filters ON in admin tables is NOT business data risk — mock OTP `123456` on the
   audit DB is acceptable (dev DB isolation).

## OBJECTIVES (definition of "complete")
1. Audit DB + seeded sample data (locations, itineraries w/ stops, driver+vehicle
   approved+pending, passengers, bookings incl. waitlist/completed, ride in progress,
   notifications) — so tables/flows show REAL density. [seed script in audit repo
   `scripts/seed-audit.py`, called against http://localhost:5287]
2. Admin web fixes from audit 1: A1 empty-branch+copy, A2 aria-sort, A6 spacer th labels,
   A3 real icon-rail collapse, A4 token alignment (suite unified). Commit+push.
3. Marketing fixes: M1 aria-hidden mocks (+ description), M2 single color util, M3 Check
   component. L-5: narrow-width captures via chromium headless -window-size 375 →
   fix anything that breaks. Commit+push.
4. Mobile apps audit: launch each with harness at sizes; audit flows (passenger:
   sign-in OTP→browse→detail→book→my bookings→profile; driver: sign-in→home/active
   assignment→manifest→add-vehicle banner→profile); fix issues found (contrast, targets,
   layout at narrow widths, state holes); commit+push to audit branches.
5. Final: journal the skill KB with anything new; WORKSTATE updated; push all.
   Report a morning summary in chat + workstate file.

## PENDING / RISKS
- gnome-window-control skill needs GNOME extension + logout/login — AVOID (would kill the
  session); prefer window_manager harness + grim/DBus screenshots.
- External network flaky (github push timeouts recur); push after each batch, retry.
- cal.com-style code audits for mobile not applicable; mobile evidence is
  screenshots + widget-code (T1) + window probes.
- If WindowSize harness fights Linux GTK quirks, fall back to `flutter run --dart-define`
  launching at fixed sizes (restart per size).

## PROGRESS LOG (append newest first)

### 2026-10-15 (morning-2) — stock-imagery pipeline + passenger seeded capture
- **User request fulfilled — free imagery**: sources verified from their
  license pages (Pexels/Pixabay/Unsplash/Commons/Openverse: see
  `knowledge/stock-image-sources.md`), and TWO real-Lusaka CC photos wired
  into the marketing site (Manda Hill bridge strip on How-it-works; Kalambo
  Road intersection on For-drivers) with `docs/IMAGE-CREDITS.md` provenance.
  Rejected: Bus-Terminus (burned-in magazine typography) and non-Lusaka
  stand-in streets. Evidence: desktop + mobile strips; lazy-load renders
  blank in headless VTB captures — flip eager for the shot, back after.
- **Passenger seeded capture**: logged-in home with 13-seat bookable route +
  "Full — Join waitlist" route (passenger-04-boot-active.png). Copy bug:
  "via 1 stops" → fix queued ('via 1 stop' when count is 1).
- **Morning queue final**: (1) 'via 1 stops' copy fix both apps if the
  passenger copy has it (which file?) + re-push; (2) V-8/P-4 promotion
  (the sentinel-suite path already covers V-8 preconditions; P-4 gate
  evidence needs the user's fresh retake); (3) driver vehicle/assignment
  walk needs real UI interaction — user-driven next; (4) merges to
  develop/main after user reviews the commits; (5) seed script rerun-safe
  — future audits can rebuild data in 1.6 s.

### 2026-10-14 (morning, final) — driver leg walked, fixes shipped, session recipe
- **Driver session boot solved (recipe in journal)**: keyring+prefs injection
  (fbss-linux one-JSON-item format) + define-gated `AUDIT_SESSION_*`
  override in the driver's SessionStorage (inert in prod) — the app boots
  straight into the signed-in tenure; approved-state transition verified
  live after the admin approve (204).
- **Driver findings fixed** (`d518468`): empty-name greeting dendrité
  ('Good evening, !' → 'Driver') via `_displayName()`; AuthPhoneField hint
  (`e.g. 97 123 4567`) + brand-green focus ring. Passenger copy got the
  same hint/focus fix (`7c40d03`). Suites: driver 87 ✓, passenger 49 ✓.
- **Second server restart hit between phases** — stack-back procedure
  (podman start audit-pg → dotnet run 5287 → npm dev 4318) documented and
  repeatable in <2 min; all git work survived (pushes happened per-batch).
- **Morning rests on**: merges to develop/main await user review; the
  passenger V-8/P-4 promotion evidence (search empty-state re-shoot with the
  login-hint fix) is ONE app relaunch + two taps away; seeded-route success
  flow + vehicle-walk remain queued behind `scripts/seed-audit.py`.

### 2026-10-14 (late-morning, post server-restart) — session-injection technique + walk resumed
- **Harness root cause found for the white windows**: Flutter GTK windows do
  NOT compose their first frame until a real input event arrives — activate +
  one click then shoot instantly → content paints. Confirmed on release AND
  debug. (And release mode ≠ cause; capture path healthy all along.)
- **Flutter-typing killswitch workaround discovered**: GNOME Keyring session
  injection. Components: flutter_secure_storage_linux stores ONE JSON
  item (label `com.example.<app>/FlutterSecureStorage`, attr
  `account=com.example.<app>.secureStorage`) whose keys are the Dart keys
  (`lr_driver_access_token` …); plus shared_preferences.json in
  `~/.local/share/com.example.<app>/` for the user id/phone. Provision the
  identity through the API (curl send-otp/verify-otp — mock 123456), then
  write both stores, relaunch app → boots straight INTO the session.
  Reusable for any future pixel-audit session (skill candidate recipe).
- **Driver identity provisioned on audit DB**: phone +260 97 123 4568, driver
  id b6530f3a-…, Status Pending (MySQL? no — Postgres). Admin token for
  approval probe: 200 (`/tmp/opencode/admin-token.txt`).
- All commits/pushes from the earlier phase survived (passenger sentinels
  `5a91a65`, A7 web `10fda22`, audit repo `704e82c`, T7 server fix).

### 2026-10-14 (morning) — overflow sentinels shipped; real bug fixed
- **overflow_sentinel_test.dart** (passenger `audit/ux-1014` 5a91a65):
  16 assertions × 4 sizes (360/375/414/768) over Login/VerifyOtp/ProfileSetup/
  ItinerarySearch; boots via AppGlobals + ApiClient(mock) + ApiCacheManager +
  SharedPreferences mock. First run caught a SHIPPED BUG: search screen
  count+sort Row overflowed 121px@360, 67px@414 (SegmentedButton ~449px
  intrinsic). Fixed via LayoutBuilder (stacked below 600px). Full suite 49 ✓.
- **A7 (web) fixed+verified** (10fda22): CompareFilter between-pair stacked
  vertically; DOM probe 4/4 at 120–123px clipped 0.
- **Mobile-leg addendum written into REPORT.md** (T7 incident, P-4/V-8
  candidates, L-6 promoted, harness lessons).

### 2026-10-14 (night, later) — gnome-window-control unlocked tomorrow's plan + mobile leg ran
- **gnome-window-control extension live** (user built it; skill at
  `~/.claude/skills/gnome-window-control/`): window screenshots + REAL clicks/
  typing. Flutter **web synthetic-semantics** limitation MOOT for desktop
  builds — molten path: run app as Linux build with harness → drive + shoot.
- **T7 server regression caught live during passenger audit**:
  search 500'd (`StopIds.Contains` JSON-column query untranslatable, again).
  Fix in-memory post-materialization committed on server `audit/ux-1014`;
  API relaunched on audit DB; curl-verified 200 + `totalCount:0`.
- **Passenger count-fix shipped** (`f00e05b`, passenger `audit/ux-1014`):
  route-count blanked while error shown (V-8 candidate re: contradictory
  "0 routes found" + error panel). Re-verify live in morning.
- **Admin A7 found+fixed+verified** (`10fda22`, web `audit/ux-1014`):
  CompareFilter side-by-side between-pair clipped native date inputs
  ("dc📅") + number placeholders ("M⇅") at default column widths — stacked
  vertically; DOM probe: 4 inputs at 120–123px, clipped 0 (was 4). KB rule
  **L-6 promoted established**. Also re-verified A1/A2/A3/A4 live on
  /bookings via DOM probe (new copy ✓, no old copy ✓, 9 aria-sort ✓,
  brand #4ebb78 ✓, collapse ✓) + Passengers window screenshot.
- **KB seeds**: P-4 (permission-ask-context-gated, candidate),
  V-8 (stale-metric-beside-error, candidate), L-6 established (42 rules now).
  REPORT.md mobile-leg addendum + journal entry written.
- **Harness lessons logged**: click element vertical centers (1px above edge
  = silent dead click); overlapping 375×859 windows swap click targets —
  separate windows spatially; screenshot-feedback-every-step (row geometry
  shifts with data). Passenger flows verified live tonight: OTP login →
  profile → home → From picker (+ exclusion + clear) → To picker → search
  error path → (fixed server) empty-state path pending visual re-shoot.
- **Morning queue**: re-shoot passenger search empty-state (To-click center
  + Search at dy≈413); driver-app leg on audit DB (onboarding → vehicle →
  assignments → manifest); seeded success flow (`scripts/seed-audit.py` —
  user call); P-4/V-8 promotion after re-verification; overflow-sentinel
  widget tests at 360/414/768 [DONE — see morning entry]; remaining portals
  (Umami/Matomo/Sentry); merges to develop/main for user review.
- Processes: API 5287 fixed-branch build on audit DB (bg shell), admin
  4318, marketing 4173 (http.server on dist), passenger window id
  2635293260 @(773,127), driver 2635293261 @(823,177) — driven via
  gnome-window-control only (Flutter web 4320 no longer needed).
  [UPDATE after server restart: ALL bg shells killed; audit DB container
  restarted `lusakaride-audit-pg`; API 5287 + admin 4318 relaunched;
  marketing 4173 still to relaunch; app windows to be relaunched as
  needed via release builds + click-for-first-frame.]

### 2026-10-14 (night, late) — state lock for morning handoff
- **DONE/pushed** (audit branches): admin-web A1/A2/A3/A4+A6 (empty-state copy
  + branch behavior, aria-sort, icon-rail collapse, LrBrand suite tokens);
  marketing M1/M2/M3 (mock aria labels, amber-ink token, SVG sprite);
  marketing multi-width L-5 evidence captured at 320/375/1728 via
  `chromium-browser --headless --screenshot --window-size=...` (320 passed;
  --virtual-time-budget needed for settled captures — noted as audit-repo
  capture-recipe lesson in workstate).
- **Mobile harness works on LINUX desktop**: window_manager harness boots
  passenger at 375×812 with resize logger (audit branch;
  --dart-define=AUDIT_WINDOW_CONTROLS=true). Pixel evidence blocked tonight:
  GNOME DBus screenshots denied (no grim/scrot/sudo), flutter VM-service
  inspector.screenshot needs inspector object ids that don't register on
  this build, and Flutter **web** app renders fine (login visible) but
  widget-driving requires the semantics DOM which resists synthetic
  activation (tried placeholder click/focus, ext.flutter.accessibility via
  DWDS → null-arg failure). NEXT (morning): semantics via a real screen
  reader/Slow DevTools, OR Flutter widget tests as overflow sentinels at
  360/414 (deterministic T0m), OR user-driven device walk-through with the
  installed APK (best fidelity anyway). [UPDATE: resolved by
  gnome-window-control — see the later log entry above.]
- **Real mobile finding already in hand (candidate)**: location-permission
  gate shows PRE-LOGIN on launch (screenshot in evidence set) — premature
  permission ask; should be context-gated (only when the map is relevant).
  Candidate rule seed: P-4 `permission-ask-context-gated`. [SEEDED in KB.]
- **Infra live for morning**: API:5287 → audit DB (lusakaride_audit,
  15 seeded locations; server auto-seeds); admin dev:4318; marketing
  preview:4173; passenger web build:4320 (via harness page in web/ folder);
  evidence http server:4321. `pkill -f` self-match hazard noted — kill by
  `/bin/` DLL path or exact port PID.
- Branches: all four target repos on `audit/ux-1014` (server now holds the
  T7 fix on its audit branch too).

### 2026-10-14 (night) — setup
- WORKSTATE created; audit DB plan set.
