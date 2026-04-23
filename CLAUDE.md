# GameFlow

A lean Claude Code template for indie and solo game development. 6 roles, 12 skills, one dependency graph. Turns a Claude Code session into a coordinated studio without the 49-agent ceremony.

## What this is

An opinionated workflow for shipping games: design → build → test → review → ship, enforced by a skill dependency graph so you can't accidentally skip a step. Agents adapt to your engine (Godot / Unity / Unreal) via a single config file instead of a pile of specialist agent files.

## Engine

Set your engine and version in `.claude/engine.md`. The builder and reviewer load this automatically when touching engine-specific code (shaders, ECS, Blueprints, GDExtension, etc.). Supported: **Godot 4**, **Unity 2022+**, **Unreal 5**, or `custom` for your own engine.

## Review intensity

Set in `production/review-mode.txt`, override per-skill with `--review <mode>`:

- **`solo`** — no director gates. Fast, one-pass. Best for prototyping or small fixes.
- **`lean`** — director approves phase transitions only (design→build, build→ship). Default.
- **`full`** — director reviews every significant decision. Use for your main project's core features.

## Roles (6, not 49)

| Role | Covers (inline sub-specialization) |
|---|---|
| **director** | Creative vision, pillars, genre fit, scope protection, final approval |
| **designer** | Game design, systems, economy, level design, narrative, UX, accessibility |
| **builder** | Gameplay code, engine code, AI, shaders/VFX, networking, UI, tools |
| **reviewer** | Code quality, rule enforcement, design-fit, game feel |
| **tester** | Automated tests, playtest scripts, manual QA, balance validation |
| **releaser** | Build pipelines, storefront packaging, changelogs, patch notes |

The original's `gameplay-programmer` / `engine-programmer` / `ai-programmer` / `tools-programmer` / `network-programmer` / `ui-programmer` are all **builder** — one role with inline sub-specialization. Prompts say "if editing `src/gameplay/**`, do X; if editing `src/engine/**`, do Y." LLMs don't need org charts; they need sharp prompts.

## Skills (12, not 72)

**Core workflow (8):**

- `/start` — pick engine, set pillars, initialize project
- `/next` — graph-driven recommendation for what to do next
- `/design` — produce a GDD section for a feature or system
- `/build` — implement from an approved design
- `/review` — quality pass against rules and design
- `/test` — author and run verification
- `/ship` — package a release with changelog and patch notes
- `/learn` — capture lessons to Claude memory so future sessions start smarter

**Game-specific (4):**

- `/balance` — tune numbers against design formulas (damage curves, economy, drop rates)
- `/playtest` — structured playtest report (what worked, what didn't, next hypothesis)
- `/asset` — asset spec + naming audit for `assets/`
- `/perf` — performance pass (frame budget, alloc hotspots, draw calls)

That's it. No `/team-combat`, `/team-narrative`, `/team-ui` — those were parameters, not skills. No `/create-epics`, `/sprint-plan`, `/retrospective` — solo/small-team dev doesn't need sprint ceremony.

## Skill dependency graph

`.claude/graph.yaml` defines prerequisites:

```
/design      requires project_initialized
/build       requires design_doc
/review      requires implementation
/test        requires implementation
/ship        requires reviewed AND tested
/balance     requires design_doc
/playtest    requires implementation
/asset       requires project_initialized
/perf        requires implementation
```

`/next` reads the graph + `production/skill-log.jsonl` and tells you what's ready. No heuristics, no `/project-stage-detect` guessing.

## Path-scoped rules

Automatically loaded when editing matching paths:

| Path | Rule |
|---|---|
| `src/gameplay/**` | Data-driven values, delta-time correct, no UI refs, no per-frame allocs |
| `src/engine/**` | Zero allocations in hot paths, thread safety, API stability |
| `src/ai/**` | Performance budgets, debuggable decisions, data-driven parameters |
| `src/networking/**` | Server-authoritative, versioned messages, no trust of client |
| `src/ui/**` | No game state ownership, localization-ready, accessibility |
| `src/shaders/**` | GPU cost budget, platform fallbacks |
| `design/**` | Required GDD sections, formulas over prose |
| `assets/**` | Naming conventions, file-size limits, metadata present |

All defined in `.claude/rules/code.md`, `.claude/rules/docs.md`, `.claude/rules/assets.md`.

## Hooks

Three Python hooks, fail-soft if Python is missing:

- `session_start.py` — orients Claude with git state, engine, and last skill run
- `pre_tool.py` — blocks risky bash (`git push --force`, `rm -rf /`, `--no-verify`)
- `post_skill.py` — logs skill completion to `production/skill-log.jsonl`

## How agents coordinate

- Explicit delegation via the Agent tool. Director doesn't "auto-route" — a skill decides which role to invoke.
- Director breaks ties. Designer and builder disagree on scope? Director decides.
- Roles respect file scope. Builder doesn't edit `design/`. Designer doesn't edit `src/`. Enforced by review.
- Memory is shared state across sessions. `/learn` writes to `~/.claude/memory/` — the template compounds.

## Compared to Claude-Code-Game-Studios

|  | Game Studios (original) | GameFlow |
|---|---|---|
| Agents | 49 across 3 tiers | 6 flat |
| Skills | 72 | 12 |
| Hooks | 12 bash scripts | 3 Python |
| Doc templates | 39 files | generated inline against rules |
| Engine support | 3 specialist agent sets | 1 config file |
| Ordering | heuristic `/project-stage-detect` | deterministic graph |
| Learning across sessions | none | `/learn` → Claude memory |
| Sprint ceremony | `/create-epics`, `/create-stories`, `/sprint-plan`, `/sprint-status`, `/estimate`, `/retrospective` | none (not needed for indie/solo) |

## Philosophy

**Fewer, smarter pieces.** LLMs don't benefit from role-splitting — they benefit from sharp, non-overlapping prompts. The original's 49 agents have routing ambiguity that a solo dev will hit on day one.

**Deterministic over heuristic.** A dependency graph that says "you need a design doc before you can `/build`" is better than a stage-detector that guesses from filenames.

**Compounds across sessions.** `/learn` turns every correction or validation into a memory file, so session 50 is strictly better than session 1.
