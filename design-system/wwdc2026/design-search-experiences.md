---
type: guide
id: design-system/wwdc2026/design-search-experiences
title: "Design Intuitive Search Experiences (WWDC26)"
description: "Designing search across Apple platforms: the search-field component, placement per platform, suggestions/recents, predictive results, scope bars/filters/tokens, and empty states."
status: stable
tags: [design, search, hig, wwdc2026, ios, ipados, macos]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
resource: "https://developer.apple.com/videos/play/wwdc2026/292/"
sources:
  - "https://developer.apple.com/videos/play/wwdc2026/292/"
  - "https://developer.apple.com/design/human-interface-guidelines"
---

# Design Intuitive Search Experiences (WWDC26)

> **Canonical source (richer than this page — watch it):**
> [Design intuitive search experiences — WWDC26](https://developer.apple.com/videos/play/wwdc2026/292/).
> This page is a distilled index; the talk has the full visual examples.

WWDC26 session by Rob (Apple Design team). Search is *"one of the most important tools for
helping people find, navigate, and discover content"* and is often the first thing users
look for. (Not currently a prominent surface in Nutritionist — kept as reference for if/when
the food log, library, or trends gain search.)

## Search field component
Standard elements: **leading search icon** (establishes it as search), **placeholder**,
**clear button** (once text entered), **cancel button** (iOS, when focused — exits + dismisses
keyboard). Branding: keep core elements intact; a custom icon should closely resemble the
standard magnifying glass.

## Placement
**iOS** — **bottom toolbar (preferred):** animates up over the keyboard, optimal reachability; **top toolbar** when the bottom is occupied; **tab bar** for a dedicated entry point; **inline/content** under the top toolbar. Decide by: how people navigate the app, and the scope of search.
**iPad & macOS** — **trailing toolbar** (split-view apps like Mail); **sidebar** (filter sidebar content, like Settings); **dedicated Search tab** (rich multi-section apps like Music). The field scales or collapses to a button as space allows.

## Suggestions, recents, predictive
- **Recent searches** — iOS: inline when the field focuses; iPad/macOS: in a menu or alongside content. Be selective (only viewed/engaged results); let users remove one (swipe) or clear all (header button).
- **Predictive suggestions** — show relevant results as fast as possible alongside input; suggestions should feel like natural completion; **visually distinguish input vs suggestion**; limit the count so results stay front and center.

## Filtering & refinement
- **Scope bar** — lightweight switch between contexts (e.g. all mailboxes vs current mailbox); reinforces *where* you're searching.
- **Contextual filters** — show only filters relevant to the current context (Maps shows restaurant/trail filters by location type); don't overwhelm.
- **Search tokens** — filter by keywords shown as highlighted chips in the field; support natural-language combos ("photos from Joshua Tree in 2021"). **Less discoverable — don't use them to replace visible filtering UI;** pair with a scope bar or other controls.

## Empty / no-results states
Always show a considered empty state so users don't wonder whether search ran: use the
**content-unavailable view** configured for search (search symbol, title, subtitle) and
**display the current search text** so typos are easy to catch.

## Chapters
0:00 Intro · 1:39 Search-field core elements · 2:52 Patterns & placement · 10:30 Best
practices (suggestions, filters, tokens) · 15:20 Next steps. Related: WWDC25 "Get to know
the new design system", "Meet Liquid Glass".
