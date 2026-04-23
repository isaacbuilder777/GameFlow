---
name: ship
description: Package a release — changelog, version bump, patch notes, storefront copy, tag/push commands. Invokes the releaser agent. Use when reviewed AND tested markers are both present for the work being shipped.
---

# /ship

Turn a verified build into a release.

## Preconditions

All three must hold. Refuse with a specific reason if any fail:

- `reviewed` marker present in `production/skill-log.jsonl`
- `tested` marker present
- Working tree clean (`git status` shows no uncommitted changes)

## Steps

1. **Verify preconditions.** Refuse and list any missing.
2. **Ask the version bump.** Major / minor / patch? Show examples of what each means in this project's context.
3. **Delegate to releaser agent** with bump and a summary of what's being released (read recent log entries + git log since last tag).
4. **Releaser produces:**
   - `CHANGELOG.md` entry under `## [Unreleased]` (or promote to version number), categorized.
   - Version bump wherever the version lives.
   - Patch notes at `docs/releases/vX.Y.Z.md` (player-facing).
   - Short storefront/community blurb (3-5 sentences).
   - Exact `git tag` and `git push` commands.
5. **Director gate:**
   - `solo` — skip.
   - `lean` — director reviews and approves. If rejected, do NOT log `released`.
   - `full` — director approves bump only (already approved at phase transition).
6. **Log marker.** `{"skill":"ship","produces":"released","version":"X.Y.Z","ts":<iso>}`.

## Output

- Files written/updated (paths).
- The exact tag + push commands (user runs them).
- Reminder: `/ship` does NOT push or upload to storefronts. User does.

## Do not

- Do not run `git push`, `git tag`, `steam upload`, `butler push`, or any publish command.
- Do not edit game content or code. Last-minute bugs kick back to builder.
- Do not skip patch notes. Players read them.
