---
type: concept
title: "AGENTS.md"
complexity: beginner
domain: ai-agents
aliases:
  - "agents.md"
  - "AGENTS dot MD"
created: 2026-05-09
updated: 2026-07-03
tags:
  - concept
  - agents-md
  - convention
  - cross-vendor
status: current
related:
  - "[[Context Engineering for Coding Agents]]"
  - "[[Project Profile]]"
  - "[[agents-md-spec]]"
  - "[[evaluating-agents-md-eth]]"
sources:
  - "[[agents-md-spec]]"
  - "[[evaluating-agents-md-eth]]"
---

# AGENTS.md

A cross-vendor convention for telling AI coding agents about a project. Plain Markdown file at the repo root (with optional nested files in subdirectories). Released August 2025, stewarded by the Agentic AI Foundation under the Linux Foundation. As of mid-2026: 60K+ open-source projects, 20+ tools support it natively (Source: [[agents-md-spec]]).

## What it is

A README for agents instead of humans. Carries the operational specifics that would clutter a regular README: build/test commands, code-style rules, testing instructions, security notes, dev-environment tips, PR conventions, deploy steps. None of these are required; the spec is intentionally minimal.

## Format

- Plain CommonMark Markdown.
- No YAML frontmatter, no JSON schema, no templating.
- Free-form headings.
- Free-form length (but evidence below favors brevity).

## Scoping rule

> "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything." (Source: [[agents-md-spec]])

Nested AGENTS.md files in subdirectories override the root one for files in their subtree. Useful for monorepos with mixed languages or layered conventions.

## Adoption (the cross-vendor piece)

Native support for AGENTS.md is broad enough that ignoring it costs interoperability:

- OpenAI Codex
- Google Jules + Gemini
- Cursor
- GitHub Copilot (since August 2025)
- Aider
- Devin, Factory, Amp, Windsurf, Zed, RooCode
- VS Code

Enterprise rollouts at Uber, Databricks, Sourcegraph standardize on it for internal AI onboarding. (Source: [[agents-md-spec]])

## Relationship to CLAUDE.md and other tool-specific files

Many tools have or had their own format: CLAUDE.md for Claude Code, .cursorrules / .cursor/rules/*.mdc for Cursor, .github/copilot-instructions.md for Copilot. These predate AGENTS.md and aren't going away. The current pragmatic pattern is: keep AGENTS.md as the cross-tool source of truth, and only put **tool-specific** details (e.g., MDC frontmatter for Cursor, @path imports for Claude) in the tool-specific files. (Source: agentrulegen.com guide)

## Does it actually help? (the empirical caveat)

The most rigorous evaluation (ETH Zurich, 2026) is sobering:

- Human-written AGENTS.md: **+4%** task success, +19% inference cost, +3-4 steps.
- LLM-generated AGENTS.md: **-2 to -3%** task success (worse than no file), +20-23% cost.
- Repository overviews specifically: no measurable benefit.
- LLM-generated content largely duplicates README.
- Even with a useful file, agents re-read it repeatedly and produce 14-22% more reasoning tokens.

(Source: [[evaluating-agents-md-eth]])

The takeaway: AGENTS.md is **a real but small win, only when hand-curated, and only when content is specific and actionable**. Auto-generation is harmful.

## What works in the file

From AGENTbench observations:

- Concrete tool/command names ("use `pytest -m unit`") get followed.
- "Tribal" knowledge that isn't in code or README is the most valuable kind.
- Specific don'ts ("never modify X", "use Y not Z").
- Build/test commands, with exact invocations.

What doesn't:

- Generic project overviews ("This is a Python web app...").
- Anything that just paraphrases README.
- Lengthy architecture descriptions.

## Practitioner counterpoint: keep it near-empty, prefer pull

[[Matt Pocock]] barely uses CLAUDE.md/AGENTS.md at all: everything in it is **pushed** to the agent on every turn, eating smart-zone budget whether relevant or not. His preference is **pull** — skills with small description headers the agent loads on demand — reserving push for the automated *reviewer* (standards next to the diff). He also demonstrates the lifecycle of a once-popular AGENTS.md tip: "sacrifice grammar for the sake of concision" made plans readable, but he dropped it after replacing plan-reading with grilling sessions — instructions in the always-on file should be re-audited as the workflow changes. (Source: [[yt-pocock-ai-coding-workflow]]) This is consistent with the ETH data above: the always-loaded file earns its place only for load-bearing, always-relevant directives.

## Connections

- [[agents-md-spec]] — the official specification
- [[evaluating-agents-md-eth]] — the empirical paper
- [[Context Engineering for Coding Agents]] — broader concept
- [[Project Profile]] — claude-mem design that should be AGENTS.md-compatible rather than competitive
