# Bundled shift-left method

The Shift-Left Engineering Advisor methodology, **bundled into claude-mem** so the `architecture-subagent` needs no external `anthropic-skills:shift-left-engineering-advisor` skill. The worker reads `shift-left-engineering-advisor.md` directly.

Source: the shift-left-engineering-advisor skill (see `ATTRIBUTION.md`).

## ADLC overrides (read before applying)

The advisor describes gates 1 / 1.5 / 2 / 3 (/ 4). In claude-mem Mode ADLC:

1. **Per-service specs, not a project-context folder.** Write gate outputs as Markdown into each service's own code wiki (`services/<svc>/wiki/specs/`), not a separate `project-context/` folder.
2. **Trace down from BA.** Each technical requirement traces to a BA requirement ID (from the bundled BA method set in `../ba/`).
3. **Diagrams: Mermaid** in the living spec; PlantUML reserved for formal export.
4. **Human gate between gates** (no skipping).

See [`../technical-planning.md`](../technical-planning.md).
