# GameFlow

A Claude Code template for indie and solo game development. A leaner, smarter alternative to [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios).

**6 roles. 12 skills. One dependency graph. Your engine, configured in one file.**

## Why not the original?

The original pioneered the pattern — huge credit for that. But it has real weaknesses for day-to-day solo dev:

- **49 agents is overkill.** `gameplay-programmer` vs `engine-programmer` vs `ai-programmer` vs `tools-programmer` all do the same thing from an LLM's perspective — write code in your project. Role-splitting creates routing ambiguity, not clarity.
- **72 skills is too many to remember.** Past ~15, discovery fails. Most of the 72 are parameters (`/team-combat`, `/team-narrative`, `/team-ui`) or duplicates (`/code-review` + `/design-review` + `/architecture-review`).
- **Heuristic stage detection.** `/project-stage-detect` guesses from filenames. A dependency graph is deterministic.
- **Sprint ceremony for solo devs.** `/create-epics`, `/sprint-plan`, `/retrospective` are enterprise overhead.
- **Static.** The original doesn't learn from your corrections between sessions.
- **Bash hooks on Windows.** Requires Git Bash. Python is cleaner.

## What GameFlow does differently

| | Original | GameFlow |
|---|---|---|
| Agents | 49 | 6 |
| Skills | 72 | 12 |
| Hooks | 12 bash | 3 Python |
| Doc templates | 39 files | generated inline |
| Engine support | 3 agent sets (Godot/Unity/Unreal) | 1 config file |
| Stage detection | heuristic | dependency graph |
| Learns between sessions | no | yes, via `/learn` → Claude memory |
| Sprint ceremony | yes | no |

## Setup

```
git clone <this-repo> my-game
cd my-game
claude
```

Then `/start` — picks your engine, sets game pillars, initializes the project.

## The 12 skills

**Core workflow:** `/start` `/next` `/design` `/build` `/review` `/test` `/ship` `/learn`

**Game-specific:** `/balance` `/playtest` `/asset` `/perf`

Run `/next` anytime you're not sure what to do — it reads the dependency graph and tells you what's ready.

## Engines

Edit `.claude/engine.md` on first run — pick **Godot 4**, **Unity**, **Unreal 5**, or `custom`. The builder and reviewer load this when editing engine-specific code.

## Layout

```
.claude/
  settings.json       hooks + permissions
  graph.yaml          skill dependency graph
  engine.md           your engine config
  agents/             6 roles
  skills/             12 slash commands
  hooks/              3 Python hooks
  rules/              3 path-scoped rule files
design/               GDD and design docs
src/                  gameplay, engine, ai, networking, ui, shaders
assets/               art, audio, data
tests/                unit, integration, playtest scripts
production/           release-mode, skill-log, changelog
prototypes/           throwaway experiments, isolated from src/
```

## License

MIT.
