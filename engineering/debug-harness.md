---
type: reference
id: "engineering/debug-harness"
title: "DEBUG Verification Harness — Launch-Arg Seeding"
description: "A #if DEBUG-only launch-argument seeding harness in ContentView used to screenshot design screens via simctl without a backend or manual tapping."
status: stable
tags: [engineering, debug, testing, simctl, screenshots, seeding]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# DEBUG Verification Harness — Launch-Arg Seeding

*Established: 2026-05-26*

`ContentView` (in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift)) carries a **`#if DEBUG`-only** seeding harness used to screenshot design screens via `simctl` without a backend or manual tapping:

- **`-UITestSeed`** — on launch, if the store is empty, inserts 6 sample `FoodEntry` rows for *today* (each with `aiGeneratedNutritionJSON` incl. `foodEmoji` + `healthScore` + macros), one `LibraryFoodCard` ("Chicken salad"), and pins `protein`/`fiber`/`sodium`. 2026-06-21: also seeds the previous 3 days and marks days −1 and −3 **complete** (today + −2 stay incomplete) so the solid-vs-dotted calorie-bar contrast is visible.
- **`-UITestTab N`** — sets the initial `selectedTab` (0 Today · 1 Calendar · 2 Chat · 3 Trends · 4 Settings · 5 Library) so any destination can be captured directly.
- **`-UITestAttachTray`** (added 2026-06-04) — opens the composer's `+` **AttachTray** on launch (initial value of `UnifiedChatInputBar.showingAttachTray`) so the tray can be screenshot without a tap.
- **`-UITestDrawer`** (added 2026-06-04) — opens the navigation **peek drawer** on launch (initial value of `ContentView.isDrawerOpen`) so the drawer can be screenshot without a tap.
- **`-UITestOnDeviceAI`** (added 2026-06-17) — runs the on-device Foundation Models **inference self-test** (`runOnDeviceSelfTestIfRequested`): a raw `respond`, a full nutrition analysis+decode, and a Q&A; writes results to `Documents/ondevice_selftest.txt` (read via `simctl get_app_container … data`). Use on a real Apple-Intelligence device to confirm local generation (the sim fails with ModelManagerError 1026 — no model weights). Also `-UITestLongDraft` (pre-fills a long composer draft to screenshot the grown two-row pill).
- **`-UITestCaptureCard`** (added 2026-06-20) — shows the floating `CapturedFoodCard` on launch with sample nutrition (`presentCaptureCardForUITestIfRequested`), so the food-capture UI can be screenshot without a live AI call. Pair with `-UITestSeed -UITestTab 0` to see it over a populated Today. Modifiers (2026-06-21): **`-UITestPortion2x`** (card at 2× portion → verify calorie/macro scaling), **`-UITestThinking`** (the non-blocking "Thinking…" indicator instead of the card), **`-UITestFallback`** (card with the "model isn't available here" fallback note).

All of these are gated to `#if DEBUG` **and** inert unless the launch argument is present, so they never affect normal or Release launches. Capture flow (screenshots land in the git-ignored `.artifacts/design-verify/`):

```bash
simctl launch <dev> com.example.Nutritionist -UITestSeed -UITestTab 0
simctl io <dev> screenshot .artifacts/design-verify/today.png
```

The store **persists across launches**, so the seed's `guard existing.isEmpty` short-circuits on a second seeded launch — `simctl uninstall` first for a clean re-seed. Keep this harness (it's how the design was visually verified); if removed, note it here.

*v5 addition: `-CFSeedDemo` seeds demo entries for the Caffeine home (DEBUG only) — see [[caffeine-v5]].*
