---
type: source
title: "AGENTS.md Specification"
source_type: official-specification
author: "Agentic AI Foundation (Linux Foundation)"
date_published: 2025-08
url: "https://agents.md/"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - specification
  - agents-md
  - coding-agents
status: current
related:
  - "[[AGENTS.md]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Research Pre-computed Context for Coding Agents]]"
key_claims:
  - "AGENTS.md is the dedicated, predictable place to give coding agents project context"
  - "60K+ open-source projects use it as of mid-2026"
  - "20+ tools support it including Codex, Cursor, Copilot, Aider, Devin, Jules"
  - "Stewarded by the Agentic AI Foundation under Linux Foundation"
---

# Source: AGENTS.md Specification

**Type**: Official specification
**Steward**: Agentic AI Foundation (Linux Foundation), released August 2025
**URL**: https://agents.md/

## Summary

AGENTS.md is a deliberately minimal Markdown file format for telling coding agents about a project. It complements (does not replace) `README.md`: README targets humans, AGENTS.md targets agents.

## Recommended sections (none required)

- Project overview
- Build and test commands
- Code style guidelines
- Testing instructions
- Security considerations
- Dev environment tips
- PR / commit message guidelines
- Deployment steps

## Format rules

- Plain CommonMark Markdown.
- No YAML frontmatter, no JSON schema, no curly-brace templating.
- Free-form headings; nothing is mandatory.

## Scoping rules

- Root file is the default.
- Nested AGENTS.md files allowed in monorepos / subprojects.
- "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything."
- Agents auto-discover by walking up the directory tree.

## What it explicitly excludes vs README

Quick-start sections, project-marketing descriptions, and contributor-onboarding content stay in README. AGENTS.md is for the operational specifics that would clutter human docs: how to run tests, what conventions to follow, what not to touch.

## Adoption (mid-2026)

- 60,000+ open-source projects on GitHub.
- Native support: OpenAI Codex, Google Jules + Gemini, Cursor, GitHub Copilot (since August 2025), Aider, Devin, Factory, Amp, Windsurf, Zed, RooCode, VS Code.
- Enterprise rollouts: Uber, Databricks, Sourcegraph standardize internal AI onboarding on AGENTS.md.

## Governance

Stewarded by the **Agentic AI Foundation** under the Linux Foundation. Emerged from cross-vendor collaboration (OpenAI, Google, Cursor, Factory, others) in August 2025.

## What this source contributes

- Concrete spec the `/project-profile` skill should be compatible with rather than competitive with.
- A list of section headings that have already converged across the ecosystem (so claude-mem doesn't reinvent its own taxonomy).
- An adoption signal: this is now the default convention; tooling that ignores it loses interoperability.

## Connections

- [[AGENTS.md]] — concept page interpreting this spec
- [[Research Pre-computed Context for Coding Agents]] — synthesis page
- [[evaluating-agents-md-eth]] — empirical evaluation of whether the format actually helps
