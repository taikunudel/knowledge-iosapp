---
type: rule
id: "engineering/pinned-nutrient-totals"
title: "Pinned-Nutrient Totals — Already-Scaled Payload"
description: "Values summed from aiGeneratedNutritionJSON are already portion-scaled at log time and must not be re-multiplied by portionMultiplier."
status: stable
tags: [engineering, swiftdata, nutrition, portion, totals]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Pinned-Nutrient Totals — Already-Scaled Payload

*Established: 2026-05-26 (Codex adversarial review fix)*

The food entry's `aiGeneratedNutritionJSON` is **already portion-scaled at log time** by `logFoodEntry`, which writes `scaledNutritionPayload(basePayload, scale: boundedPortion)`. `FoodEntry.portionMultiplier` is stored alongside for *future re-scaling*, not as a factor to re-apply.

Therefore, in `todaysPinnedNutrientTotals()` in [Nutritionist/Views/TodayView.swift](Nutritionist/Views/TodayView.swift) and anywhere else that sums values from `aiGeneratedNutritionJSON`:

```swift
totals[key, default: 0] += raw      // CORRECT — payload already scaled
totals[key, default: 0] += raw * entry.portionMultiplier   // WRONG — double-counts
```

If a future feature wants the *base* (unscaled) values, parse the JSON and divide by `portionMultiplier` — but the JSON itself stays scaled by convention.

*Still load-bearing in v5: `CFDayTotals` and the portion stepper's scaled payloads rely on this convention — see [[caffeine-v5]].*
