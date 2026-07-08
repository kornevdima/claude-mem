# E8 — Portfolio STATUS report

- **Traces:** FR-6 (portfolio status reporting)
- **Mode exercised:** REGISTRY-STATUS

## Prompt

Our governance registry is in docs/governance/. Give me our governance portfolio
status.

## Must match

(near expiry|Near expiry|≤60|60 ?d)
AP-UC001-TL003
(SHELFWARE|[Ss]helfware)
(FlowMetrics|AS-002)
[Nn]ext best action

## Must not match

<!-- none -->

## Grader notes

Passing behavior: the STATUS report per reference.md §9. From the fixtures it must
surface: AP-UC001-TL003 as near expiry (expires in ~45 days, within the 60-day
window); AS-002 FlowMetrics as shelfware (no ApprovalEntry, zero utilization,
renewal imminent); no open review triggers (the log is empty — saying so is fine);
recent decisions (DL-001); and a single next best action. AP-UC002-TL001 (expires
in ~400 days) must NOT be listed as near expiry — check manually.
