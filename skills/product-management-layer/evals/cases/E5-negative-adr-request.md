# E5 — Negative: engineering request must NOT trigger the PM layer

- **Traces:** trigger-vocabulary disjointness (SKILL.md → Governance Escalation)
- **Mode exercised:** none — the PM layer must stay silent.

## Prompt

Write an ADR for choosing JWT versus server-side sessions for our web app's
authentication.

## Must match

ADR

## Must not match

Intake —
ApprovalEntry
AP-UC
compliance class
[Ss]helfware
Gate 0
vendor viability

## Grader notes

Passing behavior: the response is an engineering answer (an ADR, ideally routed via
the shift-left advisor's vocabulary) with NO Gate 0 governance artifacts. ADR,
requirements, spec, and architecture belong to shift-left's vocabulary; the PM layer
owns vendor / tool approval / buy-vs-build / subscription / compliance class /
shelfware. This case fails if the PM layer's intake or approval machinery appears.
