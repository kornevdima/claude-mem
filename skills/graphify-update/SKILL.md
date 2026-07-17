---
name: graphify-update
description: Incrementally rebuild the code-structure graph after a feature is implemented. Detects changed files, re-extracts only those, merges into existing graph.json, preserves community labels via Jaccard matching, refreshes wiki/code/. One-shot - run after each feature, before commit. Trigger phrases - refresh the graph, update the code graph, /graphify-update, rebuild after this feature, graph update.
---

# graphify-update

Incremental rebuild of an existing code graph. Run this after a feature is implemented (or any meaningful code/doc change). It is the **maintenance** counterpart to `graphify-ingest`.

## When to invoke

- A code project already has `graphify-out/graph.json` (the initial build was done via `graphify-ingest`)
- The user just finished a feature, refactor, or doc edit
- The user says "refresh the graph", "update after this feature", "/graphify-update"

Do NOT invoke for the very first run — use `graphify-ingest` instead.

## What gets preserved across runs

**Community labels** are the expensive thing — they require Claude to read clusters and write 2–5 word names. Re-running update should not throw them away.

`update.py` matches each new cluster against the previous run's clusters via Jaccard similarity on member sets. If the overlap is ≥ 0.6, the new cluster inherits the old label. Otherwise, it goes onto a "needs labeling" list that Claude handles in step 5 below.

This means: after a small feature (a few new files), most labels survive untouched. Only genuinely new or substantially-restructured clusters need fresh names.

## Cost

| Change shape | What runs | Cost |
|---|---|---|
| Code-only edits | AST extraction (cache-fast) | $0 |
| Code + a few changed docs | AST + 1–2 subagents | ~$0.10–0.50 |
| Wholesale doc rewrite | AST + many subagents | up to graphify-ingest cost |

## Steps to follow when invoked

### Step 0 — Resolve target path and verify a graph exists

```bash
TARGET="${1:-$PWD}"
TARGET=$(cd "$TARGET" && pwd)

if [ ! -f "$TARGET/graphify-out/graph.json" ]; then
    echo "No existing graph. Run /graphify-ingest first for the initial build."
    exit 1
fi
```

### Step 1 — Resolve Python interpreter

The pinned interpreter from the previous run usually still works. Validate it; if missing or stale, run the bundled installer to repin.

```bash
PYTHON=""
if [ -f "$TARGET/graphify-out/.graphify_python" ]; then
    _PIN=$(cat "$TARGET/graphify-out/.graphify_python")
    if [ -x "$_PIN" ] && "$_PIN" -c "import graphify" 2>/dev/null; then
        PYTHON="$_PIN"
    fi
fi

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(ls -d "$HOME"/.claude/plugins/cache/*/adlc/*/ 2>/dev/null | sort -V | tail -1 | sed 's:/$::')}"
[ -z "$PLUGIN_ROOT" ] && PLUGIN_ROOT="$HOME/.claude/plugins/adlc"

if [ -z "$PYTHON" ]; then
    SETUP="$PLUGIN_ROOT/bin/setup-graphify.sh"
    bash "$SETUP" "$TARGET"
    PYTHON=$(cat "$TARGET/graphify-out/.graphify_python")
fi
```

`PLUGIN_ROOT` is reused in later steps. If `CLAUDE_PLUGIN_ROOT` is unset, the snippet locates the newest install under `~/.claude/plugins/cache/*/adlc/*/`.

### Step 2 — Detect what changed

```bash
SKILL_DIR="$PLUGIN_ROOT/skills/graphify-update"
"$PYTHON" "$SKILL_DIR/scripts/detect.py" "$TARGET"
```

Show the output verbatim. It tells the user which files changed (counts only — file names go to `.update_changes.json`).

If detect prints "Nothing changed since last run" — stop. Tell the user there's nothing to do. Done.

If only code changed — `detect.py` writes `.update_changes.json` only and skips chunk planning. Jump to Step 4.

If docs/images changed — `detect.py` writes a `.path_b_chunks.json` with one chunk per ~22 changed docs (or 1 per image). Continue to Step 3.

### Step 3 — Dispatch subagents for changed docs/images (only if needed)

If the chunk count is 0 (code-only update), skip this step entirely.

Otherwise, read `$TARGET/graphify-out/.path_b_chunks.json`. For each chunk, dispatch ONE `graphify-extract-subagent` — same worker as `graphify-ingest` uses (defined in `agents/graphify-extract-subagent.md`).

All Agent tool calls in a single message so they run concurrently. `model: "sonnet"`.

For each chunk:

```
Agent tool call:
  subagent_type: "graphify-extract-subagent"
  description: "Graphify update chunk N/TOTAL (KIND)"
  model: "sonnet"
  prompt: |
    chunk_num: <N>
    total_chunks: <TOTAL>
    kind: <docs | image>
    deep_mode: false
    output_path: <absolute path to graphify-out/.graphify_chunk_NN.json>

    files:
    <one absolute path per line>

    ast_ids:
    <one ID per line, or 'none' if empty>
```

Wait for all subagents. The chunk file existing on disk is the success signal. Re-dispatch any missing chunks individually.

### Step 4 — Merge, re-cluster, preserve labels

```bash
"$PYTHON" "$SKILL_DIR/scripts/update.py" "$TARGET"
```

This:
1. Loads existing `graphify-out/graph.json`
2. Re-extracts AST for changed code files (cached, fast)
3. Prunes nodes from changed/deleted source files
4. Merges new extraction into the existing graph
5. Re-clusters (Louvain — community IDs may shift)
6. Matches new clusters to old via Jaccard on member sets; inherits labels at ≥0.7 similarity
7. Writes `graphify-out/.unlabeled_communities.json` for Claude to handle (step 5)

Show the merge output verbatim — especially the "Labels inherited" / "Labels needed" lines.

### Step 5 — Label new clusters (Claude does this)

Read `$TARGET/graphify-out/.unlabeled_communities.json`. Each entry has:

```json
{
  "community_id": 7,
  "size": 12,
  "best_match_jaccard": 0.42,
  "best_match_old_label": "Some Old Label",
  "sample_members": ["NodeA", "NodeB", ...]
}
```

For each entry, write a 2–5 word label based on the sample members. If the best_match was close (Jaccard 0.4–0.7), consider whether it's the same concept that grew/shrunk and could keep the old label, or a genuinely new theme.

Then update `$TARGET/graphify-out/labels.json` — merge your new labels with the existing entries:

```bash
$PYTHON -c "
import json, sys
labels = json.load(open('$TARGET/graphify-out/labels.json'))
new = {'<cid>': '<label>', ...}  # the labels you just wrote
labels.update(new)
json.dump(labels, open('$TARGET/graphify-out/labels.json', 'w'), indent=2)
"
```

If `.unlabeled_communities.json` is empty (everything inherited), skip this step.

### Step 6 — Regenerate wiki/code/ + hot.md

Reuse `graphify-ingest`'s regenerate script — same outputs, same shape:

```bash
INGEST_SCRIPT="$PLUGIN_ROOT/skills/graphify-ingest/scripts/regenerate.py"
"$PYTHON" "$INGEST_SCRIPT" "$TARGET" "$TARGET/graphify-out/labels.json"
```

This regenerates `GRAPH_REPORT.md`, `wiki/code/_COMMUNITY_*.md`, `graph.canvas`, rewrites `wiki/hot.md`, appends to `wiki/log.md`.

### Step 7 — Show the user the diff

After everything finishes, tell the user:

- How many nodes/edges changed (compare to pre-update numbers if you remembered them)
- How many labels were preserved vs newly written
- Any new god nodes or surprising connections worth flagging

Keep it short — 3–5 lines. The user can read the full updated `GRAPH_REPORT.md` if they want details.

## Cleanup

After a successful run, these intermediate files are auto-removed by `update.py`:
- `.update_changes.json`
- `.path_b_chunks.json`
- `.graphify_chunk_*.json`

Persisted artifacts:
- `graphify-out/graph.json` (committed)
- `graphify-out/labels.json` (committed)
- `graphify-out/GRAPH_REPORT.md` (committed)
- `graphify-out/graph.html` (committed)
- `wiki/code/*` (committed)
- `wiki/hot.md`, `wiki/log.md` (committed)

## Known limitations

- **Cluster split/merge not detected**: if one old cluster splits into two (or two merge into one), Jaccard will pick the closest match for each new cluster but may miss the relationship. Manual review of the GRAPH_REPORT helps.
- **No semantic re-extraction for changed code by default**: only AST runs on changed code. Semantic edges (INFERRED) for changed code don't refresh unless you run full `graphify-ingest` again. Acceptable for small feature work; reconsider if you've done a major refactor.
- **Whole graph re-clusters every run**: not just the changed region. Necessary because community structure is global. Cheap (just Louvain over the in-memory graph).
- **Labels.json corruption is not self-healing**: `graphify-out/labels.json` and `graphify-out/graph.json` MUST be from the same run. If something writes one without the other (e.g., a manual edit, a partial test run, a copy from an older state), update.py will faithfully *preserve* the wrong labels via Jaccard inheritance — every subsequent update locks in the mismatch. Sanity check after a run: open `wiki/code/_COMMUNITY_NN_<slug>.md` and verify the title matches the members. If labels look wrong, **re-run `graphify-ingest`** to recompute labels from scratch.
