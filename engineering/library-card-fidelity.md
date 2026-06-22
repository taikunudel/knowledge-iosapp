---
type: rule
id: "engineering/library-card-fidelity"
title: "Library Card Visual Fidelity"
description: "LibraryFoodCardPreview must mirror the chat nutrition card's full visual hierarchy and never drift back into a flat list-row presentation."
status: stable
tags: [engineering, library, food-card, ui, liquid-glass]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Library Card Visual Fidelity

*Established: 2026-05-26 (Codex adversarial review fix)*

`LibraryFoodCardPreview` in [Nutritionist/ContentView.swift](Nutritionist/ContentView.swift) now mirrors the chat nutrition card's visual hierarchy more faithfully — image strip, food name, large flame/calories + heart/health-score pair, **macro breakdown** (Carbs / Protein / Fat / Fiber), **AI reasoning text** (up to 4 lines), saved-date footnote — all inside a `LiquidGlassRoundedModifier` surface.

When extending: add new sections (e.g. vitamins) to **both** this preview and the chat card, or extract the shared content into a reusable subview. **Don't let the library preview drift back into a flat list-row presentation.**
