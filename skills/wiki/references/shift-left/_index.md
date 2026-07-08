# Bundled shift-left method

The Shift-Left Engineering Advisor methodology, **bundled into claude-mem** so the `architecture-subagent` needs no external `anthropic-skills:shift-left-engineering-advisor` skill. The worker reads `shift-left-engineering-advisor.md` directly.

Source: the shift-left-engineering-advisor skill (see `ATTRIBUTION.md`).

## ADLC overrides (read before applying)

The advisor describes gates 1 / 1.5 / 2 / 3 (/ 4). In claude-mem Mode ADLC:

1. **Per-service specs, not a project-context folder.** Write gate outputs as Markdown into each service's own code wiki (`services/<svc>/wiki/specs/`), not a separate `project-context/` folder.
2. **Trace down from BA.** Each technical requirement traces to a BA requirement ID (from the bundled BA method set in `../ba/`).
3. **Diagrams: Mermaid** in the living spec; PlantUML reserved for formal export.
4. **Human gate between gates** (no skipping).
5. **Gate 0 escalation (up).** Governance questions — vendor viability, tool approval, buy-vs-build, subscription/budget, compliance class, shelfware — are not engineering decisions. Route them up to the planned `product-management-layer` skill and keep the advisor's vocabulary disjoint. See the doc's "Governance Escalation" section; design is documented at `wiki/concepts/Product Management Layer Skill.md`.
6. **Headless operation.** The advisor is written for an interactive chat; the `architecture-subagent` runs it headless. Skip the On Init interview and the per-gate "Does this look right?" loop: inputs come from the dispatch packet, and approval is the dispatcher's / operator's human gate between gates. File open questions in the spec instead of asking mid-run.
7. **Code-grounded claims.** Where the advisor says to extract constraints from source docs, the ADLC override is stricter: any claim about the existing codebase must be confirmed in the service checkout or marked `[UNVERIFIED — from docs]` (see `agents/architecture-subagent.md`).

See [`../technical-planning.md`](../technical-planning.md).
