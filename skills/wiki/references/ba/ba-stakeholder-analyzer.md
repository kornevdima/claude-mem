---
name: ba-stakeholder-analyzer
description: >
  Produces a complete stakeholder intelligence package from a list of stakeholder names, titles,
  departments, or interview excerpts: power/interest grid classification, RACI matrix against
  standard BA deliverables, engagement strategy per stakeholder, communication plan, and
  concern/resistance narrative per persona. Trigger this skill whenever a user provides a list
  of project stakeholders or roles and asks for analysis; says "stakeholder map", "stakeholder
  analysis", "who are my stakeholders", "engagement plan", "RACI", "communication plan",
  "power interest grid", "who do I need to manage", "stakeholder register", or "who cares about
  this project". Also triggers when a user needs to plan a workshop and wants to understand the
  room first, or when conflict between stakeholders is mentioned and needs a structured view.
  Use before ba-workshop-facilitator when participants are not yet mapped. Use after
  ba-elicitation-synthesizer when unresolved issues need owner assignment.
---

# BA Stakeholder Analyzer

Produces a structured stakeholder intelligence package in one pass. Scales from a name-and-title
list to a fully annotated engagement strategy depending on how much input is provided.

## Reference Files

Read both before processing any input:
- `references/stakeholder-archetypes.md` — 8 archetypes with default engagement strategies, concern profiles, and resistance triggers
- `references/ba-deliverables-raci.md` — standard BA deliverable set with default RACI assignments per archetype

---

## Input Handling

### Minimum Viable Input
A list of at least two people with name + role or title.

### Optimal Input
| Input | What It Enables |
|-------|----------------|
| Name, title, department | Archetype classification |
| Interview excerpts or quotes | Concern narrative, conflict detection |
| Project description or objective | Strategic alignment inference |
| Org chart or reporting lines | Power scoring refinement |
| Known conflicts or sensitivities | Resistance flag |

### Clarification Rule
If fewer than two stakeholders are provided, ask:
> "Can you give me at least two stakeholders — name and role is enough to start?"

If no project context is provided, ask:
> "What is this project trying to achieve in one sentence?"

Do not ask both questions at once. Ask the more important one first (usually project context if entirely absent).

---

## Processing Steps

### Step 1 — Classify Archetypes
Read `references/stakeholder-archetypes.md`. Assign each stakeholder to the closest archetype.
A stakeholder may span two archetypes — record primary and secondary.

| Archetype | Typical Titles |
|-----------|---------------|
| Sponsor | CXO, VP, Programme Director, Business Owner |
| Decision-Maker | Department Head, Product Owner, Director |
| Subject Matter Expert | Senior Analyst, Technical Lead, Process Owner |
| End User | Staff, Operator, Customer-facing Role |
| Regulator / Compliance | Legal, Risk, Audit, Data Protection Officer |
| Technical Gatekeeper | Enterprise Architect, CTO, Security Officer |
| Influencer | External Advisor, Key Customer, Industry Body |
| Blocker | Any stakeholder with stated or implied opposition |

### Step 2 — Score Power and Interest
Score each stakeholder on two dimensions, each 1–5.

**Power:** Ability to approve decisions, allocate budget, or block delivery.
| Score | Meaning |
|-------|---------|
| 5 | Final sign-off authority; can stop or fund the project |
| 4 | Significant influence; shapes decisions without final say |
| 3 | Moderate influence in their domain only |
| 2 | Advisory input; rarely blocks |
| 1 | Minimal influence; informs rather than decides |

**Interest:** Degree to which this stakeholder's work or goals are affected by the project outcome.
| Score | Meaning |
|-------|---------|
| 5 | Directly affected daily; outcome changes their role or tools significantly |
| 4 | Regular touchpoint; outcome affects their KPIs |
| 3 | Periodic touchpoint; some process or reporting impact |
| 2 | Aware but minimally affected |
| 1 | Tangential involvement only |

Scoring rationale must be stated for each stakeholder (one sentence).

### Step 3 — Assign Quadrant and Engagement Strategy
| Quadrant | Condition | Strategy |
|----------|-----------|----------|
| Manage Closely | Power ≥ 4 AND Interest ≥ 4 | Frequent bilateral engagement; involve in key decisions; keep fully informed |
| Keep Satisfied | Power ≥ 4 AND Interest < 4 | Regular updates at their level; avoid surprises; escalation channel open |
| Keep Informed | Power < 4 AND Interest ≥ 4 | Include in reviews and comms; gather input; acknowledge their concerns |
| Monitor | Power < 4 AND Interest < 4 | Light-touch; periodic email updates; flag if their status changes |

### Step 4 — Build RACI Matrix
Read `references/ba-deliverables-raci.md`. Assign each stakeholder to R/A/C/I for each standard
BA deliverable. Apply archetype defaults from the reference, then adjust for the specific project context.

RACI rules:
- Every deliverable must have exactly **one A** (Accountable)
- A deliverable may have **multiple R** (Responsible) if warranted
- **C** (Consulted) = input required before deliverable is complete
- **I** (Informed) = receives the output; no input required

### Step 5 — Write Concern Narratives
For each stakeholder in Manage Closely or Keep Satisfied quadrant, write a concern profile (3–5 sentences):
- What does this stakeholder primarily care about (based on archetype + role + any input provided)?
- What might make them resist or disengage?
- What framing will land best with them?
- What would a bad outcome look like from their perspective?

For Keep Informed and Monitor stakeholders, write one sentence only.

### Step 6 — Build Communication Plan
Produce a communication plan table. One row per stakeholder group (group stakeholders sharing
the same quadrant and archetype).

| Column | Content |
|--------|---------|
| Stakeholder / Group | Names or group label |
| Quadrant | From Step 3 |
| Objective of Communication | What must they know, believe, or decide? |
| Key Messages | 2–3 bullet points specific to their concerns |
| Channel | Meeting / email / dashboard / report / workshop |
| Cadence | Weekly / bi-weekly / monthly / milestone-driven |
| Owner (BA action) | Who from the project team owns this relationship |
| Notes | Sensitivities, preferred format, language level |

### Step 7 — Detect Conflicts
If two stakeholders have opposing stated positions, or if their archetype combination suggests
structural tension (e.g., Sponsor wants speed, Regulator wants thoroughness), flag as:
`[STAKEHOLDER CONFLICT: {Name A} vs {Name B} — {nature of conflict}]`
Suggest a resolution approach in the Issues section.

### Step 8 — Change Impact Mode (conditional)
Activate Change Impact Mode when:
- The skill is invoked as part of the `/change-impact` workflow command, OR
- The user states "this is a change initiative", "what is the impact on stakeholders", or
  "how will this change affect people", OR
- A gap analysis output or change description is provided alongside the stakeholder list

In Change Impact Mode, for **every** stakeholder (not just Manage Closely), produce a
**Change Impact Narrative** structured as follows:

| Field | Content |
|-------|---------|
| What changes for this stakeholder | Specific process steps, tools, reporting lines, or responsibilities that will change |
| What they lose | Any capability, autonomy, relationships, or status they currently have that will be reduced or removed |
| What they gain | New capabilities, efficiencies, or opportunities the change creates for them |
| Transition risk | The likelihood and consequence of this stakeholder resisting, disengaging, or actively blocking the change |
| Recommended engagement action | One specific BA action to reduce transition risk (e.g., "involve in TO-BE process design workshop", "provide 1:1 briefing before announcement") |

Scoring thresholds for Change Impact Mode:
- Transition risk HIGH: Power ≥ 4 AND the stakeholder loses status, role, or autonomy
- Transition risk MEDIUM: Any Manage Closely or Keep Satisfied stakeholder with moderate losses
- Transition risk LOW: Keep Informed and Monitor stakeholders with minor process adjustments only

The change impact narratives are added as a new section (Section 8: Change impact assessment)
in the Word stakeholder analysis document. This section is omitted in standard mode.

**Additional output in Change Impact Mode:**
A change impact summary table added to the inline summary and to the Word document:

| Stakeholder | Quadrant | Change impact severity | Primary risk | Recommended action |
|-------------|----------|----------------------|--------------|-------------------|
| [Name] | [Quadrant] | High / Medium / Low | [One sentence] | [One action] |

---

## Output Specification

### Output 1 — Word Stakeholder Analysis Document
Filename: `{project}_stakeholder_analysis.docx`
Location: `/mnt/user-data/outputs/`
Standard: Sentence case headings. No em dashes. Dense tables over prose lists.

Sections:
1. Document control
2. Stakeholder register — table: Name, Role, Archetype, Power Score, Interest Score, Quadrant
3. Engagement strategies — one sub-section per Manage Closely / Keep Satisfied stakeholder with full concern narrative; one combined table for Keep Informed and Monitor
4. RACI matrix — full matrix, all stakeholders × all BA deliverables
5. Communication plan — full table
6. Conflicts and sensitivities — flagged items with resolution approach
7. Next steps — three to five actions derived from the analysis

### Output 2 — Draw.io Power/Interest Grid
Filename: `{project}_stakeholder_grid.drawio`
Location: `/mnt/user-data/outputs/`

Layout:
- 2×2 grid with labelled quadrants
- Each stakeholder as a node: Name + Role, colour-coded by quadrant
- Manage Closely = red nodes; Keep Satisfied = amber; Keep Informed = blue; Monitor = grey
- Connecting lines where stakeholder conflict has been flagged
- Legend in top-right corner

### Output 3 — Inline Summary (in conversation)
Immediately after file links:
- Stakeholder count by quadrant
- Top two Manage Closely stakeholders and their primary concern (one sentence each)
- Number of conflicts flagged, if any
- Most critical RACI gap (if any A is missing from a deliverable)

---

## Quality Gates

Before delivering any output:
- [ ] Every stakeholder has a Power score, Interest score, and quadrant assignment
- [ ] Every deliverable in the RACI matrix has exactly one A
- [ ] Every Manage Closely stakeholder has a concern narrative
- [ ] Communication plan covers all quadrants
- [ ] Conflicts are documented with suggested resolution, not just flagged
- [ ] Draw.io grid has all stakeholders placed and a visible legend
- [ ] If Change Impact Mode is active: every stakeholder has a Change Impact Narrative with all five fields completed
- [ ] If Change Impact Mode is active: change impact summary table is present in Section 8 of the Word document

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| Stakeholder register + concern narratives | `ba-workshop-facilitator` — participant preparation and facilitation tone |
| RACI matrix | All downstream skills — A column defines review/approval owners for deliverables |
| Conflicts log | `ba-elicitation-synthesizer` — unresolved items need owner assignment |
| Communication plan | `ba-scrum-events-pack` — stakeholder update cadence for Scrum event outputs |
| Change Impact Assessment (Section 8, Change Impact Mode only) | `ba-business-case-builder` — stakeholder transition costs and resistance risks inform the Risk Assessment and Options sections |
