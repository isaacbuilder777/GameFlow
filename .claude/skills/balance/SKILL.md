---
name: balance
description: Tune numeric values against design formulas — damage curves, economy, drop rates, progression. Invokes designer to interpret formulas and builder to apply changes. Use when a system's shape is right but the numbers feel off, or to validate numbers before first playable.
---

# /balance

Tune the numbers without touching the shape.

## When to use

- Combat feels too slow or too fast.
- Economy is draining or inflating at the wrong rate.
- Drop rates don't produce the intended variety.
- Progression curve plateaus or spikes unexpectedly.
- Post-playtest feedback pointed at tuning, not mechanics.

## When NOT to use

- If the design itself is wrong, use `/design` to revise.
- If it's a bug (value reads wrong, formula applied wrong), that's `/build`.

## Steps

1. **Parse arg.** Feature or system name: `/balance combat`, `/balance economy`. If none, list systems with numeric formulas in `design/*.md` and ask.
2. **Read `design/<feature>.md`** — especially the Formulas section. If there are no formulas, refuse and send to `/design` first.
3. **Read current numeric values** from data files (resources / ScriptableObjects / data tables referenced in `src/`).
4. **Delegate to designer** to:
   - Confirm which curves/targets the numbers should produce (e.g., "TTK at level 10 should be 3-4 seconds").
   - Identify which values to change and the proposed new values.
   - Show before/after in a table.
5. **User approves the proposed tuning** (critical — no auto-apply; `/balance` is advisory by default).
6. **Delegate to builder** to apply the approved changes to data files.
7. **Delegate to tester** to run a headless balance check if one exists for this system.
8. **Log marker.** `{"skill":"balance","produces":"balanced","feature":"<name>","ts":<iso>}`.

## Output

- Table of values changed: `| param | old | new | reason |`
- Files touched (data files only; no code changes).
- Recommendation for a follow-up `/playtest` to validate the feel.

## Do not

- Do not change formulas (that's a design change → `/design`).
- Do not change code logic (that's `/build`).
- Do not apply tuning without user approval.
- Do not tune blindly. If there's no target curve, ask.
