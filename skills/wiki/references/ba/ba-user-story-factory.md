---
name: ba-user-story-factory
description: >
  Decomposes epics and features into INVEST-compliant user stories with Gherkin
  acceptance criteria, story dependency maps, and a backlog-ready Excel register.
  Trigger this skill whenever the user says "write user stories", "decompose this epic",
  "break this down into stories", "story decomposition", "story splitting", "acceptance
  criteria", "Gherkin", "Given When Then", "backlog refinement", "user story format",
  "story mapping", "As a user I want", or "help me write the backlog". Also triggers on
  "turn these requirements into stories", "how do I split this feature", "this epic is
  too big", or any request to convert high-level requirements into granular,
  sprint-ready Product Backlog Items. Produces an Excel backlog register and a Word
  story spec. Use after ba-elicitation-synthesizer or ba-gap-analysis. Feeds
  ba-test-case-generator directly: acceptance criteria become test inputs.
---

# BA User Story Factory

Decomposes epics and features into INVEST-compliant user stories with Gherkin acceptance criteria.
Applies systematic story splitting and outputs a backlog-ready register plus a BABOK-style spec.

## Reference Files

Read both before processing any input:
- `references/invest-criteria.md` — INVEST test definitions, failure modes, and repair patterns
- `references/story-splitting-patterns.md` — 9 splitting patterns with examples and application rules

---

## Input Handling

### Minimum Viable Input
One or more of:
- Epic or feature statement (any form — narrative, bullet, requirement statement)
- High-level capability description
- Gap analysis Quick Win items (from ba-gap-analysis)
- FR items from a requirements register (from ba-elicitation-synthesizer)

### Optimal Input
| Input | Effect |
|-------|--------|
| Persona / user role context | Correctly populates "As a [role]" — critical for accuracy |
| Technical constraints or NFRs | Enables NFR story generation and dependency tagging |
| Definition of Ready (team's) | Validates stories against the team's acceptance bar |
| Decomposition depth | Epic only / Epic + Stories / Epic + Stories + Subtasks |
| Domain or module context | Improves cluster grouping and ID scheme |
| Sprint velocity or capacity | Enables size check: do all Must-Have stories fit? |

### Clarification Rule
If no user role or persona is provided, ask one question:
> "Who is the primary user of this feature — what role or persona are they?"

If the input is a single high-level feature with no breakdown hint, do not ask — derive roles
from the domain context and proceed.

---

## Processing Steps

### Step 1 — Identify and Name Epics
If input contains multiple themes or capability clusters, name each as an Epic first.
Format: `EPIC-{NNN}: [Capability Area] — [Goal statement]`
Example: `EPIC-001: Authentication — Enable secure, self-service access management`

One epic per distinct capability cluster. Do not merge unrelated capabilities into a single epic.

### Step 2 — Apply Story Splitting
Read `references/story-splitting-patterns.md`. For each epic, identify applicable splitting
patterns and apply them to generate candidate stories.

Apply a minimum of 2 splitting patterns per epic. Common first pass: workflow step split + role split.
Do not generate more than 12 stories per epic on first pass — consolidate before adding more.

### Step 2.5 — Vertical Slice Check (tracer bullets)
Every Functional story must cut through every layer it touches (schema → service → API → minimal UI)
and end in something a reviewer can observe working. Splitting drifts horizontal by default
("build the gamification service", "create the schema") — nothing is integration-testable until the
last layer lands, and horizontal stories serialize implementers that could otherwise work in parallel.

- A story whose deliverable is a single layer with no observable behavior FAILS the check.
  Repair: re-split so the first story is the thinnest end-to-end path
  (e.g. "award points for lesson completion, visible on the dashboard"), then widen with later stories.
- `Technical Enabler` is the only story type exempt, and each one must carry a one-line
  justification for why it cannot be folded into a slice.

### Step 3 — Write Stories in Standard Form
Format: `As a [specific role], I want [specific action or capability], so that [specific outcome or value]`.

Rules:
- "As a" — use the specific role, not "user" or "person" unless genuinely universal
- "I want" — one specific action or capability; no AND
- "So that" — the business reason or value; this is not optional
- If the value is unclear, flag `[VALUE UNCLEAR — confirm with Product Owner]`

### Step 4 — Apply INVEST Test
Read `references/invest-criteria.md`. Test every story against all 6 INVEST criteria.
Flag failures explicitly. Apply repair patterns from the reference file.

Do not pass a story that fails I (Independent) or T (Testable) without a repair.
S (Small) failures are acceptable if the story is tagged for further splitting in a future refinement.

### Step 5 — Write Gherkin Acceptance Criteria
Write at minimum:
- One happy-path scenario
- One negative or exception scenario
- One boundary condition scenario (where applicable)

Gherkin format:
```
Scenario: [Scenario name — descriptive, not generic]
  Given [the initial context or precondition]
  When [the action taken by the actor]
  Then [the expected observable outcome]
  And [additional outcome if needed]
```

Rules:
- Scenario names must distinguish scenarios from each other — no "happy path 1", "happy path 2"
- Given: system or data state, not a user action
- When: one user action only — no "and then they also click"
- Then: observable, testable result — not "the system works correctly"
- One scenario per rule or condition; do not combine multiple conditions in one scenario

### Step 6 — Classify and Tag
Tag every story with:
| Tag | Values |
|-----|--------|
| Story Type | Functional / NFR / Spike / Technical Enabler |
| Effort Indicator | XS (< 1 day) / S (1–2 days) / M (3–5 days) / L (> 5 days, needs splitting) |
| Domain / Epic | Parent epic ID |
| MoSCoW | From source requirement (inherit) or assign |
| Dependencies | Story IDs that must be complete before this story can be started |

L-sized stories must be flagged: `[NEEDS SPLITTING — too large for a single sprint item]`

### Step 7 — Build Dependency Map
Identify sequencing constraints between stories:
- "This story needs [story ID] to be Done first"
- "These two stories can run in parallel"
- Circular dependencies are a defect — flag and resolve
- The map must form a DAG of independently grabbable stories: minimize chain length, maximize
  Parallel-safe entries. A long sequential chain can only be executed by one implementer at a time;
  report the longest chain and re-split if it exceeds half the story count

### Step 8 — NFR Story Generation
For each NFR in the input (or inherited from the source requirements register):
Generate a dedicated NFR story:
`As a [system operator / user role], I need [quality attribute] so that [business consequence].`
Acceptance criteria for NFR stories must include the measurable threshold from the NFR.

---

## Output Specification

### Output 1 — Excel Backlog Register
Filename: `{project}_product_backlog.xlsx`
Location: `/mnt/user-data/outputs/`

**Sheet 1: Product Backlog**
| Column | Content |
|--------|---------|
| Story ID | {PREFIX}-{EPIC}-{NNN} e.g. PAY-001-012 |
| Epic ID | Parent epic reference |
| Story Type | Functional / NFR / Spike / Technical Enabler |
| User Story | Full "As a / I want / So that" statement |
| Acceptance Criteria | All Gherkin scenarios, one per line |
| MoSCoW | Must / Should / Could / Won't |
| Effort | XS / S / M / L |
| INVEST Issues | Any failing criteria and repair applied |
| Dependencies | Story ID(s) this story depends on |
| Status | Draft |
| Notes | Value unclear flags, splitting flags, open questions |

**Sheet 2: Epics**
Columns: Epic ID, Epic Name, Goal Statement, Story Count, Total Must-Have stories, Notes

**Sheet 3: Dependency Map**
Columns: Story ID, Depends On (Story ID), Dependency Type (Blocks / Informs / Parallel-safe)

**Sheet 4: NFR Traceability**
Columns: NFR ID (from requirements register), NFR Statement, Threshold, Story ID(s) implementing it

### Output 2 — Word Story Specification
Filename: `{project}_story_spec.docx`
Location: `/mnt/user-data/outputs/`
Format: BABOK-style two-column table per story (label column narrow, content column wide)
Standard: Sentence case headings. No em dashes.

One section per epic. Within each section:
- Epic summary box (ID, name, goal, story count)
- Story cards: one BABOK-style table per story with rows for: Story ID, User Story, Acceptance Criteria, Story Type, Effort, MoSCoW, Dependencies, INVEST Notes

### Output 3 — Inline Summary (in conversation)
- Total epics and total stories generated
- Story count by MoSCoW
- Stories flagged for splitting (L-size)
- INVEST failures and repairs applied
- Dependency chain: longest chain (most stories in sequence)

---

## Quality Gates

Before delivering any output:
- [ ] Every story has a "So that" clause — no exceptions
- [ ] Every story has at minimum one happy-path and one negative-path Gherkin scenario
- [ ] No story contains AND in the "I want" clause
- [ ] Every Functional story is a vertical slice (observable end-to-end behavior); horizontal layer-stories are repaired or justified as Technical Enablers
- [ ] Every L-sized story is flagged for splitting
- [ ] Every dependency is bidirectional in the dependency map
- [ ] NFR stories have measurable thresholds in their acceptance criteria
- [ ] "As a user" has been replaced with a specific role everywhere possible

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| Product Backlog — all stories | `ba-test-case-generator` — Gherkin scenarios become test case inputs |
| Product Backlog — Must Have stories | `ba-scrum-events-pack` — Sprint Planning Product Backlog input |
| NFR Traceability sheet | `ba-test-case-generator` — NFR test scenario generation |
| Dependency Map | `ba-scrum-events-pack` — Sprint Planning sequencing input |
