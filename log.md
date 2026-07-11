# Change log

* 2026-06-22 — Initial import. Converted the Nutritionist `CLAUDE.md` into an OKF
  knowledge base: 8 topic folders, 28 knowledge pages, one `index.md` per folder.
  Content lifted faithfully (rules, file:line refs, user quotes, dates, 🔁/⚠️
  supersession markers preserved). This base is now the canonical source; `CLAUDE.md`
  is reduced to a pointer plus the few things the agent needs loaded every session.
* 2026-06-22 — Added `design-system/wwdc2026/` (3 pages) distilled from WWDC 2026 design
  sessions: Principles of Great Design (250), Communicate Your Brand Identity on iOS (251),
  Design Intuitive Search Experiences (292). Each page pins its canonical Apple link so the
  source stays reachable when it's richer than the summary.
* 2026-06-22 — Applied 3 WWDC26 design changes to the app and recorded them under each
  `design-system/wwdc2026/` page's "Applied in Nutritionist" section: (1) Dynamic Type first
  pass on the food log, (2) an AI-estimate disclaimer on the captured food card, (3)
  `.searchable` on Past Food / Library. All build- and screenshot-verified on the iOS 27 sim.
* 2026-06-23 — Read the remaining WWDC26 design sources and added 5 pages to
  `design-system/wwdc2026/`: What's New in SwiftUI (269), Modernize Your UIKit App (278),
  Liquid Glass (technology overview + SOTU 102), HIG map + iOS 27 deltas (HIG + What's new —
  Design), and Apple Design Resources (+ 9to5Mac). Two SPA pages (HIG landing, Liquid Glass
  overview) were JS-blocked for WebFetch/curl and read via the Chrome MCP (real browser).
  Each page pins its canonical link(s); two pure link-hubs (videos index, WWDC26 design
  guide) are recorded as references in the subfolder index, not mirrored.
* 2026-06-23 — During the WWDC26 improvement run, recorded the food-log row
  swipe-to-delete rejection (conflicts with the horizontal date-swipe pager) in
  design-system/rejected-experiments.md so it isn't re-attempted.
* 2026-06-23 — Added trends/charting-best-practices.md: Apple's chart best practices
  (HIG Charting data + WWDC25 313 + WWDC26 SOTU, canonical links pinned) plus the concrete
  gaps in our Trends charts (no accessibility/Audio Graph, no scrub interactivity, no
  descriptive takeaway, weak empty state).
* 2026-06-24 — Added today/planet-globe.md: a detailed worked-example of the opt-in 3D
  "Planet" calorie globe (spinnable SceneKit Mars→Earth sphere, CPU texture cross-fade by
  calorie fraction). Documents the full annotated code, the asset sourcing + licensing
  (Solar System Scope CC BY / NASA SVS public domain), the iOS-27 SceneKit shader-modifier
  dead-end, and the headless (simctl-only) verification approach.
* 2026-06-23 — Expanded trends/charting-best-practices.md with the zoom/scroll interaction
  best practice (pinch-zoom isn't idiomatic; use a range selector + native
  .chartScrollableAxes scroll + .chartXSelection scrub) and the Audio Graph accessibility
  recipe (accessibilityChartDescriptor / AXChartDescriptor), all with canonical links.
* 2026-07-10 — THE DESIGN PIVOT. Backed up the liquid-glass app as v4.0 (annotated tag
  v4.0 "liquid-glass-design" + branch liquid-glass-design + MARKETING_VERSION 4.0, pushed)
  and reimplemented the home flow against the Caffeine simplism handoff
  (design/caffeine-design-system/ in the app repo; primary spec
  templates/analyze-home/AnalyzeHome.dc.html). Added design-system/caffeine-v5.md as the
  new canon (palette, bundled Space Grotesk / Hanken Grotesk / Space Mono, flat tab bar,
  locked behaviors, verification, open items) and marked ios26-design-guide.md,
  accent-palette.md, and wwdc2026/liquid-glass.md status: superseded with banners.
  Phase 1 simulator-verified end-to-end (UITests + screenshots, both analysis outcomes).
* 2026-07-10 — Unified the AI model use (user): the catalog is exactly Gemini 3.5 Flash →
  Gemini 3.1 Pro → Apple Intelligence, with that fixed fallback chain (ids verified against
  the live Gemini ListModels API; OpenRouter/GLM removed — keys were never configured; the
  Settings fallback-order editor is no longer consulted; on-device-by-default superseded).
  The v5 analyzing panel now names the live model as its first bullet, prints an accent
  "falling back to …" line per hop, and the result footer attributes the final model.
  ai/multi-provider-ai.md marked superseded with the full delta; chain order unit-tested
  (71 unit tests green) and the flow verified live against gemini-3.5-flash on the sim.
* 2026-07-10 — Added design-system/motion.md as the SINGLE source of truth for animation/
  transition knowledge (user: "merge them into a single one, so easy for me to edit").
  Consolidates what was scattered across 16 pages: the Caffeine motion canon (no bounce/
  spring/overshoot, decelerate, instant tab swap, Reduce Motion = keep end states), the
  curve/duration token table mapped to CaffeineDesign.swift symbols, the live v5 animation
  inventory (panel, fades, pulse, press physics, keyboard, bars), locked rules (trends bar
  extends in place; no folding paper; no tab crossfade) and the archived v4 specs (drawer/
  card springs, 1:1 date-swipe pager math, globe spin physics, SceneKit idle spin). Source
  pages stay as history and are cited; caffeine-v5 + the folder index now point at it.
  Flagged one open item: CFPulseDot doesn't yet gate on Reduce Motion.
* 2026-07-10 — Added the SPATIAL PROVENANCE motion rule (user: "where it is from, where it
  is gone for every element") to design-system/motion.md canon with a per-element spec,
  audited the v5 home against it (only the analysis panel + instant tab content complied;
  everything else faded from nowhere), and implemented the fixes: detail/report drill in
  from the trailing edge, picker drops from the top, day changes slide directionally
  (leading=older/trailing=newer, layers clipped), logged rows land from the bottom out of
  the collapsing panel, composer chips/notes emerge from the control row, checklist lines
  print from the growth edge, and the tab underline now SLIDES via matchedGeometryEffect
  while content stays instant (transaction-nil). Also fixed the flagged CFPulseDot
  Reduce-Motion gap. Verified: 3 UI tests + 71 unit tests green after the changes.
* 2026-07-10 — Added design-system/exits.md (user: "i do not have a option to close the
  windows… check if the exit behavior is clear for every panel"): the no-trap exit rule,
  the per-surface exit table, and the audit that found two traps — the in-flight analysis
  panel had NO exit, and the FINAL REPORT could only be logged. Fixed both: ✕ CANCEL
  (top-trailing, restores the draft to the composer) while analyzing, ✕ CLOSE + NOT NOW
  on results (dismiss without logging — restores v4's "let user decide to add it or no").
  Guarded by testCancelAnalysisRestoresDraft + a NOT NOW assert in the main flow; all 4
  UI tests green, ✕ CLOSE stays above the fold on long results.
* 2026-07-10 — Added ai/nutrition-verification.md (user: "dedicated knowledge for checking
  the macro and micro nutrition… must be scientific… every checkpoint clickable to expand…
  reuse the old app's macro/micro schema"). The v4 NutritionResponse 37-field schema (9
  macros, 13 vitamins, 14 minerals, caffeine — with units and the >0-filtered accessors) is
  reused as-is; a new pure CFNutritionAudit (CaffeineLogic.swift) runs the scientific
  checks — Atwater 4/4/9 energy cross-check (±15% gate, stricter than FDA's 20%),
  sat+mono+poly ≤ total fat, sugar+fiber ≤ carbs (0.5 g label slack), non-negativity,
  schema coverage N/37 — and every analysis checkpoint now expands (+/−) to its real
  evidence lines (✓/⚠/·), incl. an explicit "MACROS ESTIMATED FROM CALORIES" disclosure
  when the 45/30/25 fallback filled them. 11 new unit tests (82 total green); expansion
  verified live on the sim (37/37 fields, caffeine 130 mg from an oat latte).
* 2026-07-10 (night, scheduled run) — Deepened the nutrition-verification workflow per the
  scheduled job: CFNutritionAudit gained per-macro energy bounds (grams × Atwater factor ≤
  kcal × 1.10), a per-serving plausibility screen against full-day reference caps (FDA DVs
  for sodium 5000/potassium 4700 mg; NIH ODS adult ULs for 12 vitamins/minerals; B12,
  thiamin, riboflavin, pantothenate, biotin, chromium uncapped — no established UL),
  cholesterol ≤1000 mg and caffeine ≤ FDA 400 mg/day flags, a PLAUSIBILITY roll-up in the
  recheck block, and a leading "VERDICT — PASS / REVIEW (N FLAGS)" line on every
  checkpoint; all surfaced in the expandable checkpoint evidence. Documented in
  ai/nutrition-verification.md with a full tolerances/caps table + bases. ALSO restored
  the three locked v4 FINAL REPORT controls (portion stepper with live scaling + scaled
  payload/multiplier on log, always-pick meal chips, idempotent SAVE TO LIBRARY of the
  base card) — recorded in caffeine-v5.md. Tests: 95 unit (+13) and 4 UI green, success
  branch live-verified (stepper 1×→1.5×, Dinner chip, checkpoint expansion, save button).
* 2026-07-11 — Graph legibility via CONTENT ONLY (user: don't touch the MCP or the HTML —
  the wiki content itself must make graph.html render clearly). 17 historical pages got a
  "v4 · " title prefix (liveness now reads on the canvas labels + directory) and a shared
  era-v4 tag (tightens the old constellation); the 4 live canon pages (caffeine-v5, motion,
  exits, nutrition-verification) share the rare era-v5 tag (6 bonding edges); 8 honest
  [[caffeine-v5]] era/dependency notes were added to live-relevant pages so the canon page
  is now the graph's hero (23°, verified via the generator — was the superseded v4 design
  handoff). Folder indexes re-synced to the new titles. Convention recorded in
  workflow/graph-legibility.md so future eras follow the same scheme.
