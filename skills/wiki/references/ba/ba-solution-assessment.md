---
name: ba-solution-assessment
description: >
  Evaluates solution options or vendor proposals against weighted criteria using a
  structured scoring model with sensitivity analysis and a written recommendation.
  Trigger this skill whenever the user says "compare solutions", "evaluate options",
  "build vs buy", "vendor selection", "solution comparison", "weighted scoring",
  "options appraisal", "which solution should we choose", "decision matrix", "rate
  these options", "score the vendors", "which tool is best for us", or "help me choose
  between". Also triggers on "I have three vendors and need to pick one", "I need a
  recommendation on this", "create a scoring model for this decision", or any request
  for a defensible, evidence-based recommendation between two or more alternatives.
  Distinct from ba-rfi-rfp-analyzer (which parses procurement documents): this skill
  evaluates options against already-defined criteria.
---

# BA Solution Assessment

Produces a weighted scoring model, sensitivity analysis, and written recommendation for
any decision involving two or more options. Works for vendor selection, architecture
options, build/buy, or strategic initiative prioritisation.

## Reference File

Read before processing any input:
- `references/evaluation-criteria-library.md` — default criteria sets by decision type,
  scoring rubrics, and sensitivity analysis design

---

## Input Handling

### Minimum Viable Input
- Two or more options to evaluate (names or descriptions)
- A decision context (what are we deciding and why?)

### Optimal Input
| Input | Effect |
|-------|--------|
| Evaluation criteria list | Replaces defaults; use if the team has agreed criteria |
| Criteria weights | Replaces defaults; use if the team has agreed weights |
| Vendor proposals or solution descriptions | Enables evidence-based scoring |
| Requirements register (from ba-elicitation-synthesizer) | Functional fit criteria derived from requirements |
| Stakeholder priorities (from ba-stakeholder-analyzer) | Weights reflect what the Sponsor values most |
| Budget envelope | Adds commercial criterion with hard cap flag |
| Must-have criteria | Applied as knockout before weighted scoring begins |

### Clarification Rule
If the decision context is ambiguous (e.g. "compare these tools"), ask one question:
> "What is the primary problem this solution needs to solve, and who will be most
> affected by the choice?"

---

## Processing Steps

### Step 1 — Define Must-Have Criteria (Knockout)
Identify any criteria that are binary pass/fail before weighted scoring begins:
- Regulatory or compliance requirements (must hold this certification)
- Technical non-negotiables (must integrate with X)
- Budget hard cap (must be within £Y)
- Timeline constraint (must be deliverable by Z date)

Apply knockout check first. Any option failing a must-have is eliminated and noted in the
output. Do not include eliminated options in the scored comparison.

### Step 2 — Select Evaluation Criteria
Read `references/evaluation-criteria-library.md`. Select the default criteria set for the
decision type, or use the provided criteria list.

Group criteria into clusters (4–6 clusters of 2–5 criteria each).
Total weight must sum to 100%.

Default decision types:
- **Vendor / COTS selection:** functional fit, technical fit, vendor maturity, commercial, support
- **Build vs Buy:** total cost of ownership, time to value, strategic fit, risk, team capability
- **Architecture option:** technical soundness, scalability, cost, team capability, risk
- **Initiative prioritisation:** strategic impact, urgency, feasibility, risk, dependencies

### Step 3 — Score Each Option
For each criterion, score each surviving option 1–5.

| Score | Definition |
|-------|-----------|
| 5 | Fully meets the criterion; strong evidence |
| 4 | Meets the criterion with minor gap; evidence present |
| 3 | Partially meets the criterion; some evidence |
| 2 | Minimal meeting of the criterion; weak evidence |
| 1 | Does not meet the criterion |

Every score must have a one-sentence rationale. Scores without rationale are not valid.

Calculate: Weighted Score = Score × (Weight / 100) per criterion per option.
Total Score = Sum of Weighted Scores per option.

### Step 4 — Conduct Sensitivity Analysis
Read `references/evaluation-criteria-library.md` §3 for sensitivity design.

Run three sensitivity scenarios:
1. **Sponsor scenario:** Increase the top-priority criterion weight by 20%; reduce others proportionally
2. **Risk scenario:** Increase implementation risk criterion weight to 25%; reduce others proportionally
3. **Cost scenario:** Increase commercial/cost criterion weight to 30%; reduce others proportionally

For each scenario, recalculate total scores. Record whether the ranking changes.
If the ranking is stable across all three scenarios, the recommendation is robust.
If the ranking changes in any scenario, flag the sensitivity and name the condition
under which the alternative option would be preferable.

### Step 5 — Write Recommendation
State the recommended option in the first sentence.

Support with:
- Top 2 criteria where it clearly outperforms alternatives
- Sensitivity robustness statement
- Primary risk to the recommendation and its mitigation
- One condition or prerequisite for the recommendation to hold

If scores are close (within 5 points) between top two options, state this explicitly:
"The margin between Option A (score: X) and Option B (score: Y) is narrow. The recommendation
favours Option A on [specific criteria]; if [condition changes], Option B becomes preferable."

---

## Output Specification

### Output 1 — Excel Scoring Model
Filename: `{project}_solution_assessment.xlsx`
Location: `/mnt/user-data/outputs/`

**Sheet 1: Knockout Check**
| Criterion | Type | Option A | Option B | Option C |
|-----------|------|----------|----------|----------|
| [Must-have] | Knockout | Pass/Fail | Pass/Fail | Pass/Fail |
| Result | | Proceed/Eliminated | | |

**Sheet 2: Weighted Scoring Matrix**
| Criterion | Cluster | Weight % | Option A Score | Option A Wtd | Option B Score | Option B Wtd |
|-----------|---------|---------|----------------|--------------|----------------|--------------|
| | | | | | | |
| **Totals** | | **100%** | | **=SUM** | | **=SUM** |

**Sheet 3: Scoring Rationale**
| Criterion | Option A Rationale | Option A Score | Option B Rationale | Option B Score |
|-----------|-------------------|----------------|--------------------|----------------|

**Sheet 4: Sensitivity Analysis**
| Scenario | Changed Criterion | New Weight | Option A Total | Option B Total | Rank Change? |
|----------|------------------|------------|----------------|----------------|-------------|
| Base case | — | — | | | — |
| Sponsor | | | | | |
| Risk | | | | | |
| Cost | | | | | |

**Sheet 5: Criteria Definitions**
Full description of each criterion and its scoring rubric

### Output 2 — Word Assessment Report
Filename: `{project}_solution_assessment_report.docx`
Location: `/mnt/user-data/outputs/`
Standard: Sentence case headings. Dense tables. No em dashes.

Sections:
1. Document control
2. Decision context: what is being decided, who is deciding, decision timeline
3. Options in scope: one paragraph per option; eliminated options noted with reason
4. Evaluation criteria and weights: table with rationale for each cluster weight
5. Scoring results: summary table, scores by cluster
6. Sensitivity analysis: findings narrative with ranking stability statement
7. Recommendation: explicit, evidence-based, with conditions
8. Next steps: 3–5 actions to proceed from decision to implementation

### Output 3 — Inline Summary (in conversation)
- Options evaluated, any eliminated at knockout
- Winner and total score; runner-up and total score; margin
- Sensitivity: ranking stable across all scenarios? (yes/no; if no, name the condition)
- Top criterion differentiator between winner and runner-up

---

## Quality Gates

Before delivering any output:
- [ ] Every score has a rationale — no blank rationale cells
- [ ] Weights sum to exactly 100%
- [ ] Knockout check is applied before scoring — eliminated options not in the matrix
- [ ] All three sensitivity scenarios are run and ranking stability is stated
- [ ] Recommendation explicitly states the winning option in the first sentence
- [ ] Close decisions (within 5 points) are flagged and contextualised

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| Recommended option | `ba-business-case-builder` — options analysis section |
| Scoring model | Procurement process, governance approval documentation |
| Conditions on recommendation | `ba-elicitation-synthesizer` — conditions become constraints in requirements |
