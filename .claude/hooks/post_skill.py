#!/usr/bin/env python3
"""Log skill / agent completion to production/skill-log.jsonl."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if payload.get("tool_name") != "Task":
        sys.exit(0)

    tin = payload.get("tool_input", {})
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "description": tin.get("description", ""),
        "agent": tin.get("subagent_type", ""),
    }

    Path("production").mkdir(exist_ok=True)
    with (Path("production") / "skill-log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
