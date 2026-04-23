---
scope: design/**, docs/**
---

# Doc rules — design/**, docs/**

Enforced by designer when writing, reviewer when reviewing designs.

## Required sections in feature design docs

Every `design/<feature>.md` must have these H2 headers, in order:

1. **Goal** — player experience enabled, one paragraph
2. **Non-goals** — explicit exclusions; write "None" only if truly trivial
3. **Approach** — chosen design (mechanics, states, flow)
4. **Formulas** — numeric relationships. `damage = base * (1 + crit_mult * crit_chance)`. Not prose.
5. **Edge cases** — at least three; write "None" only if the feature is trivial
6. **Tradeoffs** — what you gave up vs. alternatives
7. **Open questions** — unresolved items; `/build` refuses if this isn't empty or "None"

Missing sections = reject. Don't silently delete headers.

## Style

- **Formulas over prose.** Numeric relationships in code-block formulas.
- **Numbers, not adjectives.** "Completes in under 200ms," not "fast."
- **Diagrams in ASCII or Mermaid.** Embedded images rot; text survives.
- **Second person for player experience.** "You unlock..." not "The player unlocks..."

## Forbidden

- Aspirational sections ("future expansion", "v2 ideas") in a feature doc. Separate file if needed.
- Code blocks over 20 lines. Link to the file.
- "Here we..." narrator voice. Declarative only.

## Vision doc

`design/vision.md` is the contract. It answers:

- **Who is this for?** — target player profile
- **What is it?** — one-sentence elevator pitch
- **Pillars** — 3-5 sentences defining what this game IS
- **What it is NOT** — 2-3 adjacent-but-wrong directions

Changes to `vision.md` require director approval in `lean` or `full` review modes.

## Docs directory

`docs/` is for long-form and external-facing material:

- `docs/releases/vX.Y.Z.md` — player-facing patch notes
- `docs/adr/NNNN-title.md` — architecture decision records
- `docs/onboarding.md` — for collaborators joining the project
