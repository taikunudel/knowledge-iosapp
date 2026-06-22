---
type: rule
id: "food-entry/composer-attach-tray"
title: "Chat Bar (Composer) — Attach-Tray Layout (v6)"
description: "The chat input bar is a single pill whose + opens a glass AttachTray (recent photos + Camera/Photos/Scan/Library), with an accent paperplane send and no voice button."
status: stable
tags: [food-entry, composer, chat-bar, attach-tray, photokit, liquid-glass]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Chat Bar (Composer) — Attach-Tray Layout (v6)

*Established: 2026-05-20; v5 (2026-05-26 design-kit); **v6 supersedes v5 on 2026-06-04** per the dotted-globe design-system redesign ("follow the demos").*

The chat input bar is `UnifiedChatInputBar` in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift) (`SharedInputBar` is a thin wrapper around it for the Home tab).

> **2026-06-04 supersession (v6).** The composer `+` now opens a glass **AttachTray** *above* the pill (recent-photo rail + **Camera / Photos / Scan Nutrition Label / From Library**), and the **`+` rotates 45° into a × and fills with the accent color** while open. The **separate inline camera button is removed** — camera is now a row *inside* the tray. The pill therefore carries only the `+` (leading) and the accent paperplane **send** (trailing). This **reverses v5's "separate inline camera button" and "`+` opens a Menu" rules.** Retained: single bar, never expands, **placeholder stays `"Add your meal"`** (the demo's "Ask the AI or describe a meal…" was **NOT** adopted — user chose "keep locked text"), bar stays visible, no voice button, "From Library" still reachable from `+`.

### Layout — Single Bar, `+` (leading) + Send (trailing)

The composer is **a single rounded pill** (`LiquidGlassRoundedModifier`), **58 pt, never expands** (`isExpandedComposer` hard-coded `false`). The whole composer is a `VStack { if showingAttachTray { attachTray } ; composerPill }` so the tray stacks directly above the pill.

From inside the pill:

1. **`+` button** — `.bottomLeading`, 40 × 40 pt, `plus` glyph on a grey fill circle (`Color(.systemGray).opacity(0.18)`). **Toggles `showingAttachTray`**; rotates 45° → × and fills with `themeAccentColor` (white glyph) while open. Disabled when `isProcessing`.
2. **Text area** — placeholder `"Add your meal"` (no ellipsis). Leading padding clears the `+`; trailing padding clears the send button.
3. **Send button** — `.bottomTrailing`, 40 × 40 pt **accent-filled circle** with a white `paperplane.fill`, soft accent shadow (`themeAccentColor.opacity(0.33)`). Disabled tint `Color.secondary.opacity(0.45)`.

### AttachTray

`UnifiedChatInputBar.attachTray` — a `LiquidGlassRoundedModifier` panel (cornerRadius 22) above the pill:

- **"Add a photo"** header + × close button.
- **"RECENT"** horizontal rail of the user's **real recent photos** (PhotoKit). User verbatim (2026-06-04): *"the tray should really show the recent photos instead of place holders"* — this **reverses** the earlier gradient-swatch placeholder decision. Implemented by **`RecentPhotosProvider`** (an `@Observable`/`ObservableObject` in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift)): `loadIfNeeded()` runs on tray `.onAppear` — if photo access is **authorized/limited** it fetches the 12 newest `PHAsset` images and loads thumbnails (`PHImageManager`, `targetSize 180²`, opportunistic); if **notDetermined** it auto-requests on first open; if **denied/restricted** the rail shows a single **"Allow Photos"** tile that deep-links to Settings. Tapping a thumbnail loads full-res data (`requestImageDataAndOrientation`) → `transformImageData` → `onImageReady` (same path as the picker). Requires `NSPhotoLibraryUsageDescription` (added to Info.plist) + `import Photos`. **Don't revert to gradient placeholders.**
- Four `attachOptionRow`s:
  - **Camera** (brick chip) → `showingCamera`
  - **Photos** (neutral chip) → `showingPhotoPicker`
  - **Scan Nutrition Label** (moss chip) → `showingCamera` (snap the facts panel; AI vision reads it — there is **no separate scan backend**)
  - **From Library** (accent chip) → `showingLibraryPicker` — **preserves the locked "From Library" feature** that the demo's 3-option tray omitted
### Floating Bar + Idle Width (2026-06-11)

- **The bar FLOATS over the content** — it is an `.overlay(alignment: .bottom)` on TodayView, **never a `.safeAreaInset`**. User verbatim: *"do not trucate the food logs or any content at the bottom, the chat bar is a liquid glass bar it is supposed to float above the content."* The food log keeps the full screen height and slides UNDER the translucent glass; scroll clearance comes from `homeEntriesCardSmallBottomSpacing/LargeBottomSpacing` (90/96 pt — sized so the last row clears the bar). Don't revert to `safeAreaInset` (it shrinks the content area = the rejected truncation) and don't drop the clearance.
- **Idle bar is SHORT and right-aligned.** User verbatim: *"make the chatbar in the idel status shorter, no need to be from left to right… the shorter chatbar aligned to the right."* `UnifiedChatInputBar.isIdleComposer` (unfocused + empty draft + no mention + tray closed) caps the pill at `idleComposerWidth = 264` and aligns it `.trailing`; focusing/typing animates it back to full width. **Height and corner radius still never change** — the earlier "never expands" lock now applies to shape, not width (the user directed the width behavior).

- `selectAttach { … }` dismisses the tray, then runs the action. Tapping `+` also dismisses the keyboard.
- DEBUG-only `-UITestAttachTray` launch arg opens the tray on launch for screenshot verification (inert in Release).
- **The bar stays visible while the tray is open / a picker is driven.** User verbatim (2026-05-20): "when use the add button, the chat bar should stay, now it desappear."

### Explicitly NOT Allowed

- **No voice / microphone / waveform input button.** Still forbidden.
- **No external `+` outside the pill; no second composer variant; no inline quick-action chips/sliders.** Single-bar only; suggestions go *above* the bar.
- **Composer now GROWS taller with the text** (user 2026-06-17: *"when the text is too much you should make the input bar higher instead of just ignoring"*). **Supersedes the locked "never expands height / `isExpandedComposer = false`" rule.** `InlineMentionTextView` always wraps (`maximumNumberOfLines = 0`) and reports its `sizeThatFits` height via `onHeightChange`; `UnifiedChatInputBar.composerHeight` = text height (clamped 1…`maxExpandedLines` lines) + chrome, so the pill is 58 pt for one line and grows up to ~6 lines, then the text scrolls internally. `+`/send stay bottom-pinned; corner becomes a 22 pt rounded-rect while tall; growth is spring-animated. The earlier *width* idle-shrink still applies (legacy mode). DEBUG `-UITestLongDraft` pre-fills a long draft to screenshot the grown state.
- **Placeholder is now `"What's your meal"`** (changed 2026-06-16 — user: *"the text inside is what's your meal"*). The earlier lock (*"dont say describe your meal. just say add your meal,"* 2026-05-20; kept 2026-06-04) is **SUPERSEDED** — see "2026-06-16 Design Handoff Revamp." Don't revert to "Add your meal" without a new instruction.
- **Don't remove "From Library" from the tray** (4th canonical action).
- **Don't re-add a separate inline camera button to the pill** — camera lives in the tray now.

### Rationale / history

1. **v1–v3** — buttons outside the pill → `+` inside the pill, single bar.
2. **v4 (2026-05-20)** — bar never expands; send = flat borderless arrow; placeholder "Add your meal".
3. **v5 (2026-05-26)** — design-kit: separate camera button + accent paperplane send; `+` opens a 3-item Menu.
4. **v6 (2026-06-04, current)** — dotted-globe redesign: `+` opens the **AttachTray** (`+`→×, accent fill); inline camera removed (now a tray row); **Scan Nutrition Label** added; **From Library** preserved in the tray; send unchanged (accent paperplane). Placeholder kept "Add your meal". User direction: "follow the demos" + "All, but keep locked text".
