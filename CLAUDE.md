# GameFlow

A Claude Code template that organizes a game-development session into a coordinated studio. Six roles, twelve commands, one dependency graph.

## What this is

An opinionated workflow for shipping games: design → build → test → review → ship, enforced by a skill dependency graph so steps can't be silently skipped. Roles adapt to your engine (Godot / Unity / Unreal / custom) via a single config file. Review intensity is tunable per-project so prototypes move fast and core systems get the gates they need.

## Engine

Set your engine and version in `.claude/engine.md` on first run. The builder and reviewer load this when touching engine-specific code — Godot signals and GDScript patterns, Unity ScriptableObjects and serialization, Unreal UPROPERTY and replication, or whatever custom engine you've defined.

## Review intensity

Set in `production/review-mode.txt`. Override per-skill with `--review <mode>`.

- **`solo`** — no director gates. One-pass work. Best for prototyping or small fixes.
- **`lean`** — director approves phase transitions only (design→build, build→ship). Default.
- **`full`** — director reviews every significant decision. Use on high-stakes or core features.

## Roles

| Role | What it owns |
|---|---|
| **director** | Creative vision, pillars, genre fit, scope protection, final approval |
| **designer** | Game design, systems, economy, level design, narrative, UX, accessibility |
| **builder** | Gameplay code, engine code, AI, shaders/VFX, networking, UI, tools |
| **reviewer** | Code quality, rule enforcement, design-fit |
| **tester** | Automated tests, playtest scripts, manual QA, balance validation |
| **releaser** | Build packaging, changelogs, patch notes, storefront copy |

Sub-specializations (frontend, backend, ML, shaders, networking, tooling, level design, economy design, narrative) are handled inline by the appropriate role, not as separate agents. The builder reads its path-scoped rules and engine config to know which conventions apply.

## Skills

**Core workflow:**

- `/start` — pick engine, set pillars, initialize project
- `/next` — graph-driven recommendation for what to do next
- `/design` — produce a design doc for a feature or system
- `/build` — implement from an approved design
- `/review` — quality pass against rules and design
- `/test` — author and run verification
- `/ship` — package a release with changelog and patch notes
- `/learn` — capture a lesson to Claude memory so the next session starts smarter

**Game-specific:**

- `/balance` — tune numeric values against design formulas
- `/playtest` — structured playtest report (what worked, what didn't, next hypothesis)
- `/asset` — asset spec writing, naming validation, directory audit
- `/perf` — frame budget, allocation hotspots, draw calls, shader cost

## Skill dependency graph

Defined in `.claude/graph.yaml`. Each skill declares prerequisites:

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

`/next` reads the graph and `production/skill-log.jsonl` and deterministically picks what's ready.

## Path-scoped rules

Automatically applied when editing matching paths:

| Path | Focus |
|---|---|
| `src/gameplay/**` | Data-driven values, delta-time correctness, no UI refs, no per-frame allocs |
| `src/engine/**` | Zero allocations in hot paths, thread safety, API stability |
| `src/ai/**` | Performance budgets, debuggable decisions, data-driven parameters |
| `src/networking/**` | Server-authoritative, versioned messages, no client trust |
| `src/ui/**` | No game state ownership, localization-ready, accessibility |
| `src/shaders/**` | GPU cost budget, platform fallbacks |
| `src/tools/**` | Idempotent, auditable, cross-platform |
| `design/**` | Required GDD sections, formulas over prose |
| `assets/**` | Naming conventions, file-size limits |

Defined in `.claude/rules/code.md`, `.claude/rules/docs.md`, `.claude/rules/assets.md`.

## Hooks

Three Python hooks, fail-soft if Python is missing:

- **`session_start.py`** — orients Claude with branch, uncommitted changes, engine, review mode, and last skill run.
- **`pre_tool.py`** — blocks risky bash (`git push --force`, `rm -rf /`, `--no-verify`, `butler push`, `steamcmd app_update`).
- **`post_skill.py`** — logs Task (agent/skill) completions to `production/skill-log.jsonl`.

## How roles coordinate

- Explicit delegation via Claude Code's Agent tool. A skill picks which role to invoke.
- Director breaks ties when designer and builder disagree on scope or approach.
- Roles respect file scope. Builder doesn't edit `design/`. Designer doesn't edit `src/`. Reviewer flags violations.
- Memory is shared state across sessions. `/learn` writes to `~/.claude/memory/` — the template compounds.

## How the template compounds

`/learn` captures four kinds of lessons:

- **Corrections** — when the user pushed back on an approach, and why.
- **Validations** — when a non-obvious choice worked, and the reasoning.
- **Project facts** — constraints, deadlines, platform targets not visible in code.
- **References** — external systems, dashboards, asset libraries the project relies on.

These land in `~/.claude/memory/` and load automatically at the start of every future session on this project.

## Philosophy

**Deterministic over heuristic.** A dependency graph that says "design before build" is worth more than any number of guesses based on filenames.

**Fewer, sharper pieces.** Each role has a non-overlapping scope and a specific output. Each skill is invoked for one job, not twelve.

**Compounds across sessions.** Every correction or validation captured via `/learn` makes the next session better than the last. A project that runs this template for six months is running a meaningfully smarter version of it than the one that cloned it.
