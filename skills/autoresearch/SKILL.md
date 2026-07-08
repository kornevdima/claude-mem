---
name: autoresearch
description: >
  Autonomous plan-driven research loop. Takes a topic, decomposes it into research
  questions in a persisted plan artifact, dispatches research subagents per question,
  synthesizes findings, and files everything into the wiki as structured pages.
  Resumable: an interrupted session leaves the plan in the vault and the next run
  continues it. Based on Karpathy's autoresearch pattern plus OpenManus PlanningFlow
  patterns: program.md configures objectives and budgets, statuses live in the plan note.
  Triggers on: "/autoresearch", "autoresearch", "research [topic]", "deep dive into [topic]",
  "investigate [topic]", "find everything about [topic]", "research and file",
  "go research", "build a wiki on", "resume research".
---

# autoresearch: Plan-Driven Research Loop

You are a research agent. You take a topic, decompose it into research questions, work through them via a persisted plan, and file everything into the wiki. The user gets wiki pages, not a chat response.

Design rationale: `wiki/concepts/Plan-Driven Research Loop.md`. v1 (fixed 3-round loop) was replaced 2026-07-08.

---

## Before Starting

1. Read `references/program.md` for objectives, confidence scoring, and budgets. User-configurable.
2. Check `wiki/questions/` for an existing `_plan Research *.md` matching the topic (or any plan with open steps if the user said "resume research"). If found: show its status and ask **resume or restart**. Resume = continue from the first non-completed question.

---

## Step 1. Plan

Decompose the topic into **3-7 research questions** (budget: `max_questions` in program.md). Good questions are answerable independently and collectively cover the topic.

Write the plan artifact to `wiki/questions/_plan Research [Topic].md`:

```markdown
---
type: research-plan
title: "Plan: Research [Topic]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [research, plan]
status: active
---

# Plan: Research [Topic]

Statuses: `[ ]` not started | `[→]` in progress | `[✓]` done | `[!]` blocked

- [ ] Q1: [question]
- [ ] Q2: [question]
- [ ] Q3: [question]

## Notes
<!-- one line per completed/blocked question: what was found or why blocked -->
```

The plan is live in Obsidian — the user watches statuses flip as research progresses.

---

## Step 2. Execute (loop)

While open questions (`[ ]` or `[→]`) remain AND budgets allow:

1. Take **all currently open** `[ ]` questions that are independent of each other (research questions from Step 1 almost always are — a question only waits if its wording depends on another's answer). Mark each `[→]` in the plan (update `updated:` too).
2. **Dispatch one `research-subagent` per question in parallel** — a single turn with multiple Agent calls (`subagent_type: "research-subagent"`), max 4 concurrent; if more questions remain open, run further batches. Each dispatch carries: the question, the topic, vault path, the budgets + source rules from program.md, **and an explicit per-question page cap**. The subagent searches, fetches, files source/entity/concept pages, and returns a structured report. Parallel dispatch is why the loop is fast: questions are independent, so their wall-time overlaps; context stays isolated per question either way.
   - **Budget partitioning (required for parallel dispatch)**: parallel subagents can't see each other's page counts, so the session budget must be split *before* dispatch: per-question page cap = `floor(remaining content-page budget ÷ open questions)`, minimum 2. Count pages created after each batch and recompute before the next. A subagent that hits its cap reports the overflow as gaps instead of filing more pages — the synthesis carries them as Open Questions.
   - **Write-contention rule**: parallel subagents create pages but must NOT touch shared files — `wiki/index.md`, `wiki/log.md`, `wiki/hot.md`, `_index.md` files, and the plan artifact stay caller-owned (subagents already know this; it's what prevents write races).
   - Exception: if the plan has ≤2 questions, do the work inline (same procedure as the subagent) — dispatch overhead isn't justified.
3. On each report:
   - **New sources found** → mark `[✓]`, append a one-line note (key finding + pages created).
   - **No new sources** → rewrite the question from a different angle and re-dispatch once (these retries can join the next batch). A second empty pass → mark `[!]` blocked with a note. Never spend more than 2 passes on one question.
   - If two parallel subagents created near-duplicate pages (same entity/concept), merge them before synthesis.
4. Re-read the plan before each batch (statuses are the single source of truth — this is what makes the loop resumable).

Stop when: all questions are `[✓]`/`[!]`, or `max_pages` / per-question budgets are exhausted. On budget stop: mark remaining questions `[!]` with note "budget".

---

## Step 3. Synthesize

Create `wiki/questions/Research [Topic].md` (no colon in filename):

```markdown
---
type: synthesis
title: "Research: [Topic]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - research
  - [topic-tag]
status: developing
related:
  - "[[Every page created in this session]]"
sources:
  - "[[wiki/sources/Source 1]]"
  - "[[wiki/sources/Source 2]]"
---

# Research: [Topic]

## Overview
[2-3 sentence summary]

## Key Findings
- Finding 1 (Source: [[Source Page]])

## Key Entities
- [[Entity Name]]: role/significance

## Key Concepts
- [[Concept Name]]: one-line definition

## Contradictions
- [[Source A]] says X. [[Source B]] says Y. [Which is more credible and why]

## Open Questions
- [Every [!] blocked question from the plan, with its blocking note]
- [Anything skipped for budget]

## Sources
- [[Source 1]]: author, date
```

Blocked (`[!]`) plan steps map 1:1 into Open Questions — nothing is silently dropped.

---

## Step 4. File and Close

1. Update `wiki/index.md`: add all new pages to the right sections, bump counts and date.
2. Update `wiki/sources/_index.md`, `wiki/concepts/_index.md`, `wiki/entities/_index.md` (where the vault has them) for every page the subagents created — subagents deliberately don't touch shared index files.
3. Append to `wiki/log.md` (at the TOP):
   ```
   ## [YYYY-MM-DD] autoresearch | [Topic]
   - Questions: N total, N answered, N blocked
   - Sources found: N | Pages created: [[Page 1]], [[Page 2]], ...
   - Synthesis: [[Research [Topic]]]
   - Key finding: [one sentence]
   ```
4. Update `wiki/hot.md` with the research summary.
5. **Delete the plan artifact** — the synthesis page and log entry carry its content. (A surviving `_plan` file = interrupted session = resume marker.)

---

## Report to User

```
Research complete: [Topic]

Questions: N answered, N blocked | Searches: N | Pages created: N

Created:
  wiki/questions/Research [Topic].md (synthesis)
  wiki/sources/... wiki/concepts/... wiki/entities/...

Key findings:
- [Finding 1]
- [Finding 2]

Open questions filed: N
```

---

## Constraints

All budgets live in `references/program.md`:
- Max questions per plan (default: 7)
- Max searches / fetches per question (defaults: 5 / 3)
- Max wiki pages per session (default: 15)
- Max passes per question: 2 (hard rule, then `[!]`)
- Confidence scoring and source preference rules

If a constraint conflicts with completeness, respect the constraint and file the gap in Open Questions.
