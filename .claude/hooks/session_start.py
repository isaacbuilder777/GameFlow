#!/usr/bin/env python3
"""Orient Claude at session start. Shows engine, review mode, git state, last skill."""
import json
import re
import subprocess
import sys
from pathlib import Path


def run(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=5, shell=False)
        return out.stdout.strip()
    except Exception:
        return ""


def engine_summary():
    p = Path(".claude/engine.md")
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"##\s*Current engine\s*\n+\s*`?([^`\n]+)`?", text)
    if m:
        val = m.group(1).strip().strip("`")
        return val if val and val.lower() != "unset" else None
    return None


def main():
    lines = []

    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if branch:
        lines.append(f"Branch: {branch}")

    status = run(["git", "status", "--porcelain"])
    if status:
        lines.append(f"Uncommitted changes: {len(status.splitlines())} file(s)")

    recent = run(["git", "log", "--oneline", "-5"])
    if recent:
        lines.append("Recent commits:\n" + recent)

    engine = engine_summary()
    if engine:
        lines.append(f"Engine: {engine}")
    else:
        lines.append("Engine not set — run /start to initialize.")

    mode_file = Path("production/review-mode.txt")
    if mode_file.exists():
        lines.append(f"Review mode: {mode_file.read_text().strip()}")

    log = Path("production/skill-log.jsonl")
    if log.exists() and log.stat().st_size > 0:
        try:
            last = json.loads(log.read_text(encoding="utf-8").strip().splitlines()[-1])
            lines.append(f"Last skill: /{last.get('skill','?')} @ {last.get('ts','?')}")
        except Exception:
            pass

    if lines:
        output = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(lines)}}
        print(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
