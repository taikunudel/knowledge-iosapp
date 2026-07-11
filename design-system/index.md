# Design System

Design, UI, and visual-language rules for the Nutritionist app.

## Subfolders
* [wwdc2026/](wwdc2026/) - distilled iOS-design guidance from WWDC 2026 (iOS 27), each page linking its canonical Apple source

## Documents

* [Caffeine v5 — the simplism design era (supersedes liquid glass)](caffeine-v5.md) - The 2026-07-10 pivot: v4.0 archives the liquid-glass app; v5 reimplements it against the Caffeine handoff — olive/paper palette, one #FF4A1C accent, bundled fonts, flat tab bar, anti-glass rules, phase-1 decisions and open items.
* [Exits & Dismissal — every panel has a clear way out](exits.md) - The exit rule (no surface may trap the user; every exit states what happens to your input), the per-surface exit table for v5, and the two analysis-panel traps found and fixed on 2026-07-10.
* [Motion & Transitions — single source of truth](motion.md) - Every animation/transition rule in one editable place: Caffeine motion canon, curve/duration tokens ↔ Swift symbols, the live v5 inventory, locked rules & rejections, and the archived v4 motion specs.
* [v4 · Always Refer to the iOS 26 Design Guide](ios26-design-guide.md) - Consult Apple's iOS 26 / liquid-glass guidance for any UI surface, target the iOS 27 runtime, and use the project's native-glass modifiers without manual borders.
* [Settings Revamp 2026-06-11 — Fewer Knobs, Q&A Calorie Goal](settings-revamp.md) - Settings removed four styling sections and replaced the raw calorie-goal picker with a research-backed interactive Q&A wizard.
* [Rejected Design Experiments](rejected-experiments.md) - Retired designs the user rejected — record rejections here so they are not re-implemented, including the problematic folding-paper effect on TodayView.
* [v4 · Accent Palette — MUJI Natural Tones](accent-palette.md) - The MUJI-inspired natural accent palette, named color tokens, and the semantic status traffic-light that replace raw green/orange/red.
