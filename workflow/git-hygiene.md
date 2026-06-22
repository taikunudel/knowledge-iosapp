---
type: rule
id: "workflow/git-hygiene"
title: "Git Hygiene"
description: "Paths that must stay git-ignored, and the rule to stage named files rather than git add ."
status: stable
tags: [git, hygiene, gitignore]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Git Hygiene

*Established: 2026-05-20*

The following paths are ignored by design and must stay ignored. Don't add them to commits even if the user asks for `git add .`:

- `.artifacts/` — local scratch (~135 MB of debug screenshots, icon experiments, launch logs).
- `.claude/` — Claude Code session state and agent worktrees (~26 MB).
- `progress_by_codex` — local progress log.
- `Gemini_Generated_Image_*.png` — generated reference images.
- `*.stdout.log`, `*.stderr.log` — captured process output.

When staging, prefer named files (`git add Nutritionist/Foo.swift`) over `git add -A` / `git add .` to avoid accidentally including these or future scratch files.
