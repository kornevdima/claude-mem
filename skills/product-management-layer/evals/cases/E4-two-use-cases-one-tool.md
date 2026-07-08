# E4 — Two use cases, one tool

- **Traces:** FR-1 (approval per use case × tool pair), FR-3 (per-pair compliance scope)
- **Mode exercised:** INTAKE + COMPLIANCE-SCOPE

## Prompt

Our governance registry is in docs/governance/. We already use Arize for our LLM eval
dashboards and that's approved. The growth team now wants to use Arize for
customer-facing product analytics too, which would include customer PII. Are we
already covered by the existing approval?

## Must match

(new|separate|fresh|its own).*(intake|approval|entry|pair)
PII
(compliance|CC-)
pair

## Must not match

[Yy]es, (you are|you're|we are|we're) (already )?covered

## Grader notes

Passing behavior: the answer is NO — an ApprovalEntry is scoped to one
(use case × tool) pair and never transfers, so the new use case needs its own intake,
its own ApprovalEntry, and its own compliance sheet. The PII flag must drive a
different (stricter) compliance class than CC-002's `internal / none`; the class is
never inherited across use cases.
