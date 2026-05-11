"""Detect what changed since the last graphify run.

Reads graphify's manifest (auto-saved on each full run), compares to current
filesystem, prints a summary, and writes a chunk plan IF docs/images changed
(those need subagent dispatch). Code changes are AST-only and cheap — no chunks.

Outputs:
    graphify-out/.update_changes.json  — full delta
    graphify-out/.path_b_chunks.json   — chunks for changed docs/images (if any)

Usage:
    python detect.py <project_path> [--include-images]
"""

import argparse
import json
import sys
from pathlib import Path

from graphify.detect import detect_incremental

CHUNK_SIZE = 22

EXCLUDE_SUBPATHS = (
    "wiki", "graphify-out", "node_modules", ".next", ".git", ".idea",
    "build", "out", "dist", "coverage", ".vercel",
)


def keep(path: str, project: Path) -> bool:
    try:
        rel = Path(path).resolve().relative_to(project) if Path(path).is_absolute() else Path(path)
    except ValueError:
        return False
    return not any(p in EXCLUDE_SUBPATHS for p in rel.parts)


def chunk(lst: list, size: int) -> list[list]:
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_path", type=Path)
    ap.add_argument("--include-images", action="store_true")
    args = ap.parse_args()

    project = args.project_path.resolve()
    out = project / "graphify-out"
    if not (out / "graph.json").exists():
        print("ERROR: no existing graph.json. Run /graphify-ingest first for the initial build.")
        sys.exit(2)

    delta = detect_incremental(project)
    new_files = delta.get("new_files", {})
    deleted = delta.get("deleted_files", [])

    code_changed = [f for f in new_files.get("code", []) if keep(f, project)]
    docs_changed = [
        f for f in new_files.get("document", []) + new_files.get("paper", [])
        if keep(f, project)
    ]
    images_changed = (
        [f for f in new_files.get("image", []) if keep(f, project)]
        if args.include_images else []
    )

    print(f"Code changed:  {len(code_changed)}")
    print(f"Docs changed:  {len(docs_changed)}")
    print(f"Images:        {len(images_changed)}{' (skipped)' if not args.include_images and new_files.get('image') else ''}")
    print(f"Deleted:       {len(deleted)}")
    print()

    total = len(code_changed) + len(docs_changed) + len(images_changed) + len(deleted)
    if total == 0:
        print("Nothing changed since last run. Skip the rebuild.")
        (out / ".update_changes.json").write_text(json.dumps({"empty": True}))
        return

    # Save the delta for update.py to consume
    changes = {
        "code_changed": code_changed,
        "docs_changed": docs_changed,
        "images_changed": images_changed,
        "deleted": deleted,
        "code_only": (len(docs_changed) == 0 and len(images_changed) == 0),
    }
    (out / ".update_changes.json").write_text(json.dumps(changes, indent=2))

    # Build chunks ONLY for docs/images (semantic extraction needed)
    # Code uses graphify's AST cache + fresh extraction in update.py — no subagents.
    if not docs_changed and not images_changed:
        (out / ".path_b_chunks.json").write_text(json.dumps({"total": 0, "chunks": []}))
        print("Code-only changes — no subagent dispatch needed. Run update.py.")
        return

    plan = []
    n = 1
    for c in chunk(docs_changed, CHUNK_SIZE):
        plan.append({"chunk_num": n, "kind": "docs", "files": c, "deep_mode": False, "ast_ids": []})
        n += 1
    for img in images_changed:
        plan.append({"chunk_num": n, "kind": "image", "files": [img], "deep_mode": False, "ast_ids": []})
        n += 1

    (out / ".path_b_chunks.json").write_text(json.dumps({"total": len(plan), "chunks": plan}, indent=2))
    print(f"{len(plan)} chunks planned for changed docs/images:")
    for p in plan:
        print(f"  chunk {p['chunk_num']:02d} [{p['kind']:5s}] {len(p['files']):3d} files")


if __name__ == "__main__":
    main()
