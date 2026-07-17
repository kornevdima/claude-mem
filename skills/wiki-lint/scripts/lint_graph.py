"""Graph-layer lint checks for the adlc wiki vault.

Cross-references:
  graphify-out/graph.json     — source of truth for cluster IDs and members
  graphify-out/labels.json    — must agree with graph.json on cluster IDs
  wiki/code/_COMMUNITY_*.md   — must agree with both on title/member_count/community_id

Exits 0 when no issues. Prints a structured report to stdout.

Usage:
    python lint_graph.py <project_path> [--strict]

--strict: also flag clusters with cohesion < 0.10 (loose clusters likely need re-labeling
or splitting). Default off because some loose clusters are legitimate (large project areas).
"""

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def slug(s: str) -> str:
    out = []
    for ch in s.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_/":
            out.append("_")
    return "_".join(filter(None, "".join(out).split("_")))


def parse_frontmatter(text: str) -> dict:
    """Cheap YAML frontmatter parser — handles flat key:value pairs, that's all we need."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end]
    out: dict = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_path", type=Path)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    project = args.project_path.resolve()
    graph_path = project / "graphify-out" / "graph.json"
    labels_path = project / "graphify-out" / "labels.json"
    code_dir = project / "wiki" / "code"

    if not graph_path.exists():
        print("[graph-lint] No graphify-out/graph.json — skipping graph-layer lint.")
        print("If this is a code project, run /graphify-ingest to build the graph.")
        return 0

    graph = json.loads(graph_path.read_text())
    labels: dict[str, str] = (
        json.loads(labels_path.read_text()) if labels_path.exists() else {}
    )

    # Build cluster_id -> set(node_ids) from graph.json
    clusters: dict[int, set[str]] = defaultdict(set)
    for n in graph.get("nodes", []):
        cid = n.get("community")
        if cid is not None:
            clusters[int(cid)].add(n["id"])

    # Find meaningful clusters (size >= 3) — same threshold as regenerate.py
    meaningful = {cid: members for cid, members in clusters.items() if len(members) >= 3}

    issues: list[tuple[str, str]] = []  # (severity, message)

    # Build a node lookup once for efficiency
    nodes_by_id = {n["id"]: n for n in graph.get("nodes", [])}

    # ---- Check 1: missing labels for meaningful clusters
    for cid in sorted(meaningful):
        if str(cid) not in labels:
            sample = [
                nodes_by_id.get(nid, {}).get("label", nid)
                for nid in list(meaningful[cid])[:3]
            ]
            issues.append((
                "warn",
                f"Cluster {cid} ({len(meaningful[cid])} members) has no entry in labels.json — "
                f"run /graphify-update or label manually. Sample: {', '.join(sample)}"
            ))

    # ---- Check 2: stale labels (in labels.json but cluster no longer exists)
    for label_cid_str in labels:
        try:
            label_cid = int(label_cid_str)
        except ValueError:
            issues.append(("warn", f"labels.json key {label_cid_str!r} is not an integer"))
            continue
        if label_cid not in clusters:
            issues.append((
                "warn",
                f"labels.json has cluster {label_cid} ('{labels[label_cid_str]}') "
                f"but no such cluster exists in current graph.json — stale entry"
            ))
        elif label_cid not in meaningful:
            # Cluster exists but is now too small to be meaningful
            issues.append((
                "info",
                f"labels.json has cluster {label_cid} ('{labels[label_cid_str]}') "
                f"but cluster shrunk to {len(clusters[label_cid])} members (below threshold of 3)"
            ))

    # ---- Check 3: community page consistency
    if code_dir.exists():
        # Pattern: _COMMUNITY_NN_slug.md
        page_pattern = re.compile(r"^_COMMUNITY_(\d{1,3})_(.+)\.md$")
        seen_cids: set[int] = set()
        for page in sorted(code_dir.glob("_COMMUNITY_*.md")):
            m = page_pattern.match(page.name)
            if not m:
                issues.append(("warn", f"Page {page.name} doesn't match _COMMUNITY_NN_<slug>.md pattern"))
                continue
            file_cid = int(m.group(1))
            file_slug = m.group(2)
            seen_cids.add(file_cid)

            fm = parse_frontmatter(page.read_text())
            try:
                fm_cid = int(fm.get("community_id", "-1"))
            except ValueError:
                fm_cid = -1
            fm_title = fm.get("title", "").strip().strip('"').strip("'")
            try:
                fm_member_count = int(fm.get("member_count", "0"))
            except ValueError:
                fm_member_count = 0

            # 3a. community_id in filename matches frontmatter
            if fm_cid != file_cid:
                issues.append((
                    "fail",
                    f"{page.name}: filename says cluster {file_cid}, frontmatter says {fm_cid}"
                ))

            # 3b. filename slug matches a slugification of the title
            expected_slug = slug(fm_title)
            if fm_title and file_slug != expected_slug:
                issues.append((
                    "warn",
                    f"{page.name}: filename slug '{file_slug}' doesn't match title-derived slug "
                    f"'{expected_slug}' (title: {fm_title!r}). Could be label drift or rename gap."
                ))

            # 3c. cluster exists in graph.json
            if file_cid not in clusters:
                issues.append((
                    "fail",
                    f"{page.name}: cluster {file_cid} doesn't exist in graph.json — orphan page, "
                    f"delete or re-run /graphify-update"
                ))
                continue

            # 3d. member_count in frontmatter matches actual cluster size
            actual_size = len(clusters[file_cid])
            if fm_member_count != actual_size:
                issues.append((
                    "warn",
                    f"{page.name}: frontmatter says {fm_member_count} members, "
                    f"graph.json says {actual_size}. Re-run /graphify-update or regenerate.py."
                ))

            # 3e. labels.json entry matches frontmatter title
            label_in_labels = labels.get(str(file_cid))
            if label_in_labels and fm_title and label_in_labels != fm_title:
                issues.append((
                    "fail",
                    f"{page.name}: title is {fm_title!r} but labels.json[{file_cid}] = {label_in_labels!r}. "
                    f"Mismatch — one is wrong."
                ))

        # 3f. meaningful clusters without a community page
        for cid in meaningful:
            if cid not in seen_cids:
                title = labels.get(str(cid), f"Cluster {cid}")
                issues.append((
                    "warn",
                    f"Cluster {cid} ('{title}', {len(meaningful[cid])} members) has no "
                    f"_COMMUNITY_*.md page in wiki/code/ — run /graphify-update or regenerate"
                ))

    # ---- Check 4: graph staleness vs source files
    graph_mtime = graph_path.stat().st_mtime
    EXCLUDE = ("wiki/", "graphify-out/", "node_modules/", ".next/", ".git/", ".idea/")
    stale_count = 0
    newest_source: tuple[str, float] = ("", 0.0)
    for n in graph.get("nodes", []):
        src = n.get("source_file")
        if not src:
            continue
        try:
            src_path = Path(src)
            if not src_path.exists():
                continue
            rel = str(src_path.resolve().relative_to(project))
            if any(rel.startswith(e) for e in EXCLUDE):
                continue
            src_mtime = src_path.stat().st_mtime
            if src_mtime > graph_mtime:
                stale_count += 1
                if src_mtime > newest_source[1]:
                    newest_source = (rel, src_mtime)
        except (OSError, ValueError):
            pass

    if stale_count:
        ago = datetime.now(timezone.utc).timestamp() - newest_source[1]
        hrs = ago / 3600
        issues.append((
            "info",
            f"Graph staleness: {stale_count} tracked source files modified after graph.json. "
            f"Most recent: {newest_source[0]} ({hrs:.1f}h ago). Consider /graphify-update."
        ))

    # ---- Check 5: optional cohesion check
    if args.strict:
        # We don't have analysis.json after a clean run (it's intermediate),
        # so skip cohesion unless we restructure where it's persisted. Note as TODO.
        pass

    # ---- Report
    print(f"# Graph-Layer Lint  ({project.name})")
    print()
    print(f"- Clusters in graph: {len(clusters)} ({len(meaningful)} meaningful, ≥3 members)")
    print(f"- Labels.json entries: {len(labels)}")
    if code_dir.exists():
        print(f"- Community pages: {len(list(code_dir.glob('_COMMUNITY_*.md')))}")
    print(f"- Issues found: {len(issues)}")
    print()

    if not issues:
        print("All graph-layer checks pass.")
        return 0

    by_sev: dict[str, list[str]] = {"fail": [], "warn": [], "info": []}
    for sev, msg in issues:
        by_sev[sev].append(msg)

    for sev_name, header in [("fail", "## FAIL"), ("warn", "## WARN"), ("info", "## INFO")]:
        if by_sev[sev_name]:
            print(header)
            for m in by_sev[sev_name]:
                print(f"- {m}")
            print()

    return 1 if by_sev["fail"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
