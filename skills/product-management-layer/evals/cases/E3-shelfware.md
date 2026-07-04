# E3 — Unused subscription (shelfware)

- **Traces:** FR-5 (asset / resource tracking)
- **Mode exercised:** REGISTRY-STATUS / asset review

## Prompt

Our governance registry is in docs/governance/. We are paying six thousand dollars a
year for FlowMetrics and I don't think anyone has touched it in months. Do we still
need it?

## Must match

FlowMetrics
(SHELFWARE|[Ss]helfware)
(cancel|renew)
AS-002

## Must not match

<!-- none -->

## Grader notes

Passing behavior: AS-002 is flagged as shelfware (no linked ApprovalEntry AND zero
utilization for 90 days), with an explicit renewal-or-cancel action ahead of the
renewal date. Bonus (not asserted): the renewal date urgency is surfaced (renews in
~30 days), and the flag is written back to the asset register.
