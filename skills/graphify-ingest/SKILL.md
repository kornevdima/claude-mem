---
name: graphify-ingest
description: Build a queryable code-structure graph for a codebase using graphify (AST + optional semantic extraction), then file the result into the claude-mem wiki at wiki/code/. Trigger phrases - graphify this codebase, build the code graph, ingest the code, /graphify-ingest, refresh the graph.
---

# graphify-ingest

Build a structural knowledge graph for a code repository and integrate it with the claude-mem wiki.

This skill is the **structural layer** of claude-mem. It produces:

- `graphify-out/graph.json` — queryable NetworkX graph (committed; `source_file` paths are project-root-relative so it works across team members' checkouts)
- `graphify-out/GRAPH_REPORT.md` — god nodes, surprising connections, suggested questions, audit trail
- `graphify-out/graph.html` — interactive viz, open in browser
- `wiki/code/_COMMUNITY_NN_<slug>.md` — one summary page per meaningful cluster
- `wiki/code/graph.canvas` — visual layer for Obsidian
- `wiki/hot.md` — rewritten with the graph snapshot at the top

The **narrative layer** (`wiki/decisions/`, `wiki/concepts/`, `wiki/sources/`) stays human-owned. Use `/save` and `wiki-ingest` for that.

## When to invoke

Run this skill when:

- A code project doesn't yet have `graphify-out/` and `wiki/code/`
- The code has changed substantially since the last run
- The user says "refresh the graph", "rebuild the code graph", "graphify this"

Do NOT invoke for non-code corpuses (docs-only, research wikis). Use `wiki-ingest` instead.

## Modes

| Mode | What runs | Cost | Use when |
|---|---|---|---|
| **A** | AST extraction only (tree-sitter) | $0 | First test, sparse exploration, languages tree-sitter handles well |
| **B** | A + semantic extraction via parallel subagents on docs and code | ~$1–3 (Sonnet) | Default. Densifies the graph, finds INFERRED edges, names hyperedge patterns |
| **B+images** | B + per-image vision subagent (1 per image) | ~$6–18 extra | Only when image content carries codebase concepts (rare for pure code repos) |

**Default to B.** Switch to A if user says "no LLM" / "free only" / "AST only". Add images only on explicit request.

## Steps to follow when invoked

### Step 0 — Resolve target path

If the user gave a path, use it. Otherwise use the current working directory.

```bash
TARGET="${1:-$PWD}"
TARGET=$(cd "$TARGET" && pwd)  # absolutize
```

If `$TARGET/wiki/` doesn't exist, scaffold it first (this is a fresh project):

```bash
mkdir -p "$TARGET/wiki/code" "$TARGET/wiki/decisions" "$TARGET/wiki/concepts" "$TARGET/wiki/sources"
```

If the user has not yet seen the wiki layer, briefly tell them what you're about to create and where.

### Step 1 — Ensure graphify is installed and pin the interpreter

Delegate to the bundled installer. It detects the best Python (>=3.10,<3.14), installs `graphifyy` via the right strategy (pip, --user, --break-system-packages), verifies the import, and pins the interpreter for this project.

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(ls -d "$HOME"/.claude/plugins/cache/*/claude-mem/*/ 2>/dev/null | sort -V | tail -1 | sed 's:/$::')}"
[ -z "$PLUGIN_ROOT" ] && PLUGIN_ROOT="$HOME/.claude/plugins/claude-mem"
SETUP="$PLUGIN_ROOT/bin/setup-graphify.sh"
bash "$SETUP" "$TARGET"
PYTHON=$(cat "$TARGET/graphify-out/.graphify_python")
```

`PLUGIN_ROOT` is reused in later steps. If `CLAUDE_PLUGIN_ROOT` is unset (it should be set by Claude Code at skill invocation, but isn't always), the snippet locates the newest install under `~/.claude/plugins/cache/*/claude-mem/*/`.

If the script exits non-zero (no compatible Python, install failure), it tells the user exactly what to do next (install Python 3.13 via pyenv or Homebrew). Stop here and surface that message — don't try to recover automatically.

### Step 2 — Compute the chunk plan

```bash
SKILL_DIR="$PLUGIN_ROOT/skills/graphify-ingest"
"$PYTHON" "$SKILL_DIR/scripts/chunks.py" "$TARGET" --mode B
```

This prints the corpus summary (file counts by category, exclusions). Show the output to the user verbatim — don't paraphrase. It tells them what's about to be processed.

If the user asked for mode A, pass `--mode A`. If they asked for images, add `--include-images`.

If the corpus is huge (>2M words OR >500 files), pause and ask which subdirectory to scope to. Don't burn tokens silently on a giant corpus.

### Step 3 — Dispatch parallel semantic extraction (mode B only)

Read `$TARGET/graphify-out/.path_b_chunks.json`. For each chunk in the plan, dispatch ONE `graphify-extract-subagent` (defined in `agents/graphify-extract-subagent.md`). The subagent already knows the extraction rules, schema, and output format — you just hand it its chunk.

**All Agent tool calls in a single message** so they run concurrently. Use `model: "sonnet"` for cost.

For each chunk in the plan:

```
Agent tool call:
  subagent_type: "graphify-extract-subagent"
  description: "Graphify extract chunk N/TOTAL (KIND)"
  model: "sonnet"
  prompt: |
    chunk_num: <N>
    total_chunks: <TOTAL>
    kind: <docs | code | image>
    deep_mode: <true | false>
    output_path: <absolute path to graphify-out/.graphify_chunk_NN.json>

    files:
    <one absolute path per line>

    ast_ids:
    <one ID per line, or 'none' if empty>
```

**Why a custom subagent** (not `general-purpose`): graphify-extract-subagent centralizes the ~120-line extraction prompt — schema, ID format rules, confidence tagging, hyperedge guidance. Keeping it in `agents/graphify-extract-subagent.md` means the skill stays small and the worker definition can evolve independently.

Wait for all subagents. Verify each `graphify-out/.graphify_chunk_NN.json` exists on disk — that's the success signal, not the return message. If a chunk file is missing, re-dispatch just that one (the worker prompt is idempotent and safe to re-run).

### Step 4 — Merge and cluster

```bash
"$PYTHON" "$SKILL_DIR/scripts/merge.py" "$TARGET"
```

This reads `.ast_extract.json` + all `.graphify_chunk_*.json`, merges, drops edges with unknown endpoints, builds the NetworkX graph, runs Louvain clustering, computes cohesion + god nodes + surprises + suggested questions, writes `.graphify_analysis.json`, and emits a placeholder report.

After this step, `.graphify_chunk_*.json` files are cleaned up (data is now in `.graphify_extract.json`).

Show the merge output verbatim. Note the dropped-edge count — if it's >25% of total edges, the AST IDs hint pass didn't help enough; investigate.

### Step 5 — Label communities

Read `$TARGET/graphify-out/.graphify_analysis.json` and `$TARGET/graphify-out/.graphify_extract.json`.

The `communities` field is a dict of `{community_id: [node_id, node_id, ...]}` — each value is a plain list of member node IDs, NOT a dict with `size`/`members` keys. Iterate as:

```python
for cid, members in analysis["communities"].items():
    if len(members) >= 3:
        ...
```

For each community with size ≥ 3, look at the node labels (you can quickly scan them). Write a 2-5 word plain-language name that captures what the cluster IS — focus on the dominant concept, not every member.

Examples (from a real Next.js test run):
- Carousel + Reviews + Services + Team → "About Page Carousel Sections"
- ContactForm + onSubmit + getCookie + submitToHubSpot + tracking → "Contact Form Submission Pipeline"
- All HubSpot doc concepts → "HubSpot Integration (Docs)"

Write the labels to `$TARGET/graphify-out/labels.json` (committed file — `graphify-update` will read it on subsequent runs to preserve cluster names):

```json
{"0": "About Page Carousel Sections", "1": "Blog and Home Editorial", ...}
```

Cover every community with size ≥ 3. Skip the rest — `regenerate.py` calls them "Cluster N" and skips them anyway.

### Step 6 — Regenerate

```bash
"$PYTHON" "$SKILL_DIR/scripts/regenerate.py" "$TARGET" "$TARGET/graphify-out/labels.json"
```

This regenerates `GRAPH_REPORT.md` with real labels, writes `wiki/code/_COMMUNITY_*.md` pages, regenerates `graph.canvas`, rewrites `wiki/hot.md` with the snapshot, and appends a line to `wiki/log.md`.

`regenerate.py` defaults to `--min-members 3`. Pass a different value if the user wants tighter or looser pages.

### Step 7 — Report to the user

After the pipeline finishes, paste these sections from `GRAPH_REPORT.md` into chat:

- **God Nodes** (top 6)
- **Surprising Connections** (top 4)
- **Suggested Questions** (top 4)

Then offer one of the suggested questions to traverse via `wiki-query` or by reading `graph.json` directly. Keep it conversational — the graph is the map, your job after the pipeline is to be the guide.

## AGENTS.md addition (one-time per project)

If `$TARGET/AGENTS.md` exists but lacks a `## Wiki + Graph` section, append (or create the file if missing):

```markdown
## Wiki + Graph

This project uses claude-mem (narrative wiki) + graphify (structural code graph). Both layers are committed.

**Vault**: `wiki/`
**Code graph**: `graphify-out/graph.json`

**Query order when answering questions about this codebase**:
1. `wiki/hot.md` — recent context + graph snapshot
2. `wiki/index.md` — vault entry point
3. `graphify-out/graph.json` — for structural questions (who calls X? what's connected?)
4. `wiki/code/_COMMUNITY_*.md` — cluster summaries with source links
5. Raw source files — last resort

**What goes where**:
- Structural facts (calls, types, imports): graphify writes them
- Decisions, rationale: save to `wiki/decisions/` via `/save`
- External docs / RFCs: ingest into `wiki/sources/` via `wiki-ingest`

`wiki/code/` is graphify-owned — do not hand-edit.
```

## .gitignore additions (one-time per project)

Append if not already present:

```
# claude-mem + graphify (per-developer state, transient flags)
graphify-out/cost.json
graphify-out/.graphify_python
wiki/.needs_graph_update

# Obsidian per-user state
.obsidian/workspace.json
.obsidian/workspace-*.json
.obsidian/cache
```

## .obsidian/app.json (only if not yet configured)

If `$TARGET/.obsidian/app.json` is `{}` or missing, write a sensible default that hides non-wiki content from the Obsidian sidebar. Pick paths that exist in the project — at minimum: `src/`, `node_modules/`, `.next/`, `.git/`, `graphify-out/`, top-level config files.

## Known limitations

- **Edge drop on semantic merge**: even with AST ID hints, subagents sometimes invent IDs for nodes that don't exist. Drop count is shown by merge.py; high counts (>25%) suggest the hints aren't reaching the model.
- **Cluster labels are subjective**: large loose clusters (cohesion < 0.15) often resist a clean name. Pick the dominant concept; the user can rename a `_COMMUNITY_*.md` later.
- **No incremental update yet**: every run is a full rebuild. Future improvement: detect changed files via the cache and only re-extract those (graphify supports this via `graphify update`).

## Cleanup

Throwaway intermediate files written under `graphify-out/.` (dotfiles) are cleaned up by merge.py once they've been folded into `.graphify_extract.json`. The script-managed `.graphify_python` and `.labels.json` are gitignored.
