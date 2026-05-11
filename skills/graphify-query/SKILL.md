---
name: graphify-query
description: >
  Free-form code-structural query against the project's graphify code graph. BFS (default) or DFS
  traversal from term-matched start nodes, returning relevant subgraph as node + edge listings
  with source file pointers and community tags. Cheap (no LLM cost — pure graph traversal).
  Use for "what's connected to X", "what touches Y", "explore the auth area", or any open-ended
  code-structural exploration when a graphify graph exists for the project.
  Triggers on: "/graphify-query", "graph query", "query the graph", "explore the graph",
  "what's connected to", "what touches", "what's in the X area" (when about code).
---

# graphify-query: BFS/DFS over the code graph

Wraps `python -m graphify query` for an existing project graph. Returns nodes ranked by relevance to the query terms, with source locations and community membership.

## When to invoke

- The project has `graphify-out/graph.json` (built by `/graphify-ingest` or `/graphify-update`).
- The user asks an open-ended code-structural question: "what's connected to auth?", "explore the OAuth area", "what touches `getOAuthConfig`?".
- The question is not a single-node lookup (that's `graphify-explain`) and not a two-node trace (that's `graphify-path`).

If `graph.json` doesn't exist at the resolved target, tell the user `/graphify-ingest` is needed first. Don't invent.

## Steps

### Step 1 — Resolve target path

```bash
TARGET="${1:-$PWD}"
TARGET=$(cd "$TARGET" && pwd)
GRAPH="$TARGET/graphify-out/graph.json"
[ -f "$GRAPH" ] || { echo "No code graph at $GRAPH. Run /graphify-ingest first."; exit 1; }
```

### Step 2 — Resolve a working Python with graphifyy

```bash
PYTHON=""
PIN_FILE="$TARGET/graphify-out/.graphify_python"
if [ -f "$PIN_FILE" ]; then
    PINNED=$(cat "$PIN_FILE")
    if [ -x "$PINNED" ] && "$PINNED" -c "import graphify" 2>/dev/null; then
        PYTHON="$PINNED"
    fi
fi
if [ -z "$PYTHON" ]; then
    for cand in python3 python; do
        if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import graphify" 2>/dev/null; then
            PYTHON="$cand"; break
        fi
    done
fi
[ -z "$PYTHON" ] && { echo "graphifyy not installed. Run bin/setup-graphify.sh on this project."; exit 1; }
```

### Step 3 — Run the query

```bash
cd "$TARGET" && "$PYTHON" -m graphify query "$QUERY" [--dfs] [--budget N]
```

Defaults:
- BFS traversal (drop `--dfs` unless the user asked for depth-first).
- Token budget **1500** for normal questions; bump to **3000** for "tell me everything about X" wide queries.
- Output goes to stdout in plain text already formatted for LLM consumption.

### Step 4 — Synthesize and cite

graphify's output lists nodes in relevance order with `src=` pointers. Read it as the raw retrieval, then write a short answer in chat:

- Name the start nodes the BFS found (these tell the user what their keywords matched).
- Group results by community when ≥3 nodes share one — name the community using the labels in `graphify-out/labels.json` so users see "OAuth Config and Expo Constants" not "community 3".
- Cite source files with full paths (graphify already includes them).

If the user asks a follow-up about one node, switch to `/graphify-explain "<node>"`. If they ask "how does A reach B", switch to `/graphify-path`.

## Tips for query phrasing

graphify matches start nodes by **keyword substring against node labels**, not natural language. "What calls X?" usually returns "no matching nodes" because "calls" isn't in any label. Strip filler — query just `X` or `oauth refresh`. The BFS does the rest.

## Cost

$0. Pure Python over the existing JSON graph. No LLM tokens consumed unless the user asks for synthesis afterward.

## Cross-skill notes

- The `wiki-query` skill already routes some code-structural questions to graphify CLI. Use this skill when the user explicitly invokes `/graphify-query` or names the graph; let `wiki-query` handle ambient "what is X" type questions that may or may not map to the graph.
- `graphify-out/memory/` (when present) is graphify's Q&A feedback store. Optional follow-up: `python -m graphify save-result --question Q --answer A --type query` to record the exchange.
