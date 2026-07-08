---
name: ba-elicitation-synthesizer
description: >
  Transforms unstructured elicitation inputs (interview transcripts, workshop notes,
  email threads, uploaded PDFs or Word documents, RFP excerpts, voice memo summaries,
  stakeholder interviews) into a classified, MoSCoW-prioritised requirements package
  delivered as a Word BRD and an Excel requirements register. Trigger this skill
  whenever the user pastes or uploads raw notes and wants structured requirements
  extracted, or says "turn this into requirements", "extract requirements", "I have
  notes from a session", "help me write a BRD", "requirements gathering", "classify
  these notes", "sort out what they said", or "MoSCoW this". Also triggers on
  "what are the requirements here", "requirements register", "elicitation analysis",
  or "I need a BRD from this". Always use before ba-user-story-factory when the input
  is narrative or unstructured.
---

# BA Elicitation Synthesizer

Converts raw stakeholder input of any form into a classified, prioritised, issue-flagged requirements
package. Produces two file outputs and an inline summary.

## Reference Files

Read both before processing any input:
- `references/requirement-types.md` — full classification taxonomy with decision rules and per-type examples
- `references/moscow-language-triggers.md` — stakeholder language pattern → MoSCoW mapping with override rules

---

## Input Handling

### Minimum Viable Input
Any one of:
- Pasted text: meeting notes, email thread, transcript excerpt, bullet list
- Uploaded file: PDF, Word `.docx`, plain text
- Inline narrative ("the client said they need X and it must work offline")

### Optional Enrichment Inputs
| Input | Effect on Processing |
|-------|---------------------|
| Domain tag | Activates domain-specific NFR defaults (see `requirement-types.md` §5) |
| Project type | New build / Enhancement / Integration / Compliance / Migration — affects scope boundary inference |
| Stakeholder role of speaker | Weights authority: Sponsor statements → higher MoSCoW signal than end-user preference |
| Existing requirements register | Enables deduplication and conflict cross-reference |
| ID prefix | Sets the requirement ID scheme prefix (e.g. "CRM", "PAY", "ONBRD") |

### Multi-Source Merge Mode
When two or more input sources are provided simultaneously (for example, a workshop synthesis
export plus an interview transcript plus an existing SOP), activate Multi-Source Merge Mode:

1. **Label each source** before parsing: assign a source tag to every incoming document or paste
   (e.g. `[WS-01]` for the workshop export, `[INT-01]` for interview notes, `[DOC-01]` for a document).
2. **Parse each source independently** through Steps 1-4 before merging.
3. **Deduplication pass:** After all sources are parsed, scan for statements with overlapping intent.
   - Identical intent, same or different wording: merge into one item; record all source tags in the Source column.
   - Similar but not identical intent: keep both items; add a note "Review for merge with {ID}".
4. **Apply corroboration weighting:** Any item that appears in two or more independent sources
   (matching source tags are distinct) is flagged `[Corroborated]` in the Issues column.
   Corroborated items receive a minimum MoSCoW of Should Have. If the language triggers
   indicate Must Have on any single source, the merged item is Must Have.
5. **Source conflict detection:** If Source A and Source B make contradictory statements about
   the same element, raise a `[CONFLICT]` issue referencing both source tags.

When Multi-Source Merge Mode is active, the Stats sheet in the Excel output adds a
"Source distribution" row: count of items originating from each source, count of corroborated items.

### Synthesis Export Input Handling
When the input is a `_synthesis_export.docx` file produced by `ba-workshop-facilitator`,
parse it using the fixed section structure (Sections A through E) rather than free-text parsing:
- Section A (Raw Statements): parse each row as a candidate statement with speaker role as source tag
- Section B (Decisions): classify as CO (Constraint) or AS (Assumption) depending on content
- Section C (Parking Lot): classify as OQ (Open Question) or RI (Risk Indicator)
- Section D (Corroboration Flags): apply CORROBORATED tag and elevated MoSCoW directly
- Section E (Export Header): use the project prefix from this header for ID assignment; use session type to inform domain clustering

### Clarification Rule
If the input is ambiguous on session type, ask **one question only**:
> "Is this input from a single stakeholder, a multi-party workshop, or a document such as an RFP or SOP?"

Do not ask multiple questions. Proceed with best interpretation if user does not respond within the turn.

---

## Processing Steps

### Step 1 — Parse
Extract every discrete statement of intent, constraint, or assertion. Treat each sentence or bullet
containing a verb + subject as a candidate statement. Do not merge — keep atomic. Label each with
a provisional source tag (speaker name, document section, or "Input").

### Step 2 — Classify
Read `references/requirement-types.md` and apply the taxonomy to each statement.

| Code | Type |
|------|------|
| FR | Functional Requirement |
| NFR | Non-Functional Requirement |
| AS | Assumption |
| CO | Constraint |
| DE | Dependency |
| RI | Risk Indicator |
| OQ | Open Question |

A single source statement may produce multiple classified items. Split as needed.

### Step 3 — Rewrite to Standard Form
- **FR**: "The system shall [action] [object] [condition]." Actor must be explicit.
- **NFR**: "[System / Component] shall [metric] [measurable threshold] under [condition]."
  If threshold is absent, flag `[NO MEASURE]` and add to Issues Log.
- **AS / CO / DE**: Plain declarative. Start with "It is assumed that..." / "The solution is
  constrained to..." / "This requirement depends on..."
- **RI**: "There is a risk that [event] may [impact]."
- **OQ**: Rewrite as a direct question. Assign an owner if derivable from context.

Do not paraphrase meaning. Rewrite form only.

### Step 4 — Prioritise (MoSCoW)
Apply `references/moscow-language-triggers.md`. Where no language signal exists, apply:
- FR with regulatory or contractual basis → Must Have (note basis)
- FR with stated user workflow dependency → Should Have
- All others → Could Have, flagged "Inferred — confirm with stakeholder"

### Step 5 — Detect Issues
Scan the full classified set for:

| Issue Type | Definition | Flag |
|-----------|-----------|------|
| Conflict | Two statements that cannot both be true simultaneously | `[CONFLICT]` |
| Duplicate | Same intent, different wording — merge with a note | `[DUPLICATE]` |
| Ambiguity | Undefined scope, unmeasurable NFR, missing actor | `[AMBIGUOUS]` |
| Compound | Single statement containing AND or multiple conditions | `[COMPOUND — split]` |

Do not silently resolve conflicts. Surface all of them in the Issues Log.

### Step 6 — Assign IDs
Format: `{PREFIX}-{TYPE}-{NNN}` — e.g. `CRM-FR-001`, `CRM-NFR-003`, `CRM-OQ-001`
- Derive prefix from project name, domain, or ask if not determinable
- Sequence per type, starting at 001
- IDs are stable — do not renumber on subsequent iterations

### Step 7 — Group
Cluster requirements by:
1. Business domain or feature cluster (derive from verb-object patterns in the input)
2. Then by Type within each cluster

---

## Output Specification

### Output 1 — Excel Requirements Register
Filename: `{prefix}_requirements_register.xlsx`
Location: `/mnt/user-data/outputs/`

**Sheet 1: Register**
| Column | Content |
|--------|---------|
| ID | Auto-generated per §Step 6 |
| Type | FR / NFR / AS / CO / DE / RI / OQ |
| Domain / Cluster | Derived grouping label |
| Requirement Statement | Rewritten standard form |
| Source | Speaker name or document reference |
| MoSCoW | Must / Should / Could / Won't |
| Priority Basis | Direct language trigger or "Inferred" |
| Status | Draft (default on first pass) |
| Issues | `[CONFLICT]` / `[AMBIGUOUS]` / `[NO MEASURE]` flags, comma-separated |
| Notes | Clarification needed, linked OQ ID |

**Sheet 2: Issues Log**
Columns: Issue ID, Type, Requirement IDs Involved, Description, Suggested Resolution, Owner, Status

**Sheet 3: Open Questions**
Columns: OQ ID, Question, Context, Owner, Raised Date, Target Answer Date, Answer

**Sheet 4: Stats**
Auto-calculated: total per type, total per MoSCoW, total issues by type, % flagged

### Output 2 — Word BRD
Filename: `{prefix}_BRD_draft.docx`
Location: `/mnt/user-data/outputs/`
Standard: Sentence case headings. No em dashes. B2-level plain English. Dense tables over prose lists.

Sections:
1. Document control — version 0.1 Draft, date, author placeholder, reviewers placeholder, status
2. Executive summary — three sentences: business context, what was elicited, what remains open
3. Scope statement — two columns: In Scope / Out of Scope (derive from constraints and assumptions)
4. Stakeholder input sources — table: Name, Role, Session Type, Date
5. Requirements by domain — one table per domain cluster (ID, Statement, MoSCoW, Notes)
6. Assumptions and constraints — separate tables
7. Dependencies — table with linked requirement IDs
8. Issues and open questions — reference to register; do not duplicate in full
9. Next steps — three to five action items derived from the Issues Log

### Output 3 — Inline Synthesis Summary (in conversation)
Deliver immediately after file links:
- Total items: N (FR: x, NFR: x, AS: x, CO: x, DE: x, RI: x, OQ: x)
- Issues flagged: x conflicts, x ambiguities, x NFRs missing measurable criteria
- Top 3 Must-Have requirements (by ID and statement)
- Top 3 open questions requiring stakeholder follow-up (by ID)

---

## Quality Gates

Verify before delivering any output:
- [ ] Every FR has an explicit actor — no passive "it should be possible to"
- [ ] Every NFR has a measurable criterion, or is flagged `[NO MEASURE]`
- [ ] No requirement contains AND without being split first
- [ ] MoSCoW applied to 100% of items — no blanks
- [ ] All conflicts surfaced in Issues Log, none silently resolved
- [ ] ID scheme consistent across both outputs
- [ ] BRD executive summary accurately reflects totals from the register

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| Requirements Register — FR items | `ba-user-story-factory`: import as story seeds |
| Requirements Register — NFR items | `ba-test-case-generator`: NFR test scenario generation |
| BRD — problem statement + scope | `ba-business-case-builder`: problem statement section |
| Issues Log | `ba-stakeholder-analyzer`: unresolved items map to follow-up owners |
