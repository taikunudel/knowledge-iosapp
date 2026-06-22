---
type: guide
id: "design-system/ios26-design-guide"
title: "Always Refer to the iOS 26 Design Guide"
description: "Consult Apple's iOS 26 / liquid-glass guidance for any UI surface, target the iOS 27 runtime, and use the project's native-glass modifiers without manual borders."
status: stable
tags: [ios26, ios27, liquid-glass, design-guide, accessibility, runtime]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Always Refer to the iOS 26 Design Guide

*Established: 2026-05-20*

Whenever Claude designs, modifies, or reviews any UI surface in this project (button styles, sheets, navigation chrome, materials, typography, animations, haptics, etc.), it **must consult Apple's iOS 26 / liquid-glass design guidance first** and bias toward native iOS 26 idioms. User verbatim: "remeber always to refer to ios26 design guide."

### Taikun's iPhone Runtime — iOS 27 ONLY
*Established: 2026-06-09; **updated 2026-06-21**.*

**We only test on the iOS 27 simulator or Taikun's iOS-27 iPhone. NOT developing for iOS 26 or earlier anymore** (user 2026-06-21: *"we only test on ios 27 simulator or taikun's phone. i am not developing for ios26 or earlier anymore."*). So:
- Treat **iOS 27 runtime + API behavior** as the source of truth (e.g. Foundation Models on-device AI works on the real phone; the sim advertises availability but can't generate — see "AI model alignment").
- **New code should target iOS 26+/27 directly** — don't write iOS 17/18 fallbacks for new work. Existing `#available(iOS 26.0, *)` gates + their pre-26 fallbacks (drawer pan, Today-card pan, date-swipe recognizer) can stay until the code is next touched; the **deployment target is still iOS 17** in the pbxproj (not yet bumped), so a bare iOS-26 API call still needs an availability gate — but you never need to make the fallback branch *good*, just compile.
- Build via `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild … -destination 'platform=iOS Simulator,name=iPhone 17 Pro'`.

### What this means in practice

- **Visual vocabulary:** Prefer liquid-glass surfaces (translucent fills, subtle inner highlights, soft borders, low-opacity shadows) over flat solid backgrounds. The project already ships `LiquidGlassRoundedModifier`, `LiquidGlassCapsuleModifier`, `LiquidGlassCircleModifier`, and `LiquidGlassShapeModifier` in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift) — **use them for any new floating control, button, or sheet chrome.**
- **Don't invent custom glass.** If a new control needs the glass look, reach for the existing modifiers (and extend them only if a new shape is needed). Don't ship one-off `.background(.ultraThinMaterial).overlay(stroke).shadow(...)` reimplementations. **And never add `.overlay` stroke borders or gradient fills on top of native `.glassEffect()`** — see the "NO manual borders" rule in the Liquid Glass section.
- **Typography:** prefer the system text styles (`.body`, `.caption`, `.title3`, etc.) with weight variants rather than hard-coded `.system(size:)` unless a specific visual rhythm requires it.
- **Buttons:** for circular icon buttons, use `LiquidGlassCircleModifier`. For pill / capsule actions, use `LiquidGlassCapsuleModifier`. For rounded-rect surfaces, use `LiquidGlassRoundedModifier`.
- **Motion:** prefer `.snappy` / `.bouncy` / `.smooth` animation presets that ship with iOS 26 over hand-tuned `easeIn` / `easeOut` curves unless the snappier presets feel wrong.
- **Sheets & dialogs:** use native `.sheet`, `.confirmationDialog`, `.fullScreenCover`, and `Menu` over custom modal containers.
- **Accessibility:** respect `@Environment(\.accessibilityReduceMotion)` and `@Environment(\.dynamicTypeSize)` — already a pattern in the codebase.

### When in doubt

- If you're about to write `.background(Color.gray.opacity(...)).overlay(RoundedRectangle...)` for a control, stop and use a liquid-glass modifier instead.
- If you're unsure whether something matches iOS 26 guidance, surface the question to the user (with the relevant Apple HIG section) rather than guessing.

### Liquid Glass — native adoption status (2026-06-03 design revamp, research-backed)
The shared `LiquidGlass*` modifiers already adopt the native API per finding **F8**: `LiquidGlassShapeModifier` (in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift)) branches `if #available(iOS 26.0, *)` → `.glassEffect(Glass.regular.tint(…).interactive(), in: shape)`, with the hand-rolled `.ultraThinMaterial`-style stack as the **iOS 17 fallback** (deployment target is **iOS 17.0**, so the gate + fallback are required — don't remove them).

- **NO manual borders or highlight overlays on native glass (iOS 26 path).** User 2026-06-05: *"is there a intentional added thin board on it? why do i feel like when the glass move, the boarder stay there the same."* The native `.glassEffect()` already renders its own internal highlights and subtle edges as part of the system glass material. The old code layered `.overlay { shape.strokeBorder(…) }` + `.overlay { shape.fill(LinearGradient…) }` on top — during animation these manual layers rendered in a different pass from the system glass, causing the border to visually "stay still" while the glass moved. **These overlays are removed from the iOS 26 branch.** The fallback (iOS 17) path still uses manual borders/highlights (there is no native glass to conflict with). **Don't re-add `.overlay` strokes or gradient fills on top of `.glassEffect()` anywhere in the app — not on the hamburger, not on the composer, not on pinned chips, not on any new glass surface.** If a glass element needs a border effect, tint the `Glass` itself via `.tint()` or use `.glassEffect(.regular.interactive())` — don't hand-paint one.

Revamp changes applied from the findings:
- **F11 — Reduce Transparency (accessibility):** `LiquidGlassShapeModifier` now reads `@Environment(\.accessibilityReduceTransparency)` and, when on, routes to the **opaque fallback** (system-background base, no blur/translucency) instead of glass — because native auto-adaptation does NOT cover custom modifiers. This is the single chokepoint, so every glass surface app-wide inherits it. Don't special-case Reduce Transparency at call sites; fix it here.
- **F9 — `GlassEffectContainer`:** the Today **pinned-nutrient chip strip** (multiple adjacent glass capsules) is wrapped in a `GlassEffectContainer(spacing: 8)` on iOS 26 (`pinnedChipRow` in [Nutritionist/Views/TodayView.swift](Nutritionist/Views/TodayView.swift)) so the chips share one sampling region (glass can't sample glass). When adding any new cluster of ≥2 adjacent glass elements, wrap them in a `GlassEffectContainer` too.

### Deliberately NOT changed — glass on content cards (F10 conflict)
Apple's guidance (finding **F10**) is "glass on the navigation/floating layer only, never on content (lists, tables, media), applied sparingly." The app currently puts glass on **content** surfaces too — the Calendar day cards and the `LibraryFoodCardPreview`. That **conflicts with the locked "glass cards" design decisions** (Calendar card surface, Library card visual fidelity). **Do NOT strip glass from those cards to satisfy F10 without explicit user direction** — it's a locked aesthetic, and the trade-off is the user's call. Recorded here so this tension isn't silently "fixed" in a later pass.
