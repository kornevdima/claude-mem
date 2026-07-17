---
name: wrap-up
description: >
  Session wrap-up sync for ADLC (Agentic Development Life Cycle) vaults. Before ending a
  session, checks git changes across the vault and co-located code repos, injects updates
  into the relevant code wikis, reflects shipped features / resolved gaps / new requirements
  into the product wiki, then refreshes hot.md and appends log.md. Uses context already
  loaded in the session, no full re-scan.
  Triggers on: "wrap up the session", "end session", "wrap up", "session end",
  "session wrap-up", "sync before exit", "/wrap-up".
---

# wrap-up: Session sync for ADLC vaults

Run this when the operator signals the session is ending. The goal is to leave every wiki in the multi-wiki set coherent before exit, cheaply, using what is already in context.

## When to run

- The operator says "wrap up", "end session", "session end", or similar.
- Best in an ADLC vault (product wiki plus code wikis under `services/`), but the `hot.md` + `log.md` refresh applies to any vault.

## Steps

1. **Use loaded context first.** Do not re-scan the whole repo. Work from what this session already read and changed. Only run targeted git commands to confirm.
2. **Detect changes.** In the vault and in each `services/<checkout>`, run `git status --short` and `git diff --name-only HEAD` to see what changed this session. Note new or edited code, docs, and wiki pages.
3. **Down-propagate (code wikis).** For each code repo that changed, update its Mode B code wiki: impl specs, ADRs, plans, module / flow notes affected by the change. If a feature was specified this session, write the impl spec into that repo's wiki so its agent can build it. If a changed repo carries a code graph (`graphify-out/graph.json`) and its source changed this session, run `/graphify-update` on it (or flag it as a follow-up if time-boxed) — a stale graph silently misleads every worker that orients with it next session.
4. **Up-propagate (product wiki).** Reflect the session's outcomes into the ADLC wiki: shipped features (`features/` proposed to shipped), resolved or new gaps (`gaps/`), new or changed requirements (`requirements/`, with stable IDs), stories and tests if generated. Keep traceability links current. Reconcile the defect route: every verifier FAIL this session must have both its `bugs/` page and a backlog item tracing to it (see `technical-planning.md` dispatcher rules) — file whichever is missing.
5. **Archive delivered plans.** Point-in-time planning docs rot into traps: code drifts until the plan misleads the next agent that reads it. For every feature that shipped this session, flip its spec / plan / PRD-like pages to `status: delivered` (with a one-line "as-built diverges: see [[page]]" note when relevant), and flip or supersede any verification contract sections the ship made stale. Maintained as-built pages compound; stale plans must be visibly closed.
6. **Reconcile rollups.** `index.md`, `overview.md`, and any readiness dashboard must agree with the detailed records this session changed. In ADLC vaults this includes the two metrics-seam pages (see `wiki/references/mission-control.md`): reconcile `meta/mission-control.md` against the verdicts / FAILs / ships this session produced, and refresh `meta/ba-activity.md` from `produced_by` / `feature` / `effort_estimate` frontmatter (grep the frontmatter; do not LLM-read the vault). Refresh stale counts and claims everywhere (production vaults drifted to "scaffold only" overviews while 20 features were release-ready). For pages a decision made stale (data model, architecture overview, verification contracts), add an explicit "superseded by [[ADR-xxx]]" pointer or flip the stale flags — never leave a silent contradiction.
7. **Refresh caches.** Overwrite `hot.md` (under 500 words, hot-cache format) and append a dated entry to the TOP of `log.md` recording trigger, scope, skills run, counts, and follow-ups. If a delivery run ledger survives (`wiki/sprints/_run *.md`, see the `adlc` skill), list it in `hot.md`'s open threads and in the report as the resume pointer — next session starts with `/adlc`. Log entries are pointers — full records (verification, review, retro) belong on their own pages. If `wiki/index.json` exists, regenerate it (`skills/wiki-query/scripts/build_index_json.py`, see the wiki-query skill's generator section) — a stale locator misroutes every large-vault query next session. On Claude Code hosts, also refresh the token-usage rollup: `python3 <this-skill-dir>/scripts/usage_report.py .` regenerates `wiki/meta/usage.md` (cumulative per-session ledger + top-consumer / per-model / per-subagent-type breakdowns) from the local session transcripts, so the operator can see what drives consumption. Host-local derived view (see `wiki/references/mission-control.md` § usage): on hosts without `~/.claude/projects/` the script exits cleanly — skip without error.
8. **Report.** Summarize what was synced across which wikis, and flag anything left for the human (sign-offs, prod verification).

## Rules

- Markdown is the system of record. Do not generate Office files here (that is the export step, see `wiki/references/ba-suite-pipeline.md`).
- Append-only `log.md`: newest at top, never edit past entries.
- Keep PII out of the committed wiki; sensitive staffing / context stays in gitignored private notes.
- Do not commit or push unless the operator asks.
