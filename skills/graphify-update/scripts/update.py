"""Apply an incremental update to the existing graph.

Reads:
    graphify-out/graph.json                — existing committed graph
    graphify-out/labels.json               — existing community labels (preserved when possible)
    graphify-out/.update_changes.json      — delta from detect.py
    graphify-out/.graphify_chunk_*.json    — semantic extractions for changed docs/images (if any)

Writes (merged or new):
    graphify-out/graph.json                — updated graph
    graphify-out/.graphify_extract.json    — merged extraction (intermediate)
    graphify-out/.graphify_analysis.json   — communities, gods, surprises (intermediate)
    graphify-out/labels.json               — updated labels (preserved + placeholders for new clusters)
    graphify-out/.unlabeled_communities.json — new clusters needing Claude labeling

Then Claude reads .unlabeled_communities.json, writes labels for them, merges
into labels.json, and runs regenerate.py (from graphify-ingest skill) to refresh
wiki/code/.

Usage:
    python update.py <project_path>
"""

import json
import sys
from pathlib import Path

import networkx as nx
from networkx.readwrite import json_graph

from graphify.analyze import god_nodes, suggest_questions, surprising_connections
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.detect import save_manifest
from graphify.export import to_html, to_json
from graphify.extract import collect_files, extract
from graphify.report import generate

JACCARD_THRESHOLD = 0.6  # min member overlap to inherit an old label
# Tuned 2026-04-25 from a real run: 0.7 was too strict — small edits to a single
# file (one node added, others shifted) dropped a clearly-same cluster from 0.74 to 0.64.
# 0.6 preserves continuity while still flagging genuine cluster splits.
LABEL_MIN_MEMBERS = 3  # only label clusters at or above this size — matches regenerate.py

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


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def main() -> None:
    if not (OUT / ".update_changes.json").exists():
        print("ERROR: no .update_changes.json. Run detect.py first.")
        sys.exit(2)

    changes = json.loads((OUT / ".update_changes.json").read_text())
    if changes.get("empty"):
        print("No changes. Nothing to do.")
        return

    code_changed = changes["code_changed"]
    deleted = changes["deleted"]
    code_only = changes["code_only"]

    print(f"[1] Load existing graph + labels")
    existing = json.loads((OUT / "graph.json").read_text())
    G_existing = json_graph.node_link_graph(existing, edges="links")
    print(f"  existing: {G_existing.number_of_nodes()} nodes, {G_existing.number_of_edges()} edges")

    labels_path = OUT / "labels.json"
    old_labels: dict[str, str] = json.loads(labels_path.read_text()) if labels_path.exists() else {}

    # Capture old communities for label preservation later
    old_communities: dict[str, set[str]] = {}
    for nid, ndata in G_existing.nodes(data=True):
        cid = ndata.get("community")
        if cid is not None:
            old_communities.setdefault(str(cid), set()).add(nid)

    print(f"[2] Re-extract changed code via AST (cache-fast)")
    # Anchor every path to the project root before extraction. Ingest extracts from
    # absolute paths under PROJECT; if update passes bare relative paths, extract()
    # slugs them differently and the same file gets a second node ID
    # (services_order_service_py vs order_service_py — eval G5 finding). Same input
    # shape ⇒ same node IDs ⇒ merge and edge restoration line up.
    code_paths = []
    for f in code_changed:
        p = Path(f)
        if not p.is_absolute():
            p = PROJECT / p
        if not p.exists():
            continue
        code_paths.extend(collect_files(p) if p.is_dir() else [p])
    if code_paths:
        ast_new = extract(code_paths, cache_root=PROJECT)
        print(f"  AST: {len(ast_new['nodes'])} nodes, {len(ast_new['edges'])} edges")
    else:
        ast_new = {"nodes": [], "edges": [], "input_tokens": 0, "output_tokens": 0}

    print(f"[3] Merge semantic chunks (if any)")

    # Vault-meta docs (AGENTS.md, CLAUDE.md, wiki/, .raw/) describe adlc's own
    # conventions, not the system under analysis. Letting them into a code graph adds
    # edge-less concept nodes that perturb Louvain clustering — observed in eval G5:
    # 16 AGENTS.md nodes knocked 6 of 8 clusters below the Jaccard label-inheritance
    # threshold. Filter them out of both semantic chunks and the prune set.
    _META_DOC_SUFFIXES = ("AGENTS.md", "CLAUDE.md")
    _META_DOC_PREFIXES = ("wiki/", ".raw/", "graphify-out/")

    def is_meta_doc(f: str) -> bool:
        rf = to_rel(f, PROJECT)
        return rf.endswith(_META_DOC_SUFFIXES) or rf.startswith(_META_DOC_PREFIXES)

    sem_nodes: list[dict] = []
    sem_edges: list[dict] = []
    sem_hyper: list[dict] = []
    chunk_paths = sorted(OUT.glob(".graphify_chunk_*.json"))
    skipped_meta = 0
    skipped_meta_rel = 0
    for cp in chunk_paths:
        try:
            ch = json.loads(cp.read_text())
        except json.JSONDecodeError as e:
            print(f"  ! {cp.name}: invalid JSON ({e}). Skipping.")
            continue
        for n in ch.get("nodes", []):
            if is_meta_doc(n.get("source_file", "")):
                skipped_meta += 1
                continue
            sem_nodes.append(n)
        # Edges and hyperedges carry source_file too. Filtering only nodes left the
        # vault-meta edges dangling (build_from_json drops them) but let vault-meta
        # HYPEREDGES through — and those then replaced the real code hyperedges.
        for e in ch.get("edges", []):
            if is_meta_doc(e.get("source_file", "")):
                skipped_meta_rel += 1
                continue
            sem_edges.append(e)
        for h in ch.get("hyperedges", []):
            if is_meta_doc(h.get("source_file", "")):
                skipped_meta_rel += 1
                continue
            sem_hyper.append(h)
    if skipped_meta or skipped_meta_rel:
        print(f"  filtered {skipped_meta} vault-meta doc nodes, "
              f"{skipped_meta_rel} edges/hyperedges (AGENTS.md/wiki/.raw)")
    print(f"  semantic: {len(sem_nodes)} nodes, {len(sem_edges)} edges, "
          f"{len(sem_hyper)} hyperedges from {len(chunk_paths)} chunks")

    print(f"[4] Build new-extraction graph fragment")
    new_extract = {
        "nodes": ast_new["nodes"] + sem_nodes,
        "edges": ast_new["edges"] + sem_edges,
        "hyperedges": sem_hyper,
        "input_tokens": 0,
        "output_tokens": 0,
    }
    G_new = build_from_json(new_extract)

    print(f"[5] Prune nodes from deleted/changed source files")
    # Compare on project-root-relative paths so this works whether the existing graph
    # stored absolute (pre-migration) or relative source_file.
    # docs_changed is included: without it, doc-derived nodes are purely additive —
    # concepts removed from a doc would linger in the graph forever (eval G5 finding).
    docs_changed = [f for f in changes.get("docs_changed", []) if not is_meta_doc(f)]
    affected_files = (
        {to_rel(f, PROJECT) for f in code_changed}
        | {to_rel(f, PROJECT) for f in deleted}
        | {to_rel(f, PROJECT) for f in docs_changed}
    )

    to_remove = []
    for nid, ndata in G_existing.nodes(data=True):
        src = ndata.get("source_file", "")
        if src and to_rel(src, PROJECT) in affected_files:
            to_remove.append(nid)

    # Snapshot edges that cross the prune boundary BEFORE removing nodes. Removing a
    # node removes its incident edges — including edges to nodes in UNCHANGED files,
    # which the isolated re-extraction of changed files can never rebuild (the caller
    # of a changed function lives in a file we don't re-parse). Observed in eval G5:
    # a one-file feature destroyed 22 real edges around the most-connected node.
    to_remove_set = set(to_remove)
    boundary_edges = [
        (u, v, dict(d))
        for u, v, d in G_existing.edges(data=True)
        if (u in to_remove_set) != (v in to_remove_set)
    ]
    G_existing.remove_nodes_from(to_remove)
    print(f"  pruned {len(to_remove)} stale nodes from {len(affected_files)} affected files")
    print(f"  snapshotted {len(boundary_edges)} cross-boundary edges for restoration")

    print(f"[6] Merge new fragment into existing graph")
    G_existing.update(G_new)
    # Drop edges with unknown endpoints (defensive)
    valid = set(G_existing.nodes())
    bad_edges = [(u, v) for u, v in G_existing.edges() if u not in valid or v not in valid]
    G_existing.remove_edges_from(bad_edges)

    # Restore cross-boundary edges whose endpoints both survived the merge (node IDs
    # are stable across re-extraction, so a re-extracted node reconnects to its old
    # neighbors). Caveat: an edge FROM a changed file whose call was actually deleted
    # in the edit is restored too — a full /graphify-ingest rebuild reconciles that,
    # which is another reason periodic full rebuilds stay in the skill's guidance.
    restored = 0
    for u, v, d in boundary_edges:
        if u in G_existing and v in G_existing and not G_existing.has_edge(u, v):
            G_existing.add_edge(u, v, **d)
            restored += 1
    print(f"  restored {restored} cross-boundary edges")

    # Hyperedges live in G.graph, and nx.Graph.update() does self.graph.update(other.graph)
    # — so G_new's hyperedge list REPLACES the existing one instead of merging with it.
    # A doc chunk carrying any hyperedge therefore wiped every code hyperedge built by
    # the initial ingest. Rebuild the union explicitly: existing ones persist, a
    # re-extracted one wins by id, and any whose members no longer all exist is dropped.
    # AST extraction never emits hyperedges, so this is the only thing keeping them alive.
    merged_hyper: dict[str, dict] = {}
    for h in existing.get("hyperedges", []) + sem_hyper:
        key = h.get("id") or h.get("label", "")
        if key:
            merged_hyper[key] = h
    nodes_now = set(G_existing.nodes())
    hyper_out = [
        h for h in merged_hyper.values()
        if h.get("nodes") and all(n in nodes_now for n in h["nodes"])
    ]
    dropped_hyper = len(merged_hyper) - len(hyper_out)
    G_existing.graph["hyperedges"] = hyper_out

    print(f"  merged total: {G_existing.number_of_nodes()} nodes, {G_existing.number_of_edges()} edges")
    print(f"  hyperedges: {len(hyper_out)} kept"
          + (f", {dropped_hyper} dropped (members no longer in graph)" if dropped_hyper else ""))

    # Portability: rewrite source_file on all nodes to project-root-relative so the
    # committed graph.json works across team members' checkouts. Also migrates an
    # older graph that still holds absolute paths.
    for _nid, _d in G_existing.nodes(data=True):
        _s = _d.get("source_file")
        if _s:
            _d["source_file"] = to_rel(_s, PROJECT)

    print(f"[7] Re-cluster")
    G = G_existing
    communities = cluster(G)
    cohesion = score_all(G, communities)
    sizes = sorted((len(m) for m in communities.values()), reverse=True)
    print(f"  {len(communities)} communities | top sizes: {sizes[:8]}")

    print(f"[8] Match new clusters to old via Jaccard (preserve labels)")
    # Restrict matching to clusters that are big enough to be worth labeling.
    # Tiny/singleton clusters get placeholders and are skipped by regenerate.py.
    new_meaningful = {cid: set(members) for cid, members in communities.items() if len(members) >= LABEL_MIN_MEMBERS}
    inherited = 0
    new_label_map: dict[str, str] = {}
    unlabeled: list[dict] = []
    for cid, members in new_meaningful.items():
        # Find best matching old community (only labeled ones — others can't help)
        best_old: tuple[str | None, float] = (None, 0.0)
        for old_cid, old_members in old_communities.items():
            if old_cid not in old_labels:
                continue
            score = jaccard(members, old_members)
            if score > best_old[1]:
                best_old = (old_cid, score)
        if best_old[0] is not None and best_old[1] >= JACCARD_THRESHOLD:
            new_label_map[str(cid)] = old_labels[best_old[0]]
            inherited += 1
        else:
            sample = [G.nodes[n].get("label", n) for n in list(members)[:18]]
            unlabeled.append({
                "community_id": cid,
                "size": len(members),
                "best_match_jaccard": round(best_old[1], 2),
                "best_match_old_label": old_labels.get(best_old[0]) if best_old[0] else None,
                "sample_members": sample,
            })
            new_label_map[str(cid)] = f"Cluster {cid}"  # placeholder until Claude labels it

    # Tiny clusters get placeholders too (not in new_label_map yet)
    for cid in communities:
        if str(cid) not in new_label_map:
            new_label_map[str(cid)] = f"Cluster {cid}"

    print(f"  meaningful clusters: {len(new_meaningful)}")
    print(f"  inherited labels: {inherited}")
    print(f"  needs Claude labeling: {len(unlabeled)}")

    print(f"[9] Analyze + persist intermediate state")
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    label_int = {cid: new_label_map.get(str(cid), f"Cluster {cid}") for cid in communities}
    questions = suggest_questions(G, communities, label_int)

    # Write merged extraction (so regenerate.py can use it)
    nodes_out = [{"id": n, **d} for n, d in G.nodes(data=True)]
    edges_out = [{"source": u, "target": v, **d} for u, v, d in G.edges(data=True)]
    merged_out = {
        "nodes": nodes_out,
        "edges": edges_out,
        "hyperedges": hyper_out,
        "input_tokens": 0,
        "output_tokens": 0,
    }
    (OUT / ".graphify_extract.json").write_text(json.dumps(merged_out, indent=2))

    analysis = {
        "communities": {str(k): list(v) for k, v in communities.items()},
        "cohesion": {str(k): v for k, v in cohesion.items()},
        "gods": gods,
        "surprises": surprises,
        "questions": questions,
    }
    (OUT / ".graphify_analysis.json").write_text(json.dumps(analysis, indent=2))

    # Write labels — but only for meaningful clusters. Placeholders for tiny clusters
    # would just bloat labels.json on each subsequent run.
    persisted = {cid: lbl for cid, lbl in new_label_map.items()
                 if int(cid) in new_meaningful and not lbl.startswith("Cluster ")}
    labels_path.write_text(json.dumps(persisted, indent=2))

    # Write list of unlabeled clusters for Claude to read
    (OUT / ".unlabeled_communities.json").write_text(json.dumps(unlabeled, indent=2))

    # Regenerate report + graph.json + html with current labels
    report = generate(
        G, communities, cohesion, label_int, gods, surprises,
        {"total_files": 0, "total_words": 0, "needs_graph": True, "warning": None,
         "files": {"code": [], "document": [], "paper": [], "image": []}},
        {"input": 0, "output": 0}, str(PROJECT), suggested_questions=questions,
    )
    (OUT / "GRAPH_REPORT.md").write_text(report)
    # force=True: incremental updates legitimately prune nodes (deleted source files,
    # changed extractions). graphify's safety guard would otherwise refuse to overwrite
    # a smaller graph.
    to_json(G, communities, str(OUT / "graph.json"), force=True)
    to_html(G, communities, str(OUT / "graph.html"), community_labels=label_int)

    # Save manifest so the next update detects from this point.
    # We re-detect to capture the post-update file inventory.
    from graphify.detect import detect as full_detect
    det = full_detect(PROJECT)
    save_manifest(det["files"])

    # Cleanup transient files
    for tmp in (".update_changes.json", ".path_b_chunks.json"):
        p = OUT / tmp
        if p.exists():
            p.unlink()
    for cp in chunk_paths:
        cp.unlink()

    print()
    print("=== Update done ===")
    print(f"  Labels inherited: {inherited}")
    print(f"  Labels needed:    {len(unlabeled)} (see .unlabeled_communities.json)")
    print()
    if unlabeled:
        print("Next: Claude reads .unlabeled_communities.json, adds labels to labels.json,")
        print("then runs the regenerate.py from graphify-ingest skill to refresh wiki/code/.")
    else:
        print("All clusters inherited labels. Run regenerate.py to refresh wiki/code/:")
        print(f"  python <skill_dir>/graphify-ingest/scripts/regenerate.py {PROJECT} {labels_path}")


if __name__ == "__main__":
    main()
