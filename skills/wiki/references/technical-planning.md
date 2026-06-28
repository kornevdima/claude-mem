# Technical planning and verification (ADLC mode)

The BA layer (`ba-suite`, product wiki) produces business deliverables. Technical planning refines those into per-service specs a repo agent can build, then verification confirms the build with the operator's own toolset. Used by Mode ADLC (see [`modes.md`](modes.md)).

## No project-context folders

Do NOT scaffold a separate `project-context/` folder kit in the product wiki for technical planning. Use the ingest + refinement pipeline instead: requirements are ingested into the product wiki (`ba-suite`), then refined into specs that live in each service's own code wiki (Mode B). The product wiki holds the business view; the service code wiki holds the technical spec.

## Shift-left refinement (ingest to spec)

The `architecture-subagent` (`agents/architecture-subagent.md`) is the worker. It applies the shift-left four-gate methodology (and the `anthropic-skills:shift-left-engineering-advisor` skill when installed):

| Gate | Produces |
|---|---|
| Gate 1 | Technical requirements: FR / NFR / SR (security separate), open questions, gaps |
| Gate 1.5 | Domain model: entities, business rules, invariants, Mermaid diagrams |
| Gate 2 | Architecture Decision Records + design rationale |
| Gate 3 | Engineering workflow: CI/CD, test pyramid, deployment, incidents |

Gates are sequential with a human approval between each (no skipping). Refinement traces every technical requirement back to a BA requirement ID. Specs are written to `services/<svc>/wiki/specs/` (or the repo's `plans/` convention), one set per service.

## Per-service agentic build

Each service is its own service: its own repo, its own Mode B code wiki, its own build agent. Once a spec lands in the service code wiki, the repo agent builds the deliverable through the agentic pipeline. The product wiki `features/` page links to the service spec; the `wrap-up` skill keeps both sides in sync at session end.

## Verification (operator's toolset)

Features are verified with the same tools the agent operator has, not a bespoke harness:

- **Local run:** `docker compose up` the service stack (dev server + dependencies). Verify against localhost.
- **E2E:** the chrome-devtools MCP. Use `navigate_page` + `evaluate_script` to assert computed styles, DOM state, network calls, and console hygiene; `take_screenshot` for evidence. Mirrors the `chrome-ui-verify` pattern.
- **Backend / API:** the service's own test suite (unit + integration + e2e) run via the project's commands.
- **Record:** file a verification execution note (per test case: objective, observed value, PASS / FAIL) and link it from the feature page. The verifier never fixes bugs; it logs and stops.

## Diagrams and HTML export

Tech documentation uses **Mermaid**: inline code blocks in the spec Markdown, which render natively in Obsidian and in HTML. For a shareable rendered copy of a tech doc, HTML-export it into `.raw/exports/` (for example via `npx @mermaid-js/mermaid-cli` or a Markdown-to-HTML step). Reserve **PlantUML** for the formal export bundle that ships with `ba-suite` Office docs (see [`ba-suite-pipeline.md`](ba-suite-pipeline.md)).

## Export to the tracker

On export, deliverables map to the team's tracker via MCP (see [`mcp-setup.md`](mcp-setup.md) § ADLC MCP toolset). ClickUp hierarchy: Project to Space, Objective to Folder, Deliverable to List, Epic to Task, Story to Subtask, Task to Checklist Item. Keep a manifest mapping wiki pages to task IDs so re-export is idempotent.
