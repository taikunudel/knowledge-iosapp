---
type: guide
id: design-system/wwdc2026/modernize-uikit-app
title: "Modernize Your UIKit App (WWDC26)"
description: "Modernizing UIKit for iOS 27: mandatory scene lifecycle, app adaptivity/resizing, tab-bar/sidebar and navigation-bar APIs, Liquid Glass scroll-edge visuals, and Apple Intelligence menus."
status: stable
tags: [design, uikit, liquid-glass, adaptivity, wwdc2026, ios]
created: 2026-06-23T00:00:00Z
updated: 2026-06-23T00:00:00Z
resource: "https://developer.apple.com/videos/play/wwdc2026/278/"
sources:
  - "https://developer.apple.com/videos/play/wwdc2026/278/"
---

# Modernize Your UIKit App (WWDC26)

> **Canonical source (richer than this page — watch it):**
> [Modernize your UIKit app — WWDC26](https://developer.apple.com/videos/play/wwdc2026/278/).
> Nutritionist is SwiftUI-first, so this is mostly **reference** — but it matters for our
> UIKit touch-points (e.g. the UIKit pan in `CalendarView`) and the shared bar visuals.

## App adaptivity & resizing (iOS 27)
- iPhone apps are now resizable in iPhone Mirroring (macOS 27) and on iPad.
- **UIScene lifecycle is mandatory** — an app without it won't launch. Migrate `UIApplicationDelegate` → `UISceneDelegate`.
- Replace `UIScreen.main` → `window.windowScene.screen`; read `displayScale` from `traitCollection`; use `windowScene.effectiveGeometry` for bounds.
- Prefer **size classes** over idiom/orientation checks (an iPhone app on iPad stays "phone" idiom but is fully resizable).

## Tab bars & sidebars (iOS 27)
- `tabBarController.sidebar.preferredPlacement = .sidebar` (opt into sidebar on iPhone).
- `prominentTabIdentifier` — a tab that stays visible while the bar collapses on scroll.

## Navigation bars (iOS 27)
- `navigationItem.barMinimizationBehavior` (`.always` / `.never`).
- `.automatic` scroll-edge style now has **Liquid Glass** visuals — re-evaluate any `.soft` overrides.

## Menus & Apple Intelligence
- Menus auto-show an "Ask Siri" button when relevant; `preferredImageVisibility = .visible` keeps menu icons visible under Liquid Glass.

## Tooling
- Xcode 27 Device Hub resizes the simulator freely; previews have a resize mode; an agentic "modernization" skill automates `UIScreen.main`→scene and orientation→size-class rewrites.

## Relevance to Nutritionist
- If we keep/extend any UIKit-backed views, the scene-lifecycle and trait guidance applies; the nav-bar Liquid Glass scroll-edge note is relevant to how our toolbars read when content scrolls under them.

Chapters: ~16 segments, 0:00–15:32.
