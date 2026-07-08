---
type: concept
title: "Deep Modules"
complexity: basic
domain: software-design
aliases:
  - "Deep vs Shallow Modules"
  - "Module Depth"
created: 2026-07-03
updated: 2026-07-03
tags:
  - concept
  - software-design
  - testability
  - agent-enablement
status: current
related:
  - "[[yt-pocock-ai-coding-workflow]]"
  - "[[Vertical Slices for Agent Tasks]]"
  - "[[Context Engineering for Coding Agents]]"
sources:
  - "[[yt-pocock-ai-coding-workflow]]"
---

# Deep Modules

John Ousterhout's ideal (*A Philosophy of Software Design*): a module with a **small, simple interface hiding a lot of functionality**. The opposite — shallow modules, many small files each exporting a little — creates a dependency web that is hard to navigate and hard to draw test boundaries around. [[Matt Pocock]] repurposes this as an **AI-agent enablement principle**: "bad codebases make bad agents." (Source: [[yt-pocock-ai-coding-workflow]])

## Why depth matters for agents

- **Navigation**: shallow-module webs force the agent to trace the whole dependency graph to understand anything.
- **Testability = feedback loops**: a deep module gets one big test boundary that catches a lot; shallow modules force per-function tests with mocks, which is exactly the "bad tests" agents produce when they wrap every tiny function in its own boundary. Since *feedback-loop quality is the ceiling on agent output quality*, deep modules directly raise what agents can do. Pocock's extreme example: wrapping an entire browser video editor front-to-back in one externally-testable module made agent changes "night and day".
- **Unsupervised AI produces shallow codebases.** Left alone, agents code in thin layers and fragments; module shape must be directed by the human.

## Practices from the talk

- The **PRD names the modules** to create or modify ("gamification service is a new deep module, tested around, with this interface") and the module map is held in mind through planning and implementation.
- **Design the interface, delegate the implementation**: modules become gray boxes — you know their shape and behavior, agents own the internals. This preserves the developer's mental model of the codebase while moving fast, and bounds what needs line-by-line review.
- An **`improve codebase architecture` skill** scans the repo for module-deepening candidates: coupled clusters that could be tested as a unit, dependency substitutability (e.g., in-memory test DB), and test-coverage gaps.

## Relation to claude-mem

Mode B code wikis document modules and flows; this adds an evaluative lens: module *depth* (interface size vs functionality, test-boundary placement) is a property worth recording and linting, because it predicts agent performance in that service. A deepening-candidates scan is a natural architecture-subagent or wiki-lint extension.

## Connections

- [[yt-pocock-ai-coding-workflow]] — source
- [[Vertical Slices for Agent Tasks]] — slices cross module boundaries; deep modules make each crossing testable
- [[Context Engineering for Coding Agents]] — codebase shape as a context/feedback concern, not just docs
