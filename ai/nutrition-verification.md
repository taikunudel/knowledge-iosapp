---
type: rule
id: "ai/nutrition-verification"
title: "Nutrition Verification — scientific checkpoints, expandable in the panel"
description: "What each analysis checkpoint scientifically checks (Atwater energy cross-check, macro component sums, unit conventions, coverage over the full 37-field schema), the reused v4 nutrient schema, and the rule that every checkpoint is clickable to expand its real evidence."
status: stable
tags: [ai, nutrition, verification, atwater, macros, micronutrients, checkpoints, science, era-v5]
created: 2026-07-10T00:00:00Z
updated: 2026-07-10T00:00:00Z
---

# Nutrition Verification — scientific checkpoints, expandable

*Created 2026-07-10. User: "i want a dedicated knowledge for checking the
macro and micro nutrition given a food. it must be scientific … i want every
checkpoint clickable to expand, i wanna see how the model really check what
… i used to have many macro and micro nutrition specified in the old app
design, i want you to reuse them."*

## The reused schema (v4 → v5, unchanged on purpose)

`NutritionResponse` (ContentView.swift) is the canonical nutrient schema —
**37 tracked fields**, all reused, none re-invented:

- **Macros (9, grams unless noted):** carbohydrates, protein, totalFat,
  saturatedFat, monounsaturatedFat, polyunsaturatedFat, cholesterol (mg),
  sugar, fiber.
- **Vitamins (13):** A (mcg), B6 (mg), B12 (mcg), C (mg), D (mcg), E (mg),
  K (mcg), thiamin (mg), riboflavin (mg), niacin (mg), pantothenic acid (mg),
  biotin (mcg), folate (mcg).
- **Minerals (14):** calcium, iron, magnesium, phosphorus, potassium,
  sodium, zinc, copper, manganese (all mg); selenium, chromium, molybdenum,
  iodine (mcg); chloride (mg).
- **Other (1):** caffeine (mg).

The v4 computed accessors `macronutrients` / `vitamins` / `minerals` /
`others` (each filters to values > 0 and carries its unit) are reused
verbatim as the display source. Payloads are stored **already
portion-scaled** ([[engineering/pinned-nutrient-totals]]).

## The science behind each checkpoint

The cloud model returns one structured JSON; the checkpoints are the
verification pipeline the app runs over it (`CFNutritionAudit` in
`CaffeineLogic.swift` — pure, unit-tested). Be honest about this in UI and
docs: expansions show **real extracted values and real local cross-checks**,
never invented intermediate "thoughts."

1. **ANALYZING CALORIES — energy consistency (Atwater).** Stated kcal is
   cross-checked against the Atwater general factors **4 kcal/g protein,
   4 kcal/g carbohydrate, 9 kcal/g fat** (alcohol 7 kcal/g — not tracked).
   Gate: |stated − computed| ≤ **15%** of stated → ✓, else ⚠ REVIEW. (FDA
   labeling enforcement uses a 20% class tolerance; we warn earlier on
   purpose. Reference DB for spot checks: USDA FoodData Central.)
2. **ANALYZING MACROS — component-sum + energy-bound sanity.** Every
   reported macro with its unit, plus inequalities that must hold
   physically: **saturated + mono + poly ≤ totalFat** and **sugar + fiber ≤
   carbohydrates** (each with +0.5 g rounding slack); **no single macro may
   carry more energy than the whole food** (grams × its Atwater factor ≤
   stated kcal × 1.10 headroom — catches e.g. "200 g protein in a 300 kcal
   dish"); cholesterol > 1,000 mg/serving is flagged implausible-high
   (>3× the historical 300 mg/day Daily Value); negatives are invalid.
3. **ANALYZING MICRONUTRIENTS — coverage + per-serving plausibility
   screen.** Vitamins reported (n/13) and minerals reported (n/14), each
   listed with its unit (mcg-vs-mg is fixed by the schema so unit errors
   can't slip in silently). Every screened nutrient is compared against a
   **full-day reference cap** (FDA Daily Values for sodium/potassium, NIH
   ODS adult Tolerable Upper Intake Levels for vitamins/minerals — table
   below): ONE serving exceeding a FULL DAY's cap is a red flag → ⚠; a ✓
   "ALL WITHIN FULL-DAY REFERENCE CAPS" line confirms a clean screen.
4. **EXTRACTING NUTRITION POINTS — field coverage.** N of 37 schema fields
   reported (> 0), caffeine if present (flagged when one serving exceeds
   the **FDA 400 mg/day** guidance for healthy adults), the model's 0–100
   health score, and which model produced the JSON.
5. **RECHECKING ACCURACY — the audit summary.** Every rule above re-listed
   with its ✓/⚠ verdict: Atwater delta, fat components, sugar+fiber,
   non-negativity, and a "PLAUSIBILITY SCREEN CLEAR / PLAUSIBILITY FLAGS: N"
   roll-up of the energy-bound + cap checks. If macros were absent and the
   45/30/25 estimation fallback filled them
   (`normalizeNutritionForLogging`), that is DISCLOSED here as "MACROS
   ESTIMATED FROM CALORIES" — estimated data must never masquerade as
   extracted data.

**Every checkpoint block leads with its verdict line** — `VERDICT — PASS`
(no flags) or `VERDICT — REVIEW (N FLAGS)` — so the state of each stage
reads before any expansion detail.

## Tolerances & reference caps (the numbers, with their basis)

| Check | Threshold | Basis |
|---|---|---|
| Atwater energy delta | ±15% of stated kcal | Atwater factors 4/4/9 kcal/g; deliberately stricter than FDA's 20% labeling class tolerance |
| Per-macro energy bound | grams × factor ≤ kcal × 1.10 | pure arithmetic; 10% headroom for label rounding |
| Fat components / sugar+fiber | +0.5 g slack | label rounding |
| Cholesterol | ≤ 1,000 mg /serving | >3× the historical 300 mg/day Daily Value |
| Caffeine | ≤ 400 mg /serving | FDA guidance: 400 mg/day for healthy adults |
| Sodium | ≤ 5,000 mg /serving | >2× the 2,300 mg FDA Daily Value |
| Potassium | ≤ 4,700 mg /serving | the full-day FDA Daily Value |
| Vitamin A | ≤ 3,000 mcg | NIH ODS adult UL (preformed retinol) |
| Vitamin B6 | ≤ 100 mg | NIH ODS adult UL |
| Vitamin C | ≤ 2,000 mg | NIH ODS adult UL |
| Vitamin D | ≤ 100 mcg | NIH ODS adult UL |
| Vitamin E | ≤ 1,000 mg | NIH ODS adult UL |
| Niacin | ≤ 35 mg | NIH ODS adult UL (synthetic) |
| Folate | ≤ 1,000 mcg | NIH ODS adult UL (synthetic) |
| Calcium | ≤ 2,500 mg | NIH ODS adult UL |
| Iron | ≤ 45 mg | NIH ODS adult UL |
| Zinc | ≤ 40 mg | NIH ODS adult UL |
| Selenium | ≤ 400 mcg | NIH ODS adult UL |
| Iodine | ≤ 1,100 mcg | NIH ODS adult UL |

Caps live in `CFNutritionAudit.perServingCaps` (+ `cholesterolCapMg`,
`caffeineCapMg`, `macroBoundSlack`); they are screens for **implausible
single-serving extractions**, not dietary advice. B12, thiamin, riboflavin,
pantothenic acid, biotin, and chromium have **no established UL** (NIH), so
they are deliberately not capped.

## The UX rule — every checkpoint expands

- Once a result (or error with partial data) exists, **every checkpoint row
  is clickable**: tapping toggles an indented mono detail block (the
  evidence lines above), `+` / `−` trailing marker, flat Caffeine styling,
  expansion prints from the row per the [[motion]] provenance rule.
- While still in flight a row shows only its pulse — there is nothing real
  to show yet, so nothing expands (no fake evidence).
- Lines carry status marks: plain = extracted value, **✓ accent** = check
  passed, **⚠ accent** = review (never silently hide a failed check).
- The FIBER/SUGAR/SAT FAT/SODIUM quick grid on the FINAL REPORT stays; the
  checkpoint expansions are where the FULL 37-field schema is visible —
  this is the v4 "many macro and micro nutrition specified" surface,
  restored.

## Explicitly NOT allowed

- Don't display invented model "reasoning steps" as if they were telemetry —
  expansions show extracted fields + local checks only.
- Don't drop fields from the schema to make coverage look better; 0/absent
  is honest data.
- Don't change the Atwater factors or tolerances without recording the
  scientific justification here.

See also [[multi-provider-ai]] (superseded routing history), [[caffeine-v5]],
[[engineering/pinned-nutrient-totals]].
