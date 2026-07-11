---
type: rule
id: "design-system/exits"
title: "Exits & Dismissal — every panel has a clear way out"
description: "The exit rule (no surface may trap the user; every panel/overlay needs a visible, predictable dismissal that states what happens to your input), the per-surface exit table for v5, and the two traps found and fixed in the 2026-07-10 audit."
status: stable
tags: [exits, dismissal, close, cancel, navigation, panels, ux]
created: 2026-07-10T00:00:00Z
updated: 2026-07-10T00:00:00Z
---

# Exits & Dismissal — every panel has a clear way out

*Created 2026-07-10. User: "current i do not have a option to close the
windows, add a knowledge about exiting. check if the exit behavior is clear
for every panel." Companion to [[motion]] — motion's provenance rule says
where an exit GOES; this page guarantees an exit EXISTS and what it does.*

## The rule

1. **No surface may trap the user.** Every panel, overlay, and screen must
   offer at least one visible, tappable exit at all times — including while
   waiting on the network.
2. **An exit says what it does to your input.** Cancelling an in-flight
   analysis RESTORES the draft (text + photo back in the composer); declining
   a finished result discards it without logging; BACK never destroys data.
3. **Exit affordances are Caffeine chrome:** uppercase mono micro-labels
   ("← BACK", "✕ CANCEL", "NOT NOW", "DISMISS"), 44 pt minimum targets,
   flat — never a glass/blur scrim. Placement: BACK is top-LEADING on
   drill-in screens; CANCEL is top-TRAILING on the rising panel; result/error
   actions are a bottom row (primary accent pill + bordered decline).
4. **Exits animate along the provenance direction** ([[motion]] §1): the
   panel collapses back down, drill-ins slide back to the trailing edge, the
   picker back up.

## Per-surface exit table (v5, after the 2026-07-10 fixes)

| Surface | Exit(s) | Input/state on exit |
|---|---|---|
| Analyzing panel (in flight) | **✕ CANCEL** (top-trailing) — added 2026-07-10 | cancels the request + step pacing; **restores the typed text & photo to the composer** |
| FINAL REPORT (result) | **✕ CLOSE** (top-trailing, always visible) · **DONE — LOG IT** (accent pill) · **NOT NOW** (bordered) — added 2026-07-10 | DONE logs to the viewed day then collapses; ✕ CLOSE and NOT NOW collapse **without logging** (v4's "let user decide to add it or no", restored). ✕ stays above the fold on long results |
| Analysis error | **TRY AGAIN** · **DISMISS** | retry re-runs with the same draft; DISMISS closes, composer text retained |
| Food detail | **← BACK** (top-leading) | read-only, nothing to lose |
| Day report | **← BACK** | read-only |
| Date picker | **← BACK** · tapping any day row | row tap also navigates to that day |
| Composer / keyboard | tap anywhere outside · drag the meals list | draft retained (guarded by `testTapOutsideDismissesComposerKeyboard`) |
| Photo options dialog | system **Cancel** | — |
| Camera / photo library | system Cancel / swipe | — |
| Tabs | tab bar always visible | screens are peers, no exit needed |

## Audit record (what was broken)

The 2026-07-10 audit found two traps, both on the analysis panel
(`CaffeineHomeView`):

- **In-flight analysis had NO exit** — a hung request locked the whole app
  behind the checklist. Fixed: `✕ CANCEL` (id `cf.cancelAnalysis`) →
  `cancelAnalysis()` cancels `analysisTask`/`stepTask`, collapses the panel,
  and puts `pendingText`/`pendingImage` back into the composer.
- **The result could only be LOGGED** — no way to decline a finished
  estimate. Fixed: `NOT NOW` (id `cf.notNow`) beside DONE — LOG IT →
  `dismissPanel()` without inserting a `FoodEntry`.

## Explicitly NOT allowed

- Don't ship any new overlay without a row in the table above.
- Don't make CANCEL discard the draft (it restores; only NOT NOW/DISMISS
  leave the draft out of the composer because the send already cleared it or
  the user declined knowingly).
- Don't replace the mono-label exits with system chrome (nav bars, sheet
  grabbers) on Caffeine surfaces.

See also [[caffeine-v5]], [[motion]].
