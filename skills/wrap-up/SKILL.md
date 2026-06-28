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
3. **Down-propagate (code wikis).** For each code repo that changed, update its Mode B code wiki: impl specs, ADRs, plans, module / flow notes affected by the change. If a feature was specified this session, write the impl spec into that repo's wiki so its agent can build it.
4. **Up-propagate (product wiki).** Reflect the session's outcomes into the ADLC wiki: shipped features (`features/` proposed to shipped), resolved or new gaps (`gaps/`), new or changed requirements (`requirements/`, with stable IDs), stories and tests if generated. Keep traceability links current.
5. **Refresh caches.** Overwrite `hot.md` (under 500 words, hot-cache format) and append a dated entry to the TOP of `log.md` recording trigger, scope, skills run, counts, and follow-ups.
6. **Report.** Summarize what was synced across which wikis, and flag anything left for the human (sign-offs, prod verification).

## Rules

- Markdown is the system of record. Do not generate Office files here (that is the export step, see `wiki/references/ba-suite-pipeline.md`).
- Append-only `log.md`: newest at top, never edit past entries.
- Keep PII out of the committed wiki; sensitive staffing / context stays in gitignored private notes.
- Do not commit or push unless the operator asks.
