# Troubleshooting

Common errors and what to do about them. Each entry: symptom → cause → fix.

## graphify

### "graphifyy not installed"

**Symptom**: `/graphify-ingest` halts with `graphifyy not installed`. Same for `/graphify-update` and the query skills.

**Cause**: the Python interpreter on the machine doesn't have the `graphifyy` package importable.

**Fix**:
```bash
bash bin/setup-graphify.sh /path/to/your-code-project
```

The script tries `pip install`, `pip install --user`, `pip install --break-system-packages`, and finally a venv at `~/.venvs/graphify` in that order. It pins the working interpreter to `<project>/graphify-out/.graphify_python` so subsequent runs are fast.

### "Python version not compatible"

**Symptom**: setup-graphify.sh reports no compatible Python found, or pip install fails on Python 3.14.

**Cause**: `graphifyy` requires `Python >=3.10,<3.14`. 3.14 is excluded because some graphify dependencies don't support it yet.

**Fix**: install Python 3.13 via pyenv or Homebrew, then re-run `bin/setup-graphify.sh`.

```bash
pyenv install 3.13
pyenv global 3.13
bash bin/setup-graphify.sh /path/to/project
```

### "Edge drop > 25%"

**Symptom**: `/graphify-ingest` reports something like `dropped 29 edges with unknown endpoints` and the percentage is over 25% of total edges.

**Cause**: semantic extraction subagents emitted edges to node IDs that weren't in the AST graph. Usually a cross-language ID-naming mismatch (e.g., Kotlin `MainActivity.onCreate` vs the AST's normalized form).

**Fix**: usually no action needed for small projects; it's noise. For large projects, check `chunks.py` is correctly pre-passing AST IDs to subagents (look at the chunk plan output — each `code` chunk should show `+ N AST IDs`). If chunks have zero AST IDs, the AST extractor missed those files (often a tree-sitter language gap).

### "Vendored deps in the corpus"

**Symptom**: `/graphify-ingest` plans hundreds of chunks from a small project. Looking at `.path_b_chunks.json` shows files like `ios/Pods/...` or `android/build/...`.

**Cause**: graphify's default `_SKIP_DIRS` doesn't cover React Native / iOS / Android build artifacts.

**Fix**: drop a `.graphifyignore` file in the project root with mobile-specific patterns:

```
ios/Pods/
ios/build/
ios/DerivedData/
android/build/
android/.gradle/
android/app/build/
.expo/
.metro-cache/
```

Re-run the chunk plan. Both upstream `detect()` and our `chunks.py` honor `.graphifyignore` (gitignore-style).

### "labels.json mismatch" reported by `wiki-lint`

**Symptom**: `wiki-lint` flags `FAIL: title is X but labels.json[N] = Y` on `_COMMUNITY_NN_*.md` pages.

**Cause**: `labels.json` and `graph.json` came from different runs. Manual edit, partial run, or copy from older state.

**Fix**: re-run `/graphify-ingest` to recompute labels from scratch. **Do not** hand-edit `labels.json` to "fix" it — Jaccard inheritance will lock the wrong labels in on the next update. See [[graphify-integration]] § labels.json poisoning.

## Hot cache

### "Hot cache not loading at session start"

**Symptom**: opening a fresh session, asking "what's in the hot cache?" returns "no idea."

**Cause**: most likely the [Claude Code plugin-hook STDOUT bug](https://github.com/anthropics/claude-code/issues/10875) — plugin-defined prompt-type hooks may not have STDOUT captured.

**Fix**: copy the hook config from `hooks/hooks.json` into your user-level `~/.claude/settings.json`. The command-type hook (`cat wiki/hot.md`) is the canonical fallback when the plugin path is broken in your Claude Code version.

Test: open a fresh session in this repo and ask "what's in the hot cache?" If it still fails after the workaround, the wiki/hot.md file may be missing — run any wiki operation to populate it.

## Skills

### "Skills not appearing in Claude Code"

**Symptom**: typing `/wiki` or `/graphify-ingest` returns "command not found."

**Causes and fixes**:

1. **Plugin not installed/loaded**. Run `claude plugin list` to confirm. If absent, run the install command from `README.md` install section.
2. **Plugin cache stale**. Run `claude plugin marketplace update adlc-marketplace` then `/reload-plugins` in-session.
3. **Per-session dev mode** but session was started without `--plugin-dir`. Restart with `claude --plugin-dir /path/to/adlc`.

### "Slash command works but skill triggers don't"

**Symptom**: `/wiki` works but typing "set up the wiki" doesn't trigger the skill.

**Cause**: the skill description's trigger phrases aren't matching the user's phrasing.

**Fix**: read the skill's `description:` frontmatter — that's the trigger surface. Either invoke via the slash command, or add a phrase variant if you find yourself fighting routing repeatedly.

## Subagent dispatch

### "subagent_type not found"

**Symptom**: a skill tries to dispatch a subagent and Claude Code reports the type isn't registered.

**Cause**: subagent name has the wrong suffix. After Phase 2 (rename), all four subagents end with `-subagent`:
- `wiki-ingest-subagent`
- `wiki-lint-subagent`
- `graphify-extract-subagent`
- `mechanical-scanner-subagent`

**Fix**: confirm the skill is using the suffixed name. If you're invoking a Task tool manually, use `subagent_type: "<name>-subagent"`.

## Wiki

### "Wiki not found"

**Symptom**: a skill asks "where is the wiki?" or fails because `wiki/index.md` doesn't exist.

**Cause**: the project hasn't been scaffolded yet.

**Fix**: run `/wiki` to scaffold. It asks for the base mode (B / C / B+C) and concerns, then creates folders, `index.md`, `log.md`, `hot.md`, and the vault `AGENTS.md`.

### "Wiki edits aren't being saved"

**Symptom**: edits to `wiki/*.md` files don't appear committed.

**Cause**: the per-edit auto-commit hook was removed in Phase 3 — you now commit manually. This was intentional (avoid commit-log noise and "wiki: auto-commit" messages hiding major changes).

**Fix**: `git add wiki/ && git commit -m "..."` after a session, in whatever shape you want the commit. The `Stop` hook still nudges you to update `wiki/hot.md` if wiki changed during the session.

## See also

- [[Plugin Hooks]] — full hook design across Claude Code, Cursor, Copilot
- [[graphify-integration]] — structural-layer design and known gotchas
- `hooks/hooks.json` — current Claude Code hook config
