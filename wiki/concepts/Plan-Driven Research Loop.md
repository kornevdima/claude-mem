---
type: concept
title: "Plan-Driven Research Loop"
created: 2026-07-08
updated: 2026-07-08
tags:
  - concept
  - agents
  - autoresearch
status: implemented
related:
  - "[[openmanus-repo]]"
  - "[[OpenManus]]"
  - "[[Research OpenManus for claude-mem]]"
sources:
  - "[[openmanus-repo]]"
---

# Plan-Driven Research Loop

Redesign of `/autoresearch` from a fixed 3-round loop into a resumable, question-driven loop. Five patterns adapted from OpenManus source (`app/flow/planning.py`, `app/agent/base.py`) (Source: [[openmanus-repo]]).

## The five patterns

| # | OpenManus original | claude-mem adaptation |
|---|---|---|
| 1 | PlanningTool: persisted plan, per-step statuses `[ ] [→] [✓] [!]` + notes | Plan artifact `wiki/questions/_plan Research [Topic].md` — a visible Obsidian note, resumable across sessions |
| 2 | Loop picks first non-completed step until none remain | Topic decomposed into research questions = plan steps; loop until all closed or budget hit |
| 3 | Step-typed executor routing (`[TYPE]` tag → agent) | One `research-subagent` per question, dispatched **in parallel batches (max 4)**; isolated context, main thread stays clean; shared files (index/log/hot/_index/plan) are caller-owned to prevent write races |
| 4 | `is_stuck()` duplicate detection → change-strategy prompt | Question yielding no new sources: retry once with a rewritten angle, then mark `[!]` blocked |
| 5 | `max_steps` hard budget + graceful termination report | Per-question search/fetch budgets in `program.md`; blocked steps flow into synthesis Open Questions |

## Key properties

- **Resumable**: an interrupted session leaves the plan artifact in place; next invocation detects it and offers resume.
- **Observable**: the user watches research progress live in Obsidian as checkboxes flip.
- **Bounded**: budgets are configuration (`program.md`), not prompt folklore.
- The plan artifact is deleted after the synthesis page absorbs it; `wiki/log.md` keeps the record.

## Status

Implemented in `skills/autoresearch/SKILL.md` v2 + `agents/research-subagent.md` (2026-07-08). Eval pass via skill-creator still pending.

## Connections

- [[openmanus-repo]] | [[Research OpenManus for claude-mem]] | [[Domain-Specific Agents]] (same composition principle) | [[Structured Handoff]] (subagent report shape)
