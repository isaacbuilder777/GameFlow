# Promotion readiness checklist

A running list of what's been done and what's left before this template is ready to share broadly. Honest about gaps.

## Done

- [x] 24-test self-check suite (`tests/template/run_tests.py`), all passing
- [x] Complete working example: [`examples/crit-system/`](../examples/crit-system/) showing a full `/design → /build → /test → /review → /ship → /learn` loop with all produced artifacts
- [x] LICENSE file (MIT)
- [x] README and CLAUDE.md written as standalone docs (no comparative framing)
- [x] Python hooks (cross-platform), validated against risky commands
- [x] Path-scoped rules for code, docs, and assets
- [x] Skill dependency graph (`.claude/graph.yaml`) with internal consistency checks

## Owner-only (the repo owner must do these — not scriptable from this session)

### GitHub repo settings

- [ ] **Add repo description.** Go to the repo page → click the gear icon next to "About" on the right sidebar → set:
  > `A Claude Code template for indie and solo game development. 6 roles, 12 skills, one dependency graph.`
- [ ] **Add topics.** Same dialog → Topics field → add:
  `claude-code`, `anthropic`, `gamedev`, `game-development`, `godot`, `unity`, `unreal-engine`, `indie-game-dev`, `ai-assisted-development`, `template`
- [ ] **Mark as a Template repository.** Repo Settings → under "General" → check "Template repository." Users get a "Use this template" button instead of having to clone and re-init.
- [ ] **(Optional) Set homepage.** In the About dialog, leave homepage empty unless you make one.

### Live dogfooding (the biggest remaining gap)

The `examples/crit-system/` folder demonstrates the full workflow, but it's a constructed example — the skills weren't actually invoked live against a Claude Code session. Before promoting broadly:

- [ ] **Clone the template into a throwaway game project** and run the full `/start → /design → /build → /test → /review → /ship` loop on a small feature. Something small enough to finish in a weekend.
- [ ] **Record every friction point** (skill refused when it shouldn't, Claude invoked the wrong role, graph markers weren't logged, etc.). Fix them.
- [ ] **Commit your session transcripts** or summaries under `examples/<your-feature>/` as a second example. Two examples plus a real "built with GameFlow" credit is meaningfully stronger than one constructed example.

This is non-negotiable if you want to be taken seriously on r/gamedev, Hacker News, or game-dev Discord servers. "I built a tool" gets ignored; "I built a tool and shipped a prototype with it, here's the repo" does not.

### Screencast

- [ ] **Record a 30–60 second screencast** showing:
  1. Open Claude Code in a GameFlow project
  2. Type `/next` — show the recommendation
  3. Type `/design some-feature` — show the designer asking clarifying questions and writing the doc
  4. Type `/build some-feature` — show a few lines of generated code
  5. Type `/review` — show the structured report
  6. Fade out
- [ ] **Embed in README.** Either as an animated GIF (ScreenToGif on Windows, Kap on Mac) under the intro paragraph, or as a YouTube/Loom embed.

Recording tools:
- Windows: [ScreenToGif](https://www.screentogif.com/) (free), OBS Studio
- Mac: [Kap](https://getkap.co/) (free), QuickTime
- Linux: [Peek](https://github.com/phw/peek), OBS

### Additional polish (nice-to-have)

- [ ] **Add a `CHANGELOG.md` at repo root** with a `## [0.1.0]` initial release entry, so future template users can track what changed between template versions.
- [ ] **Enable GitHub Discussions** (Settings → Features → check Discussions). Gives users a place to ask questions without filing issues.
- [ ] **Create `CONTRIBUTING.md`** with guidelines for PRs (how to propose new skills, how to run the test suite).
- [ ] **Add status badges** to README top: build (if you add CI), license, "Built for Claude Code".
- [ ] **Consider GitHub Actions CI** that runs `python tests/template/run_tests.py` on every PR. One workflow file under `.github/workflows/tests.yml`.

## Where to promote (once the above is done)

Ordered by signal-to-noise:

1. **r/gamedev "Screenshot Saturday" / "Marketing Monday"** — post a short "I built a tool that structures Claude Code for game dev, here's what one session looks like" with the screencast.
2. **Claude Code's GitHub Discussions / Anthropic's Discord** — the audience is already using Claude Code and will immediately grok the value.
3. **Hacker News** — only once. Title: "Show HN: GameFlow — a Claude Code template for indie game dev." Expect blunt feedback.
4. **Your own social (X, Bluesky, Mastodon)** — if you have followers who care about either game dev or AI tooling.
5. **r/roguelikes / r/IndieDev / r/godot / r/unity / r/unrealengine** — engine-specific communities, one post each, spread out over a week.

Do not post to all of the above simultaneously. Space it out; you only get one launch per platform.
