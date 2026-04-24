# Review — crit-system

Reviewed diff of `src/gameplay/crit.gd` (new) and `src/gameplay/player.gd` (modified) against `design/crit-system.md` and `.claude/rules/code.md` (gameplay scope) and `.claude/engine.md` (Godot 4.3 conventions).

## Must fix

None.

## Should consider

- **src/gameplay/crit.gd:3** — Signal `crit_rolled` is defined on the class but `CritResolver` is a static utility that doesn't instance. Signals on a `RefCounted` that only runs static methods won't fire. Options: (a) move the signal to `player.gd` where the roll is invoked, (b) make `CritResolver` a non-static instance and have player hold a reference. Recommend (a) — simpler, keeps utility pure. The design specifies "emit a signal the UI listens for" but doesn't specify which class owns it.
- **src/gameplay/crit.gd:10** — Return type `CritResult` is a nested class. Godot's type system handles it, but it's unusual enough that a `class_name CritResult` in its own file would make it discoverable in the inspector and easier to extend. Not required; keeps file count down if left nested.

## Nitpicks

- **src/gameplay/crit.gd:6** — Add a short docstring on `roll()` noting the clamp behavior. The design has it but the code reader won't have the design open.

## Design fit

Aligned. All five edge cases from `design/crit-system.md` are covered by tests. Formula matches the design exactly. Multiplicative damage per the chosen tradeoff. No scope drift.

## Verdict

Marker `reviewed` logged. No Must-fix items block ship. The two Should-consider items are worth a follow-up `/build` pass but are not blocking — the system functions correctly as-is for single-player, and the signal concern only matters when the UI starts listening for it.
