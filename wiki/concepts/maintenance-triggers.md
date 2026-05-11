---
type: concept
title: "Maintenance Triggers"
complexity: practical
domain: claude-mem
created: 2026-04-26
updated: 2026-04-26
tags:
  - concept
  - maintenance
  - operations
status: developing
related:
  - "[[hot]]"
  - "[[log]]"
  - "[[graphify-integration]]"
---

# Maintenance Triggers

When to run what. This page is the answer to "the wiki/graph drifted, what should I update?"

Future Claude: read this before any maintenance action. Don't run things on autopilot — check the trigger conditions first.

---

## Triggers and the action they imply

| Signal | Action | Why |
|---|---|---|
| User adds 1–2 sources to `.raw/` | `wiki-ingest <files>` inline (no batch) | Single-source mode is interactive; subagent overhead not worth it for ≤2 |
| User adds 3+ sources at once | `wiki-ingest` with **parallel subagent dispatch** (`agents/wiki-ingest-subagent.md`) | Batch mode protects main context; one subagent per source |
| 10–15 ingests since last lint | `wiki-lint` (offer proactively) | Catches orphans, dead links, stale claims before they compound |
| User asks code-structural question ("what calls X?", "where is Y defined?") | `wiki-query` routes to `graphify explain/query/path` first, then `wiki/code/_COMMUNITY_*.md` | The graph is cheaper than re-reading source. See [[graphify-integration]] |
| Code project added to claude-mem (no `graphify-out/` yet) | `/graphify-ingest` after vault is set up | First-time graph build (~$1–3) |
| Feature implemented in a code project, before commit | `/graphify-update` | Incremental: cheap, preserves cluster labels via Jaccard ≥0.6 match |
| `wiki-lint` reports `FAIL` on title-vs-label mismatch | Re-run `/graphify-ingest` (full rebuild relabels from scratch) | labels.json got corrupted; not self-healing — see [[graphify-integration]] |
| Major refactor (50+ files moved/renamed) | `/graphify-ingest`, NOT `/graphify-update` | Incremental can't track wholesale restructure; full rebuild gives accurate clusters |
| User pulls fresh git checkout on new machine | `bash bin/setup-graphify.sh /path/to/project` | Pins a working Python interpreter to `graphify-out/.graphify_python` |
| Session reaching ~80% context | PostCompact hook fires — Claude re-reads `wiki/hot.md` automatically | Hooks are wired in `hooks/hooks.json` |
| **Plugin file edited (skill/agent/command/script)** AND installed via marketplace | `claude plugin marketplace update claude-obsidian-marketplace` then `/reload-plugins` | Marketplace install copies to `~/.claude/plugins/cache/`; source edits aren't live until refreshed. Use `--plugin-dir` flag instead for instant edit-test loops. |
| Plugin manifest version bumped (`.claude-plugin/plugin.json`) | Same as above: `marketplace update` + `/reload-plugins` | Without version bump on git-distributed plugins, every commit counts as a new version. With version bump, users only see updates when version changes. |

---

## Negative triggers (do NOT do these)

| Tempting action | Why not | What instead |
|---|---|---|
| Rebuild the graph after every Edit/Write | Token-expensive for tiny changes; cluster instability | Manual `/graphify-update` once per feature |
| Auto-fix everything `wiki-lint` flagged | Some flags need human judgment (orphans may be intentional, contradictions need resolution) | Show the report, ask "fix automatically or review each?" |
| Update labels.json by hand | Easy to typo; throws off `wiki-lint` consistency checks | Re-run `/graphify-update` and let Claude relabel new clusters; `/graphify-ingest` for full reset |
| Merge old `graph.json` with new `labels.json` from a different run | IDs don't align across re-clusterings; produces silent corruption | Both must come from the same run. See [[graphify-integration]] §labels.json poisoning |

---

## How to know what skill is right

1. **Just adding knowledge** (an article, a doc, a meeting note) → `wiki-ingest`
2. **Asking about content already in the wiki** → `wiki-query`
3. **Asking about code structure** (calls, types, modules) AND `graphify-out/graph.json` exists → `wiki-query` (it routes to graph)
4. **Code changed, want graph current** → `/graphify-update` (or `/graphify-ingest` if first time)
5. **Periodic health check** → `wiki-lint`
6. **Saving the current conversation** → `/save`
7. **Researching a topic from scratch** → `/autoresearch`

If unsure, check `wiki/hot.md` first — it lists what's recent and what's stale.

---

## Cadence guidance

- **Hot cache** (`wiki/hot.md`): updated automatically at session end + on graph rebuild. Manually rewrite if it gets stale by >30 days.
- **Log** (`wiki/log.md`): append-only. New entries at TOP. One entry per significant operation, not per file.
- **Index** (`wiki/index.md`): auto-updated by ingest. Manually bump `updated` date when you add domain pages.
- **Lint reports**: keep all of them in `wiki/meta/lint-report-*.md`. They form a maintenance history.

---

## When to come back to this page

If you're a future Claude session and you see:
- A skill or command was invoked but you're not sure if it should have been → check the trigger table above
- Plugin docs disagree about which skill handles X → trigger table is the source of truth
- User asks "what's the right thing to run?" → walk through "How to know what skill is right" with them
