# Bundled BA method set

These are the BA methodology docs (the ba-suite skill set) **bundled into claude-mem** so the external `ba-suite` plugin is NOT required. The `ba-suite-subagent` and `ba-export-subagent` read these directly; they do not call `ba-suite:*` via the Skill tool.

Source: derived from the ba-suite skill set (see `ATTRIBUTION.md`). One file per method.

## ADLC overrides (read these BEFORE applying any method doc)

The method docs were written to emit Office files to `/mnt/user-data/outputs/`. In claude-mem that is overridden:

1. **System of record is the wiki Markdown.** When authoring (ingest), write each deliverable as a Markdown note into the ADLC wiki folder (table below), with YAML frontmatter, `[[wikilinks]]`, and stable IDs. Do NOT emit Office files during authoring.
2. **Office only on export.** `.docx` / `.xlsx` are produced only by the `ba-export` path, into `.raw/exports/`. PlantUML for formal-export diagrams; Mermaid in the living wiki docs.
3. **Stable IDs, never renumber** (append new IDs at the end). The ID schemes in `ba-suite-orientation.md` are the anchors for traceability.
4. **No PII** in the committed wiki (person names, headcount, contract values) — keep those in gitignored private notes.

## Method to wiki folder to ID

| Method doc | Lifecycle | Wiki folder | ID scheme |
|---|---|---|---|
| `ba-suite-orientation` | conventions | — | ID schemes, writing standards |
| `ba-elicitation-synthesizer` | Discovery | `requirements/` | `{PREFIX}-FR/NFR-NNN` |
| `ba-stakeholder-analyzer` | Discovery | `stakeholders/` | RACI roles |
| `ba-workshop-facilitator` | Discovery | `comms/` | session synthesis |
| `ba-process-modeler` | Analysis | `features/` | process spec |
| `ba-gap-analysis` | Analysis | `gaps/` | `G-{DIM}-NNN` |
| `ba-user-story-factory` | Definition | `user-stories/` | `{PREFIX}-{EPIC}-NNN` |
| `ba-business-case-builder` | Definition | `deliverables/` | business case |
| `ba-rfi-rfp-analyzer` | Definition | `deliverables/` or `intel/` | `{Section}-NNN` |
| `ba-solution-assessment` | Validation | `deliverables/` | scoring |
| `ba-test-case-generator` | Validation | `test-cases/` (qa concern) | `TC-{STORY}-{TYPE}-NNN` |
| `ba-scrum-events-pack` | Delivery | `sprints/` | `IMP-/DEP-/RA-NNN` |
| `ba-requirements-lifecycle` | Cross-cutting | `requirements/` | RTM, approval pack, CRs |
| `ba-planning-monitor` | Cross-cutting | `planning/` | BA approach, governance |

Always read `ba-suite-orientation.md` first for the shared conventions, then the relevant method doc(s).
