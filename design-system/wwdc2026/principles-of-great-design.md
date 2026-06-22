---
type: guide
id: design-system/wwdc2026/principles-of-great-design
title: "Principles of Great Design (WWDC26)"
description: "Apple's eight foundational design principles for Apple-platform UI: purpose, agency, responsibility, familiarity, flexibility, simplicity, craft, delight."
status: stable
tags: [design, principles, hig, wwdc2026, ios]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
resource: "https://developer.apple.com/videos/play/wwdc2026/250/"
sources:
  - "https://developer.apple.com/videos/play/wwdc2026/250/"
  - "https://developer.apple.com/design/human-interface-guidelines/design-principles"
---

# Principles of Great Design (WWDC26)

> **Canonical source (richer than this page — watch it):**
> [Principles of great design — WWDC26](https://developer.apple.com/videos/play/wwdc2026/250/)
> · HIG: [Design Principles](https://developer.apple.com/design/human-interface-guidelines/design-principles).
> This page is a distilled index of the talk; the video carries the full examples and nuance.

WWDC26 session by Linda & Doug (Apple Design Evangelists). Core definition:
*"Design is making something with intention. It's focusing on what's most important to
people, so you can build something they will truly value."* There is no formula —
leaning into one principle can mean compromising another; use judgment.

## The eight principles

1. **Purpose** (1:08) — Serve people and respect their lives. Every feature asks for time, attention, and trust; choose what *not* to build as carefully as what you do. Before coding, ask "does this have real purpose?"
2. **Agency** (1:52) — Put people in control; let them explore at their own pace, no predetermined paths. **Build in forgiveness:** easy undo, confirmation before destructive actions, interruptions only for major mistakes. Recoverability makes people confident to explore.
3. **Responsibility** (3:38) — Act in people's best interest; **privacy is a human right** — request personal data only at the right moment, only what's necessary, transparently. **Anticipate harm**, especially with AI (e.g. a recipe app must guard against suggesting allergens — previews, confirmations, disclaimers; remove a feature if risk outweighs value).
4. **Familiarity** (6:04) — Build on what people already know. Use metaphors that are neither too literal nor too abstract; follow established conventions; **"things that look the same should behave the same"** (consistent placement + behavior across screens/devices).
5. **Flexibility** (8:52) — People use your design in unique ways across contexts. Design to each platform's strengths (iPhone: quick touch; Mac: deep workflows + precise pointer). Consider the audience's range (age, language, abilities, expertise); allow personalization when no single solution fits; build accessible experiences.
6. **Simplicity** (11:13) — Strip the unnecessary so the core purpose shines. **Simplicity ≠ minimalism** (burying functionality isn't simple). Be **concise** (plain language, fewer steps) and **clear** (visual hierarchy via order/spacing/contrast; the most important item obvious). Every element earns its place; sometimes *adding* context makes an interface simpler.
7. **Craft** (13:42) — Uncompromising attention to detail builds trust. Quality materials: typography, color, clear icons, responsive animation, reliable SDKs. Requires iteration and longevity (keep evolving as platforms change).
8. **Delight** (15:47) — The natural result of getting the others right — not confetti or gratuitous flourish. Identify the **emotion** you want people to feel and reinforce it throughout.

## Why it matters for Nutritionist
Maps directly onto existing project rules: forgiveness (do/catch + rollback saves),
familiarity/consistency (native iOS 26/27 idioms, `LiquidGlass*` modifiers), simplicity
(the "clear design", removed knobs), and craft (fixed `MacroPalette` identity, gesture
polish). Use this as the yardstick when judging a new UI surface.

## Applied in Nutritionist (2026-06-22)
**Responsibility** — `CapturedFoodCard` ([ContentView.swift](Nutritionist/ContentView.swift))
now shows an "✨ AI estimate. Set the portion to match what you actually ate." disclaimer
under the portion stepper, so an AI-guessed calorie/macro number isn't mistaken for a
measurement (anticipate harm, add disclaimers).
