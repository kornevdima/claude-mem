---
name: graphify-explain
description: >
  Plain-language explanation of one node in the project's graphify code graph: source file,
  type, community membership, and all incoming/outgoing edges with relations and confidence tags.
  Cheap (no LLM cost — direct graph lookup). Use for "what is X", "explain this function",
  "show me what touches Y" when Y is a single named symbol.
  Triggers on: "/graphify-explain", "explain node", "what is X (in the graph)", "describe node",
  "neighbors of", "what touches X", "show me X's connections" (when about code).
---

# graphify-explain: node + immediate neighbors

Wraps `python -m graphify explain "X"`. Returns the node's metadata (source file, type, community) and its full edge list with relations and confidence tags. Cheapest and most-used graph query.

## When to invoke

- The project has `graphify-out/graph.json`.
- The user names one specific thing and wants to know what it is or what it touches: "what is `AppDelegate`?", "explain `getOAuthConfig`", "show me everything connected to `saveSession`".
- For "how does A reach B" use `graphify-path`; for open-ended exploration use `graphify-query`.

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

### Step 3 — Run explain

```bash
cd "$TARGET" && "$PYTHON" -m graphify explain "$NODE"
```

Pass the user's name verbatim. graphify matches against node labels (substring); if multiple nodes match, it returns the highest-degree match — surface that to the user so they can pick a different name if they meant a different node.

### Step 4 — Present the result

graphify's output structure:

```
Node: <label>
  ID: <node_id>
  Source: <file:line>
  Type: <code | document | paper | image>
  Community: <cluster_id>
  Degree: <total connections>

Connections (N):
  --relation [confidence]--> <neighbor>
  <-- relation [confidence] -- <inbound>
  ...
```

When presenting in chat:
- Lead with the one-line summary: "X is a [type] in [file:line] in cluster N (label '<community label from labels.json>'), with K connections."
- Group connections by relation (calls, references, imports, semantically_similar_to, contains, etc.).
- Flag any `INFERRED` or `AMBIGUOUS` edges — those are the model's guesses, not literal source-derived facts.
- If the user asked "what is X?", lean on the source file pointer and node label. If they asked "what touches X?", lead with the connections.

## Cost

$0. Single graph lookup.

## Cross-skill notes

- Often the cheapest first step before deeper exploration. After explain, follow up with `graphify-path` (to trace from this node to another) or `graphify-query` (to widen the search to the whole community).
- The community label resolution is via `graphify-out/labels.json` — read it to map the cluster_id graphify reports into the human name.
