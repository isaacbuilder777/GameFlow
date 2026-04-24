# Examples

This directory contains complete traces of running the GameFlow workflow on real features. Each example shows every artifact the skills produce, so you can see what a full `/start` → `/design` → `/build` → `/test` → `/review` → `/ship` loop looks like before you run one yourself.

## What's here

- [`crit-system/`](./crit-system/) — Adding critical hits to a Godot 4 hack-and-slash roguelite. Demonstrates the full core loop on a small, self-contained feature.

## How to read an example

Each example folder contains:

- `walkthrough.md` — narrative of the session: what was typed, what each role produced, how long each step took
- `design/vision.md` — the game's pillars (the "contract" the feature must fit)
- `design/<feature>.md` — the GDD the designer produced
- `src/` — the code the builder wrote
- `tests/` — the tests the tester wrote and ran
- `production/skill-log.jsonl` — the dependency-graph markers written by the hooks
- `production/review-report.md` — the reviewer's structured output
- `CHANGELOG-excerpt.md` — the changelog entry the releaser produced

Start with `walkthrough.md` to follow the session chronologically, then read the artifacts in the order they were produced.
