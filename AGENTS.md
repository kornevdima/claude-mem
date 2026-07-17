# adlc: Agent Instructions

This repo is a Claude Code plugin **and** an Obsidian vault that builds persistent, compounding knowledge bases using Andrej Karpathy's LLM Wiki pattern. Cursor reads this file natively; Claude Code reads it alongside the auto-loaded skill descriptions. Codex CLI, OpenCode, and other Agent Skills-compatible hosts can use the skills via the symlink pattern below.

The skills follow the cross-platform Agent Skills spec. Frontmatter uses only `name` and `description` (no Claude-specific extensions).

## Project Structure

This single folder serves three roles simultaneously:

| Role | What lives here |
|---|---|
| Plugin source | `.claude-plugin/`, `agents/`, `hooks/`, `skills/`, `bin/` |
| Obsidian vault | `wiki/` (knowledge base), `.raw/` (immutable sources), `_attachments/` |
| Working repo | git history, `README.md`, `LICENSE`, `ATTRIBUTION.md` |

Open the entire project folder as the Obsidian vault root, not just `wiki/`. The `.obsidian/app.json` `userIgnoreFilters` (set on first open) hides plugin directories (`agents/`, `hooks/`, `skills/`) from the Obsidian sidebar, so the same folder cleanly serves as vault + plugin + repo without UI clutter.

## Skills Discovery

All skills live in `skills/<name>/SKILL.md`. Claude Code installs them via the plugin manifest (`.claude-plugin/plugin.json`); any Agent Skills-compatible host (Codex CLI, OpenCode, …) can pick them up by symlinking the directory into its own skill path:

```bash
ln -s "$(pwd)/skills" ~/.codex/skills/adlc
ln -s "$(pwd)/skills" ~/.opencode/skills/adlc
```

For the full skill list with trigger phrases, see [README.md](README.md). For individual skill behavior, read `skills/<name>/SKILL.md` directly.

## Subagents

Subagents (in `agents/<name>.md`) are dispatched by skills via the Agent tool with `subagent_type: "<name>"`. They run in their own context and return a single message — used for parallel batch work and context isolation.

| Subagent | Dispatched by | Purpose |
|---|---|---|
| `wiki-ingest-subagent` | `wiki-ingest` skill (batch mode, 3+ sources) | Process one source fully (read, extract, file pages); returns a summary |
| `wiki-lint-subagent` | `wiki-lint` skill (default for vaults ≥20 pages) | Read the whole vault and produce a structured lint report |
| `graphify-extract-subagent` | `graphify-ingest` and `graphify-update` skills | Read a chunk of files, extract entities/edges/hyperedges per the graphify schema, write JSON to disk |
| `research-subagent` | `autoresearch` skill (one per plan question) | Answer one research question: search, fetch, file source/entity/concept pages; returns a structured report |
| `mechanical-scanner-subagent` | `project-profile` skill | Scan project configs and return structured AGENTS.md mechanical sections |

Skills handle orchestration; subagents handle isolated work.

## Key Conventions

- **Vault root**: the directory containing `wiki/` and `.raw/`
- **Hot cache**: `wiki/hot.md` (read at session start, updated at session end)
- **Source documents**: `.raw/` (immutable: agents never modify these)
- **Generated knowledge**: `wiki/` (agent-owned, links to sources via wikilinks)
- **Manifest**: `.raw/.manifest.json` tracks ingested sources (delta tracking)

## Bootstrap

When the user opens this project for the first time:

1. Read this file (`AGENTS.md`) for full context.
2. Read `skills/wiki/SKILL.md` for the orchestration pattern.
3. If `wiki/hot.md` exists, read it silently to restore recent context.
4. If the user types `/wiki` (or "set up wiki"), follow the wiki skill's scaffold workflow.

## Cross-Project Access

To reference this vault as a knowledge base from another project, add to that project's `AGENTS.md`:

```markdown
## Wiki Knowledge Base
Path: /path/to/adlc

When you need context not already in this project:
1. Read wiki/hot.md first (recent context, ~500 words)
2. If not enough, read wiki/index.md
3. If you need domain specifics, read wiki/<domain>/_index.md
4. Only then read individual wiki pages

Do NOT read the wiki for general coding questions or things already in this project.
```

## MCP (Optional)

If you configure an Obsidian MCP server, an agent can read and write vault notes directly. See `skills/wiki/references/mcp-setup.md`.

## Reference

- Pattern source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Local copy of the LLM Wiki Pattern spec: [`.raw/llm-wiki-pattern-spec.md`](.raw/llm-wiki-pattern-spec.md)
- Cross-reference: https://github.com/kepano/obsidian-skills (authoritative Obsidian-specific skills)
