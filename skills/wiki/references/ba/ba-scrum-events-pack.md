---
name: ba-scrum-events-pack
description: >
  Generates structured BA input and output documentation for all five Scrum events
  defined in the Scrum Guide 2020: the Sprint, Sprint Planning, Daily Scrum, Sprint
  Review, and Sprint Retrospective. Produces event-specific documents that support
  the BA role in preparing inputs, capturing outputs, and maintaining artefact
  quality across Scrum events. Trigger this skill whenever the user says "Sprint
  Planning", "Sprint Review", "Sprint Retrospective", "Daily Scrum", "Scrum events",
  "backlog refinement", "Sprint inputs", "Definition of Ready", "Definition of Done",
  "Sprint goal", "increment review", "retrospective actions", "Sprint documentation",
  or "help me prepare for the Sprint". Do not use for non-Scrum workshops: those
  belong to ba-workshop-facilitator. Scrum Guide 2020 terminology applies throughout:
  events not ceremonies, Product Backlog Items not tickets, Developers not dev team.
---

# BA Scrum Events Pack

Produces BA-layer inputs and outputs for Scrum events. Enforces Scrum Guide 2020 terminology
and artefact standards. Does not redesign the events — supports the BA's contribution to them.

## Reference Files

Read both before processing any input:
- `references/scrum-events-guide.md` — Scrum Guide 2020 event definitions, purposes, time-boxes, and artefact connections
- `references/definition-of-ready-done.md` — Default DoR and DoD criteria with customisation rules and the BA's responsibility for each criterion

---

## Scope Boundaries

**This skill covers:**
- Sprint Planning: Product Backlog preparation inputs, Sprint Goal draft, capacity inputs
- Daily Scrum: BA-relevant impediment log, dependency tracker (BA's contribution only)
- Sprint Review: Sprint output report, acceptance evidence table, stakeholder update
- Sprint Retrospective: Retrospective facilitation guide (Scrum-specific format), improvement actions tracker
- Sprint: Sprint overview document, DoR/DoD, PBI readiness checklist across the Sprint

**This skill does not cover:**
- Backlog writing or story decomposition — use ba-user-story-factory
- Requirements elicitation — use ba-elicitation-synthesizer
- Stakeholder management — use ba-stakeholder-analyzer
- Non-Scrum workshops — use ba-workshop-facilitator

---

## Input Handling

### Minimum Viable Input
- Event type tag: Sprint / Sprint Planning / Daily Scrum / Sprint Review / Sprint Retrospective / All
- Sprint number and Sprint Goal (or "to be drafted")

### Optimal Input
| Input | Effect |
|-------|--------|
| Product Backlog items (from ba-user-story-factory) | Populates Sprint Planning PBI readiness checklist |
| Sprint number and team velocity | Enables capacity planning in Sprint Planning |
| Previous Sprint Retrospective actions | Enables continuity tracking in Retrospective |
| Stakeholder list (from ba-stakeholder-analyzer) | Tailors Sprint Review stakeholder update |
| Definition of Done (team's existing) | Validates against default; produces gap analysis |
| Sprint Review outputs (stories, demo items) | Populates Sprint Review report |

### Clarification Rule
If no event type is specified, ask one question:
> "Which Scrum event are you preparing for — Sprint Planning, Daily Scrum, Sprint Review,
> or Sprint Retrospective? Or do you need the full Sprint pack?"

---

## Event-Specific Processing

---

### Sprint Planning Support

**Scrum Guide 2020 reference:** Sprint Planning initiates the Sprint. The Scrum Team collaborates
to define the Sprint Goal, select Product Backlog Items, and create an initial plan for
delivering the Sprint Goal. Time-box: 8 hours for a one-month Sprint (proportionally less
for shorter Sprints).

**BA's role in Sprint Planning:**
- Ensure selected Product Backlog Items meet the Definition of Ready before the event
- Have acceptance criteria confirmed and unambiguous
- Surface known dependencies and risks for the Developers to consider
- Draft or refine the Sprint Goal statement for the Product Owner to propose

**Output: Sprint Planning Input Pack**
1. Definition of Ready check: table of candidate PBIs × DoR criteria, each cell Pass/Fail
2. Acceptance criteria confirmation: any unconfirmed items flagged for resolution before the event
3. Sprint Goal draft: one sentence; format — "This Sprint, we will [deliver/complete/enable]
   [capability] as evidenced by [outcome]."
4. Dependency and risk summary: any cross-team or cross-system dependencies affecting the Sprint
5. Capacity note: if provided, a table of Developers × available days in the Sprint

---

### Daily Scrum Support

**Scrum Guide 2020 reference:** The Daily Scrum is a 15-minute event for the Developers to
inspect progress toward the Sprint Goal and adapt the Sprint Backlog as necessary. The
Product Owner and Scrum Master may attend but do not direct it. It is for the Developers.
Time-box: 15 minutes.

**BA's role during the Sprint (not the Daily Scrum itself):**
The BA does not facilitate or attend the Daily Scrum unless invited by the Developers.
The BA's contribution is to maintain the impediment and dependency log so that blockers
with external BA dependencies are visible and resolved quickly.

**Output: BA Impediment and Dependency Log**
Updated continuously during the Sprint; not an event deliverable but a Sprint artefact.

| Column | Content |
|--------|---------|
| Item ID | IMP-{NNN} or DEP-{NNN} |
| Type | Impediment / Dependency |
| Story Reference | PBI ID blocked or affected |
| Description | What is blocking or what is the dependency |
| Raised By | Developer or role |
| Date Raised | |
| BA Action Required | What the BA must do to resolve |
| Status | Open / In Progress / Resolved |
| Resolution Date | |
| Resolution Notes | |

---

### Sprint Review Support

**Scrum Guide 2020 reference:** The Sprint Review is held at the end of the Sprint to inspect
the outcome of the Sprint and determine future adaptations. The Scrum Team presents the
results of their work to key stakeholders and progress toward the Product Goal is discussed.
Time-box: 4 hours for a one-month Sprint.

**BA's role in the Sprint Review:**
- Confirm which PBIs meet the Definition of Done (acceptance evidence)
- Produce a Sprint output report for stakeholders who cannot attend
- Surface any requirements changes or new insights from the Sprint that affect the Product Backlog

**Output: Sprint Review Package**

1. **Acceptance Evidence Table**

| Story ID | Story Title | Acceptance Criteria | Evidence of Pass | DoD Met? | Notes |
|----------|-------------|--------------------|--------------------|----------|-------|
| | | Each criterion listed | Test case ID or demo screenshot reference | Yes/No | If No: reason and remediation |

2. **Sprint Output Report (Word)**
One page for stakeholders. Sections:
- Sprint Goal and whether it was achieved (Yes / Partially / No — with reason)
- Delivered increment: list of completed PBIs with one-sentence description of each
- Not completed: PBIs that were started but not Done, with reason
- Metrics: stories planned vs. delivered, story points if used
- Key decisions or changes emerging from the Sprint
- Updated Product Backlog priorities: any changes driven by Sprint learning
- Next Sprint preview: top 3 candidate PBIs for the next Sprint Goal

3. **Stakeholder Update (for attendees who need a summary)**
One paragraph: Sprint goal, what was delivered, what changed, what is next.

---

### Sprint Retrospective Support

**Scrum Guide 2020 reference:** The Sprint Retrospective is for the Scrum Team to inspect
how the last Sprint went regarding individuals, interactions, processes, tools, and their
Definition of Done. Improvements should be identified and at least one is added to the
Sprint Backlog for the next Sprint. Time-box: 3 hours for a one-month Sprint.

**BA's role in the Sprint Retrospective:**
- Not the facilitator (Scrum Master facilitates)
- Contributes BA-specific observations on requirements quality, acceptance criteria clarity,
  handoff friction, and stakeholder engagement
- Ensures improvement actions have owners and are tracked

**Output: Retrospective Input and Action Tracker**

1. **BA Observation Summary (input to Retrospective)**
BA-perspective observations only — not the full retrospective. Format:
- Requirements quality: Were stories clear enough to build and test without BA intervention mid-Sprint?
- Acceptance criteria: Were any criteria misunderstood or disputed during the Sprint?
- Handoff points: Were there delays at any BA → Developer handoff?
- Stakeholder availability: Were any decisions blocked by unavailable stakeholders?

2. **Improvement Action Tracker (output from Retrospective)**

| Action ID | Improvement Action | Owner | Sprint Added | Target Sprint | Status | Outcome |
|-----------|-------------------|-------|--------------|---------------|--------|---------|
| RA-{NNN} | | | | | Open / Done / Carried | |

Rule: At least one Retrospective action must be added to the Sprint Backlog as a Product Backlog
Item per Scrum Guide 2020. Flag which action this is.

---

### Sprint Overview Document

Produced at Sprint start. Covers the full Sprint with links to all event outputs.

Sections:
1. Sprint number, start date, end date
2. Sprint Goal (confirmed)
3. Sprint Backlog: table of committed PBIs with Story ID, Title, Effort, Owner, Status
4. Capacity: table of Developers × available days
5. Definition of Ready (from references/definition-of-ready-done.md)
6. Definition of Done (from references/definition-of-ready-done.md)
7. Links to event outputs (populated as Sprint progresses)
8. Risks and dependencies active this Sprint

---

## Output Specification

### Output Files (by event)

| Event | File | Format |
|-------|------|--------|
| Sprint Planning | `sprint_{N}_planning_pack.docx` | Word |
| Daily Scrum / Sprint | `sprint_{N}_impediment_log.xlsx` | Excel |
| Sprint Overview | `sprint_{N}_overview.docx` | Word |
| Sprint Review | `sprint_{N}_review_pack.docx` | Word |
| Sprint Review | `sprint_{N}_acceptance_evidence.xlsx` | Excel |
| Sprint Retrospective | `sprint_{N}_retro_actions.xlsx` | Excel |

All files: `/mnt/user-data/outputs/`
All Word files: Sentence case headings. No em dashes.

When "All" is requested, produce all six files.

### Inline Summary (in conversation)
For each event:
- Event name, Sprint number, time-box reminder (from Scrum Guide 2020)
- Key BA deliverable for this event
- One readiness risk: what is most likely to cause this event to be less effective
  (e.g. "3 stories have unconfirmed acceptance criteria — resolve before Sprint Planning")

---

## Quality Gates

Before delivering any output:
- [ ] All Scrum terminology is Scrum Guide 2020 compliant: events (not ceremonies), Developers (not dev team), increment (not release), Sprint Backlog (not sprint tasks)
- [ ] Sprint Goal follows the format: capability + evidence of achievement
- [ ] Acceptance Evidence Table has a DoD check for every committed story — no blanks
- [ ] Retrospective actions table has at least one item flagged as "to be added to Product Backlog"
- [ ] Impediment log has an explicit BA action for every open item
- [ ] Sprint Review report is one page for the stakeholder-facing output
