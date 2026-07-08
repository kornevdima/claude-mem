---
type: concept
title: "Vertical Slices for Agent Tasks"
complexity: basic
domain: ai-agents
aliases:
  - "Tracer Bullets"
  - "Vertical Slicing"
created: 2026-07-03
updated: 2026-07-03
tags:
  - concept
  - agent-workflow
  - planning
  - task-decomposition
status: current
related:
  - "[[yt-pocock-ai-coding-workflow]]"
  - "[[Ralph Wiggum Loop]]"
  - "[[Deep Modules]]"
sources:
  - "[[yt-pocock-ai-coding-workflow]]"
---

# Vertical Slices for Agent Tasks

Decompose a PRD into **independently grabbable issues that each cut through every layer of the system** (schema → service → API → minimal UI), rather than layer-by-layer phases. The idea is the Pragmatic Programmer's *tracer bullets*: fire something that glows all the way to the target so you get feedback on your aim immediately. (Source: [[yt-pocock-ai-coding-workflow]])

## The failure mode it fixes

**AI loves to code horizontally** — phase 1 all the database work, phase 2 all the API, phase 3 the frontend. Nothing is integration-testable until phase 3; the agent "codes blind" until the end. Left alone, PRD-splitting agents will propose horizontal slices (e.g., "create the gamification service" alone), and the human must reject them: a good first slice is "award points for lesson completion, visible on the dashboard" — schema + service + minimal frontend, something reviewable at the end.

## Kanban DAG, not a sequential plan

Slices are filed as issues with **blocking relationships**, forming a directed acyclic graph:

- A **sequential multi-phase plan can only be executed by one agent**; a DAG of independently grabbable issues can be worked by parallel agents (each unblocked issue is claimable).
- Issues carry a **HITL vs AFK tag** — which ones an unattended loop may pick up.
- Manual QA feeds **new issues back onto the board** while implementation continues; the board absorbs mess (bugs arriving mid-flight) that a linear plan cannot.
- Reviewing the proposed split is cheap and high-leverage — this is a human checkpoint.

## Relation to claude-mem

The ba-suite user-story-factory already builds story dependency maps; this concept adds the *quality criterion* (each story must be a tracer bullet through all layers, ending in something observable) and the *execution consequence* (DAG enables parallel feature-builders; horizontal stories serialize them and starve feedback loops).

## Connections

- [[Ralph Wiggum Loop]] — the consumer of the issue backlog
- [[Deep Modules]] — the architecture that makes slices cheap to test
- [[yt-pocock-ai-coding-workflow]] — source, incl. the PRD-to-issues skill
