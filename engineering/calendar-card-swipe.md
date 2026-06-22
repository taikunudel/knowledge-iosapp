---
type: rule
id: "engineering/calendar-card-swipe"
title: "Calendar Card Swipe — UIKit Pan Gesture Coexists With ScrollView (iOS 26)"
description: "On Calendar, a single axis-locking UIKit pan recognizer owns both card axes and recognizes simultaneously with the ancestor ScrollView, because iOS 26 broke simultaneousGesture."
status: stable
tags: [engineering, calendar, gestures, uikit, ios26, scrollview, swipe]
created: 2026-06-22T00:00:00Z
updated: 2026-06-22T00:00:00Z
---

# Calendar Card Swipe — UIKit Pan Gesture Coexists With ScrollView (iOS 26)

*Established: 2026-06-09*

On the **Calendar** screen, the entries card supports both horizontal swipes (change date) and vertical drags (expand/collapse the card). The calendar's month-grid `ScrollView` behind the card also responds to vertical touches.

**iOS 26 broke `simultaneousGesture`** with ancestor gestures (FB18199844 — Apple's release notes: "Fixed: Gestures added using the simultaneousGesture view modifier are incorrectly simultaneous with ancestor gestures"). This means none of the pure-SwiftUI approaches work:
- `.simultaneousGesture()` → iOS 26 no longer lets it coexist with the ScrollView's pan
- `.highPriorityGesture()` → steals touches from ScrollView entirely, breaks vertical scroll
- `.scrollDisabled()` → kills all vertical scrolling

## Implementation

The solution uses the iOS 26 `UIGestureRecognizerRepresentable` path in [Nutritionist/Views/CalendarView.swift](Nutritionist/Views/CalendarView.swift):

1. **`CalendarCardPanGestureRecognizer`** — one `UIGestureRecognizerRepresentable` wrapping one `UIPanGestureRecognizer`, attached directly to the card with `.gesture(...)`:
   - `gestureRecognizerShouldBegin` locks the pan to one axis: horizontal when horizontal velocity > vertical velocity × 1.3 (and date swipe is enabled), or vertical when vertical velocity > horizontal velocity × 1.15
   - `shouldRecognizeSimultaneouslyWith`: returns `true` — allows ScrollView's vertical pan to keep working
   - `cancelsTouchesInView = false` — doesn't block other touches
   - Reports axis, translation, and final velocity back to SwiftUI state; horizontal pans change date and vertical pans expand/collapse the card
   - It must **not** be hosted in a transparent `UIViewRepresentable` overlay. That overlay becomes the hit-test surface and blocks the card's vertical SwiftUI drag.

2. **Do not stack a SwiftUI `DragGesture` with the UIKit recognizer on iOS 26.** The two recognizers compete and the UIKit attachment can prevent the SwiftUI vertical callbacks from firing. The single UIKit pan recognizer owns both card axes while recognizing simultaneously with the ancestor ScrollView.

## Explicitly NOT Allowed

- **Don't use `.scrollDisabled(...)`** — kills vertical scrolling entirely (rejected 2026-06-09).
- **Don't use `.highPriorityGesture()`** on the card's drag gesture — prevents ScrollView from receiving touches (rejected 2026-06-09).
- **Don't use `.simultaneousGesture()`** — broken on iOS 26 (FB18199844).
- **Don't use a SwiftUI-only approach for this** — iOS 26 requires UIKit gesture bridge for this specific conflict.
- **Don't put the UIKit pan recognizer in a transparent view overlay** — it steals the hit-tested surface and breaks vertical dragging/scrolling (rejected 2026-06-09).
- **Don't stack separate UIKit-horizontal and SwiftUI-vertical recognizers on the card** — the vertical SwiftUI callbacks do not reliably fire on iOS 26. Use the single axis-locking UIKit pan recognizer (rejected 2026-06-09).
