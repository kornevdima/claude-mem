---
name: ba-process-modeler
description: >
  Generates AS-IS and TO-BE business process models from narrative descriptions, interview
  outputs, SOPs, or workshop notes. Produces BPMN-notation-aligned Draw.io swimlane diagrams
  and written process specifications. Trigger this skill whenever a user says "map this process",
  "document the process", "AS-IS process", "TO-BE process", "how does this work today",
  "current state process", "future state process", "process flow", "swimlane diagram",
  "process model", "BPMN", "process documentation", "process redesign", or uploads a document
  described as an SOP, procedure, process description, or workflow. Also triggers on
  "draw the flow", "capture the steps", "who does what", "handoff between teams", or
  "model the workflow". Produces a Draw.io file plus a written process specification.
  Use after ba-workshop-facilitator post-session synthesis when the session output includes
  process narrative. Feeds ba-gap-analysis when AS-IS and TO-BE are both needed.
---

# BA Process Modeler

Converts process narrative into BPMN-notation Draw.io swimlane diagrams and written process
specifications. Handles AS-IS, TO-BE, and combined comparison models.

## Reference Files

Read both before processing any input:
- `references/bpmn-element-reference.md` — BPMN element definitions, Draw.io style mappings, and usage rules
- `references/drawio-swimlane-xml.md` — XML template library for swimlane containers, shapes, connectors, and gateways

---

## Input Handling

### Minimum Viable Input
A narrative description of a process: who does what, when, under what conditions, and what the
outcome is. Even a rough paragraph is sufficient to start.

### Optimal Input
| Input | Effect |
|-------|--------|
| Stakeholder roles or system names | Defines swimlane labels |
| Model type tag | AS-IS / TO-BE / Both / Exception flows only |
| Workshop synthesis or SOP document | Richer source; more accurate step capture |
| Known pain points (from workshop or elicitation) | Annotated onto AS-IS model as hotspots |
| Automation targets | Flagged on TO-BE model as automation candidates |
| Existing process diagram (any format) | Used as baseline; improves, does not replace |

### Clarification Rule
If the process boundaries are unclear (where does it start and end?), ask one question:
> "What triggers this process to begin, and what outcome or event marks it as complete?"

Do not ask more than one clarifying question. Derive everything else from the input.

---

## Processing Steps

### Step 1 — Define Scope Boundaries
Establish:
- **Start event:** What triggers the process? (a request received, a time trigger, a system event)
- **End event(s):** What are the valid terminal states? (approved, rejected, escalated, completed)
- **Scope in / scope out:** What sub-processes are referenced but not modelled here?

### Step 2 — Extract Process Elements
Parse the input and identify each element type. Read `references/bpmn-element-reference.md` for
definitions.

| Element | How to Identify in Narrative |
|---------|------------------------------|
| Task | Action verb + noun ("submits the form", "reviews the request") |
| Gateway (XOR) | Conditional: "if", "when", "depending on", "either/or" |
| Gateway (AND) | Parallel: "at the same time", "simultaneously", "and also" |
| Gateway (OR) | Inclusive: "one or more of", "any combination" |
| Sub-process | Reference to another named process: "goes through the approval process" |
| Intermediate event | Something that happens mid-flow: "notification received", "timer expires" |
| Exception path | "if it fails", "if rejected", "escalation", "error handling" |

### Step 3 — Assign Swimlanes
One swimlane per distinct actor or system. Rules:
- Human roles: one lane per role (not per person)
- Systems: one lane per system that takes autonomous action (not just receives data)
- Do not create a lane for a system that is only a data store
- Label lanes with role title, not person name
- Maximum 6 lanes on a single diagram; split into sub-processes if exceeded

### Step 4 — Sequence and Connect
Order tasks in chronological flow. Connect with:
- Sequence flows (solid arrows) between tasks in the same pool
- Message flows (dashed arrows) between separate pools (organisations)
- Apply gateways at every decision point — never imply a decision with a branching arrow alone

### Step 5 — Flag Issues (AS-IS only)
On AS-IS models, annotate:
- Pain points raised in elicitation: red hotspot marker
- Manual handoffs that are candidates for automation: amber marker
- Steps with no clear owner: `[NO OWNER]` annotation
- Rework loops: label the loop with "rework condition"

### Step 6 — Apply TO-BE Improvements (if requested)
Apply standard process improvement patterns:
| Pattern | Apply when |
|---------|-----------|
| Eliminate | Step adds no value; output not used downstream |
| Automate | Step is rule-based, repetitive, and system-executable |
| Consolidate | Two or more sequential steps by the same actor with the same object |
| Reorder | A step blocks flow but could be done in parallel |
| Standardise | Ad-hoc step that varies by person; can be rule-governed |
| Self-service | Step done by staff that the initiating actor could do directly |

Label each improvement on the TO-BE with its pattern type.

### Step 7 — Write Process Specification
Produce a structured written narrative alongside the diagram. One row per task in sequence.

---

## Output Specification

### Output 1 — Draw.io Process Model
Filename: `{process_name}_{model_type}.drawio`
Location: `/mnt/user-data/outputs/`

Read `references/drawio-swimlane-xml.md` for exact XML structure.

**Layout rules:**
- Canvas width: 1800–2600px depending on step count
- Canvas height: 200px per swimlane + 100px padding top/bottom
- Flow direction: left to right
- Start event: left edge, centred vertically in triggering lane
- End event(s): right edge
- Gateways: diamond shape, label above the diamond (not inside)
- Gateway branches: label each outgoing arrow (Yes/No, Approved/Rejected, etc.)
- Hotspots (AS-IS pain points): red rounded rectangle annotation above the affected task

**Colour scheme:**
| Element | Fill | Border | Text |
|---------|------|--------|------|
| Start event | `#D5E8D4` | `#82B366` | `#000000` |
| End event | `#F8CECC` | `#B85450` | `#000000` |
| Task (human) | `#DAE8FC` | `#6C8EBF` | `#000000` |
| Task (system/automated) | `#E1D5E7` | `#9673A6` | `#000000` |
| Gateway | `#FFF2CC` | `#D6B656` | `#000000` |
| Sub-process marker | `#F5F5F5` | `#666666` | `#000000` |
| Hotspot annotation | `#FFE6CC` | `#D79B00` | `#000000` |
| Swimlane header | `#F5F5F5` | `#666666` | `#000000` (bold) |

If both AS-IS and TO-BE are requested, produce two separate diagram pages within the same
`.drawio` file, labelled "AS-IS" and "TO-BE" in the page tab.

### Output 2 — Word Process Specification
Filename: `{process_name}_process_spec.docx`
Location: `/mnt/user-data/outputs/`
Standard: Sentence case headings. Dense tables. No em dashes.

Sections:
1. Document control
2. Process overview: name, scope, trigger, end states, owner, version
3. Roles and systems involved: table — Name, Type (Human/System), Responsibilities
4. Process step register: one row per task

**Process step register columns:**
| Column | Content |
|--------|---------|
| Step ID | P-{NNN} sequential |
| Step Name | Short verb-noun label matching diagram |
| Swimlane / Actor | Who performs this step |
| Description | 2–3 sentences: what is done, how, with what input |
| Inputs | Data, documents, or trigger from previous step |
| Outputs | Data, documents, or trigger to next step |
| Business Rules | Conditions or constraints governing this step |
| Systems Used | System name if applicable |
| Pain Points (AS-IS) | Annotated issues if present |
| Improvement Pattern (TO-BE) | If applicable |

5. Exception and error paths: one sub-section per exception, describing trigger, handler, and resolution
6. Key metrics and SLAs: if provided in input (elapsed time, volume, frequency)
7. Open items: steps with no owner, unclear rules, or pending decisions

### Output 3 — Inline Summary (in conversation)
- Process name and model type(s) produced
- Step count, swimlane count, gateway count
- Number of pain points flagged (AS-IS)
- Number of improvement patterns applied (TO-BE)
- Any steps with no owner or unresolved exceptions

---

## Quality Gates

Before delivering any output:
- [ ] Every gateway has all outgoing arrows labelled
- [ ] Start event and at least one end event present on every diagram
- [ ] Every task is in exactly one swimlane
- [ ] No branching arrows without a gateway
- [ ] Every exception path terminates at an end event (no hanging paths)
- [ ] Process step register has the same steps as the diagram, in the same sequence
- [ ] Every pain point on the diagram is in the step register under its step

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| AS-IS model + pain points | `ba-gap-analysis` — current state baseline |
| TO-BE model + improvement patterns | `ba-gap-analysis` — future state target |
| Process step register | `ba-user-story-factory` — each step becomes a candidate user story |
| Business rules column | `ba-elicitation-synthesizer` — business rules become FR/CO items |
