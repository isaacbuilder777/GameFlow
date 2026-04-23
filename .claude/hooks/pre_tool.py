#!/usr/bin/env python3
"""Pre-tool validation. Blocks risky bash commands. Exit 2 + stderr = block."""
import json
import re
import sys


RISKY = [
    (r"\bgit\s+push\s+(--force|-f)\b", "Refusing force-push. Run explicitly in a shell if you mean it."),
    (r"\brm\s+-rf\s+[/~]", "Refusing rm -rf on root or home. Use a specific subpath."),
    (r"\bgit\s+reset\s+--hard\b.*\borigin\b", "Hard reset to remote loses local work. Stash first or run manually."),
    (r"--no-verify\b", "Refusing to skip git hooks. Fix the underlying issue."),
    (r"\bbutler\s+push\b", "Refusing to auto-push to itch. /ship suggests the command; you run it."),
    (r"\bsteamcmd\b.*app_update", "Refusing to auto-update Steam depot. Run manually when intended."),
]


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = payload.get("tool_input", {}).get("command", "")
    if not cmd:
        sys.exit(0)

    for pattern, reason in RISKY:
        if re.search(pattern, cmd):
            print(reason, file=sys.stderr)
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
