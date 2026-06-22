---
type: rule
id: "engineering/pinned-chip-surface"
title: "Pinned Chip Surface — LiquidGlassCapsuleModifier"
description: "The pinned-nutrient chip must use LiquidGlassCapsuleModifier, not hand-rolled Capsule().fill().stroke() chrome."
status: stable
tags: [engineering, liquid-glass, ui, today, pinned-nutrients]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Pinned Chip Surface — `LiquidGlassCapsuleModifier`

*Established: 2026-05-26 (Codex adversarial review fix)*

`LiquidGlassCapsuleModifier` was promoted from `private` to internal so views in sibling files can apply it. The pinned-nutrient chip in [Nutritionist/Views/TodayView.swift](Nutritionist/Views/TodayView.swift) now uses it instead of a hand-rolled `Capsule().fill(...).stroke(...)`, matching the iOS 26 design rule "Don't invent custom glass."

**Don't reintroduce ad-hoc `Capsule().fill().stroke()` chrome.** Use the modifier.
