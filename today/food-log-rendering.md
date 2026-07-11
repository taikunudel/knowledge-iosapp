---
type: rule
id: "today/food-log-rendering"
title: "v4 · Food Log Rendering — Today Page is Meal-Grouped (Plain)"
description: "On the Today page the food log is plain (no card/glass) and grouped into Breakfast/Lunch/Dinner/Snacks sections with PlainDesignFoodRow rows."
status: stable
tags: [today, food-log, meals, plain, design, era-v4]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Food Log Rendering — Today Page is Meal-Grouped (Plain)
*Established: 2026-05-20 (plain text); date header re-added 2026-05-26; **meal-grouped redesign 2026-06-04**.*

On the **Today** page the food log is **plain** (no card panel/glass) and, as of the 2026-06-04 redesign, **grouped by meal**. User's original verbatim still holds: "the food log need no to be a panel, just plain text with dotted line to speerate."

> **2026-06-04 supersession (design-system redesign).** The Today food log is now **grouped into fixed Breakfast / Lunch / Dinner / Snacks sections**, each with a header (outline meal glyph + name + section calorie total + hairline rule) and its rows. This **replaces the earlier *flat* plain list** that interleaved `DottedSeparator`s. Rows use the **new `PlainDesignFoodRow`** design (bare food photo/emoji — **no background tile** — + calories-in-meta + micro progress bars).
>
> **2026-06-05 cleanup (empty sections + date swipe).** User verbatim: *"remove the add something to xxx under each of the meal type when they are empty. remove the add button for them as well."* Empty meal sections now show **only the header** — no "+" add button and no "Add something to <meal>…" text. Tapping an empty section does nothing. Also, the **horizontal date-swipe on the Today food log is permanently disabled** (`calendarCardSwipeEnabled` is hard-coded off and the Settings toggle has been removed) — user verbatim: *"disable the swipe betwen dates on the mainscreen food log"* and *"there is actually setting disale card swipeing, just set it to always disable, and remove that option."* Don't re-add the date swipe or its settings toggle. **🔁 REVERSED 2026-06-20** — the user asked for the date swipe back (*"add a swipeing effect on the food entry, left to right to switch date"*); it's re-enabled via a NEW UIKit horizontal `HomeDateSwipeAxisPanGestureRecognizer` on the flat-paper food log (NOT the old `calendarCardSwipeEnabled`/deck path, which stays disabled/unused). See "2026-06-20 — Food Card Capture … + Food-Log Date Swipe."

### Implementation

- `FoodEntriesCardContent` (in [Nutritionist/Views/CalendarView.swift](Nutritionist/Views/CalendarView.swift)) has **two clean branches**:
  - **`usesPlainStyle: true` (Today):** the date header (`"Friday, May 27"` 17 pt bold + entry count) then `plainMealSection(_:allEntries:)` for `[.breakfast, .lunch, .dinner, .snacks]` (**always all four, in that display order** — note dinner before snacks). Each section filters its entries (sorted by time ascending), shows the header + rows, or the empty-state button. Per-section "+" and empty-state call `onAddToMeal?(category)`.
  - **`usesPlainStyle: false` (Calendar):** the original panel header rule + `TimelineFoodRow` flat list — **unchanged**.
- **`PlainDesignFoodRow`** (mirrors `atoms.jsx` → FoodRow): a **46 × 46 leading visual with NO background tile** — the food **photo** (`resolvedCardImageData(for:)` → stored AI image, else closest chat-message image by name; rounded-rect clipped) when image features are on, **else the floating emoji** (no tile). The food name (16 pt), a meta line `[outline meal glyph] meal · time · <cal> cal` (**calories live in the meta line**, not right-aligned), two **1.6 pt micro progress bars** (accent goal-fraction + health-color health-fraction), and the ••• action `Menu` (Edit / Adjust Portion / Move / Copy / Delete). Each row has a **dashed bottom rule** (`DottedSeparator`). Takes `dailyGoal`, `accent`, `imageData`; parses `healthScore` from the entry JSON (health bar = `nutritionSuccess` ≥ 50 else `nutritionWarning`).
  - **2026-06-04 (user):** "i want the food picture stye to be back, i dont want the background of the food picture." The earlier-today gradient tile (`#faedda → #f5e1c4`) was **removed** — the leading visual is now the bare photo/emoji.
- **Time is 12-hour** (`"7:15 PM"`) — `PlainDesignFoodRow.timeFormatter` pins `Locale(identifier: "en_US_POSIX")`. Don't drop the POSIX locale or it reverts to 24-hour on 24h-region devices.
- **`MealCategory.outlineIcon`** (in [Nutritionist/Models/FoodEntry.swift](Nutritionist/Models/FoodEntry.swift)) = `sunrise` / `sun.max` / `moon` / `leaf` (lighter than the filled `.icon`), used for the section headers; tinted `Color.nutritionistPebble` so it reads on both light and dark.
- `TodayView.homePinnedCardSurface` passes `usesPlainStyle: true`, `dailyGoal:`, and **`onAddToMeal: { _ in isChatPresented = true }`** — per-meal add navigates to the **AI Chat overlay**. Still does **not** apply `CalendarCardSurfaceModifier` or the `calendarCardColorScheme` override.
- **Deck layout — top-anchored + clipped (2026-06-04, fixes the overlap):** the tall meal-grouped log overflowed *up over the date rings/globe* on real data. Fix: `FoodEntriesCardDeckPager` gained a `cardAlignment` param (default `.bottom` for Calendar); the Today deck passes **`cardAlignment: .top`** so the log pins below the header and scrolls down, and the card area is **`.clipped()`** so it can never bleed over the rings. The idle side slots are `Color.clear.frame(height: 0)` so the **center card** defines the deck height. (This supersedes the earlier same-day `height: deckCardHeight` placeholder, which over-estimated and pushed the card down → gap. User report: "the food log should be behind the date rings.")
- **Card colorScheme gotcha (still holds):** `homePinnedCardDeck` must pass `cardColorScheme: colorScheme` (page scheme), **NOT** `appSettings.calendarCardColorScheme` — that override belongs to Calendar's panel deck only.

### Supersession — date header is still SHOWN
*2026-05-26 (still in force).* The Today food log shows a `"Friday, May 27 · N entries"` header. Don't remove it without a fresh user instruction.

### Scope

- Applies to the **Today** page only. **Calendar** still uses the panel surface (`usesPlainStyle: false`) and `TimelineFoodRow`. Don't change Calendar's appearance without explicit direction.

### Explicitly NOT Allowed

- Don't reapply `CalendarCardSurfaceModifier` (or any card-surface modifier) on `homePinnedCardSurface`. The Today card is plain.
- Don't collapse the meal sections back into a single flat list on Today.
- **Don't put a background tile behind the food photo/emoji** (user rejected the gradient tile 2026-06-04). The leading visual is the bare photo (rounded) or floating emoji.
- Don't replace the row's `DottedSeparator` bottom rule with a solid `Divider()`/`Rectangle`.
- **Don't bottom-anchor the Today deck or remove the `.clipped()`** — the log must stay below the header and scroll internally, never overflowing up over the date rings.
