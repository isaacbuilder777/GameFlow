# CHANGELOG excerpt — v0.4.0

This is the entry the releaser wrote to `CHANGELOG.md` under the new version section.

```markdown
## [0.4.0] — 2026-04-22

### Added
- Critical hit system for melee attacks. Crit chance is driven by the Luck stat (linearly) plus each weapon's base crit rate, clamped to 50%. Crits deal `weapon.crit_multiplier` times base damage with a yellow damage popup and distinct audio cue.
```

## Player-facing patch notes

Releaser also wrote `docs/releases/v0.4.0.md`:

```markdown
# v0.4.0 — Critical hits

## Highlights
- Melee attacks can now critically strike. Watch for the yellow numbers.
- The Luck stat is meaningful now — every 100 Luck adds 1% to your crit chance on top of your weapon's base.
- Weapons vary: daggers crit often for moderate multipliers; greatswords crit rarely but hit hard.

## New
- Critical hit system for melee attacks.
- Distinct audio cue on crit.

## Changes & Balance
- All existing melee weapons gained a `crit_base` value (daggers: 15%, swords: 8%, axes: 6%, greatswords: 3%) and a `crit_multiplier` (1.8x–2.5x).

## Fixes
- None in this release.

## Known Issues
- Ranged weapons do not crit yet (coming in a future update).
```

## Storefront / community blurb

Also written by the releaser, for posting to Discord:

> **v0.4.0 is out — Crits!** Melee weapons can now critically strike, driven by Luck and per-weapon crit rates. Daggers are now noticeably spicier. Watch for yellow numbers.
