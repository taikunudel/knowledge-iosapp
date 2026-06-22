---
type: decision
id: "design-system/settings-revamp"
title: "Settings Revamp 2026-06-11 — Fewer Knobs, Q&A Calorie Goal"
description: "Settings removed four styling sections and replaced the raw calorie-goal picker with a research-backed interactive Q&A wizard."
status: stable
tags: [settings, calorie-goal, wizard, mifflin-st-jeor, revamp]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Settings Revamp 2026-06-11 — Fewer Knobs, Q&A Calorie Goal

User verbatim: *"on the setting, remove shape and surface, remove quick presets, remove depth and shadow, remove boardder. do some research, what is the scneitific way of deciding cariloe gain or loss everyday, make the goal a interative Q&A procedure, make it simple, instead of just setting the calorie goal. so this gonna be a major revamp of settings."*

### Removed sections (don't re-add)
**Quick Presets**, **Shape & Surface**, **Depth & Shadow**, and **Border** are deleted from [Nutritionist/Views/SettingsView.swift](Nutritionist/Views/SettingsView.swift). The backing `AppSettings` values (corner radius, tint, shadow, border, etc.) remain — defaults still style the Calendar cards and the Reset button still restores them — but the per-slider editing UI is gone. The **Glass Effect** section (not named by the user) stays.

### Calorie Goal — interactive Q&A wizard (replaces the raw picker)
- The Goals row opens **`CalorieGoalWizardView`** (bottom of SettingsView.swift), NOT the old 100-kcal wheel picker (`showingCalorieGoalPickerSheet` is no longer triggered; the sheet code remains but don't re-wire it as the primary path).
- **Method (research-backed 2026-06-11):** Mifflin–St Jeor BMR (`10·kg + 6.25·cm − 5·age + 5♂/−161♀` — the equation the Academy of Nutrition and Dietetics recommends as most accurate for the general population) × a standard activity factor (sedentary 1.2 · light 1.375 · moderate 1.55 · very 1.725 · athlete 1.9) = TDEE; then a **safe pace delta**: −500 (≈0.5 kg/wk loss) / −250 (≈0.25 kg/wk) / 0 (maintain) / +300 (lean gain — research: +200–350 minimizes fat gain). Result clamped to ≥1,200 (female) / ≥1,500 (male) kcal/day and rounded to 10. Sources: ADA/Mifflin–St Jeor consensus across TDEE references; deficits >750–1,000 kcal/day risk muscle loss and aren't sustainable — **don't add more aggressive pace options.**
- **Flow:** sex → age → height → weight → activity → pace → result (shows BMR + maintenance + the goal, "Use This Goal" writes `appSettings.dailyCalorieGoal`). One question per step, segmented/slider/choice rows, accent-tinted, back navigation, `.presentationDetents([.large])`.
