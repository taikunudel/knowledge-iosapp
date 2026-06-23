---
type: guide
id: design-system/wwdc2026/whats-new-in-swiftui
title: "What's New in SwiftUI (WWDC26)"
description: "New SwiftUI APIs for the iOS 27 releases: automatic Liquid Glass, toolbar control, reorderable containers, swipe actions on any view, AsyncImage caching, the @State macro, and @ContentBuilder."
status: stable
tags: [design, swiftui, liquid-glass, wwdc2026, ios]
created: 2026-06-23T00:00:00Z
updated: 2026-06-23T00:00:00Z
resource: "https://developer.apple.com/videos/play/wwdc2026/269/"
sources:
  - "https://developer.apple.com/videos/play/wwdc2026/269/"
---

# What's New in SwiftUI (WWDC26)

> **Canonical source (richer than this page — watch it):**
> [What's new in SwiftUI — WWDC26](https://developer.apple.com/videos/play/wwdc2026/269/).
> Distilled index; the session has the full code samples.

## Liquid Glass, automatically
- Apps pick up the refreshed Liquid Glass look on the new releases with **no code changes** (just recompile in Xcode 27).
- `appearsActive` environment value — style conditionally when the window is inactive.
- `labelStyle(.titleAndIcon)` — show icons in menus (this is what the food-card AI-estimate cue uses).

## Toolbars
- `visibilityPriority(.high)` — keep important toolbar items visible when space is tight.
- `ToolbarOverflowMenu` — group items that should always collapse into the overflow menu.
- `.topBarPinnedTrailing` placement — pin an item to an always-visible trailing slot.
- `toolbarMinimizeBehavior(.onScrollDown, for: .navigationBar)` — auto-hide the nav bar on scroll.

## Interaction
- `.reorderable()` on `ForEach` + `.reorderContainer(for:)` — drag-to-reorder in `List`/`LazyVGrid` (now on watchOS too).
- `.swipeActions()` works on **any view**, not just `List` rows; coordinate with `.swipeActionsContainer()`.
- Item-binding presentation: `confirmationDialog(item:)` / `alert(item:)` instead of `isPresented:`.

## Data flow & performance
- `AsyncImage` now honors standard HTTP caching; custom `URLRequest` + `asyncImageURLSession()`.
- `@State` is now a **macro** giving lazy init of `@Observable` objects (back-ported to iOS 17+). ⚠️ Source-breaking: drop the default value when you assign the object in `init`.
- `@ContentBuilder` — a unified builder that removes the exponential type-check blow-up of deeply nested views.

## Layout
- iPhone apps become **resizable** on iOS 27; design for a range of sizes; Xcode 27 live previews get resize handles.

## Relevance to Nutritionist
- `@ContentBuilder` directly targets the "unable to type-check in reasonable time" failures we worked around by extracting `homeFoodLogPager` — worth trying if the body grows again.
- `.swipeActions()` on any view + `.swipeActionsContainer()` could replace parts of our hand-rolled food-row swipe.
- `labelStyle(.titleAndIcon)` is already in use for the AI-estimate cue.

Chapters: 0:00 Intro · 2:12 Refreshed look (Liquid Glass, toolbar) · 8:06 Document-based apps · 15:18 Presentation & interaction · 19:58 Data flow & performance · 27:25 Next steps.
