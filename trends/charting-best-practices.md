---
type: guide
id: trends/charting-best-practices
title: "Charting / Graphing Data — Best Practices (Apple)"
description: "Apple's best practices for charting data (HIG Charting data + WWDC chart sessions), and the concrete gaps in Nutritionist's Trends charts. Keep the canonical links — the HIG page is the authoritative, current source."
status: stable
tags: [trends, charts, swift-charts, accessibility, hig, wwdc2025, wwdc2026]
created: 2026-06-23T00:00:00Z
updated: 2026-06-23T00:00:00Z
resource: "https://developer.apple.com/design/human-interface-guidelines/charting-data"
sources:
  - "https://developer.apple.com/design/human-interface-guidelines/charting-data"
  - "https://developer.apple.com/design/human-interface-guidelines/charts"
  - "https://developer.apple.com/videos/play/wwdc2025/313/"
  - "https://developer.apple.com/videos/play/wwdc2026/102/"
  - "https://developer.apple.com/documentation/swiftui/view/chartscrollableaxes(_:)"
  - "https://developer.apple.com/videos/play/wwdc2023/10037/"
  - "https://developer.apple.com/documentation/swiftui/view/accessibilitychartdescriptor(_:)"
  - "https://developer.apple.com/videos/play/wwdc2021/10122/"
  - "https://support.apple.com/guide/stocks/change-the-chart-display-stc4cfc704df/mac"
---

# Charting / Graphing Data — Best Practices (Apple)

> **Canonical sources (richer + more current than this page — open them):**
> [HIG — Charting data](https://developer.apple.com/design/human-interface-guidelines/charting-data)
> (the authoritative best-practice page) ·
> [HIG — Charts (components)](https://developer.apple.com/design/human-interface-guidelines/charts) ·
> [WWDC25 — Bring Swift Charts to the third dimension](https://developer.apple.com/videos/play/wwdc2025/313/) ·
> [WWDC26 — Platforms State of the Union](https://developer.apple.com/videos/play/wwdc2026/102/).
> The HIG page also links the foundational WWDC23 design sessions **"Design an effective
> chart"** and **"Design app experiences with charts"**. There is **no dedicated charts
> session at WWDC 2026** — its chart guidance is the interactive scroll-highlight pattern
> shown in the SOTU (the Tide Guide example) plus the 2026 HIG scroll-edge refinements.

## Core best practices (HIG — Charting data)
- **Only chart what needs interpreting.** Charts are for analyzing trends, showing current state over time, and comparing across categories. If you're just presenting values, use a list/table (scroll, search, sort) instead.
- **Keep it simple; reveal detail progressively.** Don't pack in as much data as possible — that obscures the relationships you want to show. Let people opt into more detail / subsets / functionality.
- **Add a descriptive takeaway, not just axes.** Titles, subtitles, annotations, and a short headline/summary ("Chance of light rain in the next hour" style) help people grasp the point at a glance. (A visible summary does **not** replace accessibility labels.)
- **Prefer common chart types** (bar, line) so people already know how to read them. If a chart is novel, teach it (Activity animates each ring in to explain it).
- **Make every chart accessible** — provide accessibility labels that describe values/components **and** Audio Graphs so the chart works without sight. Treated as crucial, not optional. (See HIG "Enhancing the accessibility of a chart".)
- **Match size to function** — a small glanceable chart that expands into a larger, interactive one.
- **Consistency + continuity.** Charts with a similar purpose should share type/style/color. When a small "trend" chart expands to a full one, the expanded version must reuse the **same** style, colors, marks, and annotations (Apple's example: the **Health → Trends** screen).
- **Examine the data at multiple levels** (macro totals/averages, mid-level subsets, individual points) and surface what helps people read it from each perspective.

## When to use 3D (WWDC25 — session 313)
- Use 3D **only** when the *shape* of the data matters more than exact values, the data is inherently 3D, or interaction genuinely adds value — **never for novelty**. It shines on Vision Pro.
- 2D remains better for reading precise numbers (orthographic projection compares sizes regardless of depth). **For nutrition trends, stay 2D** — this session is a "when *not* to" reference.

## Interactive highlight (WWDC26 — SOTU)
- The current direction: **subtle, interactive highlights that respond as people scroll/scrub** a chart (the Tide Guide example), so a static chart becomes explorable without clutter. Pairs with the 2026 HIG scroll-edge-effect refinements for legibility as content scrolls under bars.

## Zoom, scroll & scrub — interaction
- **Pinch-to-zoom is NOT the iOS idiom for charts.** Apple's own data apps (Health, Stocks) don't pinch-zoom a chart; they use a discrete **range selector** + horizontal scroll + scrub-to-inspect.
- **Change the window with a range selector, not free zoom.** A segmented control of preset ranges ([Apple Stocks](https://support.apple.com/guide/stocks/change-the-chart-display-stc4cfc704df/mac): 1D/1W/1M/3M/6M/1Y/ALL; for daily nutrition: **7D / 30D / 90D / All**). Highlight the active range; keep it consistent across charts.
- **Scroll natively — don't hand-roll a pan gesture.** `.chartScrollableAxes(.horizontal)` + `.chartXVisibleDomain(length:)` (the visible window) + `.chartScrollPosition(x:)` (bindable; set initial position to the latest data, read/restore on change) + `.chartScrollTargetBehavior(.valueAligned(…))` for snapping + momentum. iOS 17+ ([chartScrollableAxes](https://developer.apple.com/documentation/swiftui/view/chartscrollableaxes(_:)), [WWDC23 — Explore pie charts and interactivity in Swift Charts](https://developer.apple.com/videos/play/wwdc2023/10037/)); **unchanged through iOS 26/27** — there is no new 2D scroll/zoom API in WWDC25/26.
- **Drag / long-press over the chart = scrub to inspect** (show the point's date + value), as Stocks does — not pan. Use `.chartXSelection(value:)` (iOS 17+).

## Accessibility — Audio Graphs
- Swift Charts gives VoiceOver + an **Audio Graph** (plays a pitch per data point, modulated by the y value) largely automatically, but enrich it:
  - Add per-mark `.accessibilityLabel(…)` / `.accessibilityValue(…)` so each bar reads as "date, value".
  - For the full Audio Graph detail page, provide an **`AXChartDescriptor`** via a type conforming to `AXChartDescriptorRepresentable`, attached with **`.accessibilityChartDescriptor(_:)`** — gives VoiceOver's "Audio Graph" rotor a summary, axes, and series.
- Links: [accessibilityChartDescriptor](https://developer.apple.com/documentation/swiftui/view/accessibilitychartdescriptor(_:)) · [WWDC21 — Bring accessibility to charts in your app](https://developer.apple.com/videos/play/wwdc2021/10122/).

## Applied to Nutritionist Trends — current gaps
The per-nutrient bar charts live in
[NutrientTrendChart.swift](Nutritionist/Views/Components/NutrientTrendChart.swift) (bars +
a goal `RuleMark`, a 30-day scrollable window, pinned mini → expanded). Bars are a **locked
user preference** (2026-06-16: "the trend should be bar … not … like line") — improve
*within* bars, don't switch to line. Gaps vs the practices above:
1. **No accessibility** — no Audio Graph, no `.accessibilityLabel`/chart descriptor on the bars. This is the biggest gap (HIG calls it crucial).
2. **No interactivity** — can't tap/drag to read a specific day's value (no `.chartOverlay`/selection + annotation). The HIG "explore from multiple perspectives" + WWDC26 scrub pattern both point here.
3. **No descriptive takeaway** — only a "goal" chip and raw bars; no headline summary (e.g. average, vs-goal, or trend direction).
4. **Weak empty state** — a plain "No data available" string instead of a considered `ContentUnavailableView`.
5. **Glanceability** — the pinned mini chart could carry a one-glance stat (avg / vs goal) per the "match size to function" + "descriptive takeaway" practices.
