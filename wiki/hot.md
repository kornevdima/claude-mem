---
type: meta
title: "Hot Cache"
updated: 2026-05-09
tags:
  - meta
  - hot-cache
status: evergreen
related:
  - "[[index]]"
  - "[[log]]"
  - "[[maintenance-triggers]]"
  - "[[graphify-integration]]"
  - "[[Project Profile]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Research Pre-computed Context for Coding Agents]]"
---

# Recent Context

Navigation: [[index]] | [[log]] | [[maintenance-triggers]] | [[graphify-integration]] | [[Project Profile]]

## Last Updated

**2026-05-09 (design synthesis)**: End-to-end skill suite design at [[Project Profile Skill Suite]]. Five skills (`/project-profile`, `/capture-rule`, `/list-rules`, `/prune-rules`, `/resolve-rule-conflicts`) + 3 subagents + 1 hook. File layout: `AGENTS.md` (root) + `.agents/rules/*.md` (one per rule, <80 lines) + `.agents/rules/_index.md`. All open questions from the two research passes resolved into concrete decisions. Implementation sequence proposed; ready to build `/project-profile` first-run as step 1.

**2026-05-09 (Round 2)**: Follow-up research on the feedback half of /project-profile. 8 pages created (4 sources, 3 concepts, 1 synthesis). Synthesis at [[Research Feedback-Driven Project Profile]]; design synthesis at [[Feedback Loop for Project Profile]]. Closes design open question #5 (tribal-knowledge UX) and shapes the architecture for a planned `/capture-rule` skill.

**Round 2 headline**: Cursor's `/Generate Cursor Rules` (v0.49, April 2025) is the closest reference implementation — manual + retrospective trigger, one concept per .mdc file under 80 lines. Aider's CONVENTIONS.md is the strict-human-authored counterpoint. Reflexion (Shinn 2023) is the foundational architecture: Actor/Evaluator/Self-Reflection. Anthropic confirms generator-evaluator separation is "a strong lever" against self-grading leniency. Design adopts: three-role architecture (Generator skill + Evaluator subagent + Human gate), manual /capture-rule trigger, one rule per file with 80-line cap, separate /prune-rules for monotonic-growth control.

**2026-05-09 (Round 1)**: Autoresearch pass on pre-computed context for coding agents. 14 pages created (6 sources, 5 concepts, 2 entities, 1 synthesis). Drives design of a planned `/project-profile` skill for brownfield repos. Synthesis at [[Research Pre-computed Context for Coding Agents]]; design proposal at [[Project Profile]].

**Round 1 headline**: ETH Zurich's AGENTbench paper (Feb 2026) shows LLM-generated context files **degrade** agent performance by 2-3%; human-written give only +4% with +20-23% cost. Auto-summarization is net-negative. Right pattern: AGENTS.md-compatible format + hand-curated tribal sections + on-demand structural retrieval (Aider-style repo-map, ~1K tokens).

**2026-04-26**: graphify integration shipped (v0.2.0). Two new skills, one subagent, two slash commands, one helper script.

## Current Plugin State

- **Version**: `0.3.0` (manifest at `.claude-plugin/plugin.json`)
- **Working directory**: `~/IdeaProjects/claude-mem/`
- **Skills (15)**: `wiki`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `wiki-faq`, `save`, `autoresearch`, `obsidian-markdown`, `obsidian-bases`, `graphify-ingest`, `graphify-update`, `graphify-query`, `graphify-path`, `graphify-explain`, `project-profile`
- **Slash commands**: removed 2026-05-09 (`commands/` folder deleted). Skills cover the same UX via trigger phrases in their descriptions — typing `/wiki`, `/save`, etc. matches the skill via description triggers, no separate registration needed.
- **Subagents (4)**: `wiki-ingest-subagent`, `wiki-lint-subagent`, `graphify-extract-subagent`, `mechanical-scanner-subagent`
- **Hooks (4)**: SessionStart, PostCompact, PostToolUse, Stop
- **Per-tool dev instructions**: `AGENTS.md` only. Cursor reads it natively; Claude Code reads it alongside auto-loaded skill descriptions. Removed 2026-05-09: `GEMINI.md`, `.github/copilot-instructions.md`, `.cursor/rules/`, `CLAUDE.md` (all redundant with AGENTS.md after dedup).
- **Setup scripts**: `bin/setup-graphify.sh` only. Removed 2026-05-09: `setup-vault.sh` (vault is scaffolded by `/wiki` skill) and `setup-multi-agent.sh` (multi-tool symlink installer).
- **Marketplace**: `.claude-plugin/marketplace.json` declares `claude-mem` with `"source": "./"` (single-plugin marketplace where the marketplace root IS the plugin root). Marketplace name: `claude-obsidian-marketplace` (legacy, retained for install command compatibility).
- **Install methods**: local marketplace (persistent), `--plugin-dir` flag (per-session dev), Cowork zip, GitHub marketplace. See `README.md` install section.

## Architecture in one paragraph

claude-mem is a Claude Code plugin + Obsidian vault. Two layers per project: **narrative** (`wiki/` — decisions, concepts, sources, owned by humans + skills) and optional **structural** (`graphify-out/` — code graph from AST + semantic extraction, owned by the graphify skills). `wiki-query` routes code-structural questions to the graph CLI; `wiki-lint` cross-checks consistency between layers. Detailed design at [[graphify-integration]].

## Maintenance Triggers (the most-asked question)

**See [[maintenance-triggers]] for the full table.** Quick version:

| Signal | Action |
|---|---|
| 3+ sources to ingest | wiki-ingest with parallel subagents |
| 10–15 ingests done | offer `wiki-lint` proactively |
| Code question + graph exists | wiki-query routes to graph first |
| Code project, no graph yet | `/graphify-ingest` |
| Feature done, before commit | `/graphify-update` |
| `wiki-lint` says title-vs-label FAIL | re-run `/graphify-ingest` (don't hand-edit labels.json) |

## Active Threads

- No PostToolUse + Stop hooks for auto-rebuild — intentional design choice (manual control)
- `wiki/code/` is regenerated wholesale on every graphify run (not incremental per cluster) — acceptable at current scale
- Image vision in graphify (`--include-images`) is documented but expensive ($6–18 for 100+ images); skip unless visual concepts matter
- esg-website project at `~/esg/esg-website/` is the integration test target — has full graphify-out + wiki/code/ from this session

## Key Lessons (current)

1. **labels.json corruption is not self-healing**. graph.json and labels.json must come from the same run. If they drift, `/graphify-ingest` to recompute. See [[graphify-integration]] §labels.json poisoning.
2. **Jaccard threshold of 0.6** preserves cluster labels across small touches; 0.7 was too strict.
3. **Skills orchestrate, subagents do the heavy reading**. Three patterns: many-parallel-workers (`graphify-extract-subagent`, `wiki-ingest-subagent` batch), single-isolated-reader (`wiki-lint-subagent`), and inline (everything else).
4. **Two slash commands, not a smart router** — explicit intent beats magic auto-routing for cost-sensitive operations.
5. **graphifyy requires Python `>=3.10,<3.14`** — 3.14 is excluded. `bin/setup-graphify.sh` handles this.
6. **Edge drop fix**: pre-pass AST node IDs to semantic subagents in their prompt so they don't invent IDs that get discarded at merge.
7. **Plugin marketplace `source` requires `./` prefix** — `"."` alone fails schema validation. Single-plugin marketplace (where marketplace root IS the plugin root) uses `"source": "./"`. Acceptable plugin sources: relative-path string starting with `./`, or object form (`github`/`url`/`git-subdir`/`npm`). Local-directory object form does NOT exist for plugin sources, only marketplace sources.
8. **Persistent install ≠ live edits**. `claude plugin install` copies the plugin to `~/.claude/plugins/cache/`. Source-directory edits require `claude plugin marketplace update <name>` then `/reload-plugins` in-session. For instant edit-test loops use `--plugin-dir` flag instead (per-session, no copy).

## Style Preferences (carried over)

- No em dashes (U+2014) or `--` as punctuation. Use periods, commas, colons, parentheses.
- Keep responses short and direct. No trailing summaries.
- Parallel tool calls when independent.
- Per-developer files (`.idea/`, `.claude/settings.local.json`, `.obsidian/workspace.json`, `.python-version`) are gitignored.

## Repo Locations

- Working: `~/IdeaProjects/claude-mem/`
- Origin: (single `init` commit; no remote pushed yet from this lineage)
- Test target for graphify: `~/esg/esg-website/`
