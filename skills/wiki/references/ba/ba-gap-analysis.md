---
name: ba-gap-analysis
description: >
  Produces a structured gap analysis between an AS-IS baseline and a TO-BE target
  across any dimension: capabilities, processes, data, technology, organisation, or
  maturity. Outputs a scored gap register in Excel, a written narrative in Word, and
  a visual gap heatmap in Draw.io. Trigger this skill whenever the user says "gap
  analysis", "where are we vs where we need to be", "current state vs future state",
  "what is missing", "capability gap", "maturity gap", "process gap", "technology gap",
  "what needs to change", "delta analysis", "fit gap analysis", "requirements gap", or
  "what do we need to get from A to B". Also triggers on "identify the gaps", "assess
  what we have vs what we need", "compare current and target", or any request to
  evaluate shortfall between baseline and objective. Use after ba-process-modeler or
  ba-elicitation-synthesizer. Feeds ba-business-case-builder.
---

# BA Gap Analysis

Produces a scored, categorised gap register with recommended actions, root cause classification,
and a prioritised roadmap view. Works across any analytical dimension.

## Reference Files

Read both before processing any input:
- `references/gap-severity-rubric.md` — scoring criteria for gap severity and root cause classification
- `references/gap-action-patterns.md` — standard recommended action patterns, effort/impact defaults, and roadmap horizon rules

---

## Input Handling

### Minimum Viable Input
One of:
- A description of the current state AND a description of the desired state (any form)
- An AS-IS process or capability list AND a TO-BE target or requirements set
- A maturity assessment (current level) AND a target maturity level

### Optimal Input
| Input | Effect |
|-------|--------|
| AS-IS process model (from ba-process-modeler) | Structured baseline for process dimension |
| Requirements register (from ba-elicitation-synthesizer) | TO-BE target for capability dimension |
| Stakeholder interviews or survey data | Enriches people/organisation dimension |
| Technology inventory | Enables technology dimension analysis |
| Maturity model or framework reference | Enables maturity dimension analysis |
| Dimension tag | Process / Capability / Technology / Data / Organisation / Maturity |
| Priority weights per dimension | Scales the overall gap score |

### Multi-Dimension Analysis
If multiple dimensions are requested, process each dimension independently and then produce
a combined cross-dimension summary. Each dimension gets its own sheet in the Excel output.

### Clarification Rule
If the TO-BE target is vague ("we want to be best in class"), ask one question:
> "What specific outcome or standard defines success — is there a target state, a framework
> level, a benchmark, or a set of requirements you're measuring against?"

---

## Processing Steps

### Step 1 — Define Analysis Frame
Establish:
- **Dimension(s):** Process / Capability / Technology / Data / Organisation / Maturity
- **Baseline:** What exists today (AS-IS)
- **Target:** What must exist (TO-BE or requirement)
- **Scope:** Which part of the organisation, system, or process is in scope

### Step 2 — Decompose to Elements
Break the baseline and target into discrete, comparable elements.
- For **Process:** each process step or activity
- For **Capability:** each capability in a capability map or function list
- For **Technology:** each system, component, or integration point
- For **Data:** each data domain, entity, or quality dimension
- For **Organisation:** each role, team, or skill set
- For **Maturity:** each maturity domain or sub-dimension

Pair each baseline element with its corresponding target element. If no baseline element exists
for a target requirement, it is a **new capability gap** (score: Critical by default).

### Step 3 — Score Gap Severity
Read `references/gap-severity-rubric.md`. Apply the 5-level severity scale to each element pair.

| Score | Label | Definition |
|-------|-------|-----------|
| 0 | None | Current state fully meets the target — no action required |
| 1 | Minor | Small shortfall; addressable within current operations |
| 2 | Moderate | Meaningful shortfall; requires a defined improvement action |
| 3 | Significant | Major shortfall; requires a structured initiative or investment |
| 4 | Critical | Current state is absent or incompatible; blocks the TO-BE entirely |

Document the scoring rationale for every item with severity ≥ 2.

### Step 4 — Classify Root Cause
For each gap with severity ≥ 1, classify the primary root cause:

| Code | Root Cause |
|------|-----------|
| P | People — skills, capacity, roles, accountability |
| PR | Process — missing, broken, or inefficient workflow |
| T | Technology — absent, inadequate, or incompatible systems |
| D | Data — missing, poor quality, or inaccessible data |
| G | Governance — missing policy, ownership, or decision rights |

A gap may have a primary and secondary root cause. Record both if relevant.

### Step 5 — Derive Recommended Actions
Read `references/gap-action-patterns.md`. Map each gap to a recommended action pattern.
Assign effort (Low / Medium / High) and impact (Low / Medium / High) based on severity and root cause.

Derive action horizon:
- **Quick Win:** Low effort, Medium–High impact → execute now
- **Short-term Initiative:** Medium effort, High impact → within 90 days
- **Long-term Programme:** High effort, High impact → 90 days to 12 months
- **Accept / Monitor:** Low impact regardless of effort → monitor only, do not act now
- **Policy/Governance Fix:** G root cause, Low-Medium effort → governance action

### Step 6 — Calculate Scores and Prioritise
Aggregate:
- **Dimension score:** Mean severity across all elements in the dimension
- **Overall gap score:** Weighted mean across dimensions (apply priority weights if provided)
- **Priority order:** Sort by: Critical first → Significant → Moderate; within same severity, Quick Wins before Long-term Programmes

### Step 7 — Build Roadmap View
Group actions by horizon into a simple roadmap:
- Now (0–30 days): Quick Wins and governance fixes
- Short-term (30–90 days): Short-term initiatives
- Long-term (90+ days): Programme-level items
- Backlog: Accept/Monitor items

---

## Output Specification

### Output 1 — Excel Gap Register
Filename: `{project}_gap_analysis.xlsx`
Location: `/mnt/user-data/outputs/`

**Sheet per dimension** (named: Process Gap, Capability Gap, Technology Gap, etc.)
| Column | Content |
|--------|---------|
| Gap ID | G-{DIM}-{NNN} e.g. G-PR-001 |
| Dimension | Process / Capability / Technology / Data / Organisation / Maturity |
| Element | The capability, step, or item being assessed |
| AS-IS State | Description of current state (1–2 sentences) |
| TO-BE Target | What the element must look like or do |
| Severity Score | 0–4 with label |
| Severity Rationale | Why this score was assigned |
| Root Cause (Primary) | P / PR / T / D / G |
| Root Cause (Secondary) | Optional |
| Recommended Action | Specific action derived from gap-action-patterns.md |
| Effort | Low / Medium / High |
| Impact | Low / Medium / High |
| Horizon | Quick Win / Short-term / Long-term / Accept |
| Owner (suggested) | Role type, not person name |
| Status | Open (default) |

**Summary Sheet**
- Dimension scores table
- Overall weighted score
- Counts by severity level
- Counts by horizon
- Top 5 priority gaps (by severity + impact)

**Roadmap Sheet**
- Three-column timeline: Now / Short-term / Long-term
- Each gap action as a row under its horizon column
- Colour-coded by severity (Critical=red, Significant=amber, Moderate=yellow)

### Output 2 — Word Gap Analysis Report
Filename: `{project}_gap_analysis_report.docx`
Location: `/mnt/user-data/outputs/`
Standard: Sentence case headings. Dense tables. No em dashes.

Sections:
1. Document control
2. Executive summary: overall gap score, top 3 critical gaps, recommended first actions (one paragraph)
3. Analysis scope and method: dimensions covered, inputs used, scoring approach
4. Findings by dimension: one sub-section per dimension with key findings narrative (3–5 sentences) and top gaps table
5. Cross-dimension themes: if a root cause recurs across dimensions, name it (e.g. "Data governance appears as a root cause in 4 of 7 critical gaps")
6. Prioritised roadmap: three-horizon table with all recommended actions
7. Risks: gaps not being closed in the recommended timeframe and their consequence
8. Next steps: 3–5 specific actions with suggested owners

### Output 3 — Draw.io Gap Heatmap
Filename: `{project}_gap_heatmap.drawio`
Location: `/mnt/user-data/outputs/`

Layout: Grid of cells
- Rows: elements / capabilities being assessed
- Columns: dimensions or assessment criteria
- Cell fill colour: severity score → None=`#D5E8D4` / Minor=`#FFF2CC` / Moderate=`#FFE6CC` / Significant=`#F8CECC` / Critical=`#FF0000` with white text
- Cell label: element name + severity score (e.g. "Data Quality — 3")
- Legend in top-right corner
- Title and subtitle

### Output 4 — Business Case Seeds (conditional)
Filename: `{project}_business_case_seeds.md`
Location: `/mnt/user-data/outputs/`

**Produce this output when:**
- The skill is invoked as part of the `/investment-case` or `/change-impact` workflow command, OR
- The user states "this gap analysis feeds a business case", OR
- `ba-business-case-builder` is explicitly named as the next step

**Content:** A structured markdown file formatted as a direct input to `ba-business-case-builder`.
It contains only the elements that the business case builder needs and removes all scoring
scaffolding that is irrelevant to investment framing.

**Sections:**

**1. Problem statement seeds**
For each Critical (4) or Significant (3) gap, write one sentence in the form:
`The organisation cannot [TO-BE capability] because [AS-IS gap description], resulting in [consequence].`
These sentences feed directly into the Business Case Problem Statement section.

**2. Cost of inaction (Option 0 inputs)**
For each Critical gap, state the consequence of not closing it:
`Gap ID | Element | Consequence of inaction | Estimated annual cost or risk exposure [Estimated]`
If no cost figures are available, write "Cost unknown — confirm with [role]".

**3. Option seeds**
For each Long-term Programme item in the roadmap, produce a one-line option description:
`Proposed option: [action pattern] to close [Gap ID] — estimated effort: [Low/Medium/High]`

**4. Risk seeds**
For each Critical gap, produce one risk statement for the business case Risk Assessment section:
`Risk: If [gap] is not closed by [horizon], then [consequence] — Probability: [L/M/H] — Impact: High`

**5. Strategic alignment hooks**
If root cause codes include G (Governance) or T (Technology) across 2+ dimensions, flag:
`Cross-cutting theme: [root cause label] appears across N dimensions — recommend a programme-level response`

### Output 5 — Inline Summary (in conversation)
- Dimensions covered and total element count
- Score distribution: x Critical, x Significant, x Moderate, x Minor, x None
- Most common root cause
- Top 3 priority actions (Gap ID + action + horizon)
- Overall readiness statement: one sentence
- If Business Case Seeds produced: confirm seed count and flag any gaps with no cost data

---

## Quality Gates

Before delivering any output:
- [ ] Every gap has a severity score and a rationale for scores ≥ 2
- [ ] Every gap has a root cause classification
- [ ] Every severity ≥ 1 gap has a recommended action
- [ ] Every action has an effort, impact, and horizon assignment
- [ ] Summary sheet totals match the detail sheets
- [ ] Roadmap contains no orphan actions (every action traces back to a gap ID)
- [ ] No "new capability" gap is scored below Significant (absence = at minimum Significant)
- [ ] If Business Case Seeds output is produced: every Critical gap has a consequence of inaction statement; no consequence statement is left blank

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| Gap register — all items | `ba-business-case-builder` — gap inventory drives problem statement and options |
| Business Case Seeds file | `ba-business-case-builder` — structured pre-formatted input; use this file directly when produced |
| Roadmap — Quick Wins | `ba-user-story-factory` — Quick Win items become near-term backlog candidates |
| Roadmap — Long-term Programme items | `ba-business-case-builder` — investment case items |
| Root cause analysis | `ba-stakeholder-analyzer` — root causes map to ownership and resistance patterns |
