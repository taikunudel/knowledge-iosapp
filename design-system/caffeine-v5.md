---
type: guide
id: "design-system/caffeine-v5"
title: "Caffeine v5 — the simplism design era (supersedes liquid glass)"
description: "The 2026-07-10 design pivot: v4.0 archives the liquid-glass app; v5 reimplements it against the Caffeine handoff (AnalyzeHome template) — olive/paper palette, one #FF4A1C accent, bundled grotesk/mono fonts, flat tab bar, anti-glass rules, and the decisions/open items of the first (home-flow) phase."
status: stable
tags: [caffeine, simplism, v5, design-era, anti-glass, palette, fonts, tab-bar, composer]
created: 2026-07-10T00:00:00Z
updated: 2026-07-10T00:00:00Z
---

# Caffeine v5 — the simplism design era

## The pivot (user decision, 2026-07-10)

> "backup the old which is current design and reimplement the app following the
> new design … forget about the old design."

- **The old (liquid-glass) app is archived, not lost:** git tag **`v4.0`**
  (annotated "liquid-glass-design"), safety branch **`liquid-glass-design`**,
  `MARKETING_VERSION = 4.0` — all pushed to `taikunudel/Nutritionist`.
- **Everything liquid-glass is superseded for new work**: the iOS-26 glass
  guide, the MUJI accent palette, no-manual-blur rules, the glass hamburger /
  side drawer, the frosted capture overlay, the planet globe & decorative
  Today elements. Pages stay for history with `status: superseded`.
- v5 work happens on `main`; the first phase (home flow) was implemented and
  simulator-verified on 2026-07-10.

## Source of truth

- **Canonical spec:** the Claude Design handoff bundle, checked into the app
  repo at `design/caffeine-design-system/` (copied from
  `~/Downloads/Caffeine Design System-handoff.zip`). The primary design is
  `project/templates/analyze-home/AnalyzeHome.dc.html` — read it whole; its
  `renderVals()` script defines the interaction logic.
- **Caffeine in one line:** simplism — pure flat color, hairline separation,
  near-square geometry, uppercase Space-Mono micro-labels, physical motion
  (decelerate, never bounce), **anti liquid-glass**: no blur, no frosted
  panels, no gradients-as-decoration, no ambient card shadows.
- **Palette canon:** the template's **olive scheme wins** over
  `project/tokens/colors.css` (which holds an unused warm-brown ramp — keep it
  only as structural reference for spacing/motion/state rules). App tokens
  live in `Nutritionist/Views/Caffeine/CaffeineDesign.swift`:
  ink `#14160E`, paper `#F2F3EE`, paper-line `#DCDFD3`, olive `#333824`,
  olive-line/composer `#464C31`, composer-line `#5C6342`, chip `#3A4029`,
  muted-on-olive `#999F86`, text-on-olive `#C2C7B0`, muted-on-paper `#75786B`,
  label-on-paper `#565A4C`, faint/fat-bar `#A3A695`, **accent `#FF4A1C`**
  (press `#C8330D`). One hot color only; press states darken + nudge 1pt down.

## Type

Three bundled OFL families (TTFs in `Nutritionist/Fonts/`, registered via
`UIAppFonts` in `Nutritionist/Info.plist`):

- **Space Grotesk** (display: headings + big numerals, tracking −0.02em) —
  PostScript `SpaceGrotesk-Regular/Medium/SemiBold/Bold`
- **Hanken Grotesk** (body/UI) — `HankenGrotesk-Regular/Medium/SemiBold/Bold`
- **Space Mono** (uppercase micro-labels at 0.14em tracking + all numeric
  data) — `SpaceMono-Regular/Bold`

⚠️ Sizes are **fixed** (`Font.custom(_:fixedSize:)`) to match the fixed-metric
template; Dynamic Type support is a known regression deferred to a later pass
(the WWDC26 Dynamic-Type work applied to the OLD food log).

## What phase 1 shipped (all in `Nutritionist/Views/Caffeine/`)

- `CaffeineLogic.swift` — the pure logic behind the flow (CFDayTotals,
  calorie shares, goal fraction, day labels/clamps, meal-by-hour, echo
  truncation, meal naming, report footer), extracted from the views so
  `NutritionistTests/CaffeineLogicTests.swift` (44 cases) can exercise it.
- `CaffeineDesign.swift` — tokens: palette, fonts, motion curves
  (panel `cubic-bezier(0.32,0.72,0,1)` 0.55s, standard ease 0.18s), `CFBar`,
  `CFMacroRow`, `CFMicroCell`, `CFStripes` (photo placeholder), button styles,
  pulse dot. **All motion/transition rules live in [[motion]]** — edit there,
  not here.
- `CaffeineHomeView.swift` — the AnalyzeHome screen: paper day-summary layer
  (date switcher, kcal display-56, calorie bar, macro bars), olive meals layer
  (time/name/kcal rows, hairlines), composer ("Describe, snap, or speak…",
  photo chip, LISTENING row, camera/mic/send circles); expanded olive panel:
  ANALYZING ON CLOUD + echo quote + 5-step checklist (steps pace at 750 ms
  while the **real** `AIManager.analyzeNutrition` call runs), FINAL REPORT
  card (name, kcal-64, macro bars, FIBER/SUGAR/SAT FAT/SODIUM grid,
  "AI ESTIMATE · ANALYZED ON CLOUD", DONE — LOG IT pill) and an **error state**
  the prototype lacked (ANALYSIS FAILED + message + TRY AGAIN / DISMISS,
  composer text retained). Sub-screens per template: single-food detail
  (real photo or striped placeholder), day detailed report, date picker.
- `CaffeineSpeech.swift` — real dictation (SFSpeechRecognizer + AVAudioEngine,
  partials stream into the composer); visible notes on failure
  (`MIC ACCESS DENIED…`, `DICTATION UNAVAILABLE`). Mic/speech usage strings in
  Info.plist.
- `CaffeineRootView.swift` — the v5 root (swapped in `NutritionistApp.swift`):
  **flat tab bar HOME · TRENDS · LIBRARY · SETTINGS** (paper, top hairline,
  mono labels, 2px accent underline; instant content swap — no crossfade),
  replacing the hamburger/side-drawer chrome. Trends/Library/Settings keep
  their old internals until their own Caffeine pass. `-CFSeedDemo` launch
  argument seeds demo entries (DEBUG only).

## Locked behaviors (from the template's logic — don't "fix" these)

- **Swipe on the meals layer:** right → previous day, left → toward today;
  clamped at today (next-arrow at 0.3 opacity). Arrow buttons ‹ › do the same.
- **Macro bars show calorie share** (protein·4 / carbs·4 / fat·9 over total),
  NOT progress toward macro goals — both per-meal and day totals.
- **Analysis echo**: 60-char-truncated quote of the input (or "photo of your
  meal"); meal name comes from the AI's `foodName`.
- **Logging target:** DONE — LOG IT logs to the **viewed** day (meal category
  by hour: 4–11 breakfast, 11–16 lunch, 16–22 dinner, else snacks); the row
  lands as the panel finishes collapsing (~480 ms).
- **Date picker** lists every day from today back to the earliest logged day
  (≥14 rows) — the prototype's 14-day cap was deliberately lifted; empty days
  show "—".
- **Single fixed appearance** on home (paper + olive); the status bar flips to
  light text only while the olive panel covers the top
  (`statusBarOnOlive` binding → `preferredColorScheme`).
- **Tap anywhere outside the composer exits it** (user 2026-07-10: "when text
  bar is bought up by tapping on it, the keyboard will be up, then tap
  anywhere else will exit the chatbar"): while `composerFocused`, the summary
  + meals layers become a clear tap-catcher (no blur — anti-glass) that drops
  focus; the meals ScrollView also drag-dismisses
  (`scrollDismissesKeyboard(.interactively)`). Tapping the composer's own
  surface does NOT dismiss. Guarded by
  `testTapOutsideDismissesComposerKeyboard`.
- Prototype chrome deliberately **not** implemented: fake 9:41/LTE status bar,
  fake home-indicator bar, CSS hovers, the hard-coded "87% CONFIDENCE" line
  (no confidence in `NutritionResponse` → footer omits it).
- **FINAL REPORT v4 parity restored (2026-07-10 night):** the result card
  carries the three locked v4 controls again — a **PORTION stepper**
  (− / N× / +, 0.5×–10× step 0.5; displayed kcal/macros/micros scale live;
  DONE logs scaled calories + already-scaled payload + `portionMultiplier`),
  a **MEAL picker** (four flat chips, default by hour, the user always
  picks), and **SAVE TO LIBRARY** (saves the BASE 1× card, idempotent per
  analysis via `analysisID`; never the portion-scaled values). Guarded in
  `testCaffeineHomeFlow` (stepper 1×→1.5×, Dinner pick, save presence).
- **Unified model routing (2026-07-10), shown explicitly in the panel:** the
  chain is fixed — **Gemini 3.5 Flash → Gemini 3.1 Pro → Apple Intelligence**
  (`AIModelCatalog.chain`; on-device dropped when unavailable / for photos).
  The checklist's first bullet is "MODEL — <LIVE MODEL>", each fallback adds
  an accent "↯ <X> FAILED — FALLING BACK TO <Y>" line, and the result footer
  reads "AI ESTIMATE · <FINAL MODEL>". Don't re-add other providers to the
  catalog without a new instruction.

## Verification (2026-07-10, iPhone 17 Pro / iOS 27 sim)

**Unit layer:** `NutritionistTests/CaffeineLogicTests.swift` — 44 tests over
CFLogic + CFDayTotals + the nutrition-payload round-trip (macro-estimation
fallback when the model omits macros, malformed/missing payload degradation,
SwiftData persistence round-trip) + all 10 bundled font names resolving via
`UIFont(name:)`. Whole unit suite: 63 tests, 0 failures. Note: the test
target compiles its own copy of `FoodEntry.swift`, so tests must qualify the
app type (`Nutritionist.FoodEntry`) when calling app-module APIs.

**UI layer:** `NutritionistUITests/CaffeineFlowUITests.swift` drives the whole flow and
drops numbered screenshots into `/tmp/caffeine_shots/`: seeded home, day nav
(arrows + swipe), empty day, date picker, food detail, day report, composer
typing (keyboard squeeze clips the summary layer — nothing under the status
bar), send → analyzing → **both** end states verified on different runs (real
FINAL REPORT then DONE — LOG IT row-count +1; real Gemini 503 → error panel →
DISMISS), mic permission alerts → DICTATION UNAVAILABLE note (sim has no
dictation backend), all four tabs, back home. `xcodebuild … test` →
`** TEST SUCCEEDED **`.

## Open items for the next phases

- **Trends is blind to v5 data:** `NutritionTrendsView` charts only days in
  `appSettings.completedDates`; the new flow never marks a day complete, so
  Trends shows "No data yet" for new logging. Decide in the Trends pass:
  drop the completion gate or auto-complete past days.
- Trends / Library / Settings still fully old-design (glass, dark scheme,
  old controls — Settings even offers liquid-glass appearance knobs that no
  longer affect the home).
- Retired-from-home features still in the codebase (planet globe, hearts,
  dynamic health background, global composer design-nav, hamburger sidebar) —
  all live only in the dormant `ContentView` tree; recoverable via tag `v4.0`.
- Voice on real hardware: sim lacks a dictation backend; verify on Taikun's
  iOS-27 phone.
- The template's pill CTA / circular icon buttons technically conflict with
  the tokens' "pill = switches/tags only" rule — **template wins** (recorded
  so nobody "fixes" the pill).
- The handoff's `ui_kits/app` (login/sidebar caffeine-tracker web demo) is
  illustrative only — styling reference, never a spec for this app.

See also [[wwdc2026/liquid-glass]] (superseded era), [[accent-palette]]
(superseded palette), [[ios26-design-guide]] (superseded guide),
[[rejected-experiments]].
