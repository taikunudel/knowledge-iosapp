---
type: rule
id: "workflow/meta-rule"
title: "Meta Rule: Document Every User Requirement Here"
description: "Every user-stated requirement, preference, or rejection must be recorded in CLAUDE.md before moving on."
status: stable
tags: [meta, documentation, requirements]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Meta Rule: Document Every User Requirement Here

**Every time the user states a requirement, preference, or rule for this project, Claude must record it in this file before moving on.** This includes:

- UI / UX design constraints ("the chat bar should…", "the cards should always…")
- "Don't ever do X" / "Always do Y" rules
- Naming, structural, or architectural choices
- Workflow preferences ("just finish before reporting", "don't explain first")
- Performance, accessibility, or platform-version targets
- API choices and integrations
- Anything the user phrases as a durable rule rather than a one-off ask

How to record:

1. Find the most relevant existing H2 section, or create a new one.
2. Be **detailed**: capture the *what*, the *why* (if the user gave one), and the *where* (file paths, struct names, line numbers) so the requirement is enforceable later by anyone reading this file cold.
3. If a new requirement contradicts an existing one, ask the user which wins, then update — don't silently overwrite.
4. Never delete a requirement without the user's explicit confirmation.
5. Date entries (`Established: YYYY-MM-DD`) when the context isn't obvious from the file's history.
6. Treat rejection signals as requirements. Phrases like "X is problematic", "restore it", "never do that again", "don't ever X", "always do X" — even when said casually — are durable rules and belong in this file (under the appropriate section, or under **Rejected Design Experiments** for retired designs).

This file is the single source of truth for project-specific rules. Global personal rules live in `~/.claude/CLAUDE.md`.
