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
