# ba-suite integration (ADLC mode)

The BA method set is **bundled** into claude-mem at `skills/wiki/references/ba/` (no external `ba-suite` plugin required). This doc defines how it plugs into an ADLC vault so its outputs land as canonical wiki Markdown and can be exported back out. Used by Mode ADLC (see [`modes.md`](modes.md)).

## Principle

The wiki is the system of record. The bundled BA method set (`skills/wiki/references/ba/`) is the engine at both ends:

- **Ingest:** convert raw context (Confluence, Jira, meeting notes) into BA deliverables, written as Markdown into the ADLC folders.
- **Export:** render wiki content to Office formats for distribution.

The method docs' native output is Office files (`.docx` / `.xlsx` / `.drawio`). In ADLC mode you override that (see `ba/_index.md`): deliverables are authored as vault Markdown. Office generation is reserved for the export step.

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

## Export (the ba-export skill)

The `ba-export` skill (with `ba-export-subagent`) renders wiki content back to `.docx` / `.xlsx` via `ba-suite`, written to `.raw/exports/`, and optionally pushes to Jira (stories to issues, test cases to test management) or ClickUp over MCP. Folder + ID conventions are kept export-friendly so re-export is idempotent (a `tracker-manifest.json` maps pages to task IDs).

Diagrams in the formal export use PlantUML (rendered PNGs alongside the Office docs). The living tech docs use Mermaid with an HTML export instead (see [`technical-planning.md`](technical-planning.md)).

## Metrics seam

`log.md` is the activity ledger: each entry stamps the skill that ran and the deliverables produced. Populate the `produced_by` / `effort_estimate` / `feature` frontmatter fields on every authored note — `meta/ba-activity.md` rolls them up into deliverables produced per feature versus the BA / QA / PM time they replace, and `meta/mission-control.md` gives the operator the async delivery board. Formats and update triggers: [`mission-control.md`](mission-control.md).

## Privacy

Keep PII out of the committed wiki (person names, headcount, contract values). Sensitive context goes in a gitignored private note; role-based analysis (RACI, engagement) stays in the wiki without named individuals.
