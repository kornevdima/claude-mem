# E6 — Negative: buy-vs-build inside shift-left escalates UP

- **Traces:** FR-7 (handoff contracts — upward escalation)
- **Mode exercised:** escalation route only; shift-left must not answer it itself.

## Prompt

You are acting as the shift-left engineering advisor. We are mid-session at Gate 2
(domain model) for our notifications service. A question just came up: should we buy
LaunchDarkly for feature flags or build our own flag system? Answer as the shift-left
advisor would.

## Must match

(escalat|Gate 0|governance (layer|question|advisor)|product-management-layer)

## Must not match

<!-- Intentionally empty. After escalating, the governance layer may legitimately run
     BUY-VS-BUILD in the same reply, so we cannot forbid TCO artifacts outright.
     The assertion is that the escalation route is named, not answered in-place. -->

## Grader notes

Passing behavior: shift-left recognizes buy-vs-build as governance vocabulary and
escalates UP to the product-management-layer (Gate 0) instead of writing a
vendor evaluation inside the Gate 2 exchange. A response that produces a TCO table
with no mention of the governance layer / escalation is a FAIL (the must-match
catches this). Manual grading refinement: check that shift-left did not present the
evaluation as its own Gate 2 output.
