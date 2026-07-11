# AI

AI provider integration, model selection, and food-icon generation.

## Documents

* [Nutrition Verification — scientific checkpoints, expandable in the panel](nutrition-verification.md) - What each analysis checkpoint scientifically checks (Atwater energy cross-check, macro component sums, unit conventions, 37-field schema coverage), the reused v4 nutrient schema, and the rule that every checkpoint expands to its real evidence.
* [Genmoji Food Icons — ImagePlayground Regeneration](genmoji-icons.md) - Food icons are regenerated via the Image Playground sheet because headless ImageCreator is deprecated and runtime-dead on iOS 27.
* [Multi-Provider AI + Retry](multi-provider-ai.md) - Reference for the multi-provider LLM client (Apple on-device, Gemini, OpenRouter, GLM), the model fallback chain, retry affordance, and per-card attribution.
