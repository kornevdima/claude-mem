"""Regenerate report + wiki/code/ + hot.md snapshot using Claude-provided labels.

Reads:
  graphify-out/.graphify_extract.json
  graphify-out/.graphify_analysis.json
  <labels_path>           — JSON: {community_id: "Human Label", ...}

Writes:
  graphify-out/GRAPH_REPORT.md
  graphify-out/graph.json
  graphify-out/graph.html
  wiki/code/_index.md
  wiki/code/_COMMUNITY_NN_<slug>.md   (one per community ≥ MIN_MEMBERS)
  wiki/code/graph.canvas
  wiki/hot.md                          (graph snapshot block — REWRITES the whole file)
  wiki/log.md                          (appends a run entry — preserves prior content)

Usage:
    python regenerate.py <project_path> <labels_json_path> [--min-members N]
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from graphify.analyze import suggest_questions
from graphify.build import build_from_json
from graphify.export import to_canvas, to_html, to_json
from graphify.report import generate


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


def slug(s: str) -> str:
    out = []
    for ch in s.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_/":
            out.append("_")
    return "_".join(filter(None, "".join(out).split("_")))


def write_community_page(
    code_dir: Path, project: Path, cid: int, label: str, members: list[str],
    cohesion: float, nodes_by_id: dict[str, dict],
) -> None:
    safe = slug(label)
    path = code_dir / f"_COMMUNITY_{cid:02d}_{safe}.md"
    lines = [
        "---",
        f"title: {label}",
        "type: code-community",
        f"community_id: {cid}",
        f"cohesion: {cohesion:.3f}",
        f"member_count: {len(members)}",
        f"updated: {datetime.now(timezone.utc).isoformat()}",
        "---",
        "",
        f"# {label}",
        "",
        f"Cohesion: **{cohesion:.3f}** | Members: **{len(members)}**",
        "",
        "## Members",
        "",
    ]
    for nid in members[:60]:
        nd = nodes_by_id.get(nid, {})
        lbl = nd.get("label", nid)
        src = nd.get("source_file", "")
        loc = nd.get("source_location", "")
        rel = to_rel(src, project) if src else ""
        if rel:
            line_hint = f" _(line {loc})_" if loc else ""
            link = f"[`{lbl}`](../../{rel}){line_hint}"
        else:
            link = f"`{lbl}`"
        lines.append(f"- {link}")
    if len(members) > 60:
        lines.append(f"- _… and {len(members) - 60} more (see graph.json)_")
    lines.append("")
    lines.append("## Drill in")
    lines.append("")
    lines.append("Full structural detail lives in `../../graphify-out/graph.json`. Run `wiki-query` for traversal.")
    path.write_text("\n".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_path", type=Path)
    ap.add_argument("labels_path", type=Path, help="JSON map: {community_id: 'Label'}")
    ap.add_argument("--min-members", type=int, default=3)
    args = ap.parse_args()

    project = args.project_path.resolve()
    out = project / "graphify-out"
    vault = project / "wiki"
    code_dir = vault / "code"
    code_dir.mkdir(parents=True, exist_ok=True)

    extract = json.loads((out / ".graphify_extract.json").read_text())
    analysis = json.loads((out / ".graphify_analysis.json").read_text())
    # The labels file is the persistent record. Always written to graphify-out/labels.json
    # by both graphify-ingest and graphify-update so subsequent runs can preserve labels.
    label_map_raw = json.loads(args.labels_path.read_text())
    # Accept str or int keys
    label_map = {int(k): v for k, v in label_map_raw.items()}

    # Portability: store project-root-relative source_file in graph.json (also
    # migrates an extract that still holds absolute paths).
    for n in extract.get("nodes", []):
        s = n.get("source_file")
        if s:
            n["source_file"] = to_rel(s, project)

    G = build_from_json(extract)
    communities = {int(k): v for k, v in analysis["communities"].items()}
    cohesion = {int(k): v for k, v in analysis["cohesion"].items()}
    gods = analysis["gods"]
    surprises = analysis["surprises"]

    labels = {cid: label_map.get(cid, f"Cluster {cid}") for cid in communities}

    print("[1] Re-suggest questions with real labels")
    questions = suggest_questions(G, communities, labels)

    print("[2] Regenerate GRAPH_REPORT, graph.json, graph.html")
    detection_stub = {
        "total_files": len(set(n.get("source_file", "") for n in extract["nodes"])),
        "total_words": 0,
        "needs_graph": True,
        "warning": None,
        "files": {"code": [], "document": [], "paper": [], "image": []},
    }
    report = generate(
        G, communities, cohesion, labels, gods, surprises, detection_stub,
        {"input": 0, "output": 0}, str(project), suggested_questions=questions,
    )
    (out / "GRAPH_REPORT.md").write_text(report)
    to_json(G, communities, str(out / "graph.json"))
    to_html(G, communities, str(out / "graph.html"), community_labels=labels)

    print("[3] Wipe stale wiki/code/_COMMUNITY_*.md")
    for f in code_dir.glob("_COMMUNITY_*.md"):
        f.unlink()

    print(f"[4] Write community pages (≥{args.min_members} members)")
    nodes_by_id = {n["id"]: n for n in extract["nodes"]}
    meaningful = {cid: m for cid, m in communities.items() if len(m) >= args.min_members}
    for cid, members in sorted(meaningful.items(), key=lambda x: -len(x[1])):
        label = labels.get(cid, f"Cluster {cid}")
        write_community_page(code_dir, project, cid, label, members, cohesion.get(cid, 0.0), nodes_by_id)
    print(f"  {len(meaningful)} pages written ({len(communities) - len(meaningful)} thin clusters skipped)")

    print("[5] Regenerate canvas")
    to_canvas(G, communities, str(code_dir / "graph.canvas"), community_labels=labels)

    print("[6] Update wiki/code/_index.md")
    (code_dir / "_index.md").write_text(
        "---\n"
        "title: Code Structure\n"
        "type: code-index\n"
        f"updated: {datetime.now(timezone.utc).isoformat()}\n"
        "---\n\n"
        "# Code Structure\n\n"
        "Auto-generated by graphify-ingest. Do not hand-edit — overwritten on rebuild.\n\n"
        "## Snapshot\n\n"
        f"- {G.number_of_nodes()} nodes · {G.number_of_edges()} edges\n"
        f"- {len(communities)} raw communities · {len(meaningful)} meaningful (≥{args.min_members} members)\n\n"
        "## Layers\n\n"
        "- **Communities**: see `_COMMUNITY_*.md` summaries below\n"
        "- **Visual**: open `graph.canvas` in Obsidian, or `../../graphify-out/graph.html` in browser\n"
        "- **Full graph**: `../../graphify-out/graph.json` (queryable)\n"
        "- **Audit**: `../../graphify-out/GRAPH_REPORT.md` (god nodes, surprises, suggested questions)\n\n"
        "## Boundary\n\n"
        "Structural facts (calls, types, imports, semantic edges) live in graphify. "
        "Decisions and rationale (the *why*) belong in `../decisions/` and `../concepts/`.\n"
    )

    print("[7] Update wiki/hot.md graph snapshot")
    # Build the snapshot block. We REWRITE the whole hot.md to keep it focused.
    # gods shape: {"id": "...", "label": "...", "degree": N}
    # source_file is on the underlying node, not on the gods entry.
    god_lines = []
    for g in gods[:6]:
        nd = nodes_by_id.get(g.get("id", ""), {})
        src = nd.get("source_file", "")
        rel = to_rel(src, project) if src else ""
        suffix = f" — `{rel}`" if rel else ""
        god_lines.append(f"- `{g.get('label', '?')}`{suffix} ({g.get('degree', 0)} edges)")

    surprise_lines = []
    for s in surprises[:4]:
        rel = s.get("relation", "")
        conf = s.get("confidence", "")
        surprise_lines.append(f"- `{s.get('source', '?')}` --{rel}-> `{s.get('target', '?')}` [{conf}]")

    n_meaningful = len(meaningful)
    n_singleton = sum(1 for m in communities.values() if len(m) == 1)
    snapshot = (
        f"---\n"
        f"type: meta\n"
        f"title: \"Hot Cache\"\n"
        f"updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n"
        f"tags:\n"
        f"  - meta\n"
        f"  - hot-cache\n"
        f"status: evergreen\n"
        f"---\n\n"
        f"# Recent Context\n\n"
        f"Navigation: [[index]] | [[code/_index|code]]\n\n"
        f"## Graph Snapshot\n"
        f"Last graphify-ingest run: **{datetime.now(timezone.utc).strftime('%Y-%m-%d')}**\n"
        f"- **{G.number_of_nodes()} nodes · {G.number_of_edges()} edges · {n_meaningful} meaningful communities** ({len(communities)} raw, {n_singleton} singletons filtered)\n"
        f"- {len(extract.get('hyperedges', []))} hyperedges (group patterns)\n\n"
        f"**God nodes** (most-connected, your core abstractions):\n"
        + "\n".join(god_lines)
        + "\n\n"
        f"**Surprising connections** (cross-community):\n"
        + "\n".join(surprise_lines)
        + "\n\n"
        f"## Open Threads\n"
        f"- See `../graphify-out/GRAPH_REPORT.md` for full audit (suggested questions, ambiguous edges)\n"
        f"- {n_singleton} isolated nodes — review or accept as noise\n\n"
        f"## Conventions\n"
        f"- `wiki/code/` is graphify-owned; do not hand-edit (wiped + regenerated each run).\n"
        f"- Decisions and rationale go in `wiki/decisions/`.\n"
    )
    (vault / "hot.md").write_text(snapshot)

    print("[8] Append run entry to wiki/log.md")
    log_path = vault / "log.md"
    log_entry = (
        f"- {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}: graphify-ingest. "
        f"{G.number_of_nodes()}n/{G.number_of_edges()}e, {n_meaningful} labeled communities.\n"
    )
    if log_path.exists():
        existing = log_path.read_text()
        # Insert under the first H2 if present, else append
        if "\n## " in existing:
            head, _, tail = existing.partition("\n## ")
            log_path.write_text(head + "\n## " + tail.split("\n", 1)[0] + "\n\n" + log_entry + tail.split("\n", 1)[1])
        else:
            log_path.write_text(existing + "\n" + log_entry)
    else:
        log_path.write_text(
            "---\ntype: meta\ntitle: \"Operation Log\"\n---\n\n"
            "# Operation Log\n\n## Recent\n\n" + log_entry
        )

    print()
    print("=== Done ===")
    print(f"  wiki/code/: {len(meaningful)} community pages + _index.md + graph.canvas")
    print(f"  wiki/hot.md: rewritten with graph snapshot")
    print(f"  wiki/log.md: appended run entry")
    print(f"  graphify-out/: graph.json, graph.html, GRAPH_REPORT.md")


if __name__ == "__main__":
    main()
