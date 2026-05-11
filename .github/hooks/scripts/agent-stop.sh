#!/usr/bin/env bash
# claude-mem agentStop hook — Copilot
# If wiki pages were modified during this turn, prompt the agent to refresh wiki/hot.md.

set -e

# Only run inside a git working tree that has a wiki/ folder.
[ -d wiki ] || exit 0
[ -d .git ] || exit 0

if git diff --name-only HEAD 2>/dev/null | grep -q '^wiki/'; then
  echo 'WIKI_CHANGED: Wiki pages were modified this session. Please update wiki/hot.md with a brief summary of what changed (under 500 words). Use the hot cache format: Last Updated, Key Recent Facts, Recent Changes, Active Threads. Keep it factual. Overwrite the file completely. It is a cache, not a journal.'
fi

exit 0
