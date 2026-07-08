---
type: concept
title: "Grilling Session"
complexity: basic
domain: ai-agents
aliases:
  - "Grill Me skill"
  - "Alignment Interview"
created: 2026-07-03
updated: 2026-07-03
tags:
  - concept
  - agent-workflow
  - planning
  - elicitation
status: current
related:
  - "[[yt-pocock-ai-coding-workflow]]"
  - "[[Matt Pocock]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Vertical Slices for Agent Tasks]]"
sources:
  - "[[yt-pocock-ai-coding-workflow]]"
---

# Grilling Session

An alignment-first planning technique: before any plan or spec is written, the agent **interviews the human relentlessly** — one question at a time, each with the agent's recommended answer — until human and agent reach a shared understanding. Coined as the "grill me" skill by [[Matt Pocock]] (Source: [[yt-pocock-ai-coding-workflow]]).

The core skill prompt is tiny: *"Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the decision tree resolving dependencies one by one. For each question provide your recommended answer. Ask the questions one at a time."*

## Why it exists

- Plan mode's failure mode is **eagerness**: the agent produces a plan the moment it thinks it has enough. What's needed first is not an asset but a shared **design concept** (Frederick Brooks, *The Design of Design*) — being "on the same wavelength" as the agent.
- It surfaces questions neither the client nor the developer considered (e.g., "should points be retroactive over existing progress records?").
- The recommendations are usually good, so answering is fast — often "go with your recommendation."
- The resulting conversation history *is* the asset; the PRD afterwards merely summarizes it, which is why Pocock doesn't proofread the PRD.

## Mechanics

- Starts with an **explore subagent** (isolated context, ~90K+ tokens burned without polluting the main session) so questions are grounded in the actual codebase.
- Sessions run long: 40–100 questions is normal — an hour of chatting.
- Must be **human-in-the-loop**; it is the one stage that cannot be Ralph-looped. Crucial decisions want *more* humans: pair/mob programming with the domain expert and the AI in the same room.
- Feed **meeting transcripts** with domain experts into a grilling session to validate assumptions from the outside world.
- Tunable: if the agent hammers too hard, edit the skill (stop points, pull back).

## Relation to claude-mem

The ADLC ingest pipeline synthesizes requirements from `.raw/` sources non-interactively (ba-suite elicitation). A grilling pass is the interactive complement: it converts *unknown unknowns* into decisions before requirements are frozen. The ba-suite elicitation-synthesizer produces an open-questions list; a grilling session is a mechanism to burn that list down with the human.

## Connections

- [[yt-pocock-ai-coding-workflow]] — full workflow context
- [[Context Engineering for Coding Agents]] — the explore-subagent isolation is standard sub-agent context hygiene
