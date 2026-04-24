# Crit System

## Goal

Add critical hits to melee attacks so that the Luck stat and weapon crit-base stat become meaningful progression choices. A crit produces a visible yellow damage popup and audibly cues the player that a roll went their way. This supports pillar 1 (stat-dense runs) and pillar 2 (readable combat).

## Non-goals

- Ranged weapons crit (out of scope for this release; revisit when ranged weapons ship).
- Crit affecting status-effect application (no "crit chance to double poison stacks" — future system).
- Enemy crits against the player. Data structure is designed to allow it later; behavior is player-only for now.

## Approach

On each successful melee hit, roll a crit check. If it crits, multiply the weapon's base damage by the crit multiplier before any other modifiers (armor reduction, elemental, etc.). Emit a signal the UI listens for to draw a yellow popup. Play a distinct crit SFX.

The crit roll reads from two sources:
1. **Character luck stat** — contributes linearly to crit chance.
2. **Weapon crit base** — a flat crit chance per weapon (dagger higher, greatsword lower).

A single `CritResolver` utility class performs the roll and returns a `CritResult` struct with `is_crit`, `damage_multiplier`, and `rolled_chance` (for debug logging).

## Formulas

```
crit_chance = clamp(weapon.crit_base + character.luck * 0.01, 0.0, 0.5)
is_crit     = rng.randf() < crit_chance
damage_out  = is_crit ? (damage_in * weapon.crit_multiplier) : damage_in
```

- `character.luck` is an integer stat (typical range 0–50, hard cap 100).
- `weapon.crit_base` is a float between 0.0 and 0.3, set per-weapon resource.
- `weapon.crit_multiplier` is a float, typical range 1.5 to 3.0, set per-weapon resource.
- Max crit chance is clamped to 50%.

## Edge cases

1. **Luck = 0 and weapon crit_base = 0** → crit_chance = 0, never crits. Signal never fires. Tested.
2. **Luck = 200 and weapon crit_base = 0.5** → sum would be 2.5, clamped to 0.5. Tested.
3. **Crit on a final-blow (enemy dies)** → popup still plays, SFX still plays, death-handler runs after signal dispatch. Tested.
4. **Multiple hits in one frame** (AoE weapon) → each hit rolls independently. RNG is not shared across hits. Tested.
5. **Damage reduced to 0 by armor** → crit result is still computed and signaled (for UI), but final damage is 0. Player still gets the audio-visual cue of "you crit, armor ate it."

## Tradeoffs

- **Multiplicative over additive** — simpler math, scales naturally with weapon upgrades, matches genre convention (Diablo, PoE, most roguelites). Additive crit damage would require a separate balance pass on every stat tier.
- **Weapon crit base + luck over luck-only** — gives weapon identity (pillar 3). A dagger with 15% base crit feels different from a greatsword with 2%. Pure luck-only would make weapons differ only in damage, which flattens identity.
- **Clamp to 50% over uncapped** — avoids degenerate builds where 100% crit becomes "there's no non-crit." Keeps the excitement of the roll.
- **Single `CritResolver` over per-weapon logic** — one place to test and tune. Weapons contribute data, not logic.

## Open questions

None.
