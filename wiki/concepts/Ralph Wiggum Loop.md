---
type: concept
title: "Ralph Wiggum Loop"
complexity: intermediate
domain: ai-agents
aliases:
  - "Ralph Loop"
  - "AFK Agent Loop"
created: 2026-07-03
updated: 2026-07-03
tags:
  - concept
  - agent-workflow
  - automation
  - loops
status: current
related:
  - "[[yt-pocock-ai-coding-workflow]]"
  - "[[Vertical Slices for Agent Tasks]]"
  - "[[Matt Pocock]]"
  - "[[Context Rot]]"
sources:
  - "[[yt-pocock-ai-coding-workflow]]"
---

# Ralph Wiggum Loop

An AFK ("away from keyboard") implementation pattern: instead of a numbered multi-phase plan, specify only the **destination** (a PRD / backlog of issues) and run a fresh-context agent in a loop, each iteration making one small change that gets closer to it. "Any developer worth their salt will look at a multi-phase plan and go: this is a loop. Why don't we just have phase N?" (Source: [[yt-pocock-ai-coding-workflow]])

## Anatomy (Pocock's version)

Each iteration is a **fresh context** (the Memento property — deterministic base state, no compaction sediment):

1. A bash script `cat`s **all backlog issue files** + the **last 5 commits** + the loop prompt into the agent (accept-edits permission mode).
2. Runs inside a **Docker sandbox** (worktree per run in the parallel version).
3. The prompt encodes task selection priority: critical bug fixes → development infrastructure → tracer bullets → polish/quick wins/refactors. If no AFK tasks remain, output a sentinel ("no more tasks") that ends the loop.
4. The task itself: explore repo → TDD (red-green-refactor) → run feedback loops (tests, typecheck) → commit with a summary.

## Operational discipline

- **Run `once.sh` first** — the single-iteration human-observed version — repeatedly, to watch the agent's behavior and tune the prompt *before* going AFK. Only then run the unattended loop.
- Only **AFK-tagged** tasks are eligible; planning/alignment tasks stay human-in-the-loop. Day shift (human planning) queues work for the night shift (agents).
- Parallelization: because issues form a DAG of blocking relationships (see [[Vertical Slices for Agent Tasks]]), multiple loops can run at once. Pocock's **Sandcastle** TypeScript library does this: a *planner* agent picks parallelizable issues, each gets a git worktree + Docker sandbox + implementer, then a *merger* agent merges branches and fixes type/test fallout. Sonnet implements; Opus reviews/merges.

## Failure modes

- Ralph "works okay" bare; it needs structure (curated backlog, priorities, feedback loops) to beat naive keep-going-and-compact, which degrades as sediment accumulates in context.
- The loop's ceiling is the repo's feedback loops: no tests/typecheck ⇒ the agent codes blind.

## Relation to claude-mem

The ADLC build step (feature-builder → feature-tester → feature-reviewer → feature-verifier per feature) is a structured single pass, not a loop over a self-selecting backlog. The Ralph pattern suggests: sentinel-terminated iteration over `wiki/user-stories/` as a backlog, fresh context per story, priority rules in the prompt.

## Connections

- [[yt-pocock-ai-coding-workflow]] — source walkthrough, incl. once.sh and Sandcastle
- [[Context Rot]] — why fresh context per iteration beats compaction
- [[Generator-Evaluator Pattern]] — the separate reviewer/merger agents are the evaluator side
