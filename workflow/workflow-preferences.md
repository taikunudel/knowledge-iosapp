---
type: rule
id: "workflow/workflow-preferences"
title: "Workflow Preferences"
description: "Finish before reporting, explicitly enumerate documentation changes, and verify builds by parsing BUILD SUCCEEDED / BUILD FAILED."
status: stable
tags: [workflow, builds, reporting]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Workflow Preferences

### Finish Before Reporting
*Established: 2026-05-20*

The user prefers that Claude completes all steps of a multi-step task (edits, build verification, follow-ups) **before** writing any status update or report. Don't stop mid-task to ask clarifying questions unless something would clearly block progress — make the reasonable call and continue. The user will redirect if needed.

**Note:** This overrides the global rule "Before making SwiftUI layout changes, explain the approach first." For this project, the explanation comes at the end, not the start.

### Explicitly Enumerate Documentation Changes
*Established: 2026-05-20*

Whenever Claude updates CLAUDE.md (per the Meta Rule), the end-of-task report **must explicitly list each rule / section that was added or modified, with verbatim or near-verbatim text**, so the user can confirm at a glance that nothing was silently captured or paraphrased away. User verbatim: "if you document everytime, you explicitly let me know what you documented."

### Verify Builds by Parsing `BUILD SUCCEEDED` / `BUILD FAILED`
*Established: 2026-05-20*

When verifying an iOS build, **don't trust shell exit codes alone** — especially when `xcodebuild` is chained with `simctl install` / `simctl launch`. A failed compile can still leave the previous binary installed, so `simctl launch` will happily start the **stale** app and the chain reports "success" while the user-visible changes aren't actually running.

Always grep the xcodebuild output for the literal strings `BUILD SUCCEEDED` or `BUILD FAILED` (and `error:` lines) and react to those. Example pattern:

```bash
xcodebuild ... 2>&1 | grep -E "BUILD SUCCEEDED|BUILD FAILED|\.swift:[0-9]+:[0-9]+: error"
```

If `BUILD FAILED` is found, **stop and fix before reinstalling**. Don't report "app is live" until a fresh `BUILD SUCCEEDED` has been observed for the exact code state being claimed.

Background introduced this rule: on 2026-05-20 a chained build/install/launch silently re-ran an older binary because of a missed Swift compile error (Equatable synthesis on an enum with a closure case); the user-visible changes weren't actually running when the launch step succeeded.
