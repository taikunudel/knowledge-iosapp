---
type: decision
id: "today/today-hero-globe"
title: "v4 · Today Hero — Dotted Macro Globe + Legend"
description: "The Today hero is a DottedGlobe beside a macro legend and Food-benefit row, replacing the retired water-washed progress strips."
status: stable
tags: [today, globe, hero, macros, design, era-v4]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Today Hero — Dotted Macro Globe + Legend
*Established: 2026-05-26 (water-washed strips); **superseded 2026-06-04** by the dotted-globe redesign.*

> **2026-06-04 supersession (design-system redesign — `/Users/theo/Downloads/Nutritionist Design System`).** The Today hero is now a **`DottedGlobe`** beside a **macro legend** (Protein / Carbs / Fat / Fiber) and a **Food-benefit** row. This **replaces the two water-washed progress strips.** The user confirmed **"globe replaces strips"** when asked (the strip was previously locked as the brand's "signature visual element"; the new bundle removes both strips from Today). `WaterWashedStrip` is kept in the codebase but is **no longer on the Today hero.**

### Implementation (current — globe)

- `TodayView.todayMetricHero` (in [Nutritionist/Views/TodayView.swift](Nutritionist/Views/TodayView.swift)) is an `HStack(spacing: 18)`:
  - **`DottedGlobe(size: 170, progress:, number: totalCalories.formatted(), unit: "cal", protein/carbs/fat/fiber:)`** — left.
  - **Legend column** — right: `"of <goal> cal"` + `<pct>%` (moss when ≥ 100 %, else warm ink); four `macroLegendRow`s (color dot + name + grams + "g"); a **Food benefit** row (color dot + label + score) sitting above a **dashed top rule** (`DashedTopRule`).
- **`DottedGlobe`** (file scope in `TodayView.swift`) is a faithful Canvas port of `atoms.jsx` → `DottedGlobe`. `_hash`/`_isLand` are reproduced **bit-exact** (UInt32 wraparound) so the dot pattern matches the prototype. Land dots are colored by macro share via `MacroPalette`; ocean dots are sparse warm grey; dots reveal up to `progress`. The calorie **number is carved out** of the dot field (a `destinationOut` knockout clears the dots) **and then re-drawn on top in `Color.primary`**. A pure carve leaves the number the page-background color → **black-on-black in dark mode → invisible**, so the on-top label-colored re-draw is required. **Don't remove the on-top number/unit draw.**
- **`MacroPalette`** (file scope) holds the fixed macro hexes (protein `#7a9166`, carbs `#c08e57`, fat `#b06a6c`, fiber `#7d8c9a`) + ocean `#3c372d`. Kept **independent of the user's accent theme** so macro identity never shifts. Used by both the globe and the legend.
- Macro grams come from **`todaysMacroTotals()`** — sums `protein`/`carbohydrates`/`totalFat`/`fiber` from each entry's already-scaled payload (sum raw, never × `portionMultiplier` — see "Pinned-Nutrient Totals").

### Explicitly NOT Allowed

- **Don't put the water-washed strips (or the circular dual-ring) back on the Today hero.** The hero is the dotted globe + legend.
- **Don't tie `MacroPalette` to `themeAccentColor`.** Macro colors are fixed identities.
- **Don't delete `WaterWashedStrip` or `ProgressRingView`** — both are kept in the codebase (previews / other surfaces may reference them).
- **Don't drop the on-top number re-draw in `DottedGlobe`** (regresses to an invisible number in dark mode).
