---
type: source
title: "SDLC Team Documentation Research (web search synthesis)"
created: 2026-05-09
updated: 2026-05-09
source_type: web-search-synthesis
confidence: medium
tags:
  - sdlc
  - devops
  - qa
  - security
  - documentation
status: mature
related:
  - "[[SDLC Wiki Concerns]]"
key_claims:
  - "Modern engineering documentation lives close to code (Backstage docs-like-code)."
  - "DevOps/SRE artifact types are runbooks, incident postmortems, service catalogs, SLOs, observability docs."
  - "QA artifact types are test plans, checklists, test cases, bug reports."
  - "Real engineering teams are cross-functional; one vault must serve multiple roles."
---

# SDLC Team Documentation Research

Consolidated source page for the research pass that informed [[SDLC Wiki Concerns]] (May 2026). Three parallel web searches across DevOps/SRE, QA, and Backstage TechDocs.

## Sources cited

### DevOps / SRE

- **[SRE best practices 2026: tips, tools and KPIs](https://www.justaftermidnight247.com/insights/site-reliability-engineering-sre-best-practices-2026-tips-tools-and-kpis/)** — Service catalogs (Backstage-style) with metadata in YAML next to code. Alerts/pages should carry direct runbook links. Create-a-service templates include ownership metadata, runbook stub, OpenTelemetry defaults, baseline dashboards, alert rules, starter SLO/SLI definitions.
- **[DevOps Roadmap (Part 36): Incident Management — On-Call, Runbooks, Postmortems, War Rooms & RCA](https://medium.com/@sainath.814/devops-roadmap-part-36-incident-management-on-call-runbooks-blameless-postmortems-war-rooms-6a424abc26bf)** (Sainath, Medium) — Runbooks vs. SOPs distinction; both are living documents but governed differently. Postmortems should be centrally stored, version-controlled, comment-enabled, templated, searchable by keyword/date/team.
- **[Google SRE Workbook — On-Call](https://sre.google/workbook/on-call/)** — Foundational on-call practice: runbooks linked from alerts, blameless postmortems, severity tagging.
- **[Postmortems in DevOps](https://medium.com/@knqzx/postmortems-in-devops-5e6dc0604786)** (Medium) — Postmortem template structure and review process.
- **[awesome-sre](https://github.com/dastergon/awesome-sre/blob/master/README.md)** — Curated SRE resources index.

### QA / Testing

- **[What Is Test Documentation 2026](https://www.qamadness.com/what-is-test-documentation-and-why-do-we-need-it-2026/)** — In 2026, AI-augmented QA workflows; written benchmarks prevent scope creep; AI-powered knowledge bases handle tagging/linking/answering while humans curate.
- **[QA Documentation: Types, Roles, and Key Differences](https://fulcrum.rocks/blog/qa-documentation-test-strategy-test-plan-test-case)** — Hierarchy: test strategy → test plan → checklist → detailed test case. Test case = step-by-step + pass criteria. Checklist = grouped scenarios per module, often in TestRail/Sheets.
- **[Strategic QA Documentation: Blueprint for Enterprise Excellence](https://www.testriq.com/blog/post/how-to-write-qa-documentation-a-complete-guide)** — Documentation as the blueprint for repeatable, auditable QA.
- **[Bug Report: Definition, Examples & Best Practices (2026)](https://www.docsie.io/blog/glossary/bug-report/)** — Bug reports as primary vehicle for reporting issues; structured/actionable format requirement.

### Cross-cutting

- **[Announcing TechDocs (Spotify Backstage)](https://backstage.io/blog/2020/09/08/announcing-tech-docs/)** — Docs-like-code: markdown lives next to source. 1 component = 1 GitHub repo = 1 doc site. 5000+ doc sites at Spotify, ~10000 daily hits.
- **[Backstage TechDocs Documentation](https://backstage.io/docs/features/techdocs/)** — MkDocs render, central Backstage plugin, metadata layer (ownership, GitHub Issues, Slack support, Stack Overflow tags).
- **[What Spotify's Backstage means for documentation](https://patford12.medium.com/what-spotifys-backstage-means-for-documentation-6a5caea71bfd)** — Cross-functional team (writers + engineers) building the docs platform.

## Method

Three parallel WebSearch queries (May 2026):
1. `engineering team wiki structure DevOps SRE runbooks postmortems documentation 2026`
2. `QA test team documentation structure wiki knowledge base test plans bug reports 2026`
3. `Backstage TechDocs Spotify engineering documentation structure roles cross-functional`

Each search returned ~10 links. Citations above are the substantive sources whose content informed the synthesis. Search snippets only (not full-source ingest) — confidence rated medium pending deeper read if the design proves out.

## Synthesis output

See [[SDLC Wiki Concerns]] for the design synthesis: a base-mode-plus-opt-in-concerns pattern that lets one vault host multiple role-specific document classes without forcing a single-role label.
