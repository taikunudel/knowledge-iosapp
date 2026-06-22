---
type: rule
id: "trends/trends-routing"
title: Trends Routing — Local-Only Until HealthKit Path Has Feature Parity
description: Trends routing is hard-coded to the local view until the HealthKit path gains per-nutrient pinning and excluded-date filtering.
status: stable
tags: [trends, healthkit, routing]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Trends Routing — Local-Only Until HealthKit Path Has Feature Parity
*Established: 2026-05-26 (Codex adversarial review fix)*

`NutritionTrendsView.body` (in [Nutritionist/Views/NutritionTrendsView.swift](Nutritionist/Views/NutritionTrendsView.swift)) used to branch on `appSettings.useHealthKitTrends`:

```swift
if appSettings.useHealthKitTrends { HealthKitNutritionTrendsView() }
else                              { LocalNutritionTrendsView() }
```

`useHealthKitTrends` defaults to `true`, so **default users saw the HealthKit path which has no per-nutrient pin and no excluded-date filtering** — silently breaking both the pinned-nutrients and the "mark day as incomplete" requirements.

Routing is now hard-coded to `LocalNutritionTrendsView`. The `useHealthKitTrends` setting is left intact so existing user preferences aren't reset, but it has no current effect.

**Re-enabling the HealthKit branch requires both:**

1. Per-nutrient pin toggle on `HealthKitNutrientRow` (or its equivalent) that calls `appSettings.togglePinnedNutrient(_:)`.
2. `appSettings.excludedDates` filtering applied to the HealthKit aggregation path (mirror what `LocalNutritionTrendsView.refreshSeries()` does for the local path).

Only after both are in place should the `if appSettings.useHealthKitTrends` branch be restored.
