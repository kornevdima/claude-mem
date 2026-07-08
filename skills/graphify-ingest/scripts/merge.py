"""Merge AST extraction with semantic chunk JSONs, re-cluster, analyze.

Reads:
  graphify-out/.ast_extract.json
  graphify-out/.graphify_chunk_*.json (zero or more)

Writes:
  graphify-out/.graphify_extract.json   (merged nodes + edges)
  graphify-out/.graphify_analysis.json  (communities, cohesion, gods, surprises, questions)
  graphify-out/graph.json               (NetworkX export with placeholder labels)
  graphify-out/graph.html
  graphify-out/GRAPH_REPORT.md          (placeholder labels — replaced by regenerate.py)

Does NOT regenerate wiki/code/ — that's regenerate.py's job, after Claude
provides community labels.

Usage:
    python merge.py <project_path>
"""

import json
import sys
from pathlib import Path

from graphify.analyze import god_nodes, suggest_questions, surprising_connections
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.detect import save_manifest
from graphify.export import to_html, to_json
from graphify.report import generate

PROJECT = Path(sys.argv[1]).resolve()
OUT = PROJECT / "graphify-out"


def to_rel(src, project):
    """Project-root-relative posix source_file, for portable committed graph artifacts.
    Passes through already-relative paths; leaves paths outside the project unchanged."""
    if not src:
        return src
    p = Path(src)
    if not p.is_absolute():
        return p.as_posix()
    try:
        return p.resolve().relative_to(project).as_posix()
    except ValueError:
        return src


print("[1] Load AST extraction")
ast = json.loads((OUT / ".ast_extract.json").read_text())
print(f"  AST: {len(ast['nodes'])} nodes, {len(ast['edges'])} edges")

print("[2] Merge semantic chunks (if any)")
all_nodes = list(ast["nodes"])
all_edges = list(ast["edges"])
all_hyper: list[dict] = []
seen_ids = {n["id"] for n in all_nodes}
chunk_paths = sorted(OUT.glob(".graphify_chunk_*.json"))
for cp in chunk_paths:
    try:
        ch = json.loads(cp.read_text())
    except json.JSONDecodeError as e:
        print(f"  ! {cp.name}: invalid JSON ({e}). Skipping.")
        continue
    new_n = 0
    for n in ch.get("nodes", []):
        if n["id"] not in seen_ids:
            all_nodes.append(n)
            seen_ids.add(n["id"])
            new_n += 1
    new_e = ch.get("edges", [])
    new_h = ch.get("hyperedges", [])
    all_edges.extend(new_e)
    all_hyper.extend(new_h)
    print(f"  {cp.name}: +{new_n} new nodes, +{len(new_e)} edges, +{len(new_h)} hyperedges")

print(f"  total: {len(all_nodes)} nodes, {len(all_edges)} edges, {len(all_hyper)} hyperedges")

# Portability: store project-root-relative source_file so the committed graph.json
# works across team members' checkouts (see "Graphify Relative Paths").
for n in all_nodes:
    s = n.get("source_file")
    if s:
        n["source_file"] = to_rel(s, PROJECT)

print("[3] Drop edges with unknown endpoints")
valid_ids = {n["id"] for n in all_nodes}
clean_edges = [e for e in all_edges if e["source"] in valid_ids and e["target"] in valid_ids]
dropped = len(all_edges) - len(clean_edges)
if dropped:
    print(f"  dropped {dropped} edges with unknown endpoints")

merged = {
    "nodes": all_nodes,
    "edges": clean_edges,
    "hyperedges": all_hyper,
    "input_tokens": 0,
    "output_tokens": 0,
}
(OUT / ".graphify_extract.json").write_text(json.dumps(merged, indent=2))

print("[4] Build graph")
G = build_from_json(merged)
print(f"  {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
if G.number_of_nodes() == 0:
    print("ERROR: graph is empty. Aborting.")
    sys.exit(1)

print("[5] Cluster + analyze")
communities = cluster(G)
cohesion = score_all(G, communities)
gods = god_nodes(G)
surprises = surprising_connections(G, communities)
labels = {cid: f"Community {cid}" for cid in communities}
questions = suggest_questions(G, communities, labels)
sizes = sorted((len(m) for m in communities.values()), reverse=True)
print(f"  {len(communities)} communities | top sizes: {sizes[:8]}")
print(f"  {len(gods)} god nodes | {len(surprises)} surprises | {len(questions)} questions")

print("[6] Generate placeholder report + graph.json + html")
detection_stub = {
    "total_files": len(set(n.get("source_file", "") for n in all_nodes)),
    "total_words": 0,
    "needs_graph": True,
    "warning": None,
    "files": {"code": [], "document": [], "paper": [], "image": []},
}
report = generate(
    G, communities, cohesion, labels, gods, surprises, detection_stub,
    {"input": 0, "output": 0}, str(PROJECT), suggested_questions=questions,
)
(OUT / "GRAPH_REPORT.md").write_text(report)
to_json(G, communities, str(OUT / "graph.json"))
to_html(G, communities, str(OUT / "graph.html"), community_labels=labels)

# Persist analysis for the labeling step
analysis = {
    "communities": {str(k): v for k, v in communities.items()},
    "cohesion": {str(k): v for k, v in cohesion.items()},
    "gods": gods,
    "surprises": surprises,
    "questions": questions,
}
(OUT / ".graphify_analysis.json").write_text(json.dumps(analysis, indent=2))

# Manifest + python pin
# The manifest enables `graphify update` and our graphify-update skill to detect
# what changed since this run. Read the detection saved by chunks.py.
detect_path = OUT / ".graphify_detect.json"
if detect_path.exists():
    det = json.loads(detect_path.read_text())
    save_manifest(det["files"])
else:
    print("  WARN: .graphify_detect.json missing — incremental updates may misdetect.")
(OUT / ".graphify_python").write_text(sys.executable)

# Cleanup chunk files (we have semantic data merged into .graphify_extract.json now)
for cp in chunk_paths:
    cp.unlink()

# Cleanup intermediate AST files (no longer needed once merged)
for tmp in (".ast_extract.json", ".ast_ids_by_file.json", ".path_b_chunks.json", ".graphify_detect.json"):
    p = OUT / tmp
    if p.exists():
        p.unlink()

print()
print("=== Merge done ===")
print(f"  Communities ≥3: {sum(1 for s in sizes if s >= 3)}")
print(f"  Communities ≥5: {sum(1 for s in sizes if s >= 5)}")
print(f"  Singletons: {sum(1 for s in sizes if s == 1)}")
print()
print("Next: Claude reads .graphify_analysis.json, writes labels.json,")
print("then run: python regenerate.py <project> labels.json")
