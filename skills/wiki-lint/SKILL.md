---
name: wiki-lint
description: >
  Health check the Obsidian wiki vault. Finds orphan pages, dead wikilinks, stale claims,
  missing cross-references, frontmatter gaps, empty sections, AND graph-layer drift
  (label/title mismatches, stale labels.json, orphan community pages, graph staleness vs
  source files). Creates or updates Dataview dashboards. Generates canvas maps.
  Triggers on: "lint", "health check", "clean up wiki", "check the wiki", "wiki maintenance",
  "find orphans", "wiki audit", "lint the graph".
---

# wiki-lint: Wiki Health Check

Run lint after every 10-15 ingests, or weekly. Ask before auto-fixing anything. Output a lint report to `wiki/meta/lint-report-YYYY-MM-DD.md`.

---

## Dispatch as a Subagent

A lint pass reads dozens of wiki pages (frontmatter checks, link resolution, orphan detection). Doing this in the main thread bloats the conversation context with file contents that aren't useful after the report is written.

**Default behavior**: dispatch the work to the `wiki-lint-subagent` (defined in `agents/wiki-lint-subagent.md`). The subagent reads the entire vault in its own context and returns only the lint report — typically a few hundred tokens vs. tens of thousands.

```
Agent tool call:
  subagent_type: "wiki-lint-subagent"
  description: "Wiki health check"
  prompt: "Run a full lint pass over the vault at <vault_path>. Scope: <full | folder>. Return the structured lint report as defined in agents/wiki-lint-subagent.md."
```

After the subagent returns:
1. Save the report to `wiki/meta/lint-report-YYYY-MM-DD.md` (the caller / main thread does the file write, not the subagent)
2. Run the **graph-layer lint** in the main thread (it's a Python script call — see below — and produces small structured output)
3. Append the graph-layer output verbatim under a `## Graph Layer` heading in the report
4. Show the user a 5-line summary and ask: "Should I fix these automatically, or do you want to review each one?"

**When to skip the subagent and run inline**:
- Vault has fewer than 20 pages (overhead not worth it)
- User explicitly asks for an interactive lint (subagents can't ask questions mid-run)
- Scope is a single folder under 10 files

---

## Lint Checks

Work through these in order:

### Narrative wiki layer

1. **Orphan pages**. Wiki pages with no inbound wikilinks. They exist but nothing points to them.
2. **Dead links**. Wikilinks that reference a page that does not exist.
3. **Stale claims**. Assertions on older pages that newer sources have contradicted or updated.
4. **Missing pages**. Concepts or entities mentioned in multiple pages but lacking their own page.
5. **Missing cross-references**. Entities mentioned in a page but not linked.
6. **Frontmatter gaps**. Pages missing required fields (type, status, created, updated, tags).
7. **Empty sections**. Headings with no content underneath.
8. **Stale index entries**. Items in `wiki/index.md` pointing to renamed or deleted pages.
8a. **Stale `index.json`** (only if `wiki/index.json` exists). The generated locator's `generated` stamp predates the newest page under `wiki/` (or `services/*/wiki/` when built with `--services`) — re-run `skills/wiki-query/scripts/build_index_json.py`. Same rule for cached sub-answer pages in `questions/` (frontmatter `scope:`) whose cited pages are newer.

### ADLC / multi-wiki layer (only if Mode ADLC)

9. **Broken traceability**. `requirements/` IDs with no `traces_to` link down to `user-stories/`, or stories with no `test-cases/` coverage. The chain requirement → story → test should hold.
10. **Orphan specs**. A `features/` page with no linked per-service spec under `services/*/wiki/`, or a service spec not referenced from any `features/` page.
11. **Cross-wiki drift**. A feature marked shipped in the product wiki whose service code wiki shows no corresponding spec or decision — suggest running `wrap-up` to resync.
12. **Unstable IDs**. `req_id` / story / test IDs that were renumbered. They must be append-only and stable (ba-suite convention).

### Graph layer (only if `graphify-out/graph.json` exists)

Run the dedicated graph-lint helper. It cross-references `graph.json`, `labels.json`, and `wiki/code/_COMMUNITY_*.md` for consistency:

```bash
PYTHON=$(cat graphify-out/.graphify_python 2>/dev/null || echo python3)
# Resolve the skill directory across hosts. Honor CLAUDE_PLUGIN_ROOT when Claude Code
# sets it; otherwise check the common install paths for Claude Code, Codex, OpenCode,
# and Cursor.
SKILL_DIR=""
for cand in \
    "${CLAUDE_PLUGIN_ROOT:+$CLAUDE_PLUGIN_ROOT/skills/wiki-lint}" \
    "$HOME/.claude/plugins/adlc/skills/wiki-lint" \
    "$HOME/.codex/skills/adlc/skills/wiki-lint" \
    "$HOME/.opencode/skills/adlc/skills/wiki-lint" \
    "$HOME/.cursor/skills/adlc/skills/wiki-lint"; do
    [ -n "$cand" ] && [ -d "$cand" ] && { SKILL_DIR="$cand"; break; }
done
[ -z "$SKILL_DIR" ] && { echo "Cannot locate wiki-lint skill dir; set SKILL_DIR explicitly."; exit 1; }
$PYTHON "$SKILL_DIR/scripts/lint_graph.py" .
```

The helper checks:

9. **Title vs label mismatch (FAIL)**: a community page's frontmatter title disagrees with `labels.json`. Indicates labels.json corruption — re-run `/graphify-ingest` to recompute, or manually pick the correct label.
10. **Filename slug drift (WARN)**: `_COMMUNITY_NN_<slug>.md` slug doesn't match a slugification of the title. The page was renamed in one place but not the other.
11. **Cluster ID mismatch (FAIL)**: filename says cluster N, frontmatter says cluster M. Almost always a copy-paste mistake during manual edits.
12. **Member count drift (WARN)**: frontmatter `member_count` doesn't match actual cluster size in graph.json. Run `/graphify-update` and `regenerate.py` to refresh.
13. **Orphan community pages (FAIL)**: `_COMMUNITY_*.md` for a cluster ID no longer in `graph.json`. Delete the page or re-run `/graphify-update`.
14. **Missing labels (WARN)**: meaningful cluster (≥3 members) in graph.json without a `labels.json` entry. Run `/graphify-update` so the assistant can label it.
15. **Stale labels (WARN)**: `labels.json` entry for a cluster ID no longer in `graph.json`. Either remove manually or re-run `/graphify-update`.
16. **Missing community pages (WARN)**: meaningful cluster has no `_COMMUNITY_*.md` page. Run `regenerate.py` from the graphify-ingest skill.
17. **Graph staleness (INFO)**: source files modified after `graph.json` was last written. Suggests running `/graphify-update`.

The helper exits non-zero if any FAIL is present. Show its output verbatim in the lint report — don't paraphrase.

---

## Lint Report Format

Create at `wiki/meta/lint-report-YYYY-MM-DD.md`:

```markdown
---
type: meta
title: "Lint Report YYYY-MM-DD"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [meta, lint]
status: developing
---

# Lint Report: YYYY-MM-DD

## Summary
- Pages scanned: N
- Issues found: N
- Auto-fixed: N
- Needs review: N

## Orphan Pages
- [[Page Name]]: no inbound links. Suggest: link from [[Related Page]] or delete.

## Dead Links
- [[Missing Page]]: referenced in [[Source Page]] but does not exist. Suggest: create stub or remove link.

## Missing Pages
- "concept name": mentioned in [[Page A]], [[Page B]], [[Page C]]. Suggest: create a concept page.

## Frontmatter Gaps
- [[Page Name]]: missing fields: status, tags

## Stale Claims
- [[Page Name]]: claim "X" may conflict with newer source [[Newer Source]].

## Cross-Reference Gaps
- [[Entity Name]] mentioned in [[Page A]] without a wikilink.

## Graph Layer (if applicable)
<paste the verbatim output of scripts/lint_graph.py here>
```

---

## Naming Conventions

Enforce these during lint:

| Element | Convention | Example |
|---------|-----------|---------|
| Filenames | Title Case with spaces | `Machine Learning.md` |
| Folders | lowercase with dashes | `wiki/data-models/` |
| Tags | lowercase, hierarchical | `#domain/architecture` |
| Wikilinks | match filename exactly | `[[Machine Learning]]` |

Filenames must be unique across the vault. Wikilinks work without paths only if filenames are unique.

---

## Writing Style Check

During lint, flag pages that violate the style guide:

- Not declarative present tense ("X basically does Y" instead of "X does Y")
- Missing source citations where claims are made
- Uncertainty not flagged with `> [!gap]`
- Contradictions not flagged with `> [!contradiction]`

---

## Dataview Dashboard

Create or update `wiki/meta/dashboard.md` with these queries:

````markdown
---
type: meta
title: "Dashboard"
updated: YYYY-MM-DD
---
# Wiki Dashboard

## Recent Activity
```dataview
TABLE type, status, updated FROM "wiki" SORT updated DESC LIMIT 15
```

## Seed Pages (Need Development)
```dataview
LIST FROM "wiki" WHERE status = "seed" SORT updated ASC
```

## Entities Missing Sources
```dataview
LIST FROM "wiki/entities" WHERE !sources OR length(sources) = 0
```

## Open Questions
```dataview
LIST FROM "wiki/questions" WHERE answer_quality = "draft" SORT created DESC
```
````

---

## Canvas Map

Create or update `wiki/meta/overview.canvas` for a visual domain map:

```json
{
  "nodes": [
    {
      "id": "1",
      "type": "file",
      "file": "wiki/overview.md",
      "x": 0, "y": 0,
      "width": 300, "height": 140,
      "color": "1"
    }
  ],
  "edges": []
}
```

Add one node per domain page. Connect domains that have significant cross-references. Colors map to the CSS scheme: 1=blue, 2=purple, 3=yellow, 4=orange, 5=green, 6=red.

---

## Before Auto-Fixing

Always show the lint report first. Ask: "Should I fix these automatically, or do you want to review each one?"

Safe to auto-fix:
- Adding missing frontmatter fields with placeholder values
- Creating stub pages for missing entities
- Adding wikilinks for unlinked mentions

Needs review before fixing:
- Deleting orphan pages (they might be intentionally isolated)
- Resolving contradictions (requires human judgment)
- Merging duplicate pages
