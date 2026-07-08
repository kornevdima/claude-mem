# E2 — Buy vs build with an already-owned asset

- **Traces:** FR-4 (buy-vs-build evaluation), FR-5 (asset tracking)
- **Mode exercised:** BUY-VS-BUILD

## Prompt

Our governance registry is in docs/governance/. The team wants to buy an LLM
observability platform for monitoring our production prompts. Why would we buy
anything though — couldn't we just build our own monitoring rules? Also, I think
we already pay for Arize. Walk me through it.

## Must match

Do.?[Nn]othing
Arize
(adopt-owned|already-owned|owned asset|already pay)
TCO
[Rr]ecommendation
(owner|decide|decision)

## Must not match

<!-- none — the mode legitimately produces a full evaluation -->

## Grader notes

Passing behavior: an option table with at least the Do-Nothing baseline, the
already-owned Arize subscription (adopt-owned; AS-001 shows 1/5 seats used), a buy
option, and build in-house — plus a TCO comparison, a clear recommendation, and an
explicit ask for the owner to decide (the skill recommends; the owner approves).
