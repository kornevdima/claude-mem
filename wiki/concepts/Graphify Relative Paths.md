---
type: concept
title: "Graphify Relative Paths (plan)"
created: 2026-06-28
updated: 2026-06-28
confidence: high
tags:
  - concept
  - design
  - graphify
  - plan
  - multi-member
status: planned
related:
  - "[[graphify-integration]]"
---

# Graphify Relative Paths (plan)

**Problem.** graphify's committed artifacts bake in machine-absolute paths, so a teammate who checks the project out at a different path gets broken references. Specifically the `source_file` values in `graphify-out/graph.json`, and the absolute paths echoed in `GRAPH_REPORT.md` and `wiki/code/_COMMUNITY_*.md`. The project is meant to be shared across team members, so committed graph artifacts must be portable.

## Already fine (no change)

- `TARGET=$(cd "$TARGET" && pwd)` in the skills resolves the project root at runtime; it is not hardcoded.
- `.graphify_python` (interpreter pin) is gitignored and machine-local; a legitimately absolute, per-machine value.
- `chunks.py` / `detect.py` already compute file lists relative to the project root.

## Plan (store relative directories)

1. **Store `source_file` relative to the project root** in `graphify-out/graph.json`. Add a post-merge relativization pass (in `merge.py` or `regenerate.py`) that rewrites any absolute `source_file` to a project-root-relative path. This covers paths from both the external AST extractor and the semantic subagents.
2. **`graphify-extract-subagent.md`**: change the schema and instructions so `source_file` is recorded relative to a project root passed in the prompt (read via absolute, store relative).
3. **Query skills** (`graphify-explain` / `-path` / `-query`): treat `source_file` as relative; resolve to absolute only when opening a file. Output stays portable.
4. **Report + community pages** (`regenerate.py`): cite relative paths in `GRAPH_REPORT.md` and `wiki/code/_COMMUNITY_*.md`.
5. **Docs**: note in `graphify-ingest` that committed artifacts are project-root-relative; only `.graphify_python` stays local.
6. **Migration**: existing graphs with absolute paths -> re-run `/graphify-ingest`, or a one-off relativize script over `graph.json`.

## Risk / unknown

Whether the external `graphifyy` package emits absolute `source_file`. The post-merge relativization (step 1) makes the fix robust regardless of source.

Tracked as Phase 13.
