---
type: rule
id: "engineering/backup-restore"
title: "Backup / Restore — New Schema Coverage"
description: "Every new user-facing persisted setting must extend AppSettingsSnapshot, and every new SwiftData model must be added to the backup payload and restore loop."
status: stable
tags: [engineering, backup, restore, swiftdata, settings, persistence]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Backup / Restore — New Schema Coverage

*Established: 2026-05-26 (Codex adversarial review fix)*

The full backup/restore service in [Nutritionist/Views/SettingsView.swift](Nutritionist/Views/SettingsView.swift) (`FullDataBackupService`) now carries the post-2026-05-20 user state:

- `BackupPayload.libraryFoodCards: [LibraryFoodCardSnapshot]?` — optional for backward compat with older backup files.
- `AppSettingsSnapshot.pinnedNutrients: [String]?` — captured from `appSettings.pinnedNutrients`, restored via `AppSettings.replacePinnedNutrients(_:)`.
- `AppSettingsSnapshot.excludedDateKeys: [Double]?` — captured via `appSettings.excludedDateKeysSnapshot`, restored via `AppSettings.replaceExcludedDateKeys(_:)`.

All three are optional on the JSON snapshot so older backups still decode. **Any new user-facing persisted setting must extend both `AppSettingsSnapshot.init(from:)` and `apply(to:)`.** Any new SwiftData model must be added to the `BackupPayload` and the `restore(...)` upsert loop.
