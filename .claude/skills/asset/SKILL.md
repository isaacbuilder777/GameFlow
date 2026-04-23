---
name: asset
description: Asset spec and naming audit for the assets/ directory. Writes asset specs (resolution, format, count needs), validates naming conventions, flags stale or orphaned files. Use before requesting art/audio from yourself or a contractor, or periodically to keep the asset tree tidy.
---

# /asset

Keep `assets/` disciplined.

## Modes

- `/asset spec <feature>` — write an asset spec document (what art/audio is needed for this feature).
- `/asset audit` — validate naming conventions and flag orphaned files across `assets/`.
- `/asset count` — report current asset inventory.

## /asset spec `<feature>`

1. **Read `design/<feature>.md`** — implied asset needs come from systems and levels.
2. **Delegate to designer** to enumerate required assets with specs:
   - **Sprites/meshes:** dimensions or poly budget, style notes, variants
   - **Animations:** frame counts, FPS, states
   - **Audio:** type (SFX/music/VO), length, channel count, format
   - **UI:** resolution targets, atlas or individual, states (normal/hover/pressed/disabled)
3. **Write to `design/assets-<feature>.md`:**

```
# Assets: <feature>

## Summary
Total: X sprites, Y animations, Z SFX, W music tracks

## Sprites
| name | size | variants | reference |

## Animations
| name | frames | fps | states |

## Audio
| name | type | length | format | notes |

## Style notes
<palette, mood, reference images>

## Directory destination
assets/<category>/<feature>/<files>
```

4. **Log marker.** `{"skill":"asset","produces":"asset_spec","feature":"<name>","ts":<iso>}`.

## /asset audit

1. **Load `.claude/rules/assets.md`** for naming conventions.
2. **Walk `assets/`** and report:
   - Files violating naming rules (case, separators, category prefixes).
   - Orphaned files (assets not referenced in any `src/` or `design/` file).
   - Duplicates (same content hash, different names).
   - Oversized files (exceeding per-type thresholds in rules).
3. **Output a fix list** — the user decides what to rename/delete. Do NOT auto-fix.

## /asset count

Produce a table:
```
| category      | count | total size |
| sprites       |   42  |   8.3 MB  |
| animations    |   12  |   2.1 MB  |
| audio/sfx     |   88  |  14.2 MB  |
...
```

## Do not

- Do not create binary assets yourself. This skill writes specs and audits; humans or generators make the files.
- Do not rename or delete files without user approval.
- Do not edit `.claude/rules/assets.md` through this skill — rule changes go through a PR the user reviews.
