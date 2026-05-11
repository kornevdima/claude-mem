#!/usr/bin/env bash
# claude-mem SessionStart hook — Copilot
# Loads wiki/hot.md into the agent's context if present. Safe in non-vault repos.

set -e
[ -f wiki/hot.md ] && cat wiki/hot.md
exit 0
