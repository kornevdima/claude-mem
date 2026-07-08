---
name: ba-planning-monitor
description: >
  Plans and governs the BA engagement: BA approach document, stakeholder engagement
  plan, governance plan, information management plan, and BA performance review.
  Covers BABOK v3 Chapter 3: Plan BA Approach, Plan Stakeholder Engagement, Plan BA
  Governance, Plan BA Information Management, and Identify BA Performance Improvements.
  Trigger this skill whenever the user says "plan the BA approach", "how should we run
  BA on this project", "BA plan", "BA governance", "who approves requirements", "how do
  we manage BA information", "BA performance review", "lessons learned from BA", "BA
  methodology selection", "waterfall vs agile for BA", "hybrid approach", or "what is
  the BA strategy for this engagement". Also triggers when a project is being initiated
  with no BA plan, or at project close when a retrospective of the BA practice is
  needed. Use before any other skill at the start of a new engagement.
---

# BA Planning and Monitor

Plans the BA practice for an engagement and monitors its performance throughout. Produces
governance artefacts that all other skills rely on: the BA approach defines which skills to
use, in what order, and who approves their outputs.

## Reference Files

Read both before processing any input:
- `references/ba-approach-patterns.md` — approach archetypes (waterfall, agile, hybrid, iterative) with selection criteria, tool and technique defaults, and risk flags per approach
- `references/ba-governance-templates.md` — governance plan structure, information management schema, and performance review scoring rubric

---

## Input Handling

### Minimum Viable Input
One of:
- A project description with enough context to infer methodology (agile, waterfall, hybrid)
- A statement of BA scope: what the BA is responsible for on this engagement
- A BA retrospective request with a description of the completed project

### Optimal Input
| Input | Effect |
|-------|--------|
| Project type and methodology | Drives approach selection |
| Project size and duration | Calibrates governance overhead |
| Stakeholder list | Informs engagement plan and approval routing |
| Regulatory or compliance context | Tightens governance and documentation requirements |
| Prior BA plan or performance data | Enables improvement identification (Task 3.5) |

### Mode Selection
This skill operates in five modes corresponding to BABOK Chapter 3 tasks.

| Mode | BABOK Task | When to use |
|------|-----------|------------|
| Plan Approach | 3.1 | At project start — select and document the BA methodology |
| Plan Engagement | 3.2 | At project start — formalise the stakeholder engagement strategy |
| Plan Governance | 3.3 | At project start — define who approves what and how changes are controlled |
| Plan Information Management | 3.4 | At project start — define what artefacts are produced, where stored, and who owns them |
| Performance Improvement | 3.5 | At project close or midpoint review — assess BA effectiveness and identify improvements |

Run Plan Approach first. All other modes depend on it.

### Clarification Rule
If no project type is provided, ask one question:
> "Is this project running in an agile, waterfall, or hybrid delivery model — and roughly how long is the engagement?"

---

## Processing Steps

### Mode 1 — Plan Business Analysis Approach (BABOK 3.1)

**Purpose:** Select and document the BA methodology, techniques, and tools for the engagement.

**Step 1.1 — Classify the engagement**
Read `references/ba-approach-patterns.md`. Match the project context to an approach archetype.

| Approach | Use when |
|----------|---------|
| Waterfall / Predictive | Regulatory, construction, or fixed-scope projects; low ambiguity; requirements stable upfront |
| Agile | Iterative delivery; requirements expected to evolve; Scrum or Kanban in use |
| Hybrid | Phase-gated delivery with agile sprints within phases; common in large transformations |
| Iterative (non-Scrum) | Prototyping, research, or design-led projects with informal governance |

**Step 1.2 — Define BA activities per lifecycle phase**
Map which suite skills will be used, in what order, and with what cadence. Produce an activity table:

| Phase | BA Activity | Skill | Owner | Timing | Output |
|-------|------------|-------|-------|--------|--------|
| Discovery | Stakeholder analysis | ba-stakeholder-analyzer | BA Lead | Week 1 | Stakeholder analysis + grid |
| Discovery | Requirements workshops | ba-workshop-facilitator | BA Lead | Weeks 2–3 | Facilitator guides, workshop packs |
| ... | ... | ... | ... | ... | ... |

**Step 1.3 — State key decisions and assumptions**
Document: methodology chosen, rationale, key assumptions, and what would trigger a methodology change mid-project.

---

### Mode 2 — Plan Stakeholder Engagement (BABOK 3.2)

**Purpose:** Extend the stakeholder analysis output into a formal, auditable engagement plan.

**Note:** This mode produces the formal engagement plan document. The power/interest analysis
and concern narratives are produced by ba-stakeholder-analyzer. This mode reads that output
and structures it into governance-grade documentation.

**Step 2.1 — Engagement strategy per quadrant**
Confirm and formalise the engagement strategy from ba-stakeholder-analyzer:
- Manage Closely: bilateral meeting cadence, named BA owner, escalation protocol
- Keep Satisfied: reporting mechanism, exception alerting
- Keep Informed: distribution list, artefact sharing schedule
- Monitor: periodic check-in trigger (e.g., if their quadrant changes)

**Step 2.2 — Engagement schedule**
Produce a month-by-month engagement calendar table. One row per stakeholder group.
Columns: Month | Stakeholder Group | Engagement type | BA action | Owner

**Step 2.3 — Collaboration tools and channels**
Document agreed tools: video conferencing, shared document platform, issue tracking.
Flag any stakeholder with a stated preference for a specific channel.

---

### Mode 3 — Plan Business Analysis Governance (BABOK 3.3)

**Purpose:** Define who approves BA outputs, how changes are controlled, and how issues are escalated.

**Step 3.1 — Approval authority matrix**
For each BA deliverable type, define: who must approve, who must review (Consulted), and
who must be notified (Informed). Use the RACI from ba-stakeholder-analyzer as input.

| Deliverable | Approve (A) | Review (C) | Notify (I) | Approval deadline |
|-------------|------------|-----------|-----------|------------------|
| Requirements register | Sponsor | SMEs, Technical Gatekeeper | End Users | Before sprint 1 |
| BRD | Sponsor | Compliance | Project team | Before story writing |
| Business case | Board / CXO | Finance, BA Lead | All stakeholders | Before procurement |
| ... | ... | ... | ... | ... |

**Step 3.2 — Change control process**
Summarise the change request process (detailed rules are in ba-requirements-lifecycle):
- How to submit a change request
- Who classifies it
- Turnaround time per classification
- Where decisions are recorded

**Step 3.3 — Issue escalation path**
Define the escalation chain for unresolved conflicts, blocked approvals, or scope disputes.
Produce a simple flowchart description: BA Lead, then Sponsor, then Programme Director.

---

### Mode 4 — Plan Business Analysis Information Management (BABOK 3.4)

**Purpose:** Define what BA artefacts are produced, where they are stored, who owns them,
and how long they are retained.

**Step 4.1 — Artefact inventory**
List every artefact this engagement will produce, using the suite's standard naming conventions.
For each artefact: file name pattern, format, producing skill, owner role, storage location,
version control method, and retention period.

**Step 4.2 — Repository structure**
Define the folder structure for the project's BA artefacts. Recommended structure:

```
{project-name}/
  01-discovery/
    stakeholder-analysis/
    workshop-materials/
  02-requirements/
    requirements-register/
    BRD/
  03-analysis/
    process-models/
    gap-analysis/
  04-definition/
    product-backlog/
    business-case/
  05-validation/
    test-cases/
    solution-assessment/
  06-delivery/
    sprint-packs/
  99-archive/
```

**Step 4.3 — Access and security**
Define who has read and write access to each folder tier. Flag any artefacts containing
commercially sensitive or personally identifiable information that require restricted access.

---

### Mode 5 — Identify BA Performance Improvements (BABOK 3.5)

**Purpose:** Assess how effectively the BA practice operated during the engagement and
produce actionable improvements for the next project.

**Step 5.1 — Assess BA effectiveness**
Read `references/ba-governance-templates.md`. Score the BA practice across six dimensions:

| Dimension | What is assessed | Score 1–5 |
|-----------|-----------------|----------|
| Requirements quality | Completeness, clarity, measurability of the requirements produced | |
| Stakeholder engagement | Frequency, inclusiveness, and outcome quality of engagement activities | |
| Traceability | Degree to which requirements trace to stories, tests, and delivered features | |
| Change management | How well scope changes were captured, classified, and controlled | |
| Documentation | Completeness and accessibility of BA artefacts | |
| Delivery alignment | How well the BA outputs aligned with what was actually built and tested | |

**Step 5.2 — Identify root causes**
For any dimension scoring 3 or below, identify one root cause and one improvement action.

**Step 5.3 — Produce improvement register**
| Action ID | Dimension | Finding | Root cause | Improvement action | Owner | Apply from |
|----------|-----------|---------|-----------|-------------------|-------|-----------|
| IA-{NNN} | | | | | | Next project / Immediately |

---

## Output Specification

### Plan Approach Output
1. `{project}_ba_approach.docx` — BA approach document with activity table, methodology rationale, and key assumptions

### Plan Engagement Output
1. `{project}_engagement_plan.docx` — formalised stakeholder engagement plan with calendar and channel definitions

### Plan Governance Output
1. `{project}_ba_governance_plan.docx` — approval authority matrix, change control summary, escalation path

### Plan Information Management Output
1. `{project}_ba_information_plan.docx` — artefact inventory, folder structure, access rules

### Performance Improvement Output
1. `{project}_ba_performance_review.docx` — dimension scores, findings, root causes, improvement register
2. `{project}_ba_improvement_register.xlsx` — improvement actions with owners and timing

---

## Quality Gates

Before delivering any output:
- [ ] Plan Approach: every BA activity maps to a skill name; every phase has at least one activity
- [ ] Plan Approach: methodology choice is explicitly stated with rationale
- [ ] Plan Engagement: every Manage Closely stakeholder has a named BA owner for that relationship
- [ ] Plan Governance: every BA deliverable has exactly one named approver role
- [ ] Plan Governance: change control process states turnaround times per classification
- [ ] Plan Information Management: every artefact type has a storage location and owner role
- [ ] Performance Review: every dimension score below 3 has a root cause and an improvement action

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| BA approach document | All 11 skills — defines which skills run, in what order, and with what governance |
| Governance plan | ba-requirements-lifecycle — approval routing and change control process |
| Engagement plan | ba-stakeholder-analyzer, ba-workshop-facilitator — formal cadence and channel commitments |
| Information management plan | ba-scrum-events-pack — Sprint Review artefact distribution follows the IM plan |
| Performance improvement register | Next project initiation — improvement actions are inputs to the next BA approach |
