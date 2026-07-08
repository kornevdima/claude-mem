---
name: ba-rfi-rfp-analyzer
description: >
  Parses RFI and RFP documents and produces a compliance matrix, response outline,
  requirement extraction, clarification question list, and vendor evaluation scorecard.
  Operates in two modes: Respond (vendor answering an RFP) and Evaluate (buyer assessing
  vendor responses). Trigger this skill whenever a user uploads or pastes an RFP or RFI
  document; says "respond to this RFP", "analyse this RFI", "RFP compliance matrix",
  "vendor response", "RFP requirements", "extract requirements from this RFP",
  "score vendor responses", "evaluate proposals", "vendor selection", "build a scorecard",
  or "help me respond to this tender". Also triggers on "we received an RFP and need to
  respond", "I need to evaluate proposals from vendors", "map our solution to these requirements",
  "clarification questions for the issuer", or any request involving procurement documents,
  tender responses, or vendor evaluation. Produces Excel compliance matrix and Word response
  outline or evaluation report depending on mode.
---

# BA RFI/RFP Analyzer

Extracts, classifies, and structures requirements from procurement documents. Produces a
compliance matrix for vendor responses or an evaluation scorecard for buyer assessment.

## Reference File

Read before processing any input:
- `references/rfp-requirement-classification.md` — requirement category taxonomy, compliance
  status definitions, and common RFP document structure patterns

---

## Input Handling

### Minimum Viable Input
- Uploaded or pasted RFP or RFI document (any format)
- Mode tag: **Respond** (you are the vendor) or **Evaluate** (you are the buyer assessing responses)

### Optimal Input
| Input | Effect (Respond mode) | Effect (Evaluate mode) |
|-------|----------------------|----------------------|
| Company/solution profile | Auto-populates response stubs with relevant claims | — |
| Existing product capability list | Improves compliance status accuracy | — |
| Vendor response documents (1–4) | — | Enables side-by-side scoring |
| Evaluation criteria weights | — | Configures the scoring model |
| Deadline and submission format | Populates document control | — |

### Mode Clarification Rule
If mode is not specified, ask one question:
> "Are you responding to this RFP as a vendor, or are you a buyer evaluating vendor responses?"

---

## Processing Steps — Both Modes

### Step 1 — Parse Document Structure
Read `references/rfp-requirement-classification.md` §2 for common RFP section patterns.
Identify and extract:
- Mandatory requirements (those that must be met for a response to be valid)
- Evaluation criteria (weighted or unweighted)
- Submission requirements (format, deadline, attachments, signatures)
- Scope of work or specifications
- Terms and conditions sections
- Clarification or Q&A process details

### Step 2 — Extract and Classify Requirements
Identify every discrete requirement statement in the document. Extract one requirement per row.
Read `references/rfp-requirement-classification.md` §1 for category taxonomy.

| Category Code | Category |
|--------------|---------|
| F | Functional |
| T | Technical / Non-Functional |
| C | Commercial |
| L | Legal / Contractual |
| CO | Compliance / Regulatory |
| SL | Service Level / SLA |
| S | Submission / Process |

Mark mandatory requirements with `[MANDATORY]`. These are knockout criteria — non-compliance
disqualifies the response or the vendor.

### Step 3 — Detect Ambiguities
Flag requirements that are:
- Vague: "industry-leading solution" — no measurable criterion
- Contradictory: two requirements that cannot both be fully met
- Technically unclear: references a standard or version not specified

Log all flagged items as clarification question candidates.

---

## Respond Mode — Additional Steps

### Step 4R — Assign Compliance Status
For each extracted requirement, assign:

| Status | Definition |
|--------|-----------|
| Fully Compliant | The proposed solution meets this requirement completely, without qualification |
| Partially Compliant | The proposed solution meets the spirit of the requirement but with a stated limitation or gap |
| Non-Compliant | The proposed solution does not meet this requirement |
| Compliant with Conditions | The solution can meet this requirement subject to a stated condition (e.g. configuration, third-party) |
| To Be Confirmed | Compliance status requires internal verification before the response is finalised |

### Step 5R — Write Response Stubs
For each Fully or Partially Compliant requirement, write a 2–4 sentence response stub:
- State compliance status first
- Reference the specific capability, feature, or approach
- Quantify where possible (SLA met: 99.9%, response time: <2s)
- Flag any deviation from the requirement honestly

Non-Compliant items: write a candid one-sentence acknowledgement and, where possible, a workaround or roadmap note.

### Step 6R — Generate Clarification Questions
For each ambiguous or unclear requirement, write a specific, answerable clarification question.
Format: "Regarding section [X.Y], requirement [ID]: [Question]."
State the impact of the ambiguity on the response: "Clarification is needed to confirm whether
our [capability] satisfies this requirement."

---

## Evaluate Mode — Additional Steps

### Step 4E — Build Scoring Criteria
If weights are provided in the RFP, use them. If not, apply defaults from
`references/rfp-requirement-classification.md` §3.

### Step 5E — Score Vendor Responses
For each mandatory requirement: pass/fail.
A vendor that fails any mandatory requirement is eliminated from the scored evaluation.

For each scored criterion: apply 1–5 scale per vendor.
| Score | Definition |
|-------|-----------|
| 5 | Fully addresses the criterion with evidence |
| 4 | Addresses the criterion with minor gap or limited evidence |
| 3 | Partially addresses the criterion |
| 2 | Minimal coverage; significant gaps |
| 1 | Does not address the criterion |
| 0 | Not addressed at all |

Calculate: Weighted Score = Score × Weight per criterion. Sum for total per vendor.

### Step 6E — Write Evaluation Narrative
For the top two scoring vendors: write a 3–5 sentence comparison narrative per major criterion cluster.
Conclude with a recommended vendor and top three rationale points.

---

## Output Specification

### Output 1 — Excel Compliance Matrix / Evaluation Scorecard
Filename: `{project}_rfp_{mode}.xlsx`
Location: `/mnt/user-data/outputs/`

**Respond mode — Sheet 1: Compliance Matrix**
| Column | Content |
|--------|---------|
| Req ID | RFP section + sequential number |
| Category | F / T / C / L / CO / SL / S |
| Mandatory | Yes / No |
| Requirement Text | Verbatim or paraphrased from source |
| Compliance Status | Fully / Partially / Non / Conditions / TBC |
| Response Stub | 2–4 sentence response |
| Evidence Reference | Where in our solution/proposal this is addressed |
| Internal Owner | Who in our team confirms this |
| Notes | Ambiguity flags, deviation notes |

**Respond mode — Sheet 2: Clarification Questions**
Columns: Q ID, RFP Section, Requirement ID, Question, Impact of Ambiguity, Status (Sent/Answered)

**Evaluate mode — Sheet 1: Mandatory Check**
Columns: Req ID, Mandatory Requirement, Vendor A Pass/Fail, Vendor B Pass/Fail (etc.)

**Evaluate mode — Sheet 2: Scoring Matrix**
Columns: Criterion, Weight, Vendor A Score, Vendor A Weighted, Vendor B Score, Vendor B Weighted (etc.)
Bottom row: Total Weighted Score per vendor

**Evaluate mode — Sheet 3: Detailed Evidence**
One row per criterion per vendor with: verbatim evidence quote from the response,
page/section reference, and scoring rationale

### Output 2 — Word Response Outline (Respond) or Evaluation Report (Evaluate)
Filename: `{project}_rfp_response_outline.docx` or `{project}_rfp_evaluation.docx`
Location: `/mnt/user-data/outputs/`

**Respond mode — Response Outline:**
1. Document control and submission checklist
2. Compliance summary table (counts by status and category)
3. Mandatory requirements compliance statement
4. Response narrative outline: one section per RFP section; each section has the response stubs embedded
5. Deviations and limitations: list all Partially Compliant and Non-Compliant items with explanation
6. Clarification questions list for submission

**Evaluate mode — Evaluation Report:**
1. Document control
2. Evaluation scope: requirements extracted, vendors assessed, mandatory check results
3. Scoring summary table: all vendors, total scores, rank
4. Findings by criterion cluster: comparison narrative for top two vendors
5. Recommendation: named vendor, three financial/technical reasons, two risk points
6. Conditions on recommendation and next steps

### Output 3 — Inline Summary (in conversation)
- Mode confirmed, document sections identified
- Total requirements extracted, count by category
- Mandatory requirement count
- Respond mode: Compliance summary (counts by status), top 3 clarification questions needed
- Evaluate mode: Vendor ranking table, recommended vendor and primary rationale

---

## Quality Gates

Before delivering any output:
- [ ] Every mandatory requirement has an explicit compliance status (Respond) or pass/fail (Evaluate)
- [ ] No compliance status left as "TBC" without a named internal owner to confirm
- [ ] Every ambiguous requirement has a clarification question
- [ ] Evaluate mode: no vendor with a mandatory fail appears in the scored comparison
- [ ] Response stubs are factual — no unsubstantiated claims
- [ ] Submission requirements section is extracted and included in the Word document checklist
