# E7 — Approved intake hands off to shift-left Gate 1

- **Traces:** FR-7 (handoff contracts — downward)
- **Mode exercised:** handoff packet after approval

## Prompt

Our governance registry is in docs/governance/. AP-UC001-TL003 — Arize for the LLM
eval dashboards use case — is approved. Hand it off to engineering so they can start.

## Must match

Handoff
Gate 1
AP-UC001-TL003
CC-002
shift-left

## Must not match

<!-- none -->

## Grader notes

Passing behavior: a Handoff Packet per reference.md §10 — use case (UC-001), approved
tool (TL-003 Arize), approval AP-UC001-TL003 with expiry, compliance class CC-002
with the controls that become security requirements, and the explicit ask to start
the shift-left Gate 1 flow tracing back to the AP-id. The packet quotes trace IDs;
governance-side language only (no FRs/NFRs written here).
