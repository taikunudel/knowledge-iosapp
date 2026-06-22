---
type: rule
id: "today/per-day-completion"
title: "Per-Day Completion Flag — DEFAULT OFF (inverted 2026-06-21)"
description: "Per-day completion is opt-in and default OFF; only completed days get a full-color calorie bar and count in Trends, incomplete days show a dotted bar and are excluded."
status: stable
tags: [today, completion, trends, calorie-bar, calendar]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Per-Day Completion Flag — DEFAULT OFF (inverted 2026-06-21)
*Established: 2026-05-20 (as "mark incomplete"); **🔁 INVERTED to opt-in completion, default OFF, 2026-06-21**.*

> **⚠️ 2026-06-21 — completion is now OPT-IN (DEFAULT OFF).** User: *"by default, the complete today's log is off. and also, only when the complete today is on for a specific date, the calorie bar have full color like now, otherwise just a dotted shape of calorie bar … documenting the progress that day."* The model FLIPPED from "all days complete unless excluded" to "all days incomplete unless marked complete":
> - **New storage** `@AppStorage("completedDateKeysJSON")` + API `AppSettings.isDateComplete(_:)` / `setDateComplete(_:complete:)` / `completedDates` / `completedDateKeysSnapshot` / `replaceCompletedDateKeys(_:)`. **Default empty = every day incomplete.** The old `excludedDate*` API + storage are **kept ONLY for old-backup decode** — no longer consulted.
> - **Toggle** `dayCompleteToggle` ([CalendarView.swift](Nutritionist/Views/CalendarView.swift)) now binds to `isDateComplete` (default OFF), label "This day is complete", footnote "Off (default) marks this day incomplete: a dotted calorie bar and left out of Trends."
> - **Trends INCLUDE-filter (inverted):** `LocalNutritionTrendsView.refreshSeries()` + the goal-streak helper now count **only days in `completedDates`** (was: exclude `excludedDates`). So Trends is EMPTY until days are marked complete. The single chokepoint rule still holds — any new aggregation path must apply the same include-only-completed filter.
> - **Calorie bar (Today `CalorieTrend`):** `CalorieTrendDay.isComplete` (from `isDateComplete`) drives the Canvas — **complete day = full-color stacked macro bar; incomplete day (default) = a DOTTED rounded-top OUTLINE** (`primaryInk.opacity(0.5·emphasis)`, dashed, no fill) at the same height, so it still shows the day's calorie progress while marking it incomplete. **Don't fill incomplete bars with color; don't hide them.**
> - **Backup:** `AppSettingsSnapshot.completedDateKeys` (optional) added alongside the legacy `excludedDateKeys`.
> - **One-shot migration (added 2026-06-21, adversarial-review fix):** `ContentView.migrateCompletionModelIfNeeded()` (called from `onAppear`, gated by `@AppStorage("didMigrateCompletionV1")`) marks every PAST day (< today) that has entries **complete**, minus the legacy `excludedDates`, so an existing user's Trends history isn't silently wiped by the flip. **Today + future stay incomplete (opt-in).** The DEBUG seed sets the flag to keep its own mixed demo; restoring an OLD backup (no `completedDateKeys`) resets the flag so the migration re-runs. So the dead-looking `excluded*` API is NOT dead — the migration reads it. **Don't delete `excludedDates`.**
> - **The Today `CalorieTrend` bar HEIGHT now comes from real `FoodEntry.calories`** (`CalorieTrendDay.calories`), not the macro sum — so manual / paper-note days (no macro JSON) still draw a bar; complete macro-less days get a neutral solid fill. Macro segments still decompose by protein/carbs/fat.
> 
> The historical detail below describes the retired "mark incomplete" model; the storage/aggregation specifics are superseded by the bullets above.

The user can mark any individual day as "incomplete" so that the day's food entries are **excluded from nutrition trend aggregation** (NutritionTrendsView series). User verbatim: "add an option to mark any date as imcoplete so the nutrition analyze will ignore it."

### Storage

- Persisted in [Nutritionist/Models/AppSettings.swift](Nutritionist/Models/AppSettings.swift) under `@AppStorage("excludedDateKeysJSON")` as a JSON-encoded `[Double]` of `Date.timeIntervalSince1970` start-of-day timestamps.
- API:
  - `AppSettings.isDateExcludedFromAnalysis(_ date: Date) -> Bool`
  - `AppSettings.setDateExcludedFromAnalysis(_ date: Date, excluded: Bool)`
  - `AppSettings.excludedDates: Set<Date>` (snapshot)
- Excluded dates are NOT stored on `DayLog` itself — that model has minimal usage today and adding a new property would require a SwiftData migration.

### UI
*Superseded 2026-06-11 — the toolbar Menu is REMOVED.* User verbatim: *"move the mark this day as complete as a switcher under the last food log if any, on mean this day is done, then it can show on the trend, otherwise do not consider it on the trend since they are imcomplete."*

- The control is now **`dayCompleteToggle`** in `FoodEntriesCardContent` ([Nutritionist/Views/CalendarView.swift](Nutritionist/Views/CalendarView.swift)): a **"This day is complete" switch under the last food-log section** on Today, shown **only when the day has entries** ("if any"). ON = complete → counted in Trends (not excluded); OFF = incomplete → excluded. Footnote: "Incomplete days are left out of Trends."
- **Storage and default are unchanged** — it's the same excluded-date-keys set, so all existing days stay "complete"/included and the Trends filter below is untouched. The wording just flipped from negative (mark incomplete) to positive (day complete).
- **Don't re-add a toolbar control for this** — the old `ellipsis.circle` Menu at `.navigationBarTrailing` is gone by user direction.

### Aggregation

- `LocalNutritionTrendsView.refreshSeries()` in [Nutritionist/Views/NutritionTrendsView.swift](Nutritionist/Views/NutritionTrendsView.swift) filters out entries whose `Calendar.current.startOfDay(for: entry.date)` is in `appSettings.excludedDates` before summing per-day totals. This is the single chokepoint for the local nutrition trend; if new aggregation paths are added later, **they must apply the same filter**. (🔁 2026-06-21: now an INCLUDE filter on `completedDates` — see the inversion note above.)
