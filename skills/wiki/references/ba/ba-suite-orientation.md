---
name: ba-suite-orientation
description: >
  Sets the operating standards, writing conventions, naming patterns, lifecycle sequence,
  skill boundaries, and quality gates that apply to every other skill in the BA Suite plugin.
  Always invoke this skill once at the start of any task that uses any ba-* skill, or whenever
  the user mentions: "BA Suite", "BA suite plugin", "business analysis workflow", "ba lifecycle",
  "ba standards", "ba conventions", "ba writing standards", or asks to chain two or more BA skills
  together. Also invoke when the user asks "how should I structure this", "what naming should I use",
  "what's the discount rate default", "what's the financial horizon", "what colour for this draw.io
  element", "which skill should I use for X", "what comes before / after this skill", or any question
  about the suite's working agreements. This is a context-setting skill, not a producer of files.
---

# BA Suite Orientation

Sets the working agreements for the BA Suite plugin. Read this once per task that touches any `ba-*` skill, then apply silently throughout.

## Suite composition (13 producer skills plus this orientation)

| Phase | Skills |
|-------|--------|
| Discovery | ba-elicitation-synthesizer, ba-stakeholder-analyzer, ba-workshop-facilitator |
| Analysis | ba-process-modeler, ba-gap-analysis |
| Definition | ba-user-story-factory, ba-business-case-builder, ba-rfi-rfp-analyzer |
| Validation | ba-solution-assessment, ba-test-case-generator |
| Delivery | ba-scrum-events-pack |
| Lifecycle management | ba-requirements-lifecycle, ba-planning-monitor |

Standards applied across all skills: BABOK v3, Scrum Guide 2020, BPMN 2.0, INVEST, BDD/Gherkin, PMI/BABOK financial modelling.

## Lifecycle sequence

Skills hand artefacts to each other. Use upstream output as downstream input. Never regenerate content that already exists.

```
DISCOVERY            ANALYSIS            DEFINITION           VALIDATION          DELIVERY
elicitation          process-modeler     user-story-factory   solution-assessment scrum-events-pack
stakeholder                              business-case        test-case-generator
workshop             gap-analysis        rfi-rfp-analyzer
```

## Upstream to downstream handoff map

| Upstream | Downstream | What passes |
|----------|------------|-------------|
| ba-elicitation-synthesizer | ba-user-story-factory | FR items from requirements register |
| ba-elicitation-synthesizer | ba-business-case-builder | Problem statement, scope, issues log |
| ba-stakeholder-analyzer | ba-workshop-facilitator | Stakeholder profiles, concern narratives |
| ba-stakeholder-analyzer | ba-business-case-builder | Stakeholder context, sponsor framing |
| ba-workshop-facilitator | ba-elicitation-synthesizer | Post-session synthesis as raw input |
| ba-process-modeler | ba-gap-analysis | AS-IS and TO-BE models as baseline and target |
| ba-process-modeler | ba-user-story-factory | Process step register as story seeds |
| ba-gap-analysis | ba-business-case-builder | Gap inventory, recommended actions |
| ba-gap-analysis | ba-user-story-factory | Quick Win items as backlog candidates |
| ba-user-story-factory | ba-test-case-generator | Product Backlog with Gherkin acceptance criteria |
| ba-user-story-factory | ba-scrum-events-pack | Backlog for Sprint Planning inputs |
| ba-test-case-generator | ba-scrum-events-pack | Acceptance evidence for Sprint Review |
| ba-rfi-rfp-analyzer | ba-solution-assessment | Vendor responses ready for scoring |
| ba-business-case-builder | ba-rfi-rfp-analyzer | Approved option scope for procurement |

## Skill boundaries

| Do NOT use | For | Use instead |
|------------|-----|-------------|
| ba-scrum-events-pack | Non-Scrum workshops | ba-workshop-facilitator |
| ba-workshop-facilitator | Sprint Planning, Review, Retrospective | ba-scrum-events-pack |
| ba-solution-assessment | Parsing RFP documents | ba-rfi-rfp-analyzer |
| ba-rfi-rfp-analyzer | Evaluating already-scored options | ba-solution-assessment |
| ba-user-story-factory | Requirements elicitation | ba-elicitation-synthesizer |

## Writing standards (apply to every output file)

These apply to `.docx`, `.xlsx`, `.pptx`, `.md`, `.yaml`, `.html`, and `.drawio` outputs.

1. No em dashes. Replace with a colon, comma, or restructured phrasing. Sweep before delivery.
2. Sentence case headings. "Requirements register" not "Requirements Register".
3. B2-level plain English. Short sentences, active voice, no internal jargon without definition.
4. Dense tables over prose lists. If content fits a table, make it a table.
5. No "this isn't / this is" constructs. Rephrase positively.
6. No hyped analogies. Describe what something does, not what it is "like".
7. No arrows (`->`, `-->`) in written prose. Use "feeds", "produces", "outputs to".

## File naming conventions

All outputs follow `{project_prefix}_{artefact_type}.{ext}`:

| Artefact | Filename | Format |
|----------|----------|--------|
| Requirements register | `{prefix}_requirements_register.xlsx` | Excel |
| BRD | `{prefix}_BRD_draft.docx` | Word |
| Stakeholder analysis | `{prefix}_stakeholder_analysis.docx` | Word |
| Stakeholder grid | `{prefix}_stakeholder_grid.drawio` | Draw.io |
| Process model | `{process_name}_{model_type}.drawio` | Draw.io |
| Process spec | `{process_name}_process_spec.docx` | Word |
| Gap analysis register | `{project}_gap_analysis.xlsx` | Excel |
| Gap analysis report | `{project}_gap_analysis_report.docx` | Word |
| Gap heatmap | `{project}_gap_heatmap.drawio` | Draw.io |
| Product backlog | `{project}_product_backlog.xlsx` | Excel |
| Story spec | `{project}_story_spec.docx` | Word |
| Business case | `{project}_business_case.docx` | Word |
| Financial model | `{project}_financial_model.xlsx` | Excel |
| RFP compliance matrix | `{project}_rfp_{mode}.xlsx` | Excel |
| RFP response/eval | `{project}_rfp_response_outline.docx` or `rfp_evaluation.docx` | Word |
| Solution assessment | `{project}_solution_assessment.xlsx` | Excel |
| Solution assessment report | `{project}_solution_assessment_report.docx` | Word |
| Test cases | `{project}_test_cases.xlsx` | Excel |
| BDD spec | `{project}_bdd_spec.yaml` | YAML |
| UAT script | `{project}_uat_script.docx` | Word |
| Sprint planning pack | `sprint_{N}_planning_pack.docx` | Word |
| Sprint impediment log | `sprint_{N}_impediment_log.xlsx` | Excel |
| Sprint overview | `sprint_{N}_overview.docx` | Word |
| Sprint review pack | `sprint_{N}_review_pack.docx` | Word |
| Sprint acceptance evidence | `sprint_{N}_acceptance_evidence.xlsx` | Excel |
| Sprint retro actions | `sprint_{N}_retro_actions.xlsx` | Excel |

## Output delivery

1. Save all final outputs to `/mnt/user-data/outputs/`.
2. Provide a `computer://` link for every file.
3. Post-delivery summary: 3 to 5 bullet points or 2 sentences maximum.
4. Do not re-explain file contents after linking.

## Requirement ID schemes

| Skill | Format | Example |
|-------|--------|---------|
| ba-elicitation-synthesizer | `{PREFIX}-{TYPE}-{NNN}` | `CRM-FR-001` |
| ba-user-story-factory | `{PREFIX}-{EPIC}-{NNN}` | `PAY-001-012` |
| ba-test-case-generator | `TC-{STORY-ID}-{TYPE}-{NNN}` | `TC-PAY-001-HP-001` |
| ba-gap-analysis | `G-{DIM}-{NNN}` | `G-PR-001` |
| ba-rfi-rfp-analyzer | `{Section}-{NNN}` | `3.2-001` |
| ba-scrum-events-pack (impediment) | `IMP-{NNN}` / `DEP-{NNN}` | `IMP-007` |
| ba-scrum-events-pack (retro) | `RA-{NNN}` | `RA-003` |

IDs are stable: once assigned, never renumber. New iterations add new IDs at the end.

## Financial modelling defaults (ba-business-case-builder)

| Parameter | Default | Override |
|-----------|---------|----------|
| Horizon | 3 years | Use 5 only when explicitly requested |
| Discount rate | 8% | State the assumption inline; flag for confirmation |
| Sensitivity scenarios | Benefits minus 20%, Costs plus 20%, both adverse | Add others on request |
| Non-financial weights | Strategic 25%, Risk 20%, Time to value 20%, Stakeholder 15%, Tech fit 10%, Capability 10% | Adjust on request, document change |

## Scrum terminology (ba-scrum-events-pack)

Non-negotiable vocabulary from Scrum Guide 2020.

| Use | Never use |
|-----|-----------|
| Events | Ceremonies |
| Developers | Development team members, dev team |
| Increment | Release candidate, deliverable |
| Product Backlog Items | Tickets, tasks, stories (in formal output) |
| Sprint Backlog | Sprint tasks |
| Sprint Retrospective | Retro (in formal output) |
| Scrum Team | Agile team |

## Draw.io colour standards

Applied in ba-process-modeler, ba-stakeholder-analyzer, ba-gap-analysis.

| Element | Fill | Border |
|---------|------|--------|
| Start event | `#D5E8D4` | `#82B366` |
| End event | `#F8CECC` | `#B85450` |
| Task (human) | `#DAE8FC` | `#6C8EBF` |
| Task (system) | `#E1D5E7` | `#9673A6` |
| Gateway | `#FFF2CC` | `#D6B656` |
| Hotspot annotation | `#FFE6CC` | `#D79B00` |
| Swimlane header | `#F5F5F5` | `#666666` |
| Manage Closely stakeholder | `#FF0000` (red) | |
| Keep Satisfied stakeholder | amber | |
| Keep Informed stakeholder | blue | |
| Monitor stakeholder | grey | |
| Gap: None | `#D5E8D4` | |
| Gap: Minor | `#FFF2CC` | |
| Gap: Moderate | `#FFE6CC` | |
| Gap: Significant | `#F8CECC` | |
| Gap: Critical | `#FF0000` white text | |

## Clarification rules

- Ask one clarifying question maximum per skill invocation before proceeding.
- If ambiguous input could go two ways, pick the most probable interpretation and proceed, stating the assumption inline.
- Do not ask questions answerable from context.
- Exception: ba-rfi-rfp-analyzer must always confirm mode (Respond vs Evaluate) if not stated.

## Decision points that require explicit user input

1. Project prefix or ID scheme not determinable from context: ask once.
2. RFP mode (Respond vs Evaluate): always ask if not stated.
3. Do Nothing option in business case: always include; ask only if explicit exclusion is requested.
4. Discount rate and financial horizon: use 8% and 3 years; state assumption.
5. Workshop duration: assume 2 hours if not provided; state assumption.
6. Gap analysis dimensions: if multiple possible, list them and confirm scope.

## QA gate (before delivery)

Every non-trivial deliverable passes this check before being shared.

| Check | Pass criterion |
|-------|----------------|
| No em dashes | Sweep entire output; replace all instances |
| Sentence case headings | All headings in Word, Excel, PPTX |
| Quality gates met | Each skill's built-in checklist confirmed |
| Traceability intact | IDs consistent across all output files from the same skill run |
| Assumptions flagged | Estimated figures labelled `[Estimated]` or `[Confirm with stakeholder]` |
| Conflicts surfaced | No silent conflict resolution; all conflicts in Issues Log |
| Downstream handoff ready | Output matches format expected by the next skill |

For complex multi-file outputs (business case, solution assessment, full sprint pack): run a sub-agent QA pass and report results in a PASS/FAIL table before providing the final link.

## Citation requirements

Whenever a deliverable includes factual claims, statistics, market figures, benchmarks, or sourced findings:

1. Every factual claim includes an inline citation immediately after the claim: `([Source Name](exact-url))`.
2. A consolidated Sources section appears at the end of the deliverable.
3. Never cite sources not actually retrieved. Never fabricate URLs.
4. If no external source is used (pure client input processing), no citation section is needed.

## Reference files inside each skill

Every skill has a `references/` subdirectory. Read the reference files listed at the top of each SKILL.md before processing input. They contain classification taxonomies, scoring rubrics, templates, and decision rules that the skill logic depends on.
