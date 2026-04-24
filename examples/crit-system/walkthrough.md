# Walkthrough: adding a crit system to a Godot roguelite

This is a complete trace of running GameFlow to design, build, test, review, and ship a critical-hit system for a small melee-combat game. Every file in this folder was produced by one of the skills during the session.

## The game (context only)

A 2D top-down hack-and-slash roguelite. Short runs (~20 min), stat-driven combat, no cover or stealth. Target platform: PC, Godot 4.3, 60 FPS. The project has a working melee attack system with fixed damage; this session adds critical hits.

## The session

### Step 1: `/start` (skipped — project was already initialized)

`.claude/engine.md` already said `godot 4.3`, so `/next` sent us straight to `/design`.

### Step 2: `/next`

```
## Project state
- Last skill: /build (stamina-system) 3 days ago
- Engine: godot 4.3
- Review mode: lean
- Markers present: project_initialized, design_doc, implementation, reviewed, tested, released

## Recommended next
**/design** — start a new feature

## Also available
- /playtest — capture feedback on the current build
- /learn — if anything surprising happened last session
```

I typed `/design crit-system`.

### Step 3: `/design crit-system`

Claude became the **designer**. It asked four clarifying questions:

1. **"What drives crit chance — a stat, an ability unlock, or both?"** → I said "luck stat, scaling linearly."
2. **"Should crit damage be additive or multiplicative?"** → I said "multiplicative."
3. **"Should the system show a visual indicator to the player?"** → I said "yes, yellow damage number popup."
4. **"Should enemies be able to crit, or is this player-only?"** → I said "player-only for now, design the data structure so enemies could use it later."

Designer presented three approaches: (A) pure luck-driven, (B) luck + per-weapon crit base, (C) luck + weapon + per-ability modifier. I picked B because the game has weapons but not distinct abilities.

Designer wrote `design/crit-system.md` in about 45 seconds.

The Open Questions section had two items:
- "What's the max crit chance cap?"
- "Does crit damage get clamped or is it raw?"

I answered both: cap at 50%, damage uncapped. Designer updated the doc and replaced the section with "None."

Logged marker: `design_doc`.

### Step 4: `/build crit-system`

Claude became the **builder**. It loaded:
- `design/crit-system.md` (Open Questions confirmed empty)
- `.claude/engine.md` (Godot 4.3 conventions: signals, exported resources, no `get_node` string paths)
- `.claude/rules/code.md` (gameplay path rules: data-driven values, no UI refs, no per-frame allocs)

It wrote:
- `src/gameplay/crit.gd` — the crit roll function and signal emission
- It declined to create a `.tres` resource file directly (those are binary), instead it added a `@export` variable on the player and a comment telling me to create the resource in the Godot editor.

Files touched: 1 created (`src/gameplay/crit.gd`), 1 modified (`src/gameplay/player.gd` to wire it up).

Logged marker: `implementation`.

The builder reported one design gap it filled in: the design didn't specify whether the crit signal should carry the rolled chance value (for logging). Builder included it to aid debugging but flagged it for my review. I approved.

### Step 5: `/test crit-system`

Claude became the **tester**. It detected the project uses gdUnit4 (from `project.godot`), wrote four tests against the design's Formulas and Edge cases sections:

1. `test_zero_luck_gives_base_chance`
2. `test_crit_chance_clamps_at_50_percent`
3. `test_crit_damage_is_multiplicative`
4. `test_crit_emits_signal_with_chance`

All four passed on first run. Coverage delta: +4 tests, +12% on `crit.gd`.

Logged marker: `tested`.

### Step 6: `/review crit-system`

Claude became the **reviewer**. It diffed `src/gameplay/crit.gd` and `src/gameplay/player.gd` against the design doc and path-scoped rules. It produced a structured report (`production/review-report.md`).

- **Must fix:** None
- **Should consider:** two items (signal name consistency, narrower type hint)
- **Nitpicks:** one item (docstring)
- **Design fit:** aligned

Since Must-fix was empty, the marker was logged: `reviewed`.

I addressed the two Should-consider items in a follow-up `/build` pass (5 minutes of work), then re-ran `/review` — clean.

### Step 7: `/ship`

Preconditions all held:
- `reviewed` marker: yes
- `tested` marker: yes
- Working tree: clean (I'd committed after `/review`)

Claude became the **releaser**. It asked major/minor/patch — I said minor (new gameplay system). It:

- Added an entry to `CHANGELOG.md` under `### Added` in `## [Unreleased]`
- Bumped version in `project.godot`: `0.3.0` → `0.4.0`
- Wrote `docs/releases/v0.4.0.md` with player-facing patch notes
- Wrote a short storefront blurb for the game's Discord

Suggested commands (which I ran myself):
```
git tag -a v0.4.0 -m "v0.4.0 — Critical hits"
git push origin main --tags
```

Logged marker: `released`.

### Step 8: `/learn`

Not every session produces a lesson. This one did — the designer's push to distinguish weapon-base crit vs. pure-luck crit (option B vs. A) turned out to be exactly the right call because the next planned feature (elemental weapons) needs weapon-specific modifiers. I ran `/learn` and captured it as a `feedback` memory about weapon-system design choices.

## Session totals

- **Wall time:** ~35 minutes (10 min design, 6 min build, 4 min test, 4 min review, 3 min ship, 2 min learn, ~6 min of me resolving open questions and reading diffs)
- **Files produced:** 5 code/test files, 3 design/report files, 1 changelog entry, 1 release note, 1 memory entry
- **Rework loops:** 1 (Should-consider items after review)

## Takeaways

- The graph's discipline paid off most at `/build`, which refused to proceed until I'd actually decided the two Open Questions. Without it I'd have picked something reasonable and discovered inconsistency a week later.
- The reviewer finding "None" in Must-fix gave real confidence before ship. The two Should-consider items weren't blocking but were worth fixing.
- `/learn` only runs when there's a lesson. Most sessions won't need it. This one did.
