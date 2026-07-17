# Requirements

What you need installed before adlc is useful. Most of this is optional — you only need the pieces for the skills you'll actually run.

## Host (the AI coding agent that loads adlc)

adlc is primarily a Claude Code plugin but the skills follow the cross-platform Agent Skills spec. Pick one:

| Host | Status | How it loads |
|---|---|---|
| **Claude Code** | Primary | Plugin install via local marketplace, GitHub marketplace, or `--plugin-dir`. See `README.md` install section. |
| **Cursor** | Supported | Reads `AGENTS.md` natively. Symlink `skills/` into `~/.cursor/skills/adlc` or use Cursor's plugin loader. Hooks: `.cursor/hooks.json` already configured. |
| **Codex CLI** | Supported | `ln -s "$(pwd)/skills" ~/.codex/skills/adlc` |
| **OpenCode** | Supported | `ln -s "$(pwd)/skills" ~/.opencode/skills/adlc` |
| **GitHub Copilot** (cloud / CLI / JetBrains preview) | Hooks supported | Reads `AGENTS.md` natively. Hooks: `.github/hooks/hooks.json` already configured. |

The `wiki/`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `save`, `autoresearch`, `project-profile`, `obsidian-markdown`, `obsidian-bases`, `wiki-faq` skills work in any of these. The `graphify-*` skills additionally need Python (see below).

## Obsidian

Required for the wiki layer. Any version 1.7+ works; 1.12+ adds the native CLI which simplifies a few flows.

- macOS: `brew install --cask obsidian` or download from [obsidian.md/download](https://obsidian.md/download)
- Linux: `flatpak install flathub md.obsidian.Obsidian`
- Windows: `winget install Obsidian.Obsidian`

adlc ships **no bundled Obsidian plugins or themes**. The first time you open a project folder in Obsidian, Obsidian creates a fresh `.obsidian/` config. Install whatever community plugins you want; nothing is required for the skills to work.

## Python (only for `graphify-*` skills)

graphify is a Python library (`graphifyy` on PyPI) that powers the structural code-graph layer. Required only if you use:

- `/graphify-ingest`
- `/graphify-update`
- `/graphify-query`
- `/graphify-path`
- `/graphify-explain`

**Version constraint: Python `>=3.10,<3.14`.** Python 3.14 is excluded because some of graphify's dependencies don't yet support it.

Recommended install via [pyenv](https://github.com/pyenv/pyenv):

```bash
pyenv install 3.13
pyenv global 3.13
```

Or Homebrew on macOS:

```bash
brew install python@3.13
```

Then run the bundled installer **once per project** the first time you graphify it:

```bash
bash bin/setup-graphify.sh /path/to/your-code-project
```

This:
1. Detects a compatible Python on the system
2. Installs `graphifyy` via pip / `--user` / `--break-system-packages` / venv (in that fallback order)
3. Pins the resolved interpreter path to `<project>/graphify-out/.graphify_python` so all subsequent skill runs use the same one

If you skip `bin/setup-graphify.sh`, the first `/graphify-ingest` will halt with a clear error pointing at the script.

## Git (recommended)

adlc hooks (`SessionStart` load hot cache, `Stop` refresh hot cache) and graphify's manifest tracking work best in a git working tree. None of the skills *require* git, but several of them recommend it for change tracking.

## What you do NOT need

- **Node.js / npm**: not used. (We dropped the `defuddle` skill and its npm dep.)
- **MCP server**: optional. `skills/wiki/references/mcp-setup.md` describes adding an Obsidian MCP server if you want agents to read/write the vault directly. The skills work without it.
- **Bundled Obsidian plugins**: none ship. Install your own.
- **GitHub Copilot setup files**: not required — the existing `AGENTS.md` is enough. The hooks at `.github/hooks/` are optional convenience.

## Verifying the install

After install:

- Open Claude Code, Cursor, or your host of choice in this repo.
- Run `/wiki-faq` (this skill) to confirm the skill registry is loaded.
- For graphify: run `/graphify-ingest` on a small code project to confirm the Python path resolves.
- For hot cache: `wiki/hot.md` should print at the top of every new session in this repo (the `SessionStart` hook does this).
