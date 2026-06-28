# ba-suite integration (ADLC mode)

How the `ba-suite` plugin plugs into an ADLC vault. `ba-suite` is external to claude-mem; this doc defines the contract so its outputs land as canonical wiki Markdown and can be exported back out. Used by Mode ADLC (see [`modes.md`](modes.md)).

## Principle

The wiki is the system of record. `ba-suite` is the engine at both ends:

- **Ingest:** convert raw context (Confluence, Jira, meeting notes) into BA deliverables, written as Markdown into the ADLC folders.
- **Export:** render wiki content to Office formats for distribution.

`ba-suite`'s native output is Office files (`.docx` / `.xlsx` / `.drawio`) under its own output folder. In ADLC mode you override that: deliverables are authored as vault Markdown (a deliberate deviation from the skill's default output). Office generation is reserved for the export step.

## Convention bridge

When invoking a `ba-suite` skill inside an ADLC vault, tell it:

1. System of record is the vault Markdown, not Office files.
2. Write into the mapped folder (table below), one note per artifact, with YAML frontmatter and `[[wikilinks]]`.
3. Preserve stable IDs and never renumber (append new IDs at the end). The `ba-suite` ID schemes are the anchors that make traceability work.
4. Build `[[traceability]]` links between requirements, stories, tests, and gaps.
5. Do not write Office files during ingest; those are produced only on export.

## Ingest map (source + skill to folder)

| ba-suite skill | Lifecycle | Wiki folder | ID scheme |
|---|---|---|---|
| elicitation-synthesizer | Discovery | `requirements/` | `{PREFIX}-FR/NFR-NNN` |
| stakeholder-analyzer | Discovery | `stakeholders/` | RACI roles |
| workshop-facilitator | Discovery | `comms/` | session synthesis |
| process-modeler | Analysis | `features/` | process spec |
| gap-analysis | Analysis | `gaps/` | `G-{DIM}-NNN` |
| user-story-factory | Definition | `user-stories/` | `{PREFIX}-{EPIC}-NNN` |
| business-case-builder | Definition | `deliverables/` | business case |
| rfi-rfp-analyzer | Definition | `deliverables/` or `intel/` | `{Section}-NNN` |
| solution-assessment | Validation | `deliverables/` | scoring model |
| test-case-generator | Validation | `test-cases/` (qa concern) | `TC-{STORY}-{TYPE}-NNN` |
| scrum-events-pack | Delivery | `sprints/` | `IMP-/DEP-/RA-NNN` |
| requirements-lifecycle | Cross-cutting | `requirements/` | RTM, approval pack, CRs |
| planning-monitor | Cross-cutting | `planning/` | BA approach, governance |

Inbound sources land in `.raw/` first and get a summary page in `sources/` (via `wiki-ingest`); BA deliverables cite those `sources/` pages.

## Sub-agent orchestration

`ba-suite` runs through a single worker that covers the whole skill family: `agents/ba-suite-subagent.md`. The main thread (the Mode ADLC initial pass, or the `wrap-up` skill) is the only dispatcher; workers never dispatch each other.

- **One task per dispatch.** Give the worker a task, the `ba-suite` skill(s) to run, the vault path, and the inputs (sources or upstream IDs). It invokes the skills via the Skill tool and files Markdown.
- **Sequence the handoffs.** Honor the choreography: requirements to stories to tests; gap to business case. Run dependent steps in order.
- **Parallelize independent work.** Decomposing three unrelated features, or authoring FRs across disjoint areas, can run as parallel workers in one message.
- **Caller owns the indexes.** After the workers finish, the dispatcher updates `index` / `log` / `hot` once and runs a cross-reference pass. Workers do not touch those files.
- **Coordinate by scope.** For overlapping writes, partition by folder or serialize the consolidating step; the Edit drift check is the backstop.

After the BA layer is filed, the shift-left `architecture-subagent` refines requirements into per-service technical specs. See [`technical-planning.md`](technical-planning.md).

## Export seam (build later)

Reuse `ba-suite`'s Office generation to render wiki content back to `.docx` / `.xlsx`, written to `.raw/exports/`. From there, integrate to Jira (stories to issues, test cases to test management) or ClickUp. This direction is documented so folder + ID conventions stay export-friendly; it is not implemented yet.

Diagrams in the formal export use PlantUML (rendered PNGs alongside the Office docs). The living tech docs use Mermaid with an HTML export instead (see [`technical-planning.md`](technical-planning.md)).

## Metrics seam (build later)

`log.md` is the activity ledger: each entry stamps the skill that ran and the deliverables produced. To enable cost-saving rollups later, populate the `produced_by` / `effort_estimate` / `feature` frontmatter fields and keep a `meta/ba-activity.md` summary. Rollup target: deliverables produced per feature versus the BA / QA / PM time they replace.

## Privacy

Keep PII out of the committed wiki (person names, headcount, contract values). Sensitive context goes in a gitignored private note; role-based analysis (RACI, engagement) stays in the wiki without named individuals.
