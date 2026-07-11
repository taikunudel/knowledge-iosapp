---
type: decision
id: "design-system/rejected-experiments"
title: "Rejected Design Experiments"
description: "Retired designs the user rejected — record rejections here so they are not re-implemented, including the problematic folding-paper effect on TodayView."
status: stable
tags: [rejected, folding-paper, todayview, design-experiments, swipe-actions, food-log]
created: 2026-06-22T00:00:00Z
updated: 2026-06-23T00:00:00Z
---

# Rejected Design Experiments

When the user says a design is "problematic", "doesn't work", asks for it stashed/restored, or otherwise rejects it, record the rejection here so it doesn't get re-implemented in a future session.

### Folding paper effect on TodayView
*Rejected: 2026-05-20*

A folding-paper animation experiment in [Nutritionist/Views/TodayView.swift](Nutritionist/Views/TodayView.swift) (≈+380 lines) was rejected by the user with the verbatim feedback: "restore it the folding paper is problematic." The work is preserved in git stash as `stash@{0}: folding paper effect (problematic)` but **must not be reapplied to TodayView without explicit user approval**. If a future task asks for a folding / paper / origami transition on TodayView cards, surface this entry and confirm before proceeding.

### Native row swipe-to-delete on the food log
*Rejected: 2026-06-23*

Adding SwiftUI `.swipeActions()` / `.swipeActionsContainer()` swipe-to-delete to the
food-log rows was considered (WWDC26 "What's new in SwiftUI" now allows swipe actions on
any view) but **rejected: it conflicts with the food log's existing horizontal swipe**,
which changes the selected date (the velocity-aware card pager in
[TodayView](Nutritionist/Views/TodayView.swift) / [CalendarView](Nutritionist/Views/CalendarView.swift)).
A horizontal row-swipe and a horizontal date-swipe on the same rows are ambiguous. Delete,
edit, and move stay in the row's ellipsis **Menu** (`PlainDesignFoodRow`). Don't add
row-level horizontal swipe actions to the food log unless the date-swipe is first moved to a
different gesture or surface.

*Era-independent: rejections bind in every era, including [[caffeine-v5]].*
