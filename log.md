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
