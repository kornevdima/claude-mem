---
name: graphify-path
description: >
  Find the shortest path between two named nodes in the project's graphify code graph. Returns
  the hop sequence with edge relations and confidence tags. Cheap (no LLM cost — NetworkX shortest
  path on the existing graph). Use for "how does A reach B", "trace the dependency chain from X to Y",
  "what connects A and B".
  Triggers on: "/graphify-path", "shortest path between", "how does X reach Y", "trace path from",
  "dependency chain from A to B", "path A to B" (when about code).
---

# graphify-path: shortest path between two graph nodes

Wraps `python -m graphify path "A" "B"`. Returns the smallest hop count between two nodes plus the relations and confidence tags along the way.

## When to invoke

- The project has `graphify-out/graph.json`.
- The user names two specific things and wants to see the connection between them: "how does `LoginScreen.handleSignOn` reach `saveSession()`?", "trace from `getOAuthConfig` to the AppDelegate".
- For "what is X" use `graphify-explain`; for open-ended exploration use `graphify-query`.

If `graph.json` is missing, tell the user to run `/graphify-ingest` first.

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

### Step 3 — Run the path query

```bash
cd "$TARGET" && "$PYTHON" -m graphify path "$NODE_A" "$NODE_B"
```

Pass the user's two names verbatim. graphify matches against node labels (substring); if either name doesn't match a node, it returns a clear error and you should surface it.

### Step 4 — Present the path

Output is one line per hop:

```
Shortest path (N hops):
  A --relation [confidence]--> intermediate --relation [confidence]--> B
```

When presenting in chat:
- Lead with the hop count.
- Note whether any hop is `INFERRED` or `AMBIGUOUS` (lower confidence) versus all `EXTRACTED`.
- Cross-reference the communities each node belongs to (look up in `graphify-out/labels.json`) when the path spans multiple clusters — that's often the interesting finding.

If no path exists, the two nodes are in different connected components. That's a real answer: tell the user the graph thinks A and B are unrelated.

## Cost

$0. NetworkX shortest path on the existing graph.

## Cross-skill notes

- For traces involving more than two anchors ("A → B → C → D"), run `graphify-path` twice (A→B, B→C, etc.) and stitch.
- For a single node's full neighborhood, use `graphify-explain` instead (it's faster and shows all edges, not just one path).
