---
type: decision
id: "navigation/ai-chat-overlay-retired"
title: "v4 · AI Chat Overlay — Native Sheet With Detents (RETIRED 2026-06-20)"
description: "The AI chat sheet overlay was retired on 2026-06-20 when the chat window was removed entirely in favor of a floating food card; this page is kept as history."
status: stable
tags: [navigation, ai-chat, retired, superseded, sheet, ios26, era-v4]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# AI Chat Overlay — Native Sheet With Detents (iOS 26 Liquid Glass), Not a Separate Screen

*Established: 2026-06-05 (blurred overlay); **2026-06-09 updated**; **🔁 RETIRED 2026-06-20** — see "2026-06-20 — Food Card Capture (No Chat Window)" above.*

> **⚠️ 2026-06-20 — THIS WHOLE SECTION IS SUPERSEDED.** The user removed the AI chat window entirely (*"i do not want the ai chat window"*). Sending a food now blurs the screen + shows ONE floating `CapturedFoodCard` (no conversation, no `.sheet`, no `AIChatView` presented). The `.sheet(isPresented: $isChatPresented)`, `isChatPresented` state, and the `.switchToChat*` posts are removed; `AIChatView` is dead-but-compiled. **Don't reintroduce a chat sheet/screen.** The details below are kept only as history of the retired design.

AI Chat is **not** a drawer destination. User verbatim: *"i actually do not need a seperate ai chat screen, just when i tab the chat bar, show the model selector."*
User verbatim (2026-06-09): *"remove the ai chat title on the ai chat screen, and also, do not make it full screen, it can be just partially occupy the screen."*
User verbatim (2026-06-09 follow-up): *"the ai chat windows should be above whatever in the current screen not just blanket and weird."*

### Implementation
- `ContentView` holds `@State isChatPresented: Bool`. When true, a native `.sheet(isPresented:)` presents `AIChatView(showCloseButton: true, onClose: …)` with `.presentationDetents([.fraction(0.85)])` (≈ 85 % screen height), `.presentationDragIndicator(.visible)`, `.presentationCornerRadius(28)`, and `.interactiveDismissDisabled(false)`. This gives a proper iOS-native partial sheet that floats above the current screen content, with system-provided dimming, keyboard handling, and swipe-to-dismiss.
- **No title.** The `AIChatView` navigation title is empty (`.navigationTitle("")`) with `.navigationBarTitleDisplayMode(.inline)` — the chat screen shows no "AI Chat" header.
- `TodayView` receives `@Binding isChatPresented` and passes it to `SharedInputBar(onPresentChat:)`. Tapping the chat bar's send button, adding an image, or tapping "add to meal" on an empty section all set `isChatPresented = true` with a spring animation instead of navigating to tab 2.
- `AIChatView` gains `showCloseButton` and `onClose` params — when in overlay mode, a leading `xmark.circle.fill` toolbar button dismisses. The model selector, message list, input bar, and retry button all work identically.
- `SharedInputBar` no longer sets `selectedTab = 2`. Its `sendFromHome()` calls `onPresentChat?()` + posts `.switchToChatFocused` with the message text. `onImageReady` calls `onPresentChat?()` + posts `.switchToChatWithImage`.

### Explicitly NOT Allowed
- **Don't re-add AI Chat as a drawer destination** (`selectedTab == 2` is dead). The conversation is the overlay only.
- **Don't navigate via `selectedTab = 2`** from anywhere in the app — use `isChatPresented = true` instead.
- **Don't make the chat overlay full screen.** It's a native `.sheet` with `.presentationDetents([.fraction(0.85)])` — it occupies ≈ 85 % of the screen height. Don't revert to full-screen or a manual GeometryReader overlay.
- **Don't add a title ("AI Chat") to the chat overlay.** The navigation title is empty (`.navigationTitle("")`, `.inline` display mode). The model selector, close button, and new-chat button in the toolbar are sufficient navigation chrome.
- **Don't replace the native `.sheet` with a manual `ZStack`/`GeometryReader` overlay.** The native sheet gives proper dimming, keyboard handling, swipe-to-dismiss, and accessibility for free. Manual overlays look "blanket and weird" (user verbatim 2026-06-09).
