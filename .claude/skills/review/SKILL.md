---
name: review
description: Quality review pass. Invokes the reviewer agent. Use before /ship or any time a diff is ready for critique. Checks code rules, engine conventions, and design-fit. Does not modify code.
---

# /review

Critical review of current changes.

## Steps

1. **Scope the diff:**
   - Arg given: `/review crit-system` → files mentioned in the design doc + the implementation files the builder touched.
   - No arg: diff against `main` or `master`.
2. **Delegate to reviewer agent** with:
   - Diff content
   - Relevant design doc if one exists
   - `.claude/rules/code.md` (relevant sections only)
   - `.claude/engine.md`
3. **Reviewer produces** a structured report: Must fix / Should consider / Nitpicks / Design fit.
4. **Log marker** only if there are **zero Must-fix items.** `{"skill":"review","produces":"reviewed","ts":<iso>}`.
5. **If Must-fix items exist:** do NOT log. Show report; suggest `/build` to address, then re-run `/review`.

## Output

The report verbatim, plus:
- `reviewed` marker logged? (yes/no)
- Suggested next: `/test` if not yet run, or `/ship` if all markers present.

## Do not

- Do not log `reviewed` when Must-fix items exist.
- Do not fix inline — builder owns fixes.
- Do not skip design-fit check. Drift is a real and common problem.
