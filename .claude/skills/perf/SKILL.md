---
name: perf
description: Performance pass — frame budget, allocation hotspots, draw calls, shader cost. Invokes builder or reviewer in diagnostic mode. Use before ship on any frame-rate-sensitive feature, or when a playtest reported hitches or slowness.
---

# /perf

Find and fix performance regressions before they ship.

## Modes

- `/perf scan` — static analysis: identify hot paths and red flags from code alone.
- `/perf profile <scene>` — suggests profile command for the engine + what to look for.
- `/perf budget` — show the project's perf budget and check current worst-case against it.

## /perf scan

1. **Identify hot paths:** scan `src/gameplay/**`, `src/engine/**`, `src/ai/**` for:
   - Per-frame allocations (new arrays, closures, string concatenations inside Update/tick/process functions).
   - Unbounded loops (iterating entire entity lists instead of spatial queries).
   - Inefficient lookups (`GameObject.Find`, `get_tree().get_nodes_in_group` in hot paths).
   - Synchronous I/O on main thread.
2. **Load `.claude/engine.md` flags** for engine-specific perf patterns.
3. **Produce a report:**
```
## Hot path concerns
- <path:line> — <concern> — <why it matters> — <suggested fix direction>

## Allocation concerns
- <path:line> — <what allocates> — <how often>

## Engine-specific flags
- <path:line> — <rule violated>
```

## /perf profile `<scene>`

1. **Suggest the exact profile command** for the current engine:
   - Godot: `godot --debug --verbose --profile-filter <scene>`, or launch editor with Profiler.
   - Unity: "Open Profiler window, enter Play mode, capture frame, look at Scripting/Rendering/Physics."
   - Unreal: `stat unit`, `stat scenerendering`, `Insights`.
2. **List what to measure:**
   - CPU frame time breakdown
   - GC allocs per frame
   - Draw call count
   - Set pass count
   - Physics step time
3. **User runs the profile** and pastes results back. Then delegate to reviewer to interpret.

## /perf budget

1. **Read perf budget** from `design/vision.md` or `design/perf-budget.md` if exists. If neither, ask user to define:
   - Target FPS (60? 30? 120?)
   - Target platform (PC / Switch / mobile / web)
   - Per-system budget in ms (gameplay update: Xms, rendering: Yms, AI: Zms)
2. **Check current worst-case** against budget (from last `/perf profile` report, if one exists).
3. **Flag systems over budget** with suggested direction.

## Common output

Log marker: `{"skill":"perf","produces":"perf_checked","ts":<iso>}`.

Suggested next: `/build` to address specific issues, then re-run `/perf`.

## Do not

- Do not auto-optimize. Premature optimization is real — verify a thing is actually slow before rewriting it.
- Do not run profilers. Engines need human-in-loop for real profiling.
- Do not accept "probably fine" for ship-critical code. Measure.
