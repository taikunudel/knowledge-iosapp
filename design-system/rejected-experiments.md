---
type: decision
id: "design-system/rejected-experiments"
title: "Rejected Design Experiments"
description: "Retired designs the user rejected — record rejections here so they are not re-implemented, including the problematic folding-paper effect on TodayView."
status: stable
tags: [rejected, folding-paper, todayview, design-experiments]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Rejected Design Experiments

When the user says a design is "problematic", "doesn't work", asks for it stashed/restored, or otherwise rejects it, record the rejection here so it doesn't get re-implemented in a future session.

### Folding paper effect on TodayView
*Rejected: 2026-05-20*

A folding-paper animation experiment in [Nutritionist/Views/TodayView.swift](Nutritionist/Views/TodayView.swift) (≈+380 lines) was rejected by the user with the verbatim feedback: "restore it the folding paper is problematic." The work is preserved in git stash as `stash@{0}: folding paper effect (problematic)` but **must not be reapplied to TodayView without explicit user approval**. If a future task asks for a folding / paper / origami transition on TodayView cards, surface this entry and confirm before proceeding.
