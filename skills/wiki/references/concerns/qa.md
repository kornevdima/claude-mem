# Concern: QA / QC / Testing

Add when: the team produces structured test artifacts (test plans, test cases, bug reports) and there's a testing discipline beyond ad-hoc developer self-tests. Skip when testing is purely informal or fully automated with no human-curated documentation.

## Folders

```
wiki/
├── test-plans/      # Per-project / per-release strategy and scope
├── test-cases/      # Detailed, executable test cases grouped by area
├── bugs/            # Filed defect summaries; full trackers stay external
└── coverage/        # Coverage reports, gaps, regression suites
```

## Frontmatter — `wiki/test-plans/*.md`

```yaml
---
type: test-plan
title: "..."
release: "..."                  # release/version this plan covers
scope: feature                  # feature | release | regression | exploratory
modules_in_scope: []            # wikilinks to wiki/modules/ (Mode B)
entry_criteria: ""
exit_criteria: ""
risks: []
owner: "..."
status: active                  # draft | active | done | superseded
tags: [test-plan]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/test-cases/*.md`

```yaml
---
type: test-case
title: "..."
test_id: "..."                  # mirrors external tracker if used (TestRail, Xray, etc.)
area: "..."                     # functional area
priority: 2                     # 1 (highest) to 4
preconditions: ""
steps: []                       # ordered list
expected: ""
automation_status: manual       # manual | automated | flaky | skipped
related_modules: []
tags: [test-case]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/bugs/*.md`

```yaml
---
type: bug
title: "..."
external_id: "..."              # Jira/Linear/GitHub issue ID
severity: high                  # critical | high | medium | low
priority: 2
status: open                    # open | in-progress | fixed | wontfix | closed
reported_date: YYYY-MM-DD
fixed_in_release: ""
reproducer: ""                  # steps to reproduce
related_modules: []
related_incidents: []           # link to wiki/incidents/ when a bug caused production impact
tags: [bug]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/coverage/*.md`

```yaml
---
type: coverage
title: "..."
scope: module                   # module | flow | regression-suite
target: "..."                   # what's being measured
last_run: YYYY-MM-DD
metric: ""                      # e.g. "82% line coverage" or "237 cases / 12 gaps"
gaps: []
tags: [coverage]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Key wiki pages to create

`[[Test Strategy]]`, `[[Regression Suite Map]]`, `[[Bug Triage Process]]`, `[[Release Test Checklist]]`.

## Patterns

- **Hierarchy**: test strategy → test plan (per release/feature) → test cases (per scenario). Plans link down to cases; cases link up to plans. (Source: [[sdlc-team-documentation-research]] / Fulcrum.)
- **Don't duplicate trackers**: `wiki/bugs/` summarizes notable bugs and their context; the external tracker (Jira, Linear, GitHub) remains the authoritative status board. Use `external_id` to link out.
- **Cross-link to Mode B**: test cases reference `wiki/modules/` and `wiki/flows/` so an agent reading either side gets the other.
- **Automation tag**: `automation_status` lets the team query "which manual cases should we automate next?" via Obsidian Bases or Dataview.
- **Assertion-coverage ledger (ADLC)**: in a service code wiki, `coverage/_index.md` doubles as the ledger — one row per verification-contract scenario (feature, scenario id, `coverage:` tag, test title, last scoped-suite result + date). `feature-tester` maintains it; it is derived, and on any disagreement the contract + spec win. `wiki-lint` cross-checks it for drift.
