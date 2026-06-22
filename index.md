# Nutritionist — Development Wiki

Project-specific design decisions, locked rules, and engineering invariants for the
Nutritionist iOS app. Each folder groups related rules; pages keep their dates and 🔁
supersession history. Converted from the app's `CLAUDE.md` on 2026-06-22; this wiki is
the canonical store going forward.

## Subfolders
* [workflow/](workflow/) - meta-rule (document every requirement), finish-before-reporting, verify-builds, git hygiene
* [design-system/](design-system/) - iOS 26/27 design guide + Liquid Glass, MUJI accent palette, settings revamp, rejected experiments
* [navigation/](navigation/) - peek drawer (DrawerShell), global swipe axis decision, retired AI chat overlay
* [today/](today/) - Today screen: 2026-06-16 design handoff, dotted macro globe, food-log rendering, per-day completion, drag-to-move
* [food-entry/](food-entry/) - food-card capture (no chat window), clear design, composer attach-tray (v6), food card library
* [trends/](trends/) - pinned nutrients monitor, in-place graphs, local-only routing
* [ai/](ai/) - Genmoji food icons, multi-provider + on-device AI with retry
* [engineering/](engineering/) - SwiftData saves, already-scaled payload, backup/restore, glass capsule, DEBUG harness, elegant-architecture reference, calendar card swipe
