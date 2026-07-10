---
type: rule
id: "design-system/motion"
title: "Motion & Transitions — single source of truth"
description: "The one page for every animation/transition rule: Caffeine motion canon (no bounce, decelerate, instant where movement adds nothing), the curve/duration tokens and their Swift symbols, the live v5 inventory, locked interaction rules and rejections, and the archived v4 motion specs."
status: stable
tags: [motion, animation, transition, easing, curves, reduce-motion, caffeine, design-tokens]
created: 2026-07-10T00:00:00Z
updated: 2026-07-10T00:00:00Z
---

# Motion & Transitions — single source of truth

*Created 2026-07-10 at the user's request: "add a dedicated knowledge for
animation and transition … merge them into a single one, so easy for me to
edit." Motion knowledge previously scattered across 16 pages is consolidated
here; the source pages remain as historical records and this page cites them.
Edit HERE first; the code tokens live in
`Nutritionist/Views/Caffeine/CaffeineDesign.swift`.*

## 1. Canon — Caffeine motion principles (v5, current)

From the Caffeine handoff (`design/caffeine-design-system/project/tokens/motion.css`
+ readme "VISUAL FOUNDATIONS → Motion"):

- **Honest, decelerating.** Objects move and settle like physical things —
  **no bounce, no overshoot, no spring.** A panel *rises*, a bar *fills*, a
  pressed surface *gives* (darken + 1 pt down-nudge).
- **Spatial provenance — "where it is from, where it is gone," for every
  element** (user rule, 2026-07-10). Every element that enters the screen
  must arrive FROM the place that caused it, and every element that leaves
  must exit TO a meaningful place (usually where it came from). A bare
  `.opacity` fade from nowhere is a violation; fades may only *accompany* a
  move. Per-element spec:
  - **Analysis panel** ← rises from the composer (bottom) that spawned it;
    exits back down.
  - **Food detail / day report** ← drill-in from the TRAILING edge (the row
    tap / the "VIEW DETAILED REPORT →" arrow points right); BACK exits to
    the trailing edge.
  - **Date picker** ← drops in from the TOP (its origin is the date switcher
    at the top); exits back up.
  - **Day change** ← directional page slide: navigating to an OLDER day, the
    content enters from the LEADING edge (you moved back); to a NEWER day,
    from the TRAILING edge. Arrows and swipes agree. (Supersedes the plain
    cross-fade the first v5 pass shipped.)
  - **Newly logged meal row** ← lands from the BOTTOM — it comes out of the
    collapsing analysis panel.
  - **Composer chips / LISTENING / notes** ← emerge from the composer's
    control row (bottom, small travel) and leave the same way.
  - **Checklist steps & fallback hops** ← print upward from the list's
    growth edge (bottom, subtle).
  - **Tab selection underline** ← SLIDES between items (it is the element
    that travels); tab CONTENT stays instant (locked, see §4).
  - Scope: v5 Caffeine surfaces. Legacy Trends/Library/Settings adopt this
    on their own redesign pass.
- **Short and purposeful.** Token durations 80–240 ms; the only long move is
  the analysis panel (550 ms) because it travels the whole screen.
- **Instant where movement adds nothing.** The tab switch swaps content with
  NO crossfade — only the accent underline "moves" (see the tab-ghosting fix,
  2026-07-10). Don't animate for decoration.
- **Reduce Motion: keep end states, drop the travel.** And remember the
  engineering rule ([[engineering/elegant-architecture]] F11): native
  components adapt automatically, **hand-rolled surfaces must check
  `accessibilityReduceMotion` manually** — every continuous/looping animation
  here must state its Reduce-Motion behavior.
- ⚠️ This canon **supersedes** the iOS-26 guide's "prefer `.snappy` /
  `.bouncy` / `.smooth` presets" advice ([[ios26-design-guide]], already
  `status: superseded`) — bouncy presets violate no-overshoot.

## 2. Tokens — curves & durations (edit these, not magic numbers)

CSS source (handoff) ↔ Swift (`CaffeineDesign.swift`, enum `Caffeine`):

| Token | Value | Swift symbol | Use |
|---|---|---|---|
| ease-standard | cubic-bezier(0.2, 0, 0, 1) · 180 ms | `Caffeine.ease` (0.18 s) | small state changes: status-bar scheme flip, bar fills, selection |
| panel grow | cubic-bezier(0.32, 0.72, 0, 1) · 550 ms | `Caffeine.panelCurve` | analysis panel rising (template `panelGrow`) |
| panel shrink | same curve · 500 ms | `Caffeine.panelCollapse` | panel dismissing (template `panelShrink`); logged row lands ~480 ms after |
| fade | ease-out · 300 ms | `Caffeine.fade` | day-change content fade, sub-screen enter/leave (template `fadeIn` 0.25–0.4 s) |
| pulse dot | 0.9 s loop | `CFPulseDot` (0.45 s autoreverse) | recording dot + active analysis step |
| press | instant | `CFPressStyle` / `CFAccentCircleStyle` / `CFBorderedCircleStyle` / `CFPillStyle` | darken fill + `offset(y: 1)` — never lighten, never glow, no scale |
| (CSS only, unused in Swift yet) | ease-out (0.16,1,0.3,1) · ease-in (0.4,0,1,1) · 80/120/240 ms | — | available if a new surface needs them; add a Swift constant when first used |

## 3. Live inventory — every animation/transition in the v5 app

All in `Nutritionist/Views/Caffeine/` unless noted:

- **Analysis panel enter/exit** — `CaffeineHomeView.expandedPanel`:
  `.transition(.asymmetric(insertion: .move(edge: .bottom), removal: .move + .opacity))`
  driven by `panelCurve`/`panelCollapse`. The logged meal row is inserted
  ~480 ms after collapse starts so it lands as the panel clears (template
  rhythm).
- **Analysis checklist** — step rows, model row, and fallback hops print in
  from the list's growth edge (`.move(edge: .bottom) + .opacity`,
  `Caffeine.fade`); the active step pulses (`CFPulseDot`).
- **Newly logged meal row** — lands from the BOTTOM (out of the collapsing
  panel): row `.transition(.move(edge: .bottom) + .opacity)`, insert wrapped
  in `withAnimation(Caffeine.fade)`.
- **Composer chips / LISTENING / notes** — emerge from and leave toward the
  control row below (`.move(edge: .bottom) + .opacity`, `Caffeine.ease` via
  `.animation(value:)` on the composer).
- **Tab underline** — SLIDES between items (`matchedGeometryEffect`,
  `Caffeine.ease`); the content switch stays instant via
  `.transaction { $0.animation = nil }` on the root content group.
- **Day change** (arrows, swipe, picker) — directional page slide per the
  provenance rule: day content (summary + meals, `.id(viewOffset)` +
  `dayTransition`) enters from the LEADING edge going older, TRAILING going
  newer; layers are `.clipped()` so slides stay inside their bands. The
  swipe commits at >40 pt horizontal translation (no finger-tracking pager
  in v5 — deliberate simplism; the v4 1:1 pager spec is archived in §5).
- **Sub-screens** — detail/report drill in from the TRAILING edge and exit
  back to it; the picker drops from the TOP and exits back up (each
  `.move(edge:) + .opacity`, `zIndex(1)` over home).
- **Bars** — `CFBar` animates width with `Caffeine.ease` when values change.
- **Press feedback** — all buttons: instant darken + 1 pt down-nudge
  (physical "the surface gives"); no animation curve on purpose.
- **Status bar scheme flip** — `statusBarOnOlive` with `Caffeine.ease` when
  the panel covers/reveals the top.
- **Keyboard** — layers squeeze (system timing); the summary layer `.clipped()`
  so compression never spills; meals ScrollView drag-dismisses
  (`scrollDismissesKeyboard(.interactively)`).
- **Tab switch** — `CaffeineTabBar`: **instant** content swap, no transition
  (locked; crossfade caused mid-swap ghosting).
- **Pulse dot Reduce Motion** — ✅ fixed 2026-07-10: `CFPulseDot` reads
  `accessibilityReduceMotion` and holds steady at full presence (keep end
  states, drop the travel).

## 4. Locked interaction rules & rejections (don't re-litigate)

- **Trends: a tapped bar EXTENDS into its graph in place** — user verbatim
  ([[trends/trends-graphs]]): *"do not open a new graph when tapping on one
  bar, the bar should extend into a graph, this animation makes more sense."*
  Any Trends redesign must keep expand-in-place, never present a new screen.
- **No folding-paper effect** — rejected with "problematic"
  ([[rejected-experiments]]); don't reintroduce page-fold/curl transitions.
- **No crossfade on tab switch** (2026-07-10, ghosting fix) — underline only.
- **No bounce/spring/overshoot anywhere in v5** (canon §1). Springs in the
  dormant v4 code are archive-only.
- **Continuous animation must gate on Reduce Motion** (engineering F11) —
  the v4 globes did this correctly; any new looping motion must too.
- **Chart teaching**: if a chart form is novel, animate it in to explain it
  (HIG note, [[trends/charting-best-practices]]) — bar/line charts don't need
  entrance animation.

## 5. Legacy archive — v4 motion specs (dormant code, tag `v4.0`)

Kept for the record and because the code still compiles in `ContentView.swift`
/ `TodayView.swift`; none of it is on-screen in v5:

- **Peek drawer**: `spring(response: 0.46, dampingFraction: 0.82)` on
  open/close; eased (not sprung) under Reduce Motion; snap decided by
  projected end position = translation + ~150 ms of release velocity
  ([[navigation/peek-drawer]], [[navigation/global-swipe]]).
- **Capture card pop**: `spring(response: 0.4, dampingFraction: 0.86)`;
  phase fades `easeInOut(0.2)` ([[food-entry/food-card-capture]]).
- **Food-log date swipe (1:1 pager)**: current + neighbor day track the
  finger; commit is velocity-driven — threshold `dx + v·0.20 > 0.22·width`
  OR flick `|v| > 320`; commit spring response scales `remaining/speed`
  clamped 0.16–0.40 s; past-today rubber-bands ×0.22
  ([[food-entry/food-card-capture]] follow-ups).
- **DottedGlobe auto-spin**: analytic `velocity(t) = base + (v0−base)e^(−t/τ)`,
  base 14 °/s, τ 1.2 s; drag sets `v0 = release.velocity.width × 0.6`
  (clamped ±720); `TimelineView(.animation)` redraw; Reduce Motion freezes
  base spin, drag still repositions ([[today/design-handoff-2026-06-16]]).
- **LiquidGlobe waves**: animated stacked macro waves; frozen under Reduce
  Motion.
- **Planet globe (SceneKit)**: `idleSpin` `SCNAction` + `rendersContinuously
  = true` (required for idle animation); drag removes the action, restores
  on release ([[today/planet-globe]]).
- **Attach tray / composer**: `+` rotates 45°→× (later removed); pill growth
  spring-animated; idle width shrink ([[food-entry/composer-attach-tray]]).
- **Chat sheet**: native detents/`presentationCornerRadius(28)` transitions
  ([[navigation/ai-chat-overlay-retired]], retired).

## 6. How to edit motion (the workflow)

1. Change the token in `CaffeineDesign.swift` (or add a new named token —
   never inline a magic curve at a call site).
2. Verify on the iOS 27 sim — the UI suite exercises the panel, day change,
   sub-screens, and tab switch; screenshot anything visual.
3. Update **this page** (tokens table + inventory) in the same change; other
   pages should link here rather than restate curves.

See also [[caffeine-v5]] (the era canon this page details).
