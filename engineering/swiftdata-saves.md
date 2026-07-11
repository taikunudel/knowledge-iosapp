---
type: rule
id: "engineering/swiftdata-saves"
title: "SwiftData Save Failures — Always do/catch"
description: "User-observable writes must wrap modelContext.save() in do/catch, roll back on failure, and only update the UI inside the do block."
status: stable
tags: [engineering, swiftdata, persistence, error-handling]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# SwiftData Save Failures — Always `do/catch`

*Established: 2026-05-26 (Codex adversarial review fix)*

Writes that the user can observe as success (button label flip, sheet dismiss, list refresh) **must** wrap `modelContext.save()` in `do/catch`, roll back on failure, and only update the UI inside the `do` block. Silent `try?` swallows persistence errors and leaves the user looking at a confirmation while the data was discarded.

Sites currently following this rule (all in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift)):

- `MessageBubble.saveCurrentNutritionToLibrary(_:)` — only sets `didSaveToLibrary = true` after a successful save.
- `FoodCardLibraryView.handleTap(on:)` (picker mode) — only fires `onPicked` + `dismiss()` after a successful FoodEntry insert.
- `FoodCardLibraryView.deleteCard(_:)` — rolls back and logs on failure.
- `MessageBubble.logFoodEntry(...)` — pre-existing pattern.

**Don't reintroduce `try? modelContext.save()` followed by an unconditional UI mutation.** If you add a new save site, follow the same shape.

*Still load-bearing in v5: the Caffeine home's DONE — LOG IT and SAVE TO LIBRARY follow this pattern — see [[caffeine-v5]].*
