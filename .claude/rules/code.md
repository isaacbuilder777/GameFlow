---
scope: src/**
---

# Code rules — src/**

Enforced by the builder when writing and the reviewer when reviewing. Sections apply based on file path.

## General (all of src/)

1. **No dead code.** If it's not called, delete it. No speculative helpers "for later."
2. **No error handling for impossible states.** Validate at boundaries (user input, file I/O, network); trust internals.
3. **Comments explain WHY, not WHAT.** Default to zero comments. If removing the comment wouldn't confuse a reader, don't write it.
4. **Named constants at module top; magic numbers inside formulas are OK.** `MAX_RETRIES = 3` up top, not buried in logic.
5. **Small diffs.** One feature per change. No refactoring bundled with feature work.
6. **No `catch Exception` / `except:` without specific handling or re-raise.**

## src/gameplay/**

- **Data-driven values only.** Read from resource files (`.tres` / ScriptableObjects / data tables). No hardcoded tuning numbers.
- **Delta-time correct.** `position += velocity * delta`. Never assume fixed framerate.
- **No UI references.** Gameplay emits events; UI listens. Do not import UI classes from gameplay.
- **No per-frame allocations.** Pool anything created more than once per second.

## src/engine/**

- **Zero allocations in hot paths.** Use object pools, preallocated arrays, stack alloc where possible.
- **Thread safety.** Document and enforce invariants for anything accessed from multiple threads.
- **API stability.** Breaking changes require updating all call sites in the same commit.

## src/ai/**

- **Performance budget.** Stay under the per-frame budget in `design/perf-budget.md` or `design/vision.md`.
- **Debuggable decisions.** AI logs *why* it chose an action in dev builds — structured entries, not print spam.
- **Data-driven parameters.** Aggression, flee thresholds, etc. live in resources, not code.

## src/networking/**

- **Server-authoritative.** Client sends intent; server validates and responds. Never trust client state.
- **Versioned messages.** Every packet has a version field; old clients fail gracefully.
- **No PII in logs.** Player input may contain personal info — scrub before logging.
- **No client-side game logic** that affects authoritative state (movement prediction is OK; damage calc is not).

## src/ui/**

- **No game state ownership.** UI reflects state; doesn't own it. Game state lives in gameplay/core.
- **Localization-ready.** User-facing strings route through the localization system from day one.
- **Accessibility.** Keyboard navigation on all controls. Screen-reader hints. No color-only information.

## src/shaders/**

- **GPU cost awareness.** Check instruction count, texture samples, branching. Flag anything over the platform budget.
- **Platform fallbacks.** If targeting mobile or web, provide a simpler variant.
- **Uniform documentation.** Non-obvious shader parameters get a comment explaining the unit and range.

## src/tools/**

- **Idempotent.** Running twice produces the same result as once.
- **Auditable.** Log what the tool changed.
- **Cross-platform.** Game tools should run on all dev machines the team uses.

## Security (all of src/)

- Never log secrets, tokens, or full user input.
- Never build SQL/shell/HTML with string concatenation on untrusted input. Use parameterization.
- Never ship debug-only cheats in release builds. Guard with build flags.
