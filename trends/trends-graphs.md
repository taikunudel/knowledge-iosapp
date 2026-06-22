---
type: rule
id: "trends/trends-graphs"
title: Trends Graphs — In-Place Expansion, Pinned-First, Custom Goals
description: Trends rows expand into a graph in place, pinned nutrients sort first and auto-expand, and per-nutrient custom goals are supported.
status: stable
tags: [trends, graphs, pinning, goals]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Trends Graphs — In-Place Expansion, Pinned-First, Custom Goals
*Established: 2026-06-09 (user requests); implemented 2026-06-10/11. All in [Nutritionist/Views/NutritionTrendsView.swift](Nutritionist/Views/NutritionTrendsView.swift) + [Nutritionist/Views/Components/NutrientTrendChart.swift](Nutritionist/Views/Components/NutrientTrendChart.swift).*

User verbatim: *"the trend graphs, do not open a new graph when tapping on one bar, the bar should extend into a graph, this animation makes more sense. also, remove redundent text on the trend graphs. allow to set individually the intake of each nutrition"* and *"when pin a nutrition, by default expand its graph and move the graph to the begining of the trend session."*

- **In-place expansion:** tapping a nutrient row toggles `isExpanded` and the `NutrientTrendChart` renders inline under the row — never a pushed screen or sheet. Don't add a NavigationLink/detail screen for a nutrient graph.
- **Redundant text removed:** the chart no longer repeats the nutrient name ("`X` Trend" header gone — the row already names it); "recommand" → "goal" (chip + RuleMark annotation); Y-axis labels are bare numbers with the unit shown ONCE at top-right. Each row also gained a thin **today-vs-goal progress bar** (accent tint).
- **Pinned-first + auto-expand:** the trends list opens with a **"Pinned" section at the top** (pinned non-calorie nutrients, then calories standalone unless pinned, then Macro/Minor excluding already-shown). `computeInitialExpandedNutrients()` expands calories + all pinned keys on appear, and `.onChange(of: appSettings.pinnedNutrients)` expands a nutrient the moment it's pinned.
- **Custom nutrient goals** (per-nutrient intake): stored in [Nutritionist/Models/AppSettings.swift](Nutritionist/Models/AppSettings.swift) under `@AppStorage("customNutrientGoalsJSON")` (`[String: Double]`, keys = `NutritionResponse` JSON keys) with `setCustomNutrientGoal(forKey:value:)` / `replaceCustomNutrientGoals(_:)` / `customNutrientGoalsSnapshot`. **The single chokepoint is `AdultNutrientGoalReference.goal(forLocalKey:calorieGoal:)`** — it consults the custom map first, then FDA defaults, so pinned chips, trends rows, and any future goal consumer all honor the override automatically. Edit UIs: a small pencil on each trend row (sheet) and a **"Nutrient Goals" Section in Settings** (`NutrientGoalEditorView`; a `person.fill` accent badge marks customized nutrients; "Reset to Default" clears the override). **Backup-covered:** `AppSettingsSnapshot.customNutrientGoals: [String: Double]?` (optional for old backups) in `FullDataBackupService` — keep extending it per the Backup/Restore rule.
