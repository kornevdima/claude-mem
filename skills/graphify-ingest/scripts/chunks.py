"""Compute the chunk plan for parallel semantic extraction.

Outputs `graphify-out/.path_b_chunks.json` with per-chunk file lists,
plus AST ID hints (so subagents only connect to existing nodes — fixes the
edge-drop issue from the test run).

Usage:
    python chunks.py <project_path> [--mode A|B] [--include-images]
"""

import argparse
import json
import sys
from pathlib import Path

from graphify.detect import detect
from graphify.extract import collect_files, extract

CHUNK_SIZE = 22  # graphify's tested batch size

EXCLUDE_SUBPATHS = (
    "wiki",
    "graphify-out",
    "node_modules",
    ".next",
    ".git",
    ".idea",
    "build",
    "out",
    "dist",
    "coverage",
    ".vercel",
)


def keep(path: str, project: Path) -> bool:
    rel = Path(path).resolve().relative_to(project) if Path(path).is_absolute() else Path(path)
    parts = rel.parts
    return not any(p in EXCLUDE_SUBPATHS for p in parts)


def chunk(lst: list, size: int) -> list[list]:
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_path", type=Path)
    ap.add_argument("--mode", choices=["A", "B"], default="B",
                    help="A: AST only (no chunks). B: AST + semantic (chunks dispatched)")
    ap.add_argument("--include-images", action="store_true",
                    help="Include image files in semantic extraction (expensive)")
    args = ap.parse_args()

    project = args.project_path.resolve()
    out = project / "graphify-out"
    out.mkdir(exist_ok=True)

    det = detect(project)
    docs = [f for f in det["files"].get("document", []) + det["files"].get("paper", []) if keep(f, project)]
    code = [f for f in det["files"].get("code", []) if keep(f, project)]
    images = [f for f in det["files"].get("image", []) if keep(f, project)] if args.include_images else []
    excluded_total = (
        len(det["files"].get("document", []))
        + len(det["files"].get("paper", []))
        + len(det["files"].get("code", []))
        + len(det["files"].get("image", []))
        - len(docs) - len(code) - len(images)
    )

    print(f"Mode:       {args.mode}")
    print(f"Docs:       {len(docs)}")
    print(f"Code:       {len(code)}")
    print(f"Images:     {len(images)}{' (skipped)' if not args.include_images and det['files'].get('image') else ''}")
    print(f"Excluded:   {excluded_total} (under wiki/, graphify-out/, node_modules/, etc.)")
    print()

    # Build AST ID hints: which IDs already exist in the AST graph for each file?
    # Subagents need this so they only create edges to known nodes.
    print("Pre-extracting AST to compute per-file ID hints...")
    code_paths = []
    for f in code:
        p = Path(f)
        code_paths.extend(collect_files(p) if p.is_dir() else [p])
    ast = extract(code_paths, cache_root=project) if code_paths else {"nodes": [], "edges": []}
    file_to_ast_ids: dict[str, list[str]] = {}
    for n in ast["nodes"]:
        src = n.get("source_file", "")
        if src:
            file_to_ast_ids.setdefault(str(Path(src).resolve()), []).append(n["id"])
    print(f"  AST: {len(ast['nodes'])} nodes across {len(file_to_ast_ids)} files")

    # Save the AST IDs so merge.py can avoid duplicating work
    (out / ".ast_ids_by_file.json").write_text(json.dumps(file_to_ast_ids))
    (out / ".ast_extract.json").write_text(json.dumps(ast))
    # Save the full detection so merge.py can write a proper manifest for incremental updates
    (out / ".graphify_detect.json").write_text(json.dumps(det))

    if args.mode == "A":
        # No chunks needed — merge.py handles AST-only path
        (out / ".path_b_chunks.json").write_text(json.dumps({"total": 0, "chunks": []}))
        print("\nMode A: no chunks. Run merge.py + regenerate.py.")
        return

    # Mode B: build chunks
    plan = []
    n = 1
    for c in chunk(docs, CHUNK_SIZE):
        plan.append({"chunk_num": n, "kind": "docs", "files": c, "deep_mode": False, "ast_ids": []})
        n += 1
    for c in chunk(code, CHUNK_SIZE):
        # Collect AST IDs for files in this chunk
        ids = []
        for f in c:
            ids.extend(file_to_ast_ids.get(str(Path(f).resolve()), []))
        plan.append({"chunk_num": n, "kind": "code", "files": c, "deep_mode": True, "ast_ids": ids})
        n += 1
    if args.include_images and images:
        # Each image gets its own chunk (vision needs separate context per graphify spec)
        for img in images:
            plan.append({"chunk_num": n, "kind": "image", "files": [img], "deep_mode": False, "ast_ids": []})
            n += 1

    (out / ".path_b_chunks.json").write_text(json.dumps({"total": len(plan), "chunks": plan}, indent=2))

    print(f"\n{len(plan)} chunks planned:")
    for p in plan:
        ast_hint = f" + {len(p['ast_ids'])} AST IDs" if p["ast_ids"] else ""
        print(f"  chunk {p['chunk_num']:02d} [{p['kind']:5s}] {len(p['files']):3d} files  deep={p['deep_mode']}{ast_hint}")
    print(f"\nPlan: {out / '.path_b_chunks.json'}")


if __name__ == "__main__":
    main()
