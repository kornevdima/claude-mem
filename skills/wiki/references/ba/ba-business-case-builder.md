---
name: ba-business-case-builder
description: >
  Constructs a full, structured business case document following PMI/BABOK standards with
  financial modelling: executive summary, problem statement, strategic alignment, options
  analysis including Do Nothing baseline, cost-benefit model, NPV/ROI/payback period,
  risk assessment, and a clear recommendation. Delivers Word document plus Excel financial
  model. Trigger this skill whenever a user says "business case", "investment case",
  "justify this project", "write a business case", "ROI analysis", "cost benefit analysis",
  "options analysis", "build vs buy", "make the case for", "we need approval for",
  "investment approval", "board paper", "project justification", or "financial case".
  Also triggers on "what's the ROI", "how do we justify this spend", "I need to present
  the options", "help me get budget approved", or any request to produce a decision-support
  document for an investment, initiative, or project. Use after ba-gap-analysis when
  the gap inventory needs to be translated into an investment case.
---

# BA Business Case Builder

Constructs a structured, board-ready business case with financial modelling from strategy
inputs, gap analysis, and solution options. Applies PMI/BABOK structure with NPV, ROI,
and payback period calculated explicitly.

## Reference Files

Read both before processing any input:
- `references/business-case-anatomy.md` — section-by-section content guide, writing standards, and quality criteria per section
- `references/financial-model-formulas.md` — NPV, ROI, payback period formulas with worked examples and sensitivity analysis design

---

## Input Handling

### Minimum Viable Input
One of:
- A problem or opportunity statement
- A gap analysis output (from ba-gap-analysis)
- A brief project description with at least one option to evaluate

### Optimal Input
| Input | Effect |
|-------|--------|
| Gap analysis register (from ba-gap-analysis) | Populates problem statement and gap inventory |
| Solution options (1–3) | Enables Options Analysis section |
| Cost estimates (order-of-magnitude acceptable) | Enables financial model |
| Benefit assumptions | Enables cost-benefit analysis |
| Strategic objectives or OKRs | Enables Strategic Alignment section |
| Risk register or assumptions log | Populates Risk Assessment section |
| Stakeholder analysis (from ba-stakeholder-analyzer) | Informs Executive Summary framing |
| Decision-maker profile | Adjusts tone and level of financial detail |

### Assumptions Handling
If cost or benefit figures are not provided, derive order-of-magnitude estimates from context
and label every figure as `[Estimated — requires validation]`. Never present invented figures
as confirmed. The financial model must work with clearly stated assumptions.

### Clarification Rule
If no options are provided, ask one question:
> "Should I include a Do Nothing baseline plus the main proposed option, or do you have
> specific alternatives to compare?"

---

## Processing Steps

### Step 1 — Frame the Problem
Write the Problem / Opportunity Statement:
- What is the current state? (use AS-IS from gap analysis if available)
- What is the consequence of inaction? (link to risk indicators or cost of the status quo)
- What is the strategic opportunity? (link to organisational objectives if provided)
- Who is affected and how?

This section must be factual and evidence-based. Do not include the solution here.

### Step 2 — Confirm Strategic Alignment
Map the initiative to at least one organisational objective, OKR, strategy pillar, or regulatory
requirement. If none are provided, derive plausible alignment from the problem context and flag
as `[Alignment — confirm with sponsor]`.

### Step 3 — Define Options
Options must always include:
- **Option 0: Do Nothing** — the baseline. What happens if the organisation takes no action?
  Cost this option: ongoing cost of the problem, risk exposure, opportunity cost.
- **Option 1: Proposed Solution** — the primary recommendation
- **Option 2 (if applicable):** An alternative approach (build vs. buy, phased vs. full scope, etc.)

For each option, document:
- Description (what it involves)
- In scope / out of scope
- Key assumptions
- Dependencies and prerequisites
- Estimated implementation timeline

### Step 4 — Build Financial Model
Read `references/financial-model-formulas.md`.
Apply a 3-year or 5-year horizon (use 3-year unless specified).

For each option:
- List all cost categories and annual values
- List all benefit categories and annual values
- Calculate: Net Benefit per year, Cumulative Net Benefit, NPV, ROI %, Payback Period
- State discount rate used (default 8% if not provided; flag assumption)

Apply sensitivity analysis for the recommended option: what happens to NPV if:
- Benefits are 20% lower than estimated?
- Costs are 20% higher than estimated?

### Step 5 — Score Non-Financial Criteria
Apply a weighted scoring model for criteria that cannot be captured financially:
| Default Criteria | Default Weight |
|-----------------|----------------|
| Strategic alignment | 25% |
| Implementation risk | 20% |
| Time to value | 20% |
| Stakeholder impact | 15% |
| Technical fit | 10% |
| Organisational capability to deliver | 10% |

Score each option 1–5 per criterion. Calculate weighted total. Adjust weights if context warrants.

### Step 6 — Assess Risks
For each option, identify the top 3–5 risks:
- Probability: Low / Medium / High
- Impact: Low / Medium / High
- Risk rating = Probability × Impact (as L/M/H matrix)
- Mitigation: one sentence per risk

### Step 7 — Write Recommendation
State the recommended option explicitly. Do not hedge.
Support with: top 3 financial reasons, top 2 non-financial reasons, and primary risk.
Include: conditions for success (what must be true for this option to deliver its benefits).

---

## Output Specification

### Output 1 — Word Business Case Document
Filename: `{project}_business_case.docx`
Location: `/mnt/user-data/outputs/`
Standard: Sentence case headings. No em dashes. B2-level plain English. Dense tables over prose.

Sections (following business-case-anatomy.md):
1. Document control
2. Executive summary — one page maximum; problem, recommendation, key financial figures, decision required
3. Problem statement — factual, evidence-based
4. Strategic alignment — table: Initiative feature vs. Objective/OKR
5. Options analysis — one sub-section per option with description, scope, dependencies, timeline
6. Financial analysis — cost-benefit summary table per option; key metrics table (NPV, ROI, Payback)
7. Non-financial scoring — weighted scoring matrix
8. Risk assessment — risk table per option
9. Recommendation — explicit, supported, with conditions for success
10. Assumptions and constraints — full log
11. Appendix: detailed financial model reference (points to Excel file)

### Output 2 — Excel Financial Model
Filename: `{project}_financial_model.xlsx`
Location: `/mnt/user-data/outputs/`

**Sheet 1: Summary**
- Key metrics table: NPV, ROI %, Payback Period per option, side by side
- Recommended option highlighted

**Sheet 2: Financial Model (one tab per option)**
| Row | Year 0 | Year 1 | Year 2 | Year 3 | Total |
|-----|--------|--------|--------|--------|-------|
| COSTS | | | | | |
| [Cost category 1] | | | | | |
| [Cost category 2] | | | | | |
| Total Costs | =SUM | | | | |
| BENEFITS | | | | | |
| [Benefit category 1] | | | | | |
| Total Benefits | =SUM | | | | |
| Net Benefit | =Benefits-Costs | | | | |
| Discount Factor (8%) | 1.0 | 0.926 | 0.857 | 0.794 | |
| Discounted Net Benefit | =Net×Discount | | | | |
| Cumulative NPV | =running sum | | | | |

**Sheet 3: Sensitivity Analysis**
Scenario table for recommended option:
| Scenario | NPV | ROI % | Payback |
|----------|-----|-------|---------|
| Base case | | | |
| Benefits -20% | | | |
| Costs +20% | | | |
| Both adverse | | | |

**Sheet 4: Assumptions Log**
Columns: Assumption ID, Description, Value Used, Basis, Owner to Confirm

**Sheet 5: Non-Financial Scoring**
Weighted scoring matrix with formulas

### Output 3 — Inline Summary (in conversation)
- Options evaluated and Do Nothing included (confirm)
- Recommended option
- Key financials for recommended option: NPV, ROI %, payback period
- Sensitivity: does the recommendation hold if benefits are 20% lower? (yes/no)
- Top risk to the recommendation

---

## Quality Gates

Before delivering any output:
- [ ] Do Nothing option is present and costed
- [ ] Every financial figure has a stated assumption basis
- [ ] NPV uses a stated discount rate
- [ ] Sensitivity analysis covers both downside scenarios
- [ ] Recommendation is explicit — no "it depends" conclusions
- [ ] Every risk has a stated mitigation
- [ ] Executive summary fits on one page (approximately 400 words)
- [ ] Assumptions log in Excel matches assumptions referenced in the Word document

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| Approved business case | Project initiation, procurement, ba-rfi-rfp-analyzer |
| Recommended option scope | `ba-elicitation-synthesizer` — seeds requirements if not already done |
| Risk assessment | Project risk register; `ba-stakeholder-analyzer` — risks map to stakeholder concerns |
