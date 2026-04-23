---
name: start
description: Initialize the project. Picks engine, writes game pillars into vision doc, sets review mode. Run once at project start, or when adopting an existing game project into GameFlow. Do not run twice on an already-initialized project.
---

# /start

Deterministic onboarding. No guessing.

## Steps

1. **Detect state.** Check for existing config:
   - `.claude/engine.md` already has a specific engine set? → project is initialized; redirect to `/next`.
   - `design/vision.md` exists? → this may be an adoption; ask the user if they want to adopt.
   - Fresh or mostly-empty? → normal flow.

2. **Ask four questions** (use AskUserQuestion if available):
   - **Engine:** `godot`, `unity`, `unreal`, or `custom`?
   - **Engine version:** (e.g., Godot 4.3, Unity 2022.3 LTS, UE5.4, or your custom version)
   - **Review mode:** `solo`, `lean`, or `full`?
   - **Game pillars:** 3-5 short sentences. What IS this game? What makes it feel different from adjacent games?

3. **Write config:**
   - `.claude/engine.md` ← update "Current engine" section, remove the unused engine blocks (keep the chosen one's reference section).
   - `production/review-mode.txt` ← chosen mode.
   - `design/vision.md` ← four sections filled in:
     - **Who is this for?** (ask the user; genre-literate audience or broader?)
     - **What is it?** (one-sentence elevator pitch; ask)
     - **Pillars** (the user's 3-5 sentences, verbatim)
     - **What this game is NOT** (ask the user to name 2-3 adjacent-but-wrong directions)
   - `production/skill-log.jsonl` ← create empty if missing.

4. **Log marker.** Append `{"skill":"start","produces":"project_initialized","ts":<iso>}`.

5. **Recommend next.** Usually `/design` for the core gameplay loop, then `/asset` to plan art/audio naming, then `/build`. Show those three as the typical path.

## Do not

- Do not write any design details beyond pillars — that's `/design`.
- Do not pick an engine for the user. Ask.
- Do not assume the genre from anything — ask.
