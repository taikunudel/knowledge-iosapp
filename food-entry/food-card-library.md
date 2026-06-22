---
type: rule
id: "food-entry/food-card-library"
title: "Food Card Library"
description: "A user-curated library of AI-generated food cards that can be saved from chat and reused from the chat-bar + menu, each rendered as the same nicely-designed card."
status: stable
tags: [food-entry, food-card, library, swiftdata, picker]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Food Card Library

*Established: 2026-05-20*

User-curated library of AI-generated food cards. After a chat nutrition analysis completes, the user can **save the card** and later **reuse it from the chat-bar `+` menu** without re-prompting the model. User verbatim: "when ask a food, when it complete, it shows a nicely designed food card, that can be added to a library and reused. add button should add a function library so reuse the card from the library."

### Model

- `LibraryFoodCard` (SwiftData `@Model`) lives at the bottom of [Nutritionist/Models/DayLog.swift](Nutritionist/Models/DayLog.swift). Fields: `id`, `name`, `calories` (denormalized for fast list rendering), `nutritionJSON` (full `NutritionResponse` JSON), `imageData` (optional JPEG), `savedAt`, `sourceMessageID` (optional back-reference to `ChatMessage.id`).
- Registered in the `Schema` in [Nutritionist/NutritionistApp.swift](Nutritionist/NutritionistApp.swift) alongside the existing models. The same model list is mirrored in every preview's `.modelContainer(for:)` call.
- The model lives inside `DayLog.swift` (rather than a sibling .swift file) **because the Xcode project uses traditional pbxproj file references**, and adding a brand-new `.swift` file would require editing `project.pbxproj` by hand. Don't try to "clean this up" by splitting the model unless you're prepared to do the pbxproj edit.

### Save Action (in chat)

- `MessageBubble.nutritionCard(_:image:)` in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift) now shows a **"Save to Library"** capsule button next to the existing "Follow up on this food" button. Tapping it calls `saveCurrentNutritionToLibrary(_:)`, which:
  - Saves the **base** `NutritionResponse` (multiplier = 1.0), not the portion-scaled `displayNutrition`.
  - Encodes the image as JPEG at quality 0.85 (falls back to `message.imageData`).
  - Sets `sourceMessageID = message.id`.
- After save, the button flips to a `checkmark` glyph with "Saved" label and is disabled. Idempotent: `saveCurrentNutritionToLibrary` first fetches any `LibraryFoodCard` with this `sourceMessageID` and won't insert a duplicate; `hydrateLibrarySavedState()` (on the button's `.onAppear`) restores the "Saved" label after the bubble is recreated (Codex 2026-05-31).

### Library View — Must Show the "Nicely Designed Food Card"

> **2026-06-11 update — compact 2-up grid + emoji + Frequent-first.** User verbatim (2026-06-09): *"on the library, the card should be smaller and rank the most frequent food at front in a past week with data. and they should have emoji."* The list is now a **2-column `LazyVGrid` of `LibraryFoodCardCompact`** cards (photo or big emoji, emoji + name, flame calories, heart health score, glass surface). The **default sort is "Frequent"**: cards ranked by how often that food (lowercased name match) was **logged as a `FoodEntry` in the past 7 days**, tiebroken by lifetime `usageCount` (a new `LibraryFoodCard` property incremented on every picker reuse; lightweight migration), then `savedAt`. Recent / Name sorts remain in a **trailing** toolbar `Menu` (NOT leading — the hamburger covers leading items). **Tapping a card in browse mode opens the full `LibraryFoodCardPreview` in a sheet** (`.medium`/`.large` detents) — this is how the locked "Library Card Visual Fidelity" rule below is preserved now that the grid cards are compact: the full saved card is one tap away, the grid card keeps its identity cues. Don't revert the grid to full-width cards, don't drop the emoji, and don't make "Recent" the default again.

`FoodCardLibraryView` (in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift)) has two modes via the `Mode` enum:
  - `.browse` — accessible from the side drawer as the **"Library"** destination (`selectedTab == 5`, SF Symbol `books.vertical`). Long-press a card for a destructive Delete in a context menu.
  - `.picker(targetDate:mealCategory:onPicked:)` — used as a sheet from the chat-bar `+` menu's **"From Library"** action.

**Each library entry must render as the same nicely-designed food card the user saw in chat**, not a flat list row. User verbatim: "when ask a food, when it complete, it shows a nicely designed food card, that can be added to a library and reused." A "reused" card the user can't recognize visually is a regression — when picking from the library, the user must see the same card they saved.

Required visual elements on every library entry (browse and picker):

- Saved image (if any), shown prominently — full-width thumbnail strip.
- Food name as `.headline`.
- Calories displayed large with the orange `flame.fill` icon (same treatment as the chat nutrition card).
- Health score displayed large with the heart icon (color from `healthScoreColor(...)`).
- Saved-date footnote.
- Wrapped in a rounded, lightly-tinted glass-style container (use the project's liquid-glass vocabulary — see the iOS 26 Design Guide section).

`LibraryFoodCardPreview` is the dedicated view that renders this. **Don't replace it with a plain `HStack(thumbnail, text)` list row.** Cards are sorted `savedAt` descending.

### + Button "From Library" Action

- `UnifiedChatInputBar.plusButton` menu (in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift)) gained a third item: `Label("From Library", systemImage: "books.vertical")`. Tapping it sets `showingLibraryPicker = true`, which presents `FoodCardLibraryView(mode: .picker(...))` in a `.sheet`.
- The picker callback creates a new `FoodEntry` from the chosen card and inserts it into the `ModelContext`. After insertion, `onPicked` fires and the sheet dismisses.
- **Target date:** the entry logs to the date the composer is showing, not unconditionally today. `UnifiedChatInputBar.libraryTargetDate` (passed by `SharedInputBar.targetDate` ← `ContentView.captureTargetDate` = the focused `selectedDate`) drives `.picker(targetDate:)`. **Meal: the user picks it** — 🔁 **2026-06-20** tapping a card opens a meal `confirmationDialog` (`commitPick(_:meal:)`); the old fixed `.snacks` category is gone (user: *"let me select meal and still add to the currently highlight date, not always today"*). (Codex 2026-05-31 — previously always logged to `Date()`/`.snacks`.)
- **Provenance:** a reused entry sets `aiSourceMessageID = nil` (NOT the card's `sourceMessageID`) so the original chat bubble doesn't get linked to / mutate the reused entry.

### Explicitly NOT Allowed

- **Don't remove "From Library"** from the `+` menu. It is the fourth canonical thing the menu does (after the three image flows: Photo Library, Take Photo, and now From Library).
- **Don't save the portion-scaled nutrition** to the library. The library card is the canonical base nutrition; portions belong on `FoodEntry`.
- **Don't change the side-drawer position of "Library"** (currently 5th, between Trends and Settings) without explicit user direction — the drawer order is a locked design.
