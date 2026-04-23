---
name: learn
description: Capture a non-obvious lesson from this session to Claude memory, so future sessions inherit it. Use after finishing a feature, debugging a tricky issue, getting correction feedback, or making a non-obvious call that worked. Compounds — the template gets smarter each session.
---

# /learn

Capture a lesson so the next session is strictly better than this one. This is the compounding edge GameFlow has over static templates.

## What to capture

- **Corrections** — user corrected the approach ("no, not that — do X because Y"). Save as `feedback`.
- **Validations** — user confirmed a non-obvious choice worked. Save as `feedback`.
- **Project facts** — deadlines, platform constraints, stakeholder asks, target audience tweaks. Save as `project`.
- **References** — external tools, dashboards, asset libraries, art style references. Save as `reference`.
- **User info** — "I'm a solo dev," "I've shipped Unity games before but new to Godot," etc. Save as `user`.

## What NOT to capture

- Game design patterns derivable from the code or `design/` (those are already persisted).
- Commit history (git knows).
- Fix recipes (the fix is already in the code; the commit message explains).
- In-progress task state (belongs in task tracking, not memory).

## Steps

1. **Ask one question** (or use the user-provided arg):
   "What's the one thing from this session that would help a future session on this project?"
2. **Classify** into one of: `user`, `feedback`, `project`, `reference`.
3. **Check existing memory** at `~/.claude/memory/MEMORY.md` for duplicates/related entries. Update in place if one exists.
4. **Write memory file** at `~/.claude/memory/<topic>.md` with frontmatter (name, description, type) and body.
   - For `feedback` and `project`: include **Why:** and **How to apply:** lines.
5. **Update `MEMORY.md` index** — one line: `- [Title](file.md) — one-line hook`.
6. **Log marker.** `{"skill":"learn","produces":"lesson_captured","ts":<iso>}`.

## Output

- Memory file path.
- One-sentence summary of what was captured.
- Confirmation that future sessions will auto-load it.

## Do not

- Do not capture obvious or ephemeral facts.
- Do not duplicate. Check existing memory first.
- Do not capture things that rot fast (current branch, today's bug).
