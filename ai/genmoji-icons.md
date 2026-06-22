---
type: rule
id: "ai/genmoji-icons"
title: Genmoji Food Icons — ImagePlayground Regeneration
description: Food icons are regenerated via the Image Playground sheet because headless ImageCreator is deprecated and runtime-dead on iOS 27.
status: stable
tags: [ai, icons, imageplayground, ios27]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Genmoji Food Icons — ImagePlayground Regeneration
*Established: 2026-06-09 (user request + research); implemented 2026-06-11.*

User verbatim: *"search online is there an api to use genmoji to generate the food emoji? if so, add a button to use genmoji to regenrate the food icon."* Research finding: **there is no public "true Genmoji" API** (`NSAdaptiveImageGlyph` is render/storage-only); the supported path is **ImagePlayground's `ImageCreator`** (iOS 18.4+, requires Apple Intelligence hardware/enablement).

### 2026-06-17 — REWRITTEN to the Image Playground SHEET (headless `ImageCreator` is DEAD on iOS 27)
**Root cause of "regenerate doesn't work":** Taikun's iPhone runs **iOS 27**, where Apple **discontinued `ImageCreator`** — they moved Image Playground's image models to **Private Cloud Compute** with system-managed limits, so **headless/programmatic on-device generation NO LONGER EXISTS** ([Apple deprecation news](https://developer.apple.com/news/?id=dz9wvq0r), WWDC26 session 375). His phone DOES have Apple Intelligence (the Foundation Models *text* model works — the composer shows "Apple Intelligence"), but `ImageCreator()` throws `.notSupported` on iOS 27. The text-model availability and the (now-removed) image API are independent.
- **The only supported path now is the UI sheet** — SwiftUI **`.imagePlaygroundSheet(isPresented:concepts:onCompletion:)`** (iOS 18.1+, works on BOTH iOS 26 and 27). `onCompletion` hands back a file `URL`.
- **UI:** `PlainDesignFoodRow`'s ••• "Regenerate Icon" (`wand.and.stars`, gated `#if canImport(ImagePlayground)` + `if #available(iOS 18.1, *)`) sets `showingImagePlaygroundSheet = true`. The row carries the **`ImagePlaygroundIconSheet` ViewModifier** (a `concepts: [.text("a cute, simple icon of <name>, single centered object, plain background")]` sheet). `onCompletion` → `applyGeneratedIcon(from: URL)`: `UIImage(contentsOfFile:)` → 256² JPEG (0.85) → `entry.aiGeneratedImageData` (do/catch + rollback; row re-renders via `resolvedCardImageData` + `@Query`).
- **Silent auto-generation is GONE** (the old `autoGenerateIconIfNeeded` / `autoIconAttempts` / headless `ImageCreator` are all removed) — it required the now-removed headless API, and you can't silently present a sheet. Emoji-less entries show the 🍽️ fallback until the user taps Regenerate. The whole `ImageCreator` block + `GenmojiIconError` + `genmojiErrorMessage` were deleted (would stop compiling on the iOS 27 SDK anyway).
- **Don't reintroduce `ImageCreator`** — it's deprecated and runtime-dead on iOS 27. Use the sheet. Don't fake icons with a remote image API.
