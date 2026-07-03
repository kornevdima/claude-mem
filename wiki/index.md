---
type: meta
title: "Wiki Index"
updated: 2026-07-03
tags:
  - meta
  - index
status: evergreen
related:
  - "[[overview]]"
  - "[[log]]"
  - "[[hot]]"
  - "[[concepts/_index]]"
  - "[[entities/_index]]"
  - "[[sources/_index]]"
  - "[[LLM Wiki Pattern]]"
  - "[[Hot Cache]]"
  - "[[Compounding Knowledge]]"
  - "[[Andrej Karpathy]]"
  - "[[Project Profile]]"
  - "[[AGENTS.md]]"
---

# Wiki Index

Last updated: 2026-07-03 | Total pages: 80 | Source pages: 23

Navigation: [[overview]] | [[log]] | [[hot]] | [[maintenance-triggers]]

---

## Concepts

- [[Context Engineering for Coding Agents]] — discipline of curating optimal tokens for LLM coding agents; hybrid upfront-plus-JIT model (status: developing)
- [[AGENTS.md]] — cross-vendor convention for in-repo agent context; 60K+ projects, Linux Foundation steward (status: current)
- [[Repo Map]] — Aider's tree-sitter + PageRank pattern for compressed structural codebase summaries (status: current)
- [[Contextual Retrieval]] — Anthropic's RAG technique that prepends generated context to chunks; 35-67% failure-rate reduction (status: current)
- [[Project Profile]] — claude-mem design for a calibration artifact informed by 2026-05-09 research (status: developing)
- [[Rule Generation from Chat]] — pattern of converting validated chat into persistent rules; pioneered by Cursor (status: developing)
- [[Generator-Evaluator Pattern]] — trust-boundary architecture: split agent that produces from agent that judges (status: current)
- [[Feedback Loop for Project Profile]] — design synthesis for the feedback half of /project-profile (status: developing)
- [[Project Profile Skill Suite]] — end-to-end design: 5 skills + 3 subagents + 1 hook; implementation sequence (status: developing)
- [[Product Management Layer Skill]] — "Gate 0" governance skill above shift-left: intake/approval registry, vendor lifecycle, buy-vs-build, compliance scoping, shelfware (status: implemented)
- [[maintenance-triggers]] — when to run which skill/command; the answer to "what should I update?" (status: current)
- [[graphify-integration]] — design of the structural code-graph layer; option C, Jaccard preservation, labels.json gotcha (status: current)
- [[LLM Wiki Pattern]] — the pattern for building persistent, compounding knowledge bases using LLMs (status: mature)
- [[Hot Cache]] — ~500-word session context file, updated after every ingest and session (status: mature)
- [[Compounding Knowledge]] — why wiki knowledge grows more valuable over time, unlike RAG (status: mature)
- [[cherry-picks]] — prioritized feature backlog from ecosystem research; 13 features to add to claude-obsidian (status: current)
- [[SDLC Wiki Concerns]] — design pattern for serving SDLC roles (DevOps, QA, security, design, writing) via base mode + opt-in concerns (status: evergreen)
- [[Spec-Kit and claude-mem]] — comparison with GitHub spec-kit; recommend coexistence over integration; BA-without-code-access angle (status: evergreen)
- [[Wiki Sharing Patterns]] — three sub-problems for team adoption: multi-role access, multi-service structure, wiki location; options awaiting field feedback before defaults change (status: developing)
- [[Recursive Language Models]] — inference strategy: long context as a REPL variable the model greps/chunks/recurses over; sidesteps context rot (status: developing)
- [[Context Rot]] — model accuracy degrades as context grows even within the window; the motivation for RLM and tight-context habits (status: current)
- [[RLM-Optimized Wiki Querying]] — design: apply RLM (grep-first + bounded recursion over the wiki filesystem) to wiki-query for large ADLC vaults (status: developing)
- [[Graphify Relative Paths]] — design+impl: store project-root-relative source_file in committed graph artifacts so the project is portable across team members (status: implemented)
- [[Domain-Specific Agents]] — composition over inheritance for agents: small complete agents under a coordinator, minimal per-agent context; >80% token-efficiency claim (status: developing)
- [[Multi-Agent Communication Taxonomy]] — five primitives: delegation, creator-verifier, direct communication, negotiation, broadcast; missions composes four (status: current)
- [[Validation Contract]] — correctness written at planning time before any code; assertion coverage accounted across features; validated behaviorally by adversarial validators (status: current)
- [[Structured Handoff]] — schema-shaped worker report (done / undone / commands + exit codes / issues / procedure compliance); progress blocks on unresolved issues (status: current)
- [[Grilling Session]] — alignment-first relentless interview (one question at a time + recommended answer) until a shared design concept exists; precedes any plan/PRD (status: current)
- [[Ralph Wiggum Loop]] — AFK implementation loop: fresh context per iteration over an issue backlog, sentinel-terminated, Docker-sandboxed; Sandcastle parallel version (status: current)
- [[Vertical Slices for Agent Tasks]] — tracer-bullet issue decomposition; Kanban DAG of independently grabbable all-layer slices enables parallel agents (status: current)
- [[Deep Modules]] — Ousterhout's small-interface/big-functionality modules as agent enablement; feedback-loop quality is the ceiling on agent output (status: current)

---

## Entities

- [[ETH Zurich AGENTbench Team]] — Gloaguen, Mündler, Müller, Raychev, Vechev; only rigorous empirical evaluation of AGENTS.md (status: current)
- [[Aider]] — open-source AI pair-programmer; originator of tree-sitter + PageRank repo-map (status: current)
- [[Andrej Karpathy]] — AI researcher, creator of the LLM Wiki pattern, former Tesla AI director (status: developing)
- [[Ar9av-obsidian-wiki]] — multi-agent compatible LLM Wiki plugin; delta tracking manifest (status: current)
- [[Nexus-claudesidian-mcp]] — native Obsidian plugin + MCP bridge; workspace memory, task management (status: current)
- [[ballred-obsidian-claude-pkm]] — goal cascade PKM; auto-commit hooks, /adopt command (status: current)
- [[rvk7895-llm-knowledge-bases]] — 3-depth query system, Marp slides, parallel deep research (status: current)
- [[kepano-obsidian-skills]] — official skills from Obsidian creator; defuddle, obsidian-bases (status: current)
- [[Claudian-YishenTu]] — native Obsidian plugin embedding Claude Code; plan mode, @mention (status: current)
- [[Alex L. Zhang]] — MIT CSAIL; lead author of Recursive Language Models (status: current)
- [[Justin Schroeder]] — StandardAgents engineer; domain-specific-agents advocate; Dmux, ArrowJS (status: current)
- [[StandardAgents]] — stealth startup building a domain-specific-agent ecosystem; tracks token prices (status: developing)
- [[Orlov]] — Ukrainian-language YouTube educator on AI tooling; popularized Wiki LLM + graphify (status: current)
- [[Factory]] — AI dev-tools company; missions system for multi-day autonomous delivery; agents called droids (status: current)
- [[Luke Alvoeiro]] — leads core agent harness at Factory; started Goose at Block; "droid whispering" (status: current)
- [[Matt Pocock]] — developer educator (Total TypeScript, AI Hero); grilling → PRD → vertical-slice Kanban → Ralph loop workflow; author of Sandcastle (status: current)

---

## Sources

- [[agents-md-spec]] — 2025-08 | Agentic AI Foundation | the official AGENTS.md spec
- [[evaluating-agents-md-eth]] — 2026-02-12 | Gloaguen et al., ETH Zurich | the only rigorous empirical evaluation
- [[aider-repo-map]] — 2023-10-22 | Paul Gauthier (Aider) | canonical reference for tree-sitter repo-map
- [[anthropic-context-engineering]] — Anthropic Engineering | principles + Claude Code's hybrid model
- [[anthropic-contextual-retrieval]] — 2024-09 | Anthropic | strongest published retrieval numbers (35-67%)
- [[racg-survey-2025]] — Tao, Qin, Liu | comprehensive landscape survey of repo-level RACG
- [[cursor-generate-rules]] — 2025-04-15 | Cursor v0.49 | /Generate Cursor Rules feature
- [[aider-conventions]] — Aider docs | strict-human-authorship CONVENTIONS.md baseline
- [[reflexion-paper]] — 2023 | Shinn et al. | foundational Actor/Evaluator/Self-Reflection paper
- [[sdlc-team-documentation-research]] — 2026-05-09 | web-search synthesis | DevOps/SRE + QA + Backstage TechDocs sources informing the concerns design
- [[spec-kit-research]] — 2026-05-10 | web-research synthesis | github/spec-kit toolkit, methodology, BA fit; informs the Spec-Kit and claude-mem comparison
- [[wiki-sharing-research]] — 2026-05-10 | web-research synthesis | Obsidian sharing tools (Sync, Relay, Publish), docs-as-code topologies, Backstage TechDocs cross-team patterns
- [[anthropic-harness-design]] — 2026 | Anthropic Engineering | generator-evaluator separation as trust-boundary
- [[claude-obsidian-ecosystem-research]] — 2026-04-08 | web research across 16+ repos | 8 wiki pages created
- [[rlm-paper-arxiv]] — 2025-12-31 | Zhang, Kraska, Khattab (MIT CSAIL) | the RLM paper (arXiv 2512.24601)
- [[rlm-blog-zhang]] — 2025-10 | Alex L. Zhang | informal primary writeup with mechanics
- [[rlm-github-repo]] — alexzhang13/rlm | reference implementation (REPL backends, rlm_query)
- [[rlm-reproduction-overthink]] — 2026 | reproduction (arXiv 2603.02615) | confirms mechanism, flags over-recursion
- [[campbell-after-ai-hype]] — 2026-06-18 | Richard Campbell, NDC keynote | post-hype landscape; agentic-PR loop validated, LLM-judge failure case, vendor volatility
- [[yt-schroeder-domain-specific-agents]] — 2026-06-29 | Justin Schroeder (StandardAgents), AI Engineer | domain-specific agents; composition over inheritance; 2027 = multi-agent orchestration
- [[orlov-rag-wiki-llm-graphify]] — 2026-06-27 | Orlov (YouTube, uk) | three waves of agent memory: RAG → Wiki LLM → graphify; chunk-as-assertion heuristic; auto-transcript caveats
- [[yt-alvoeiro-multi-agent-architecture]] — 2026-05-06 | Luke Alvoeiro (Factory), AI Engineer | five multi-agent primitives; missions: validation contracts, structured handoffs, serial execution, per-role models; 16-day runs
- [[yt-pocock-ai-coding-workflow]] — 2026-04-24 | Matt Pocock @ AI Engineer | full workflow: grilling → PRD → vertical-slice Kanban → AFK Ralph loop → TDD → fresh-context review → manual QA; deep modules; doc rot

---

## Questions

- [[Research Pre-computed Context for Coding Agents]] — 2026-05-09 synthesis: what to pre-compute for coding agents (status: developing)
- [[Research Feedback-Driven Project Profile]] — 2026-05-09 synthesis: how engineer feedback should update AGENTS.md (status: developing)
- [[How does the LLM Wiki pattern work]] — how the pattern works and why it outperforms RAG at human scale (status: developing)
- [[Research Recursive Language Models]] — 2026-06-28 synthesis: RLM mechanics, results, limits, and the wiki-query/structure application for ADLC (status: developing)

---

## Comparisons

- [[Wiki vs RAG]] — when to use a wiki knowledge base versus RAG; verdict: wiki wins at <1000 pages
- [[claude-obsidian-ecosystem]] — feature matrix of 16+ Claude+Obsidian projects; where claude-obsidian wins and gaps

---

## Domains

<!-- Add domain entries here after scaffold -->

---

