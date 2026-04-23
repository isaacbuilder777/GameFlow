---
name: build
description: Implement from an approved design doc. Invokes the builder agent. Use after /design has produced a doc and open questions are resolved. Do not use without a design for non-trivial changes.
---

# /build

Implement a designed feature.

## Steps

1. **Parse argument.** Feature name: `/build crit-system`. If none, list `design/*.md` and ask.
2. **Verify design doc** exists at `design/<feature>.md`. Refuse with `/design <feature>` suggestion if not.
3. **Check Open Questions section.** If non-empty and not "None", refuse. Show the user the questions — they need decisions first.
4. **Verify engine is set** in `.claude/engine.md`. If "unset", refuse and suggest `/start`.
5. **Delegate to builder agent** with:
   - Design doc path
   - Engine from `.claude/engine.md`
   - Applicable rules from `.claude/rules/code.md` based on paths being edited
   - Review mode
6. **Builder implements** following path-scoped rules and engine conventions.
7. **Review gate:**
   - `solo` — skip.
   - `lean` — skip here (review happens at `/ship`).
   - `full` — invoke reviewer immediately on the diff.
8. **Log marker.** `{"skill":"build","produces":"implementation","feature":"<name>","ts":<iso>}`.

## Output

- Files changed (by path).
- Design gaps builder had to fill in — flagged for user sanity-check.
- Suggested next: `/test <feature>`, then `/review <feature>`. If numeric, consider `/balance <feature>` before `/test`.

## Do not

- Do not auto-commit.
- Do not extend scope beyond the design.
- Do not skip engine convention loading — engine-specific mistakes are the most common source of bugs.
