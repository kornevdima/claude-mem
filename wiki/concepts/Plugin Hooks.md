---
type: concept
title: "Plugin Hooks"
created: 2026-05-09
updated: 2026-05-09
tags:
  - architecture
  - hooks
  - infrastructure
status: evergreen
related:
  - "[[graphify-integration]]"
---

# Plugin Hooks

Plugin lifecycle hooks for the adlc wiki vault. Three host tools are supported: Claude Code, Cursor, and GitHub Copilot. Each reads its own config file in its native format; the runtime behavior is the same.

## Per-tool config locations

| Host | File | Format |
|---|---|---|
| Claude Code | [`hooks/hooks.json`](../../hooks/hooks.json) | Claude plugin hooks (matchers, `type: "command"` / `type: "prompt"`) |
| Cursor | [`.cursor/hooks.json`](../../.cursor/hooks.json) | Cursor hooks (`version: 1`, inline `command` strings) |
| Copilot (cloud + CLI + JetBrains preview) | [`.github/hooks/hooks.json`](../../.github/hooks/hooks.json) + scripts in [`.github/hooks/scripts/`](../../.github/hooks/scripts) | Copilot hooks (`version: 1`, `bash` field references a script path) |

## Active events

We register **two** events (after Phase 3's auto-commit reform — see "History" below):

### 1. Session start — load hot cache

When a session begins, read `wiki/hot.md` so the agent inherits recent context without crawling the full vault.

| Host | Event | Implementation |
|---|---|---|
| Claude Code | `SessionStart` (matcher: `startup\|resume`) | inline `cat wiki/hot.md` + a prompt-type fallback |
| Cursor | `sessionStart` | inline `cat wiki/hot.md` |
| Copilot | `sessionStart` | runs [`scripts/session-start.sh`](../../.github/hooks/scripts/session-start.sh) |

All three are no-ops in non-vault repos (the file check returns gracefully if `wiki/hot.md` doesn't exist).

### 2. Stop — refresh hot cache when wiki changed

At the end of every agent turn, if `wiki/` has uncommitted changes, the hook prints a `WIKI_CHANGED:` notice asking the agent to update `wiki/hot.md`.

| Host | Event | Implementation |
|---|---|---|
| Claude Code | `Stop` | inline shell pipeline checks `git diff --name-only HEAD` for `wiki/` matches |
| Cursor | `stop` | same inline pipeline |
| Copilot | `agentStop` | runs [`scripts/agent-stop.sh`](../../.github/hooks/scripts/agent-stop.sh) |

## Removed events

### `PostToolUse` auto-commit (Phase 3, 2026-05-09)

Originally, every `Write` or `Edit` tool call triggered an auto-commit of `wiki/` and `.raw/`. This caused two real problems:

1. **Commit log noise** — sessions produced 10+ "wiki: auto-commit YYYY-MM-DD HH:MM" entries that had to be squashed before pushing feature work.
2. **Hidden major changes** — bulk deletions (e.g., the `.obsidian/` removal in commit `d65cf57`, 17,000+ lines) got bundled into a generic "wiki: auto-commit" message, making history hard to review.

Phase 3 dropped the hook entirely. Wiki changes now follow the user's normal git workflow — one commit per logical unit of work, no squashing required.

## Known issue: plugin hooks STDOUT bug (Claude Code)

[anthropics/claude-code#10875](https://github.com/anthropics/claude-code/issues/10875) documents that **plugin-defined hook STDOUT may not be captured** by Claude Code in some versions, while identical inline hooks in `~/.claude/settings.json` work correctly.

**Impact**: If the bug is active, the prompt-type `SessionStart` and `PostCompact` hooks may not inject context as expected.

**Workaround**: The command-type `SessionStart` hook (`cat wiki/hot.md`) is the canonical safety check. If hot cache restoration fails in a fresh session, copy the hook config from `hooks/hooks.json` into your user-level `~/.claude/settings.json` instead of relying on plugin discovery.

**Test**: open a fresh Claude Code session in a directory containing a populated `wiki/hot.md` and ask "what's in the hot cache?" — if the answer is "no idea", the bug is active in your version.

## Non-vault sessions

All three host configs are designed to be safe in non-vault repos: every hook ends with `|| true` (Claude/Cursor) or `set -e` plus an early `exit 0` (Copilot scripts), so missing `wiki/` or `.git/` directories never raise errors.

## Cross-tool feature parity

| Need | Claude Code | Cursor | Copilot |
|---|---|---|---|
| Session start (load hot.md) | ✓ | ✓ | ✓ |
| Stop / refresh hot.md prompt | ✓ | ✓ | ✓ (`agentStop`) |
| Auto-load `AGENTS.md` for context | ✓ | ✓ | ✓ |
| Custom skills (`/wiki`, `/save`, …) | ✓ | ✓ (symlink `skills/`) | partial (custom agents, no skill system) |

Copilot for JetBrains IDE hooks were public preview as of March 2026; cloud agent and Copilot CLI are GA.

## Maintenance

When changing one hook's behavior, update all three config files in lockstep. The shell logic is short enough to keep inline; only Copilot needs script files because its `bash` field expects a path.
