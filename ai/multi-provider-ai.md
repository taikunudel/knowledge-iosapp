---
type: reference
id: "ai/multi-provider-ai"
title: Multi-Provider AI + Retry
description: Reference for the multi-provider LLM client (Apple on-device, Gemini, OpenRouter, GLM), the model fallback chain, retry affordance, and per-card attribution.
status: stable
tags: [ai, providers, foundation-models, fallback, retry]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Multi-Provider AI + Retry
*Established: 2026-06-03. Implements the user's "let me choose different provider and model (like openclaw)" + "add a retry button" requests, following the conventions in "Elegant-Architecture Reference §3".*

### On-device AI — Apple Foundation Models (default when available)
*Added 2026-06-17 (user: "add local AI as one option to the model list, and use it by default"); researched against Apple's iOS 26/27 docs.*
- **Framework:** `import FoundationModels` (iOS 26+, expanded iOS 27). `FoundationModelsClient` (top-level enum in ContentView.swift) wraps it, gated `#if canImport(FoundationModels)` + `@available(iOS 26.0, *)` because the deploy target is iOS 17 — **every** Foundation Models reference MUST stay gated. API used (verified, don't fabricate): `SystemLanguageModel.default.availability` → `.available` / `.unavailable(.deviceNotEligible | .appleIntelligenceNotEnabled | .modelNotReady)`; `SystemLanguageModel.default.isAvailable`; `LanguageModelSession(instructions:)`; `try await session.respond(to:).content`.
- **Provider:** `LLMProviderKind.appleOnDevice` (no API key, no baseURL). Catalog option `AIModelOption(provider: .appleOnDevice, modelID: "system", label: "Apple Intelligence")` is `AIModelCatalog.all[0]`; the picker group is "On-Device".
- **Default-when-available:** `AIModelCatalog.default` is now a **computed** property → `onDeviceOption` when `FoundationModelsClient.isAvailable`, else `cloudDefault` (Gemini Flash) — so AI never silently breaks on hardware without Apple Intelligence. Existing users keep their saved `selectedAIModelOptionID`; only fresh installs get the dynamic default.
- **Routing:** `analyzeNutrition` / `askGeneralQuestion` branch `.appleOnDevice` FIRST → `onDeviceNutrition` / `onDeviceChat` (reuse the same system prompts; parse JSON via `stripJSONFences` + decode). **Text-only:** a photo nutrition request with `.appleOnDevice` selected falls back to `cloudDefault` (Gemini) via a local `effectiveModelID` (NOT by mutating `selectedModelOption` — that's `@Published` + persists, would flicker the chip). Vision on the on-device model is iOS-27-version-dependent; revisit when verifiable.
- **Runtime-tested 2026-06-17 (DEBUG `-UITestOnDeviceAI` harness, `ContentView.runOnDeviceSelfTestIfRequested`).** Ran REAL inference on the iPhone 17 Pro sim and wrote results to `Documents/ondevice_selftest.txt`. Finding: `isAvailable == true` in the sim BUT actual `respond()` **fails with `ModelManagerError Code=1026`** — the simulator advertises availability but **doesn't ship the model weights**, so generation can't run (Apple's documented sim limitation, NOT a code bug). On real Apple-Intelligence hardware the on-device call succeeds. **So `isAvailable` is necessary but NOT sufficient** — a device can report available yet fail to generate.
- **Transparent cloud fallback = the "never fail" guarantee** (user 2026-06-17: "the on device should never fail tho"). `analyzeNutrition` / `askGeneralQuestion` wrap the on-device call in do/catch; on ANY failure they fall through to `cloudDefault` (Gemini) via `effectiveModelID` (NOT by mutating `selectedModelOption`). Proven in the same self-test run: on-device failed (1026) → fell back → returned correct results (`Banana 105 cal, health 90, protein 1.3g`; a real apple Q&A). So the USER-FACING path never hard-fails: on-device first (free/private on real HW), cloud only if local can't generate. Keep this fallback unless the user explicitly wants pure on-device (hard-error) behavior.
- **To verify pure on-device generation:** run the app on a real Apple-Intelligence iPhone (Xcode → your device) with `-UITestOnDeviceAI`; `A_raw_respond` (no fallback) succeeding there confirms real local inference. The sim will always show `A_raw_respond FAIL: …1026`.
- **Future:** `@Generable` guided generation would give guaranteed structured output (stronger than prompt-asked JSON); `LanguageModelSession.prewarm()` cuts first-call latency; iOS 27's model-abstraction layer + vision are the next steps.
- `LLMProviderKind` (in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift)): `.appleOnDevice` (local), `.gemini` (native API), `.openrouter`, `.glm` (Z.AI). OpenRouter + GLM are **OpenAI-compatible** (`/chat/completions`) and share one client; only baseURL + key + model id differ. Base URLs: OpenRouter `https://openrouter.ai/api/v1`, GLM `https://open.bigmodel.cn/api/coding/paas/v4` (mirrors the user's openclaw config).
- `AIModelOption` + `AIModelCatalog.all` — the **curated** model list (user chose "curated list only"). Edit `AIModelCatalog.all` to add/remove models. Selection persists under `@AppStorage`-style `UserDefaults` key `selectedAIModelOptionID`; `AIManager.selectedModelOption` is the single source of truth for routing. The legacy `GeminiModel`/`selectedModel` is retained only so old prefs decode — **don't route on it**.
- Picker UI: the AI Chat top bar `Menu` + the composer's `modelSelectorChip` show a `Section` per provider (On-Device / Gemini / OpenRouter / GLM) via `AIModelCatalog.grouped`, bound to the shared `selectedAIModelOptionID`.

### Keys (Secrets.xcconfig → Info.plist → `infoDictionary`)
- `GEMINI_API_KEY` (existing), `OPENROUTER_API_KEY`, `ZAI_API_KEY` — all mapped in Info.plist via `$(VAR)`. **The OpenRouter/GLM values are blank placeholders the user must fill** in `Secrets.xcconfig`. `AIManager.apiKey(for:)` reads them; an empty key throws a clear "not configured" error surfaced in chat.
- ⚠️ Per "Elegant-Architecture Reference §5", Info.plist keys are extractable from the built app; this is the pragmatic personal-build trade-off. A future hardening is Keychain + in-app key entry.

### Request paths
- Gemini: unchanged native path (`responseSchema` structured output). Now uses `selectedModelOption.modelID` for the endpoint.
- OpenAI-compatible (`openAICompatibleRequest`): `POST {baseURL}/chat/completions`, `Authorization: Bearer`, `response_format: {type:"json_object"}` for nutrition (schema described in the system prompt; `json_object` is the broadly-supported lowest common denominator vs. provider-specific `json_schema`), plain for Q&A. Vision images are attached as a `data:` URL **only** for models flagged `supportsVision`. Response parsed from `choices[0].message.content` (fences stripped before JSON decode).

### Retry
- `AIChatView` captures a `FailedSendAttempt` (text, image, flags, the user+error message ids) in each `sendMessage` `catch`. A **"Retry last message"** capsule appears above the composer when `failedAttempt != nil && !isProcessing`; `retryLastFailedSend()` deletes the failed user+error bubbles, restores the inputs, and re-sends — so a failed API call never makes the user retype. (Chat completions are side-effect-free, so re-sending is safe.)

### Model fallback chain + per-card attribution (2026-06-17)
User: *"add a model fallback in the setting, let me decide the order of the model tries, and explicitly show what model generate a food card going forward."*
- **Chain routing.** `AIManager.modelChain` = the primary (`selectedModelOption`, the chip) first, then `AppSettings.modelFallbackOrder` (user-ordered IDs), de-duped, with `cloudDefault` appended as a last resort; on-device entries are dropped when `!FoundationModelsClient.isAvailable`. `analyzeNutrition` / `askGeneralQuestion` are now thin **loops** over `modelChain` calling `…Single(…)`; the first success wins, and the winning `model.label` is stamped on `AIManager.lastUsedModelLabel`. On-device is skipped for PHOTO requests (text-only) so the chain moves to a vision model.
- **`requestModel` indirection (don't undo).** The `…Single` helpers + the OpenAI-compatible helpers read **`requestModel`** (= `activeModelOverride ?? selectedModelOption`), and the chain loop sets `activeModelOverride` per attempt. This lets the loop retarget every helper WITHOUT threading a model param through all of them, and WITHOUT mutating the persisted `selectedModelOption` (which would flicker the chip + write UserDefaults). `selectedModelOption` stays the UI/persistence source of truth.
- **Settings UI:** `SettingsView` → "AI Behavior" → **Model Fallback** → `ModelFallbackEditorView` — a reorderable (`.onMove`)/deletable (`.onDelete`) list of `AppSettings.modelFallbackOrder` + an "Add a Model" section. `EditButton` is scoped to this sub-screen (NOT the main Settings list). Stored under `@AppStorage("modelFallbackOrderJSON")` (`[String]`, order-preserving + de-duped); backup-covered (`AppSettingsSnapshot.modelFallbackOrder`).
- **Card attribution:** `ChatMessage.aiModelUsed: String?` (new optional field → lightweight migration) is set from `aiManager.lastUsedModelLabel` at the nutrition call sites; `MessageBubble.nutritionCard` shows a "✨ Generated by <model>" footnote (only when present, so old cards are unaffected — "going forward").

### Explicitly NOT Allowed
- **Don't route AI calls on `GeminiModel`/`selectedModel`** — use `requestModel` (the chain-aware effective model) in request helpers; `selectedModelOption` is the chip/primary. The `GeminiModel` enum stays only for legacy-pref decoding.
- **Don't hardcode provider keys in source.** Read from `apiKey(for:)` (Info.plist). Don't commit real keys (Secrets.xcconfig is gitignored).
- **Don't fork the OpenRouter and GLM clients** — they're the same OpenAI-compatible path; differences are data (baseURL/key/model), not code.
