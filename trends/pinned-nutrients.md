---
type: rule
id: "trends/pinned-nutrients"
title: Pinned Nutrients Monitor
description: Users can pin any nutrient so its today-running total shows on the Today page with units and an over/under indicator.
status: stable
tags: [trends, nutrients, today, pinning]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Pinned Nutrients Monitor
*Established: 2026-05-20*

The user can pin any nutrient (Protein, Fiber, Sodium, etc.) so its today-running total appears at a glance on the Today page. User verbatim: "add a function to mark any nutrition and it will be pined, so user can easily monitor if that is over or not enough etc."

### Storage

- [Nutritionist/Models/AppSettings.swift](Nutritionist/Models/AppSettings.swift): `@AppStorage("pinnedNutrientsJSON")` as JSON-encoded `[String]` (ordered).
- API:
  - `AppSettings.pinnedNutrients: [String]` — ordered list of JSON keys (e.g. `"protein"`, `"saturatedFat"`).
  - `AppSettings.isNutrientPinned(_:)`, `setNutrientPinned(_:_:)`, `togglePinnedNutrient(_:)`.
- Nutrient keys must match `NutritionResponse` JSON keys (see `nutritionMetricFieldKeys` in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift) for the canonical list).

### Pin / Unpin UI

- `LocalNutrientRow` in [Nutritionist/Views/NutritionTrendsView.swift](Nutritionist/Views/NutritionTrendsView.swift) renders a `pinToggleButton` between the value text and the expand chevron: `pin` (outline) when unpinned, `pin.fill` tinted with `appSettings.themeAccentColor` when pinned.

### Today Strip — Required Chip Contents

TodayView shows a horizontal scrollable `pinnedNutrientStrip` between the `WeekCalendarView` and the food-log card deck. Each chip **must** show:

1. A `pin.fill` glyph.
2. The nutrient label (auto-prettied from camel-case key, e.g. `"saturatedFat"` → `"Saturated Fat"`).
3. The current value **with its unit** (e.g. `"35g"`, `"1200mg"`, `"450mcg"`). Units come from `LocalNutrientDefinition.all` in [Nutritionist/Views/NutritionTrendsView.swift](Nutritionist/Views/NutritionTrendsView.swift) — **don't infer units from training data**.
4. An **over/under indicator** against the daily goal from `AdultNutrientGoalReference.goal(forLocalKey:calorieGoal:)`. Render as `"value/goal unit"` (e.g. `"35/50g"`) with the value-portion tinted:
   - **Green** when within ±15 % of the goal (`0.85 ≤ value/goal ≤ 1.15`) — on target.
   - **Orange** when well under (`< 0.30`) or well over (`> 1.50`) — needs attention.
   - **Secondary** otherwise — neutral.
- **Upper-limit nutrients are asymmetric** (added 2026-05-31, Codex): for `sodium`, `sugar`, `saturatedFat`, `cholesterol`, `transFat`, `addedSugars`, **`caffeine`** (the `upperLimitNutrientKeys` set in `TodayView`), being *low* is fine — warn (amber) when **over the limit** (`pct > 1.0`, so 2500/2300 is NOT green), success when comfortably under (`pct ≤ 0.85`), secondary in between. Don't apply the symmetric under-warning to these, or low sodium falsely shows amber. `caffeine` must stay in the set — it has an upper-limit goal.
- When no goal exists for a nutrient (`goal == nil`), fall back to showing just `"value unit"` with secondary color, without the slash.

This is the **canonical pinned-chip spec**. User verbatim: "so user can easily monitor if that is over or not enough etc." — meeting this means showing both the unit and a visible over/under signal, not just a raw number.

### Implementation pointers

- Totals are computed by `todaysPinnedNutrientTotals()` in [Nutritionist/Views/TodayView.swift](Nutritionist/Views/TodayView.swift), which parses each entry's `aiGeneratedNutritionJSON` via the existing `nutritionDictionaryForAverage` + `numericValue(forKey:in:)` helpers.
- Unit + goal lookup helpers live next to `todaysPinnedNutrientTotals()` and reuse `LocalNutrientDefinition.all` and `AdultNutrientGoalReference.goal(forLocalKey:calorieGoal:)`.
