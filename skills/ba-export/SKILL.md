---
name: ba-export
description: >
  Export the wiki's canonical BA / project deliverables to formal Office documents
  (.docx / .xlsx) and diagrams (PlantUML), written to .raw/exports/, by reusing the
  ba-suite skills. Optionally push to a tracker (ClickUp / Jira) over MCP. The wiki stays
  the source of truth; Office files are a generated view. For Mode ADLC and Mode C vaults.
  Triggers on: "/ba-export", "ba export", "export to docs", "export the BRD",
  "export the backlog", "generate the requirements doc", "export test cases",
  "export BA deliverables", "export to clickup", "export to jira", "produce office docs".
---

# ba-export: Export BA deliverables to documents

The wiki holds the canonical BA deliverables as Markdown. This skill renders them to formal Office files (and pushes to a tracker on request). It does NOT author or change deliverables — that is ingest. Export is one-way: wiki to docs.

## When to use

- An ADLC or Mode C vault has BA deliverables (requirements register, backlog, test cases, gap analysis, business case, ...) and a human needs `.docx` / `.xlsx`, or wants them in ClickUp / Jira.
- Do NOT use to create or edit deliverables. That is `wiki-ingest` plus the BA workers.

## Principle

Wiki Markdown is the system of record. `ba-suite` is the rendering engine. Office files land in `.raw/exports/` (a generated view; safe to delete and regenerate). Diagrams in the formal export use PlantUML (Mermaid stays in the living wiki docs). See `wiki/references/ba-suite-pipeline.md` and `mcp-setup.md`.

## Deliverable to ba-suite skill to output

| Wiki source | ba-suite skill | Office output |
|---|---|---|
| `requirements/` register, RTM, approval pack | ba-elicitation-synthesizer / ba-requirements-lifecycle | `*_BRD.docx`, `*_requirements_register.xlsx`, `*_traceability.xlsx`, `*_sign_off_pack.docx` |
| `user-stories/` backlog | ba-user-story-factory | `*_product_backlog.xlsx`, `*_story_spec.docx` |
| `test-cases/` + `coverage/` | ba-test-case-generator | `*_test_cases.xlsx`, `*_uat_script.docx`, `*_bdd_spec.yaml` |
| `gaps/` | ba-gap-analysis | `*_gap_analysis.xlsx`, `*_gap_analysis_report.docx`, `*_gap_heatmap` (PlantUML) |
| `deliverables/` business case | ba-business-case-builder | `*_business_case.docx`, `*_financial_model.xlsx` |
| `deliverables/` solution assessment | ba-solution-assessment | `*_solution_assessment.xlsx`, `*_report.docx` |
| `stakeholders/` | ba-stakeholder-analyzer | `*_stakeholder_analysis.docx`, `*_grid` (PlantUML) |
| `features/` process models | ba-process-modeler | `*_process_spec.docx`, `*_model` (PlantUML) |
| `sprints/` | ba-scrum-events-pack | `sprint_N_*.docx` / `.xlsx` |
| `planning/` | ba-planning-monitor | `*_ba_*.docx` |

## Steps

1. **Scope.** Ask what to export (a named deliverable, a folder, or "all current deliverables"). Read the relevant `wiki/<folder>/_index.md` to list candidates. Default to what the user named.
2. **Prepare output.** Ensure `.raw/exports/` exists.
3. **Dispatch workers.** For each deliverable, dispatch ONE `ba-export-subagent` (parallel, one message) with the wiki source page path(s), the target `ba-suite` skill, and the output dir `.raw/exports/`. The worker invokes the `ba-suite` skill to render the Office file(s).
4. **Collect + report.** Verify each expected file exists in `.raw/exports/`. Report the produced files grouped by deliverable.
5. **Tracker push (optional, on request).** If the user asked to push to ClickUp / Jira: map deliverables to the tracker (stories to issues / subtasks, test cases to test items) over MCP, and maintain `.raw/exports/tracker-manifest.json` (wiki page to task ID) so re-export is idempotent. This is outward-facing — confirm before creating tracker items. See `wiki/references/mcp-setup.md`.

## Rules

- Read-only on `wiki/` and `.raw/` sources. Write only under `.raw/exports/`.
- Preserve the stable IDs from the wiki in the exported docs; never renumber.
- Diagrams: PlantUML for the formal export, not Mermaid.
- Tracker creation is outward-facing: confirm first; reads are fine.
- Do not commit / push unless asked.

## Output

```
Exported to .raw/exports/:
- [deliverable] -> [files]
...
Tracker: [N created / updated, or "skipped"]
```
