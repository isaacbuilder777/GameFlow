# GameFlow

A Claude Code project template for indie and solo game development. Turns a Claude Code session into a coordinated studio with six specialized roles, twelve workflow commands, and a dependency graph that tells you what to do next.

## What it gives you

- **Six roles** Claude can step into — director, designer, builder, reviewer, tester, releaser. Each has a defined scope and delegates to the others.
- **Twelve slash commands** covering the full lifecycle: design, build, review, test, ship — plus game-specific commands for balance tuning, playtesting, asset planning, and performance.
- **A skill dependency graph** so `/next` can always tell you what's ready to work on and what's still blocked.
- **Path-scoped rules** that automatically enforce different coding standards for gameplay, engine, AI, networking, UI, shaders, and tools.
- **Engine awareness** — one config file (`.claude/engine.md`) teaches Claude the conventions for Godot 4, Unity, Unreal 5, or your custom engine.
- **Review modes** — `solo`, `lean`, or `full` — controlling how much gatekeeping happens on each change.
- **Python hooks** that orient Claude at session start, block risky bash commands, and keep a skill-completion log.
- **Cross-session memory** — `/learn` captures lessons into Claude's memory so the next session starts smarter than the last.

## Setup

```
git clone https://github.com/isaacbuilder777/GameFlow.git my-game
cd my-game
claude
```

Then run `/start` on your first session. It will ask:

- Which engine you're using (and its version)
- Your review mode
- Your game's pillars (3-5 sentences on what the game IS)

From there, type `/next` any time you're unsure what to do.

## The twelve commands

**Core workflow:**

| Command | Purpose |
|---|---|
| `/start` | Initialize the project: pick engine, set pillars, choose review mode |
| `/next` | Read the dependency graph and recommend the next command |
| `/design` | Write a design doc for a feature, system, level, or narrative beat |
| `/build` | Implement from an approved design |
| `/review` | Quality pass against rules and design-fit |
| `/test` | Author and run verification |
| `/ship` | Package a release with changelog and patch notes |
| `/learn` | Capture a lesson to Claude memory for future sessions |

**Game-specific:**

| Command | Purpose |
|---|---|
| `/balance` | Tune numeric values against design formulas |
| `/playtest` | Structured playtest report with hypothesis and follow-ups |
| `/asset` | Asset specs, naming audits, and directory checks |
| `/perf` | Frame budget, allocation hotspots, draw calls |

## The six roles

| Role | What it owns |
|---|---|
| **director** | Creative vision, game pillars, genre fit, scope protection, final approvals |
| **designer** | Game design, systems, economy, level design, narrative, UX, accessibility |
| **builder** | Gameplay, engine, AI, shaders, networking, UI, and tooling code |
| **reviewer** | Code review, rule enforcement, design conformance |
| **tester** | Unit, integration, and smoke tests, plus manual QA scripts |
| **releaser** | Build packaging, changelogs, patch notes, storefront copy |

Roles delegate explicitly and stay in their lane. The designer doesn't write code; the builder doesn't rewrite designs; the reviewer critiques but doesn't apply fixes.

## Layout

```
.claude/
  settings.json       hooks + permission rules
  graph.yaml          skill dependency graph
  engine.md           your engine config
  agents/             6 role definitions
  skills/             12 slash-command instruction files
  hooks/              3 Python hooks (session start, pre-tool, post-skill)
  rules/              code, docs, and assets rules
design/               vision and feature design docs
src/                  gameplay, engine, ai, networking, ui, shaders, tools
assets/               sprites, models, animations, audio, data
tests/                unit, integration, playtest scripts
production/           review mode, skill log, playtest reports
prototypes/           throwaway experiments (isolated from src/)
docs/                 ADRs, release notes, onboarding
```

## Philosophy

Games ship when the loop is clear: design → build → test → review → ship. GameFlow makes that loop explicit. A dependency graph means you can't accidentally skip a step. Path-scoped rules mean your gameplay code doesn't drift into a tangled mess while your engine code calls for a different discipline. Review modes mean a prototype can move fast while a core feature gets the gates it deserves.

The template is opinionated on structure and silent on everything else — it tells you when to design and when to build, but never what to design or how to build it. Those calls stay with you.

## License

MIT.
