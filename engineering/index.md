# Engineering

Engineering invariants, persistence and gesture rules, the DEBUG verification harness, and the aspirational elegant-architecture reference for the Nutritionist app.

## Documents

* [Pinned-Nutrient Totals — Already-Scaled Payload](pinned-nutrient-totals.md) - Values summed from aiGeneratedNutritionJSON are already portion-scaled at log time and must not be re-multiplied by portionMultiplier.
* [SwiftData Save Failures — Always do/catch](swiftdata-saves.md) - User-observable writes must wrap modelContext.save() in do/catch, roll back on failure, and only update the UI inside the do block.
* [Library Card Visual Fidelity](library-card-fidelity.md) - LibraryFoodCardPreview must mirror the chat nutrition card's full visual hierarchy and never drift back into a flat list-row presentation.
* [Backup / Restore — New Schema Coverage](backup-restore.md) - Every new user-facing persisted setting must extend AppSettingsSnapshot, and every new SwiftData model must be added to the backup payload and restore loop.
* [Pinned Chip Surface — LiquidGlassCapsuleModifier](pinned-chip-surface.md) - The pinned-nutrient chip must use LiquidGlassCapsuleModifier, not hand-rolled Capsule().fill().stroke() chrome.
* [DEBUG Verification Harness — Launch-Arg Seeding](debug-harness.md) - A #if DEBUG-only launch-argument seeding harness in ContentView used to screenshot design screens via simctl without a backend or manual tapping.
* [Elegant-Architecture Reference — Target Conventions vs Current State](elegant-architecture.md) - Aspirational, research-backed iOS-26 conventions to migrate the app toward, with current divergences flagged and the full F1–F11 adversarial findings.
* [Calendar Card Swipe — UIKit Pan Gesture Coexists With ScrollView (iOS 26)](calendar-card-swipe.md) - On Calendar, a single axis-locking UIKit pan recognizer owns both card axes and recognizes simultaneously with the ancestor ScrollView, because iOS 26 broke simultaneousGesture.
