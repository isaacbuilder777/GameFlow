#!/usr/bin/env python3
"""GameFlow template self-tests. Runs static validation of the .claude/ tree.

What it covers:
- settings.json is valid JSON and has required keys
- settings.json deny list blocks known risky commands
- graph.yaml parses and is internally consistent
- Every skill in graph.yaml has a matching SKILL.md file
- Every SKILL.md on disk has a matching graph entry
- Every SKILL.md has valid frontmatter (name + description)
- Every agent .md has valid frontmatter (name + description)
- All rule files have scope frontmatter
- Python hooks compile
- pre_tool.py correctly blocks risky commands and allows safe ones
- post_skill.py correctly logs Task invocations
- session_start.py produces valid JSON output

What it does NOT cover:
- Whether Claude actually invokes the right agent when a skill is typed
- Whether design docs get written with required sections
- End-to-end loop through /start -> /design -> /build -> /ship
"""

import io
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT / ".claude"

results = []  # (name, passed, message)


def test(name):
    def wrapper(fn):
        try:
            fn()
            results.append((name, True, ""))
        except AssertionError as e:
            results.append((name, False, str(e)))
        except Exception as e:
            results.append((name, False, f"{type(e).__name__}: {e}"))
        return fn
    return wrapper


# ---------- parse helpers ----------

def parse_frontmatter(text):
    """Return (frontmatter_dict, body). Raises AssertionError if missing."""
    normalized = text.replace("\r\n", "\n")
    assert normalized.startswith("---\n"), "file missing frontmatter"
    parts = normalized.split("---\n", 2)
    assert len(parts) >= 3, "file has malformed frontmatter"
    fm_raw = parts[1]
    body = parts[2]
    fm = {}
    for line in fm_raw.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip()
    return fm, body


def parse_graph_yaml(text):
    """Minimal parser for our graph.yaml format. Returns dict of skill_name -> entry."""
    skills = {}
    current = None
    in_skills = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("#") or not line.strip():
            continue
        if line.startswith("skills:"):
            in_skills = True
            continue
        if not in_skills:
            continue
        m = re.match(r"^  (\w+):$", line)
        if m:
            current = m.group(1)
            skills[current] = {"requires": [], "produces": [], "description": ""}
            continue
        if current is None:
            continue
        m = re.match(r"^    requires:\s*(.*)$", line)
        if m:
            skills[current]["requires"] = re.findall(r"\w+", m.group(1))
            continue
        m = re.match(r"^    produces:\s*(.*)$", line)
        if m:
            skills[current]["produces"] = re.findall(r"\w+", m.group(1))
            continue
        m = re.match(r"^    description:\s*(.*)$", line)
        if m:
            skills[current]["description"] = m.group(1)
            continue
    return skills


# ---------- tests ----------

@test("settings.json parses as JSON")
def t_settings_parses():
    data = json.loads((CLAUDE / "settings.json").read_text(encoding='utf-8', errors='replace'))
    assert "hooks" in data, "missing hooks"
    assert "permissions" in data, "missing permissions"


@test("settings.json registers the 3 expected hooks")
def t_settings_hooks():
    data = json.loads((CLAUDE / "settings.json").read_text(encoding='utf-8', errors='replace'))
    assert "SessionStart" in data["hooks"]
    assert "PreToolUse" in data["hooks"]
    assert "PostToolUse" in data["hooks"]


@test("settings.json deny list blocks risky git and fs commands")
def t_settings_deny():
    data = json.loads((CLAUDE / "settings.json").read_text(encoding='utf-8', errors='replace'))
    deny = data["permissions"]["deny"]
    expect_patterns = [
        r"git push --force",
        r"rm -rf",
        r"\.env",
        r"credentials\.json",
    ]
    deny_str = "\n".join(deny)
    for pat in expect_patterns:
        assert re.search(pat, deny_str), f"deny list missing {pat}"


@test("graph.yaml parses into expected skills")
def t_graph_parses():
    text = (CLAUDE / "graph.yaml").read_text(encoding='utf-8', errors='replace')
    skills = parse_graph_yaml(text)
    expected = {"start", "next", "design", "build", "review", "test", "ship", "learn",
                "balance", "playtest", "asset", "perf"}
    assert set(skills.keys()) == expected, f"skill set mismatch: {set(skills.keys()) ^ expected}"


@test("every graph skill has a matching SKILL.md on disk")
def t_skills_exist():
    skills = parse_graph_yaml((CLAUDE / "graph.yaml").read_text(encoding='utf-8', errors='replace'))
    for name in skills:
        p = CLAUDE / "skills" / name / "SKILL.md"
        assert p.exists(), f"skill {name} in graph but no {p} on disk"


@test("every SKILL.md on disk appears in graph")
def t_no_orphan_skills():
    skills = parse_graph_yaml((CLAUDE / "graph.yaml").read_text(encoding='utf-8', errors='replace'))
    on_disk = {p.parent.name for p in (CLAUDE / "skills").glob("*/SKILL.md")}
    orphans = on_disk - set(skills.keys())
    assert not orphans, f"skill folders with no graph entry: {orphans}"


@test("graph requirements reference valid producers")
def t_graph_requirements_valid():
    skills = parse_graph_yaml((CLAUDE / "graph.yaml").read_text(encoding='utf-8', errors='replace'))
    all_produces = {p for s in skills.values() for p in s["produces"]}
    for name, entry in skills.items():
        for req in entry["requires"]:
            assert req in all_produces, f"skill {name} requires '{req}' which is not produced by any skill"


@test("every SKILL.md has name and description in frontmatter")
def t_skill_frontmatter():
    for p in (CLAUDE / "skills").glob("*/SKILL.md"):
        fm, _ = parse_frontmatter(p.read_text(encoding='utf-8', errors='replace'))
        assert "name" in fm and fm["name"], f"{p} missing name"
        assert "description" in fm and fm["description"], f"{p} missing description"
        assert fm["name"] == p.parent.name, f"{p} frontmatter name '{fm['name']}' != folder '{p.parent.name}'"


@test("every agent .md has name and description in frontmatter")
def t_agent_frontmatter():
    agents = list((CLAUDE / "agents").glob("*.md"))
    assert len(agents) == 6, f"expected 6 agents, found {len(agents)}"
    expected_names = {"director", "designer", "builder", "reviewer", "tester", "releaser"}
    found_names = set()
    for p in agents:
        fm, _ = parse_frontmatter(p.read_text(encoding='utf-8', errors='replace'))
        assert "name" in fm and fm["name"], f"{p} missing name"
        assert "description" in fm and fm["description"], f"{p} missing description"
        found_names.add(fm["name"])
    assert found_names == expected_names, f"agent name mismatch: {found_names ^ expected_names}"


@test("all rule files have scope frontmatter")
def t_rule_frontmatter():
    for p in (CLAUDE / "rules").glob("*.md"):
        fm, _ = parse_frontmatter(p.read_text(encoding='utf-8', errors='replace'))
        assert "scope" in fm and fm["scope"], f"{p} missing scope"


@test("hooks compile without syntax errors")
def t_hooks_compile():
    for p in (CLAUDE / "hooks").glob("*.py"):
        r = subprocess.run([sys.executable, "-m", "py_compile", str(p)], capture_output=True, text=True)
        assert r.returncode == 0, f"{p} fails to compile: {r.stderr}"


def run_hook(hook_path, stdin_payload):
    r = subprocess.run([sys.executable, str(hook_path)], input=json.dumps(stdin_payload),
                       capture_output=True, text=True, timeout=10)
    return r.returncode, r.stdout, r.stderr


@test("pre_tool.py blocks git push --force")
def t_pre_tool_blocks_force_push():
    code, _, err = run_hook(CLAUDE / "hooks" / "pre_tool.py",
                            {"tool_name": "Bash", "tool_input": {"command": "git push --force origin main"}})
    assert code == 2, f"expected exit 2, got {code}"
    assert "force-push" in err.lower(), f"expected force-push message, got {err!r}"


@test("pre_tool.py blocks rm -rf /")
def t_pre_tool_blocks_rm_rf():
    code, _, err = run_hook(CLAUDE / "hooks" / "pre_tool.py",
                            {"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}})
    assert code == 2
    assert "rm -rf" in err.lower() or "root" in err.lower()


@test("pre_tool.py blocks butler push to itch")
def t_pre_tool_blocks_butler():
    code, _, err = run_hook(CLAUDE / "hooks" / "pre_tool.py",
                            {"tool_name": "Bash", "tool_input": {"command": "butler push mygame:release"}})
    assert code == 2
    assert "itch" in err.lower() or "butler" in err.lower()


@test("pre_tool.py blocks --no-verify")
def t_pre_tool_blocks_no_verify():
    code, _, err = run_hook(CLAUDE / "hooks" / "pre_tool.py",
                            {"tool_name": "Bash", "tool_input": {"command": "git commit --no-verify -m x"}})
    assert code == 2
    assert "hook" in err.lower() or "no-verify" in err.lower()


@test("pre_tool.py allows safe git status")
def t_pre_tool_allows_safe():
    code, _, _ = run_hook(CLAUDE / "hooks" / "pre_tool.py",
                          {"tool_name": "Bash", "tool_input": {"command": "git status"}})
    assert code == 0, f"expected exit 0 for safe command, got {code}"


@test("pre_tool.py allows normal git push")
def t_pre_tool_allows_normal_push():
    code, _, _ = run_hook(CLAUDE / "hooks" / "pre_tool.py",
                          {"tool_name": "Bash", "tool_input": {"command": "git push origin main"}})
    assert code == 0


@test("pre_tool.py ignores non-Bash tool calls")
def t_pre_tool_ignores_non_bash():
    code, _, _ = run_hook(CLAUDE / "hooks" / "pre_tool.py",
                          {"tool_name": "Read", "tool_input": {"file_path": "/tmp/anything"}})
    assert code == 0


@test("post_skill.py writes log entry for Task calls")
def t_post_skill_logs():
    with tempfile.TemporaryDirectory() as td:
        cwd_before = os.getcwd()
        os.chdir(td)
        try:
            code, _, _ = run_hook(CLAUDE / "hooks" / "post_skill.py",
                                  {"tool_name": "Task", "tool_input": {"description": "test", "subagent_type": "designer"}})
            assert code == 0
            log = Path(td) / "production" / "skill-log.jsonl"
            assert log.exists(), "log file not created"
            entry = json.loads(log.read_text(encoding='utf-8', errors='replace').strip().splitlines()[-1])
            assert entry.get("agent") == "designer"
            assert entry.get("description") == "test"
            assert "ts" in entry
        finally:
            os.chdir(cwd_before)


@test("post_skill.py ignores non-Task calls")
def t_post_skill_ignores_non_task():
    with tempfile.TemporaryDirectory() as td:
        cwd_before = os.getcwd()
        os.chdir(td)
        try:
            code, _, _ = run_hook(CLAUDE / "hooks" / "post_skill.py",
                                  {"tool_name": "Bash", "tool_input": {"command": "ls"}})
            assert code == 0
            assert not (Path(td) / "production" / "skill-log.jsonl").exists()
        finally:
            os.chdir(cwd_before)


@test("session_start.py produces valid JSON output")
def t_session_start_json():
    r = subprocess.run([sys.executable, str(CLAUDE / "hooks" / "session_start.py")],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=10)
    assert r.returncode == 0, f"hook failed: {r.stderr}"
    # stdout may be empty if no git, or a single JSON object. If present, must parse.
    if r.stdout.strip():
        data = json.loads(r.stdout)
        assert "hookSpecificOutput" in data


@test("README.md exists and mentions key commands")
def t_readme_mentions_commands():
    text = (ROOT / "README.md").read_text(encoding='utf-8', errors='replace')
    for cmd in ["/start", "/next", "/design", "/build", "/ship"]:
        assert cmd in text, f"README missing mention of {cmd}"


@test("CLAUDE.md exists and describes the 6 roles")
def t_claude_md_mentions_roles():
    text = (ROOT / "CLAUDE.md").read_text(encoding='utf-8', errors='replace')
    for role in ["director", "designer", "builder", "reviewer", "tester", "releaser"]:
        assert role in text, f"CLAUDE.md missing mention of {role}"


@test("engine.md covers godot, unity, unreal, custom")
def t_engine_covers_engines():
    text = (CLAUDE / "engine.md").read_text(encoding='utf-8', errors='replace').lower()
    for engine in ["godot", "unity", "unreal", "custom"]:
        assert engine in text, f"engine.md missing {engine}"


# ---------- runner ----------

def main():
    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = total - passed

    print("=" * 60)
    print(f"GameFlow template self-tests")
    print("=" * 60)
    for name, ok, msg in results:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}")
        if not ok:
            print(f"       {msg}")
    print("=" * 60)
    print(f"Results: {passed}/{total} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
