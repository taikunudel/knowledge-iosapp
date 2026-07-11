---
type: rule
id: "workflow/graph-legibility"
title: "Graph Legibility — content conventions the graph.html reads"
description: "How wiki CONTENT (titles, tags, links) is authored so the untouched graph renderer stays legible: v4 · title prefixes on historical pages, rare era tags (era-v5 bonds the live canon cluster), and canon-hub links that keep the current era page as the hero."
status: stable
tags: [workflow, graph, legibility, tags, titles, era]
created: 2026-07-11T00:00:00Z
updated: 2026-07-11T00:00:00Z
---

# Graph Legibility — content conventions

*Established 2026-07-11. The user's constraint: do NOT change the MCP or the
graph renderer — the wiki CONTENT alone must make graph.html render clearly.
The renderer reads titles (labels), tags (IDF-weighted cluster bonds), and
`[[wikilinks]]` (edges; max-degree node = the pulsing hero). These are the
levers:*

1. **Era title prefixes.** Historical pages carry `v4 · ` at the start of
   `title:` so liveness reads directly on the canvas labels and in the
   directory panel. Live pages carry no prefix. On the next pivot, prefix the
   then-old era (`v5 · `) the same way.
2. **Rare era tags.** The current era's canon pages (and ONLY those — keep
   the tag rare so its IDF stays above the edge threshold) share `era-v5`,
   which bonds them into one visual cluster. Historical pages share
   `era-v4`, tightening the old constellation away from the live one.
   Currently `era-v5` = caffeine-v5, motion, exits, nutrition-verification.
3. **The canon page must be the hero.** graph.html crowns the max-degree
   node. Every live page that genuinely relates to the current era links
   `[[caffeine-v5]]` (era notes, "still load-bearing in v5" notes) so the
   canon out-degrees historical hubs. Check after edits:
   the regen summary prints `hero=…` — it must be the canon page.
4. **Links must stay honest.** Never add a `[[caffeine-v5]]` link purely to
   inflate degree — each one carries a true sentence (era note, dependency,
   supersession). If the hero drifts, find genuinely missing relations first.

Verified 2026-07-11: hero = `design-system/caffeine-v5` (23°), era-v5 bonds
6 edges, the v4 ball self-clusters via era-v4 + its own dense cross-links.
