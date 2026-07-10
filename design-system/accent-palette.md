---
type: reference
id: "design-system/accent-palette"
title: "Accent Palette — MUJI Natural Tones"
description: "The MUJI-inspired natural accent palette, named color tokens, and the semantic status traffic-light that replace raw green/orange/red."
status: superseded
tags: [accent-palette, colors, muji, status-tones, design-tokens]
created: 2026-06-22T00:00:00Z
updated: 2026-07-10T00:00:00Z
---

# Accent Palette — MUJI Natural Tones

> ⚠️ **Superseded 2026-07-10** by the Caffeine palette — one hot accent
> `#FF4A1C` on olive/paper neutrals; see [[caffeine-v5]]. MUJI tones remain
> only inside the untouched legacy screens (Trends/Library/Settings) until
> their Caffeine pass.

*Established: 2026-05-26 (design system handoff)*

The three preset accent themes use the **MUJI-inspired natural palette** from the design system in `.artifacts/design-system/nutritionist-design-system/project/colors_and_type.css`. The earlier saturated Pink/Blue/Orange trio is retired.

| Enum case (raw) | Display name | Hex      | sRGB                       |
|-----------------|--------------|----------|----------------------------|
| `pink` *(default)* | **Persimmon** | `#b06a6c` | rgb(0.690, 0.416, 0.424) — dusty rose-clay |
| `blue`             | **Stone**     | `#7d8c9a` | rgb(0.490, 0.549, 0.604) — slate-blue stone |
| `orange`           | **Clay**      | `#b8865a` | rgb(0.722, 0.525, 0.353) — warm terracotta |

### Rules

- **Don't rename the enum cases.** The `WaterwashedTheme` rawValue stays `pink`/`blue`/`orange` so existing `@AppStorage("waterwashedTheme")` picks survive the palette swap without a migration. Users who chose "Pink" before the change see Persimmon after, with no data loss.
- **Don't reintroduce the saturated values.** The retired triple was: Pink `(0.95, 0.33, 0.60)`, Blue `(0.27, 0.58, 0.94)`, Orange `(0.98, 0.52, 0.24)`. Those are off-spec relative to the design system.
- **Display name is the natural name.** Settings UI shows "Persimmon", "Stone", "Clay" — never the rawValue.
- **Custom-color picker is unchanged.** Users can still pick any color via `customThemeColor`; the preset trio is just the curated defaults.

### Natural status tones — IN ACTIVE USE; earth surfaces — available, not yet applied
*Updated: 2026-05-26 (status tones adopted)*

The full MUJI-inspired palette is exposed as named `Color` extensions in [Nutritionist/Models/AppSettings.swift](Nutritionist/Models/AppSettings.swift) (UIKit equivalents on `UIColor` for Core Graphics paths):

| Token | Hex | Use |
|---|---|---|
| `Color.nutritionistOat`    | `#efe5cf` | Warm off-white surface |
| `Color.nutritionistLinen`  | `#e8dec6` | Toastier surface |
| `Color.nutritionistRice`   | `#f6f1e6` | Lightest paper surface |
| `Color.nutritionistInk`    | `#3d3a33` | Warm-black ink |
| `Color.nutritionistPebble` | `#a39b8b` | Soft warm grey |
| `Color.nutritionistMist`   | `#c9c2b2` | Lighter warm grey |
| `Color.nutritionistMoss`   | `#7a9166` | Success |
| `Color.nutritionistAmber`  | `#c08e57` | Warning |
| `Color.nutritionistBrick`  | `#a55c54` | Danger |

**Status tones are now the project traffic-light.** Use the semantic aliases — **never** raw `.green`/`.orange`/`.red` — for health-score, calorie-goal, and destructive signals:

- `Color.nutritionSuccess` (→ moss) — health ≥ 50, calorie goal met (progress ≥ 1.0), pinned-nutrient on-target, "Restore" affordance.
- `Color.nutritionWarning` (→ amber) — health < 50, pinned-nutrient under/over, "Mark Day Incomplete" icon, "Recently Deleted" affordance, backup-failed status.
- `Color.nutritionDanger` (→ brick) — HealthKit heart icon, deletion borders.

`UIColor.nutritionSuccess/Warning/Danger` exist for the `TodayTabIconRenderer` ring (drawn with `UIGraphicsImageRenderer`). Retargeted call sites (2026-05-26): `ProgressRingView`, `WeekCalendarView`, `HealthScoreHeartsEffect`, `MealTimelineView`, `MessageBubble.healthScoreColor` + `LibraryFoodCardPreview` + `TodayTabIconRenderer` (ContentView), `TodayView` (pinned chip, exclude icon, sync heart), `SettingsView` (backup status, sync heart, restore tint, recently-deleted icon).

**Deliberately NOT retargeted** (these are not status signals): the orange `flame.fill` calorie icon (iconographic — the design system README shows it orange), the developer debug-log panel colors, and the `NutrientTrendChart` palette enum.

**Earth surfaces are still NOT applied** to base surfaces — per the design system's "Background. Plain." principle, base surfaces stay `.systemBackground` (system white / near-black). Don't repaint base backgrounds with oat/linen/rice without explicit user direction. If a *card* or accent surface should adopt an earth tone, that's a reasonable opt-in, but confirm first.
