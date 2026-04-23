---
name: playtest
description: Structured playtest report — hypothesis, observations, what worked, what didn't, next change. Invoke after a play session (solo or external). Produces a dated report in production/playtests/ that feeds back into design and balance decisions.
---

# /playtest

Turn a playtest into actionable signal.

## When to use

- After solo play session of 30+ minutes where you were observing critically.
- After external tester session (friend, discord tester, formal playtest).
- Before any significant design or balance change — you want a baseline report.

## Steps

1. **Ask the structure questions** (if arg not provided, or user wants the full interview):
   - **Hypothesis** — what did you want to learn this session? (e.g., "Is combat paced right at level 5?")
   - **Build version** — commit hash or tag of what was tested.
   - **Tester** — solo, friend, external.
   - **Duration** — minutes played.
   - **What worked** — specific moments, not vague praise.
   - **What didn't** — specific friction points with context.
   - **Surprises** — unexpected reactions, both good and bad.
   - **Next hypothesis** — what should the next playtest test?

2. **Write the report** at `production/playtests/<YYYY-MM-DD>-<feature-or-scope>.md` with those sections.

3. **Cross-reference designs.** For each friction point, note the relevant `design/*.md`. This makes it easy to trace what needs changing.

4. **Propose follow-ups:**
   - If a formula felt wrong → `/balance <system>`
   - If a mechanic felt wrong → `/design <feature>` (revise)
   - If it's a bug → file via commit / issue, route to `/build`
   - If it's unclear → note as "needs another test"

5. **Log marker.** `{"skill":"playtest","produces":"playtested","build":"<version>","ts":<iso>}`.

## Output format (the report)

```
# Playtest: <date> — <scope>

## Hypothesis
<what you wanted to learn>

## Build
<commit or tag>

## Tester(s)
<who, how long>

## What worked
- <specific observation>

## What didn't
- <specific friction with context>

## Surprises
- <unexpected reaction>

## Related designs
- design/<file>.md — <why related>

## Proposed follow-ups
- /balance <system> — <reason>
- /design <feature> — <reason>
- (file bug) — <reason>

## Next hypothesis
<what the next test should check>
```

## Do not

- Do not accept vague observations ("felt fun"). Push for specifics.
- Do not skip the hypothesis. Without a question, you're just noting things.
- Do not propose follow-ups without tying them to specific observations.
