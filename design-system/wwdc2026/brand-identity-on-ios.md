---
type: guide
id: design-system/wwdc2026/brand-identity-on-ios
title: "Communicate Your Brand Identity on iOS (WWDC26)"
description: "Express brand identity on iOS under Liquid Glass: the UI-layer vs content-layer model, and color/typography/iconography/logo guidance that keeps the native feel."
status: stable
tags: [design, branding, liquid-glass, typography, color, wwdc2026, ios]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
resource: "https://developer.apple.com/videos/play/wwdc2026/251/"
sources:
  - "https://developer.apple.com/videos/play/wwdc2026/251/"
  - "https://developer.apple.com/design/human-interface-guidelines"
---

# Communicate Your Brand Identity on iOS (WWDC26)

> **Canonical source (richer than this page — watch it):**
> [Communicate your brand identity on iOS — WWDC26](https://developer.apple.com/videos/play/wwdc2026/251/).
> This page is a distilled index; the talk has the full app walkthroughs (Crumbl, Moonlitt, NYT Cooking, Gentler Streak, Slack).

WWDC26 session by Sarah (Apple Design Evangelist). Thesis: **express a distinct brand
without compromising the native iOS feel.**

## The two-layer model (Liquid Glass, iOS 26+)
Think of an app as two layers:
- **UI layer** — global navigation/actions (tab bars, top toolbars). Use **standard, familiar components**; it floats above content for easy access.
- **Content layer** — the features, imagery, video, information that make the app unique. **This is the best place to express brand identity**; it sits beneath the UI controls.

## Guidance by element
- **Components** — Lean into platform familiarity for navigation/standard UI; reserve custom components for **high-impact** content areas. Custom components for purely utilitarian purposes make apps feel dated. (Moonlitt's lunar calendar is custom but backed by Liquid Glass + native patterns.)
- **Content** — Use full-bleed imagery, video, words, animation as the canvas, with clear purpose. Apply voice/tone to evoke emotion; use transitions thoughtfully (NYT Cooking uses SwiftUI Zoom Transitions to connect tap targets to state).
- **Color** — Move solid background color **out of UI elements and into the content area** so Liquid Glass controls read cleanly above. Use color **sparingly, with intention**: hierarchy/grouping, interaction feedback, status (accent/tint on actions, badges, selected states). Slack tints only primary actions, new-info sections, and badges. **Support Dark Mode.** Extend branding into Widgets with a consistent palette.
- **Typography** — Custom typefaces can be expressive (Crumbl Sans for headers) **but must support Dynamic Type** (built into system fonts; test custom fonts; wrap, don't truncate). System options: **SF Pro** (default), **SF Compact** (small sizes), **SF Mono** (code/data), **SF Rounded** (warmth, still native), **New York** (serif). Gentler Streak gets variety from system fonts + mixed widths/variants.
- **Iconography** — Custom icons work in tab bars, toolbars, inline content, but keep conventions (a Share icon should follow the platform pattern). Icons: recognizable, consistent, scalable at small sizes, not over-detailed. **Alternative: SF Symbols** (7,000+, font-scaled, neutral, multiple weights, accessible, built into Xcode — no export).
- **Logos** — Use **sparingly** (people know which app they're in). Best: show on the home tab and fade on scroll (NYT Cooking); keep it refined and unobtrusive.

> Guiding principle: *"Be mindful of where [brand] oversteps with system behavior or
> confuses familiar conventions. Continue to exercise your creativity while honoring that
> iOS is a platform with established interactions."*

## Why it matters for Nutritionist
This is the design rationale behind several locked project rules: the **MUJI accent
palette + fixed `MacroPalette`** identity (content-layer color, used sparingly), keeping
navigation/composer on standard `LiquidGlass*` chrome (UI layer), and SF Symbols for
glyphs. When adding brand flourish, put it in the content layer, not the nav/composer.

## Applied in Nutritionist (2026-06-22)
**Typography → Dynamic Type (first pass).** The food log now scales with the user's text
size: `PlainDesignFoodRow` food name → `.body` (wraps to 2 lines, no truncation) and meta →
`.caption`; `plainMealSection` headers → `.subheadline`
([CalendarView.swift](Nutritionist/Views/CalendarView.swift)). `CapturedFoodCard` already
used semantic styles. Verified at the largest accessibility text size. **NOT yet converted**
(a fuller sweep remains): the globe/trend `Canvas` numerals (geometric, fixed by design) and
assorted `.system(size:)` chrome.
