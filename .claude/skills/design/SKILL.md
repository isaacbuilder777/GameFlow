---
name: design
description: Produce a GDD section for a feature, system, level, narrative beat, or UX flow. Invokes the designer agent. Use before non-trivial implementation. Do not use for tuning numbers on an already-designed system (use /balance) or for typo/bug fixes.
---

# /design

Write a game design doc.

## Steps

1. **Parse argument.** Feature name as arg: `/design crit-system`. If no arg, ask.
2. **Check for existing doc.** If `design/<feature>.md` already exists, ask: extend, replace, or abort?
3. **Delegate to designer agent** with:
   - Feature name
   - Engine from `.claude/engine.md`
   - Review mode from `production/review-mode.txt`
   - User's verbal brief for this feature
4. **Designer produces** `design/<feature>.md` with required sections: Goal, Non-goals, Approach, Formulas, Edge cases, Tradeoffs, Open questions.
5. **Review gate:**
   - `solo` — skip.
   - `lean` — skip (director gates phase transitions, not individual designs).
   - `full` — invoke director for approval before finalizing.
6. **Log marker.** `{"skill":"design","produces":"design_doc","feature":"<name>","ts":<iso>}`.

## Output

- Path to the new doc.
- Open questions, highlighted — `/build <feature>` will refuse until resolved.
- Suggested next: resolve open questions, then `/build <feature>`. If the feature has numeric tuning, `/balance <feature>` can run in parallel.

## Do not

- Do not produce empty sections — "None" is acceptable, absent header is not.
- Do not bundle features. One file per feature.
- Do not write code.
