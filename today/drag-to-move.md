---
type: rule
id: "today/drag-to-move"
title: "v4 · Drag-to-Move Food Entries (long-press)"
description: "Long-pressing a Today food row lets the user drag it onto another meal section (change meal) or a trend day (change date)."
status: stable
tags: [today, food-log, drag-drop, meals, trends, era-v4]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Drag-to-Move Food Entries (long-press)
*Established 2026-06-21.* User: *"when i long press on a food entry, i can move it by draging it into a differet date, or different meal type."*

- **Draggable rows:** each Today food row (`PlainDesignFoodRow` in [CalendarView.swift](Nutritionist/Views/CalendarView.swift)) is `.draggable(entry.id.uuidString)` — long-press starts a system drag carrying the entry's UUID string.
- **Drop on a MEAL → change meal (same date):** each `plainMealSection` is a `.dropDestination(for: String.self)` that calls `onMoveEntryToMeal?(uuid, category)`; it highlights (`dropTargetMeal`, accent tint) while targeted. Wired in `FoodEntriesCardContent`; `TodayView.homePinnedCardSurface` passes `onMoveEntryToMeal: { id, meal in dropEntry(id: id, onMeal: meal) }`.
- **Drop on a TREND DAY → change date (same meal + time):** each `CalorieTrend` day-selector button is a `.dropDestination` calling `onDropEntryOnDay?(uuid, day.date)` (highlights via `dropTargetIndex`). `TodayView` passes `onDropEntryOnDay: { id, date in dropEntry(id: id, onDate: date) }` (reuses `moveEntry`).
- **`TodayView.dropEntry(id:onMeal:)` / `dropEntry(id:onDate:)`** look the entry up in `allEntries` by UUID and mutate `mealCategory` / `date` with do/catch + rollback. Empty meals aren't drop targets (hidden), so the ••• menu gained a **"Move to Meal" submenu** (`PlainDesignFoodRow.onMoveToMeal`, all 4 meals, current one checked/disabled) as the fallback.
- Coexists with the food-log date-swipe pan + vertical scroll (drag = long-press, swipe/scroll = movement). **The drag couldn't be automated headlessly — verify the feel on device.**
