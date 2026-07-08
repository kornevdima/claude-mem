---
name: ba-requirements-lifecycle
description: >
  Manages requirements traceability, change impact assessment, prioritisation scoring,
  version logs, and formal approval packs. Covers BABOK v3 Chapter 5: Trace Requirements,
  Maintain Requirements, Prioritise Requirements, Assess Requirements Changes, and Approve
  Requirements. Trigger this skill whenever the user says "trace requirements",
  "requirements traceability", "link stories to requirements", "requirements change",
  "impact of changing this requirement", "prioritise requirements", "get requirements
  approved", "sign-off pack", "requirements baseline", "maintain the register", or
  "formal requirements approval". Also triggers when the user provides a requirements
  register and asks what changed, what is approved, what traces to what, or how to handle
  a scope change. Use after ba-elicitation-synthesizer and alongside ba-user-story-factory.
  Do not use for initial requirements capture: that belongs to ba-elicitation-synthesizer.
---

# BA Requirements Lifecycle

Governs the requirements from their point of capture through prioritisation, traceability,
change control, and formal approval. Works on an existing requirements register as its
primary input.

## Reference Files

Read both before processing any input:
- `references/traceability-matrix-template.md` — column definitions, link types, and coverage rules for the requirements traceability matrix
- `references/change-impact-classification.md` — change request classification, impact scoring criteria, and approval routing rules

---

## Input Handling

### Minimum Viable Input
One of:
- An existing requirements register (from ba-elicitation-synthesizer) as Excel or text
- A requirements list with IDs, even if partially complete
- A change request description referencing one or more requirement IDs

### Optimal Input
| Input | Effect |
|-------|--------|
| Requirements register from ba-elicitation-synthesizer | Full traceability starting point |
| Product backlog from ba-user-story-factory | Enables story-to-requirement tracing |
| Test case register from ba-test-case-generator | Enables requirement-to-test coverage check |
| Change request document | Enables Change Impact Assessment (Task 5.4) |
| Approval authority list | Enables Approve Requirements output (Task 5.5) |

### Mode Selection
This skill operates in five modes corresponding to BABOK Chapter 5 tasks. State the mode
or let the skill infer from the trigger phrase.

| Mode | BABOK Task | When to use |
|------|-----------|------------|
| Trace | 5.1 | Building or updating the RTM |
| Maintain | 5.2 | Versioning, flagging stale items, producing a change log |
| Prioritize | 5.3 | Scoring and ranking a requirements set |
| Assess Change | 5.4 | Evaluating the impact of a proposed change to a requirement |
| Approve | 5.5 | Producing a sign-off pack with named approvers |

Multiple modes may be run in sequence (e.g., Trace then Approve). Run them in the order listed.

### Clarification Rule
If the mode is ambiguous, ask one question:
> "Are you tracing existing requirements to other artefacts, managing a change request,
> or preparing requirements for formal approval?"

---

## Processing Steps

### Mode 1 — Trace Requirements (BABOK 5.1)

**Purpose:** Create and maintain a Requirements Traceability Matrix (RTM) linking requirements
to their origin, to solution components, and to test cases.

**Step 1.1 — Identify link levels**
Read `references/traceability-matrix-template.md`. Establish which link levels are in scope:
- Business need to requirement (origin tracing)
- Requirement to epic or story (decomposition tracing)
- Requirement to test case (coverage tracing)
- Requirement to solution component (implementation tracing)

**Step 1.2 — Build the RTM**
For each requirement in the register, populate all in-scope link levels.
Flag any requirement with no downstream link as `[UNTRACEABLE — no story or test case]`.
Flag any story or test case with no upstream requirement as `[ORPHAN — no source requirement]`.

**Step 1.3 — Coverage report**
Calculate:
- Requirements with full trace: N / Total (%)
- Requirements with no downstream link: list by ID
- Test coverage: % of requirements with at least one test case linked

---

### Mode 2 — Maintain Requirements (BABOK 5.2)

**Purpose:** Keep the register accurate as the project evolves. Detect stale, superseded,
or contradicted items and produce a versioned change log.

**Step 2.1 — Baseline check**
Compare the current register against any prior version provided. For each changed item, record:
`Requirement ID | Change type (Added / Modified / Deleted / Status changed) | Change description | Who changed it | Date`

**Step 2.2 — Staleness scan**
Flag any requirement as `[STALE — review required]` if:
- Its Status has been Draft for more than 30 days with no update activity (if dates are available)
- A dependency (DE) it references has been deleted or superseded
- An assumption (AS) it depends on has been overturned in the Issues Log

**Step 2.3 — Version stamp**
Assign a version number to the updated register following: `v{major}.{minor}` where:
- Major version: baseline agreed with sponsor (v1.0, v2.0, etc.)
- Minor version: working changes between baselines (v1.1, v1.2, etc.)

---

### Mode 3 — Prioritize Requirements (BABOK 5.3)

**Purpose:** Apply a scoring model to rank requirements and surface the highest-value items
for implementation sequencing.

**Step 3.1 — Select prioritisation technique**
Default: MoSCoW (already applied by ba-elicitation-synthesizer).
Supplementary techniques available when MoSCoW is insufficient for ranking within tiers:

| Technique | When to use |
|-----------|------------|
| Weighted scoring | Multiple competing criteria (e.g., business value, urgency, risk) |
| Kano model | User satisfaction context: Basic / Performance / Delight |
| Business value / effort matrix | Two-axis prioritisation for backlog sequencing |
| Dependency-first ordering | When certain requirements unlock others |

**Step 3.2 — Score and rank**
Apply the selected technique. Produce a ranked list with scores, rationale, and any
dependencies that force a re-ordering.

**Step 3.3 — Conflict resolution**
If two stakeholders have assigned conflicting priorities to the same requirement
(from the ba-elicitation-synthesizer Issues Log), surface the conflict and suggest a
resolution route (defer to decision-maker, split the requirement, or accept both versions
with scope boundaries).

---

### Mode 4 — Assess Requirements Changes (BABOK 5.4)

**Purpose:** Evaluate the impact of a proposed change to one or more requirements and
produce a structured change request assessment.

**Step 4.1 — Classify the change**
Read `references/change-impact-classification.md`. Classify the change request:

| Class | Definition | Approval route |
|-------|-----------|----------------|
| Minor | Wording clarification; no functional change | BA sign-off only |
| Moderate | Functional scope change within agreed boundaries | BA + Sponsor sign-off |
| Major | Adds new capability, removes agreed capability, or affects budget/timeline | Formal change control board |
| Critical | Changes baseline assumptions or contractual commitments | Escalate to programme level |

**Step 4.2 — Impact analysis**
For the changed requirement(s), identify all downstream items affected:
- Stories that implement this requirement
- Test cases that test this requirement
- Dependencies that reference this requirement
- Business case assumptions that this requirement supported

**Step 4.3 — Produce change request record**
| Field | Content |
|-------|---------|
| Change Request ID | CR-{NNN} |
| Requirement ID(s) affected | List |
| Change description | What is being proposed |
| Reason for change | Business driver or stakeholder request |
| Impact: stories affected | Count and list of Story IDs |
| Impact: test cases affected | Count and list of TC IDs |
| Impact: effort estimate | Low / Medium / High [Estimated] |
| Impact: schedule | No impact / Minor delay / Significant delay [Estimated] |
| Classification | Minor / Moderate / Major / Critical |
| Recommendation | Approve / Reject / Defer / Descope and replace |
| Approval required from | Named role(s) |

---

### Mode 5 — Approve Requirements (BABOK 5.5)

**Purpose:** Produce a formal requirements sign-off pack for stakeholder review and approval.

**Step 5.1 — Prepare approval register**
From the requirements register, extract all items with Status = Draft or Status = Under Review.
Group by domain cluster.

**Step 5.2 — Assign approvers**
Using the RACI matrix from ba-stakeholder-analyzer (if available), assign an approver (A column)
to each requirement domain. If no RACI is available, assign approver by stakeholder archetype:
- Functional Requirements: Sponsor or Decision-Maker
- Non-Functional Requirements: Technical Gatekeeper
- Constraints and Compliance: Regulator / Compliance stakeholder
- Assumptions: Sponsor

**Step 5.3 — Build sign-off pack**
The sign-off pack is a Word document with one section per domain cluster, each containing:
- The requirements table for that domain (ID, statement, MoSCoW, open issues)
- A signature block: Approver name, role, signature line, date
- A conditional approval field: "Approved with the following conditions: ___"

**Step 5.4 — Post-approval action**
Once approved requirements are returned, update the register:
- Status: Draft → Approved
- Add Approved By and Approval Date columns
- Move any conditionally approved items to the Issues Log for resolution

---

## Output Specification

### Trace Mode Outputs
1. `{project}_requirements_traceability.xlsx` — RTM with all link levels, orphan/untraceable flags, coverage %
2. Inline coverage summary: % fully traced, count orphaned stories, count untraceable requirements

### Maintain Mode Outputs
1. `{project}_requirements_register_v{N}.xlsx` — versioned register with change log sheet added
2. `{project}_requirements_change_log.docx` — narrative version history with all changes since last baseline

### Prioritize Mode Outputs
1. `{project}_requirements_prioritised.xlsx` — scored and ranked register with rationale column
2. Inline summary: top 10 ranked requirements, technique used, conflicts surfaced

### Assess Change Mode Outputs
1. `{project}_change_request_{CR-NNN}.docx` — change request record per CR
2. `{project}_change_impact_register.xlsx` — running log of all CRs with status and decisions

### Approve Mode Outputs
1. `{project}_requirements_sign_off_pack.docx` — approval document with signature blocks per domain
2. `{project}_requirements_register_approved.xlsx` — post-approval register with status updated

---

## Quality Gates

Before delivering any output:
- [ ] Trace mode: every requirement has at least one link level populated; orphans are flagged, not ignored
- [ ] Maintain mode: every change in the change log traces to a named person and a date; no undocumented changes
- [ ] Prioritize mode: every requirement has a score; no ties resolved without a stated rationale
- [ ] Assess Change mode: every change request has a classification and an approval route; no unclassified CRs
- [ ] Approve mode: every domain cluster has a named approver; no approver listed without a role reference
- [ ] All output IDs are consistent with the source register (no renumbering)

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| RTM (Trace) | `ba-test-case-generator` — coverage check before UAT; `ba-scrum-events-pack` — Sprint Review acceptance evidence |
| Approved requirements register (Approve) | `ba-user-story-factory` — only approved FRs should seed stories in a formal project |
| Change impact register (Assess Change) | `ba-business-case-builder` — scope change costs and schedule impacts |
| Prioritised requirements (Prioritize) | `ba-user-story-factory` — sequencing input for epic and story ordering |
