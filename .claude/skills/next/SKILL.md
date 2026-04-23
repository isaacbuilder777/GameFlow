---
name: next
description: Read the skill dependency graph and project state, then recommend the next skill. Use when you're unsure what to do next, or after any skill finishes. Does not execute the recommendation — only suggests.
---

# /next

Deterministic "what's ready to do" — no guessing.

## Algorithm

1. **Read** `.claude/graph.yaml` — defines skills, their `requires`, and `produces`.
2. **Read** `production/skill-log.jsonl` — each line is a completion marker.
3. **Compute fired markers** — union of all `produces` values across log entries.
4. **Compute ready skills** — skills whose `requires` are all in the fired set.
5. **Detect the current phase:**
   - No `project_initialized` → suggest `/start`.
   - `project_initialized` but no `design_doc` → suggest `/design`.
   - `design_doc` but no `implementation` → suggest `/build`, optionally `/balance` and `/asset`.
   - `implementation` but not both `reviewed` and `tested` → suggest whichever is missing.
   - Both `reviewed` and `tested` → suggest `/ship`.
   - Recently had friction or surprise → suggest `/learn` as a sidebar.
6. **Broadcast ready skills** — show primary recommendation + alternatives.

## Output

```
## Project state
- Last skill: /<name> (<timestamp>)
- Engine: <engine> <version>
- Review mode: <mode>
- Markers present: <list>
- Markers missing: <list>

## Recommended next
**/<skill>** — <why, one sentence>

## Also available
- /<skill> — <why>
- /<skill> — <why>

## Consider
- /learn — if the last session had a correction or a non-obvious success
```

## Edge cases

- **Empty log** → recommend `/start`.
- **Many ready skills** → pick primary by graph order (`design` > `build` > `review` > `test` > `ship`).
- **Commits without matching skill runs** → note the drift ("you have 3 commits since last `/review` — consider running it").
- **`ship` is ready** → briefly acknowledge (one line), then show the command.

## Do not

- Do not auto-invoke the recommended skill.
- Do not recommend `/start` on an initialized project.
- Do not invent markers that aren't in the graph.
