---
name: ba-workshop-facilitator
description: >
  Designs and delivers full facilitation packages for BA discovery and requirements
  workshops: timed agenda, facilitation script, participant pre-read, canvas templates,
  and a post-workshop synthesis template. Covers workshop types including Discovery,
  Requirements, Prioritisation, Design Sprint, Process Mapping, and Retrospective.
  Trigger this skill whenever the user says "plan a workshop", "I need to run a workshop",
  "help me facilitate a session", "workshop agenda", "workshop design", "I am running a
  discovery session", "facilitation guide", "how do I run a requirements session", or
  mentions a specific workshop type. Also triggers on "I have a session with stakeholders
  next week", "we need to define requirements together", or "help me structure a working
  group". Do not use for Scrum events (Sprint Planning, Daily Scrum, Sprint Review,
  Sprint Retrospective): those belong to ba-scrum-events-pack.
---

# BA Workshop Facilitator

Produces a complete, run-ready facilitation package for a BA-led workshop. Covers pre-session
design, in-session facilitation script, and post-session synthesis.

## Reference Files

Read both before processing any input:
- `references/facilitation-frameworks.md` — framework selection by workshop type, with activity designs, time allocations, and facilitation tips
- `references/canvas-templates.md` — reusable canvas templates in text/table form for the most common workshop canvases

---

## Input Handling

### Minimum Viable Input
One of:
- Workshop objective (what must be decided or produced by the end)
- Workshop type tag (Discovery / Requirements / Prioritisation / Process Mapping / Design Sprint / Retrospective)

### Optimal Input
| Input | Effect |
|-------|--------|
| Stakeholder list or Skill 2 output | Tailors facilitation tone, pre-read, and opening framing |
| Duration | Time-boxes all activities |
| Participant count | Shapes group exercise design (pairs, small groups, plenary) |
| Known tensions or conflicts | Pre-empts difficult moments in the facilitation script |
| Deliverable required at output | Ensures the agenda is structured to produce it |
| In-person or virtual | Adjusts tool suggestions and logistics notes |

### Clarification Rule
If both objective and type are absent, ask:
> "What is the one thing participants must leave this session having decided, agreed, or produced?"

If duration is not provided, assume 2 hours and state the assumption inline.

---

## Processing Steps

### Step 1 — Select Framework
Read `references/facilitation-frameworks.md`. Match the workshop type to the recommended framework.
If the type is unclear, derive it from the objective statement using this logic:

| Objective contains | → Workshop type |
|--------------------|----------------|
| "understand", "explore", "learn about", "define the problem" | Discovery |
| "capture requirements", "define what we need", "agree scope" | Requirements |
| "rank", "vote", "decide what to build first", "roadmap" | Prioritisation |
| "map the process", "how does it work today", "current state" | Process Mapping |
| "how might we", "design", "prototype", "ideate" | Design Sprint |
| "what went well", "improve the team", "lessons learned" | Retrospective |

### Step 2 — Design the Agenda
Time-box each activity against the available duration. Structure must follow this pattern:
1. **Opening** (10% of time): Purpose statement, ground rules, warm-up
2. **Context setting** (10–15%): Shared understanding of the problem or goal
3. **Core activity** (50–60%): The primary framework activity that produces the deliverable
4. **Synthesis** (15–20%): Grouping, prioritising, or agreeing on outputs in the room
5. **Close** (10%): Decisions log, actions, parking lot, next steps

If duration is under 60 minutes, collapse Context and Core. Never remove Opening or Close.

### Step 3 — Write the Facilitation Script
For each agenda item, write:
- **Facilitator says (verbatim opening):** The exact sentence to open the activity
- **What to listen for:** Key signals that the activity is working (or breaking down)
- **If stuck:** Prompt to use if the room goes quiet or goes off track
- **Transition phrase:** The sentence to close this activity and introduce the next

Script tone: direct, calm, time-aware. No filler phrases ("Great!", "Awesome!").

### Step 4 — Write the Participant Pre-Read
A single page (max 400 words). Sections:
1. Why we are meeting (context, not history)
2. What we need from you (specific preparation, if any)
3. What we will produce together (the output, in plain terms)
4. Logistics (time, location/link, format)

Tone: clear, human, no jargon. Write for the end user archetype as the least-informed participant.

### Step 5 — Prepare Canvas(es)
Read `references/canvas-templates.md`. Select the canvas(es) appropriate to the framework chosen.
Reproduce the canvas structure in a table format suitable for inclusion in the Word output and for
printing or sharing as a Miro/Mural/whiteboard template.

### Step 6 — Build Post-Workshop Synthesis Template
Produce a pre-structured template (not completed content) for synthesis after the session:
- Decisions log: table with Decision, Owner, Date, Next Review
- Action items: table with Action, Owner, Due Date, Status
- Parking lot: table with Item, Who Raised It, How to Resolve, Owner
- Key insights from the session (free text field with prompt)
- Next steps: numbered list with placeholder rows
- Open questions not resolved in the session

### Step 7 — Post-Session Synthesis Export (complete after the session)
When the facilitator has run the session and filled in the synthesis template, produce a
**Synthesis Export Note** structured specifically for consumption by `ba-elicitation-synthesizer`.
This export is a one-page structured document (not a free-text debrief) with the following
fixed sections:

**Section A: Raw statements**
One row per discrete statement made in the session. Format each row as:
`[Speaker Role] | [Statement verbatim or close paraphrase] | [Context: activity name]`
Include all statements, not just those the facilitator judged as requirements. The synthesizer
classifies them — the facilitator records them.

**Section B: Decisions**
Each decision on its own line: `DECIDED: [what was agreed] — [who agreed] — [date]`
Decisions carry CO (Constraint) or AS (Assumption) weight in downstream classification.

**Section C: Parking lot items**
Each item on its own line: `PARKED: [item] — [who raised] — [resolution path if known]`
Parking lot items are classified as OQ (Open Question) or RI (Risk Indicator) downstream.

**Section D: Corroboration flags**
Where the same theme or requirement was raised by two or more participants independently,
flag it: `CORROBORATED: [theme] — [Speaker 1], [Speaker 2]`
The synthesizer will mark these items `[Corroborated]` and weight them as higher MoSCoW priority.

**Section E: Synthesis export header**
A five-field header required by `ba-elicitation-synthesizer` for session-type processing:
- Session type: Discovery / Requirements / Prioritisation / Process Mapping / Design Sprint / Retrospective
- Participant count: [N]
- Duration: [N hours]
- Facilitator: [Name]
- Project prefix: [PREFIX] (for ID assignment)

Filename for the export note: `{workshop_type}_{date}_synthesis_export.docx`
This file is distinct from the facilitator guide. It is the formal handoff artefact.

---

## Output Specification

### Output 1 — Word Facilitator Guide
Filename: `{workshop_type}_{date}_facilitator_guide.docx`
Location: `/mnt/user-data/outputs/`
Standard: Sentence case headings. No em dashes. Dense and functional — this is a working document.

Sections:
1. Session overview: objective, type, duration, participant list, format, facilitator name
2. Materials checklist: what to prepare before the session
3. Timed agenda: table (Time | Activity | Duration | Facilitator notes)
4. Facilitation script: one sub-section per agenda item with verbatim opens, prompts, transitions
5. Canvas templates: reproduced in table format for printing or screen sharing
6. Ground rules (standard set — editable)
7. Post-workshop synthesis template

### Output 2 — PowerPoint Workshop Deck
Filename: `{workshop_type}_{date}_workshop_deck.pptx`
Location: `/mnt/user-data/outputs/`

Slides:
1. Title: Workshop name, date, facilitator
2. Agenda: timed list
3. Why we are here: 3-sentence context (from pre-read)
4. Ground rules
5. Activity slide(s): one per core activity, with the canvas or exercise instructions
6. Synthesis slide: "What did we agree?" — blank decision log table
7. Parking lot slide: blank table
8. Next steps slide: blank action table
9. Thank you + contact

### Output 3 — Participant Pre-Read (Word, 1 page)
Filename: `{workshop_type}_{date}_pre_read.docx`
Location: `/mnt/user-data/outputs/`

### Output 4 — Post-Session Synthesis Export (Word, 1 page)
Filename: `{workshop_type}_{date}_synthesis_export.docx`
Location: `/mnt/user-data/outputs/`
Produced after the session. Contains Sections A through E as defined in Step 7.
This file is the formal input to `ba-elicitation-synthesizer`.

### Output 5 — Inline Summary (in conversation)
Immediately after file links:
- Workshop type confirmed, framework selected
- Duration covered, activity count
- Key risk or facilitation challenge to prepare for (one sentence)
- One thing the facilitator must resolve before the session (if anything critical is missing)

---

## Ground Rules — Standard Set

Include in every facilitator guide and workshop deck unless overridden:
1. One conversation at a time.
2. Phones away during activities. Breaks for everything else.
3. No idea is wrong in this room — challenge the idea, not the person.
4. Speak from your own experience.
5. The facilitator manages time. Trust the process.
6. Parking lot is real — it will be addressed, just not right now.

---

## Quality Gates

Before delivering any output:
- [ ] Agenda activities sum to the stated duration (allow ±5 minutes)
- [ ] Every agenda item has a transition phrase in the script
- [ ] The canvas selected matches the framework and produces the stated deliverable
- [ ] Pre-read is under 400 words and contains no internal jargon
- [ ] Post-workshop synthesis template has all four sections (Decisions / Actions / Parking Lot / Open Questions)
- [ ] If stakeholder analysis was provided, concern narratives from at-risk stakeholders are reflected in the facilitation script ("watch for resistance from X around topic Y")
- [ ] Synthesis export note (when produced post-session) contains all five sections: Raw Statements, Decisions, Parking Lot, Corroboration Flags, Export Header
- [ ] Every Raw Statement in the export has a speaker role tag and an activity context tag
- [ ] Export header contains a valid project prefix for ID assignment

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| Synthesis export note (`_synthesis_export.docx`) | `ba-elicitation-synthesizer` — the structured export format is the required handoff; raw synthesis template is not sufficient |
| Decisions log | All downstream skills — decisions constrain scope and requirements |
| Action items | Project or Scrum team — integrate into backlog or task tracker |
| Corroboration flags | `ba-elicitation-synthesizer` — items tagged CORROBORATED receive elevated MoSCoW weighting |
