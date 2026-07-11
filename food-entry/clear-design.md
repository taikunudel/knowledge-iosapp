---
type: decision
id: "food-entry/clear-design"
title: "v4 · Clear (No-Blur) Design + Non-Blocking AI Indicator + Model Alignment"
description: "All background blur is removed for a clear design, AI thinking is non-blocking with the card only on finish, and the chosen AI model is actually used with a fallback note."
status: stable
tags: [food-entry, design, blur, ai-model, foundation-models, ios27, era-v4]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Clear (No-Blur) Design + Non-Blocking AI Indicator + Model Alignment

*Established 2026-06-21. Build-verified (`BUILD SUCCEEDED`, iPhone 17 Pro sim) + screenshot-verified (clear card, "Thinking…" pill, fallback note).*

### NO background blur anywhere — clear design (REVERSES the blur policies)
User: *"remove all the background blury policy, and when the card is shown, do not blur the background. i think the clear design is modern."* All screen-dimming/frosting is removed:
- **Food-capture overlay** (`ContentView.foodCaptureOverlay`): the `.ultraThinMaterial` frosted backdrop is GONE. The result/error card now floats over a **`Color.clear`** tap-catcher (tap-outside still dismisses, no dim).
- **`designNavRoot`**: the `.blur(radius: globalComposerActive ? 3 : 0)` is removed; the composer-active catcher is now `Color.clear` (was `Color.black.opacity(0.05)`). **This supersedes the 2026-06-16 "the background should be blur just like when tab the cahtbar" rule.**
- **`TodayView`**: the `.blur(radius: shouldDimBackground ? composerBlurRadius : 0)` + its `.allowsHitTesting(!shouldDimBackground)` are removed (a clear catcher still dismisses the keyboard on tap). `composerBlurRadius` is now unused.
- **Don't reintroduce any `.blur(…)` on a background, or a `.ultraThinMaterial`/dimming backdrop, behind the card or composer.** (The dead `AIChatView`'s own blur is left as-is — it's never presented.)

### AI thinking is NON-BLOCKING — small indicator, card only on finish
User: *"i want the AI thinking do not disturb everything else, it can show an indicator representing the AI is working, but only when it finishes, it pop up the card."* `foodCaptureOverlay` is now a `switch` on `foodCapturePhase`:
- **`.analyzing`** → a small floating **`foodCaptureThinkingIndicator`** ("Thinking…" + spinner, opaque capsule + shadow, NO blur) pinned just above the composer, wrapped in `.allowsHitTesting(false)` so **the rest of the app stays fully usable while the AI works**. (URLSession timeout → `.error` card, so it can't hang forever.)
- **`.result`** → the `CapturedFoodCard` pops up (only when finished), over the clear background.
- The old full-screen `foodCaptureLoadingCard` + "Tap anywhere to cancel" are removed.

### AI model alignment — the chosen model is actually used (+ "why Gemini" note)
User: *"the AI used is not aligned with the chosen want, like i want to use apple intelligence but i dont know why gemini is really used."* **Root cause (a real bug):** `AIManager.init` reads `selectedAIModelOptionID` from UserDefaults **once**; the composer's model chip writes that same key via its OWN `@AppStorage`, which does NOT update the manager's `@Published selectedModelOption`. So `modelChain` used a STALE primary and the chip choice was ignored.
- **Fix:** `AIManager.refreshSelectedModelFromDefaults()` re-reads the persisted chip choice into `selectedModelOption`; `beginFoodCapture` calls it on the main actor **before** each analysis. Now the selected model is the chain's primary. **Don't remove this sync** (the chip and the manager are otherwise decoupled).
- **Why Gemini still shows on the SIMULATOR:** Apple Intelligence (Foundation Models) **cannot generate on the sim** (advertises `isAvailable == true` but `respond()` fails with ModelManagerError 1026 — no model weights), so the chain falls back to the cloud default (Gemini). On Taikun's real iOS-27 phone the on-device model is used. To make this transparent, `AIManager.lastUsedWasFallback` is set in the chain loop, and the card shows a **`fallbackNote`** ("`<selected>` isn't available here", amber) under the "✨ `<model>`" attribution. **So on the sim, Apple-Intelligence-selected → Gemini-used is EXPECTED + now explained on the card; verify the on-device path on the real phone.**

### Runtime target is iOS 27 ONLY (see "Taikun's iPhone Runtime")
User: *"we only test on ios 27 simulator or taikun's phone. i am not developing for ios26 or earlier anymore."* New code targets iOS 27; don't add iOS 17/18 fallbacks for new work (existing `#available(iOS 26)` fallbacks can stay until touched). See the updated runtime note below.
