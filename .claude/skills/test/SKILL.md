---
name: test
description: Write and run verification. Invokes the tester agent. Use after /build to add coverage, or anytime to run existing tests. Does not fix bugs (those go to builder).
---

# /test

Verify behavior matches design.

## Modes

- `/test` — run the existing suite, report results.
- `/test <feature>` — author tests for a feature against `design/<feature>.md`, then run them.
- `/test --smoke` — fast smoke subset only.
- `/test --qa` — generate/update a manual QA script in `tests/qa/<feature>.md`.

## Steps

1. **Detect test runner** based on engine and project:
   - Godot → `gut` or `gdunit4`, invoked via `godot --headless --script ...`
   - Unity → Unity Test Framework (Edit/Play mode)
   - Unreal → Automation Framework, via `UE4Editor-Cmd.exe ... -ExecCmds="Automation ..."`
   - Pure Python/Rust/etc. code → `pytest` / `cargo test`
   - Ask user if ambiguous.
2. **Delegate to tester agent** with mode, feature name, runner.
3. **Tester authors** tests (if feature mode) under `tests/` mirroring `src/` layout, then runs the suite.
4. **Collect evidence** — command, results, skipped, coverage delta, duration, flakes.
5. **Log marker** only on clean pass. `{"skill":"test","produces":"tested","ts":<iso>}`. On failure, do NOT log.

## Output

Evidence report from the tester. Plus:
- `tested` marker logged? (yes/no)
- Failing test list if any, with suggested next step (likely `/build` to fix).

## Do not

- Do not log `tested` on a failing or flaky run.
- Do not count retries as passes.
- Do not generate tests that don't reflect the design. Tests verify intent.
