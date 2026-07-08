---
type: source
title: "Full Walkthrough: Workflow for AI Coding (Matt Pocock)"
source_type: video-transcript
author: "Matt Pocock"
publisher: "AI Engineer conference (workshop)"
published: 2026-04-24
url: https://youtu.be/-QFHIoCo-Ko
raw_file: ".raw/yt-pocock-ai-coding-workflow.md"
ingested: 2026-07-03
tags:
  - source
  - transcript
  - ai-coding
  - agent-workflow
  - context-engineering
status: current
related:
  - "[[Matt Pocock]]"
  - "[[Grilling Session]]"
  - "[[Ralph Wiggum Loop]]"
  - "[[Vertical Slices for Agent Tasks]]"
  - "[[Deep Modules]]"
  - "[[Context Rot]]"
  - "[[Context Engineering for Coding Agents]]"
---

# Full Walkthrough: Workflow for AI Coding (Matt Pocock)

~1h36m live workshop. Thesis: AI coding is not a new paradigm that invalidates software engineering — the fundamentals (Brooks, Fowler, Pragmatic Programmer, Ousterhout) are exactly what makes agents work. Pocock demos an end-to-end workflow: idea → grilling → PRD → Kanban of vertical-slice issues → AFK agent loop → TDD + feedback loops → fresh-context review → manual QA.

## The two LLM constraints the workflow is built on

1. **Smart zone / dumb zone** (idea credited to Dex Horthy, HumanLayer). Attention relationships scale quadratically with tokens; around **~100K tokens the model gets dumber**, regardless of whether the window is 200K or 1M. "They shipped a lot more dumb zone to you" — 1M context is good for retrieval, not for coding. Size every task to fit the smart zone. See [[Context Rot]].
2. **LLMs are "the guy from Memento"** — they reset. Pocock prefers `clear` over compaction: clearing returns to a deterministic base state; compaction accumulates "sediment". He also keeps the always-in-context layer (system prompt, CLAUDE.md) tiny, and runs a **token-count status line** in every session ("essential information on every coding session").

## Workflow stages

| Stage | Artifact / mechanism | Human-in-the-loop? |
|---|---|---|
| 1. Idea | Client brief (e.g., Slack message) | yes |
| 2. [[Grilling Session]] | `grill me` skill — relentless one-question-at-a-time interview with recommended answers, until shared understanding ("design concept", Brooks). 40–100 questions is normal. Starts with an explore **subagent** (~94K tokens on Opus, isolated context). | yes — must be |
| 3. PRD | `write a PRD` skill — the **destination document**: problem, solution, user stories, implementation + testing decisions, proposed modules to modify, out-of-scope section (retains negative decisions, gives definition of done). He does **not review the PRD** — once aligned, it only tests the LLM's summarization, which is reliably good. | reviewed lightly |
| 4. Kanban of issues | `PRD to issues` skill — break PRD into **independently grabbable issues** as [[Vertical Slices for Agent Tasks]], with blocking relationships (a DAG, so agents can parallelize). Each tagged human-in-the-loop or AFK. Human reviews the split — cheap to do, and AI defaults to horizontal slicing. | yes — cheap, high value |
| 5. Implementation | [[Ralph Wiggum Loop]] — bash script cats all issue files + last 5 commits + prompt into the agent (accept-edits, Docker sandbox). Run the single-iteration `once.sh` repeatedly first to tune the prompt, then go AFK. Parallel version: his **Sandcastle** library (planner → sandboxed implementers per issue → merger agent). | no — AFK ("night shift") |
| 6. TDD + feedback loops | Red-green-refactor skill: failing test first, so the agent can't "cheat at the tests". "The quality of your feedback loops is the ceiling on how good your AI can code." | no |
| 7. Automated review | **Clear context, then review** — reviewing in the same session means reviewing in the dumb zone. Coding standards are **pushed** to the reviewer, **pull** (skills) for the implementer. Sonnet implements, Opus reviews. | no |
| 8. Manual QA | Where the human "imposes taste". QA's output is **more issues onto the Kanban board** while implementation continues. Full automation of idea/QA/research/prototype ⇒ "slop". | yes |
| 9. Team review / merge | Ordinary PR flow; up-to-PRD assets are the team-collaboration surface (RFC-style loops). | yes |

## Codebase architecture as agent enablement

- **"Bad codebases make bad agents."** Garbage in, garbage out at the repo level.
- [[Deep Modules]] (Ousterhout): small interface, lots of functionality, one big test boundary. AI left unsupervised produces shallow-module codebases that are hard to navigate and hard to test.
- The PRD names the modules to create/modify and keeps that **module map in mind through planning and implementation**.
- "Design the interface, delegate the implementation" — modules become gray boxes; you keep the mental model of the codebase without reviewing every line.
- `improve codebase architecture` skill: scans the repo for module-deepening candidates (coupled clusters testable as a unit, dependency substitutability, test gaps). "If you take one thing away from today, run this skill on your repo."

## Strong claims and tips

- **Against specs-to-code**: editing only specs and ignoring code "is vibe coding by another name... the code is your battleground."
- **Doc rot**: delete or close PRDs/plans once implemented. A stale PRD found later by an agent misleads it — names, structure, even requirements have changed. He closes them as GitHub issues (fetchable, but visually done).
- **Don't over-optimize the PRD.** Alignment (grilling) is where the value is; QA is where the effort belongs.
- **Own your planning stack** (vs Spec Kit / OpenSpec / Taskmaster): with no clear winner yet, you need observability and control over the whole thing — inversion of control.
- **Old books are prompt gold**: 20-year-old software books already verbalize best practices in English — ideal prompt material (tracer bullets, deep modules, design concept).
- **Frontend**: agents can't judge visuals; generate ~3 throwaway prototypes on a throwaway route, human picks, feed the winner back into the grilling session.
- **HITL vs AFK task taxonomy**: planning/alignment must be human-in-the-loop (multiple humans — pair/mob with AI and the domain expert); implementation can be AFK. "Day shift" (human planning) queues work for the "night shift" (agents).
- **More code review is the price**: delegating implementation means more review, not less; no good answer yet for keeping PRs small under multi-issue loops.

> [!contradiction] Contradicts [[Compounding Knowledge]] on keeping planning docs
> Pocock deletes/closes PRDs after implementation to avoid doc rot misleading future agents. The wiki thesis is that persistent docs compound in value. Resolution candidate: both hold — *stale point-in-time plans* rot, while *maintained as-built knowledge* compounds; claude-mem's wrap-up/document-as-built rule is the mechanism that separates the two. See callout on [[Compounding Knowledge]].

## Connections

- [[Grilling Session]], [[Ralph Wiggum Loop]], [[Vertical Slices for Agent Tasks]], [[Deep Modules]] — concepts extracted from this talk
- [[Context Rot]] — smart/dumb zone is the practitioner framing of the same phenomenon
- [[Context Engineering for Coding Agents]] — this talk is a full practitioner instantiation
- [[Generator-Evaluator Pattern]] — his fresh-context reviewer with pushed standards is the same trust boundary
- [[Spec-Kit and claude-mem]] — his "own your stack" stance on Spec Kit et al.
