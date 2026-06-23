---
type: guide
id: design-system/wwdc2026/liquid-glass
title: "Liquid Glass — the design system (iOS 26 → second iteration in iOS 27)"
description: "What Liquid Glass is, how to adopt it, its HIG design principles, and the WWDC26 second-iteration refinements (personalization slider, accessibility adaptation, sidebar/toolbar/icon changes, removal of the old-design opt-out)."
status: stable
tags: [design, liquid-glass, materials, wwdc2026, ios, foundation]
created: 2026-06-23T00:00:00Z
updated: 2026-06-23T00:00:00Z
resource: "https://developer.apple.com/documentation/technologyoverviews/liquid-glass"
sources:
  - "https://developer.apple.com/documentation/technologyoverviews/liquid-glass"
  - "https://developer.apple.com/videos/play/wwdc2026/102/"
---

# Liquid Glass — the design system

> **Canonical sources (richer than this page):**
> [Liquid Glass — Technology Overviews](https://developer.apple.com/documentation/technologyoverviews/liquid-glass)
> (with its deep dives "Adopting Liquid Glass" and the Landmarks sample) ·
> [Platforms State of the Union — WWDC26](https://developer.apple.com/videos/play/wwdc2026/102/) ·
> WWDC25 "Meet Liquid Glass". Open these for the authoritative, current detail.

## What it is
A dynamic material combining the optical properties of glass with a sense of fluidity. It
exists to establish hierarchy, create harmony, and keep consistency across devices. Standard
SwiftUI / UIKit / AppKit controls and navigation adopt it **automatically**; you can also
apply it to custom interface elements.

## Adopting it (overview)
Don't rebuild from scratch: build in the latest Xcode to see the changes, then follow best
practices — embrace the refresh for materials/controls/app icons; provide a universal
navigation + search experience; keep organization/layout consistent with the system; adopt
best practices for windows, modals, menus, toolbars; test across platforms. Sample: the
**Landmarks** app (Icon Composer app icon, background extension effect for edge-to-edge
content, scroll views extending under a sidebar/inspector, adaptable window sizes, search
conventions, Liquid Glass on custom elements).

## Design principles (from the HIG)
- Choose a layout + navigation structure that puts the most important content in focus.
- Reimagine the app icon as simple, bold layers with dimensionality and consistency.
- Be **judicious with color** in controls/navigation so they stay legible and let content shine through.
- Make elements fit the software + hardware design across devices.
- Adopt standard iconography and predictable action placement.

## Second iteration (WWDC26, iOS 27)
- Better **diffusion** of complex content behind the glass; a darkened edge plus brighter specular highlights for depth.
- New **user personalization slider**: ultra-clear → fully tinted.
- Adapts to accessibility settings (reduce transparency, increase contrast).
- macOS 27 gains the "show borders" environment value and a tighter, consistent window corner radius.
- **Sidebars** expand to the edges (Mac/iPad), refracting app content + wallpaper; sidebar icons regain color via the app's **accent color** (List/Label APIs do this automatically, with per-item tint).
- **Floating bars**: as content scrolls under, a uniform toolbar appears across the top to keep text legible.
- ⚠️ The opt-out for the **old design is being removed** — recompiling with Xcode 27 auto-adopts the new Liquid Glass design.

## Icon Composer
Design icons from multiple Liquid Glass layers; sharper rendering; optional refraction effects; preview how the icon looks on earlier releases.

## Relevance to Nutritionist
This is the foundation under our `LiquidGlass*` modifiers and the "clear design" direction.
The personalization slider + accessibility adaptation reinforce our no-manual-blur stance
(the system owns translucency now). "Be judicious with color in controls; let content shine
through" is the rationale for the MUJI-accent-used-sparingly rule. Because recompiling on
Xcode 27 auto-adopts the second iteration, **re-verify our custom glass surfaces** after the
next toolchain bump. See also [[whats-new-in-swiftui]] and [[brand-identity-on-ios]].
