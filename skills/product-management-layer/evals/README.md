# product-management-layer evals (E1–E8)

Encodes the eval matrix from the skill's design (one case per functional
requirement, plus two negative trigger cases) as runnable fixtures. The golden
case E1 is the vendor-sunset retrospective that motivated the skill.

| Case | Scenario | Asserts |
|------|----------|---------|
| E1 | Vendor sunset (golden) | sunset ReviewTrigger fired; dependent approval → `under-review`; migration checklist; approvals never transfer (FR-2) |
| E2 | Buy-vs-build with owned asset | option table ≥3 incl. Do-Nothing + already-owned Arize; TCO; recommendation + owner decision (FR-4/5) |
| E3 | Unused subscription | shelfware flagged with renewal-or-cancel action (FR-5) |
| E4 | Two use cases, one tool | approval per pair; separate compliance sheets, class not inherited (FR-1/3) |
| E5 | Negative: "write an ADR" | PM layer does NOT trigger — no Gate 0 artifacts |
| E6 | Negative: buy-vs-build inside shift-left | shift-left escalates UP, doesn't answer in-place (FR-7) |
| E7 | Approved intake | handoff packet to shift-left Gate 1 with trace IDs (FR-7) |
| E8 | STATUS mode | portfolio report: near expiry, triggers, shelfware, next best action (FR-6) |

## Layout

- `cases/E*.md` — one file per case: `## Prompt`, `## Must match`, `## Must not match`
  (one POSIX extended regex per line; HTML comments ignored), `## Grader notes`
  (human context, not parsed).
- `fixtures/governance/` — a coherent fixture portfolio (2 approved pairs, an
  underused Arize sub, ungoverned zero-utilization FlowMetrics, empty trigger
  log). Dates are `{{PLUS_45D}}`-style placeholders substituted **relative to the
  run date**, so "near expiry" cases never go stale.
- `run-evals.sh` — the runner. Per case: builds a throwaway workspace with the
  fixtures under `docs/governance/`, runs one non-interactive `claude -p` turn in
  it, grades the transcript **plus the registry diff** (writes count, unmodified
  fixture text can't trip negative assertions).
- `results/` — transcripts (`E*.out.md`), registry diffs, grading blobs. Gitignored.

## Running

```bash
./run-evals.sh              # all 8 (8 real model calls — costs tokens)
./run-evals.sh E1 E5        # smoke subset (the two from the original plan)
./run-evals.sh --dry-run    # print substituted prompts only, no API calls
./run-evals.sh --grade-only E3   # re-grade an existing transcript
```

Env knobs: `CLAUDE_CMD` (default `claude`; put extra flags here), `EVAL_MODEL`
(optional `--model`), `EVAL_MAX_TURNS` (default 25).

**Precondition:** the claude-mem plugin must be installed for the invoking user —
the scratch workspace carries no plugin config, so skill triggering (what E5/E6
test) relies on the user-level install.

## Grading semantics

A case passes when every `Must match` regex hits and no `Must not match` regex
hits, against `transcript + governance diff`. Assertions are deliberately
generous (behavioral invariants, not exact wording). `Grader notes` list
stricter checks worth a manual look on borderline output — e.g. E8: confirm the
~400-day approval is NOT listed as near-expiry.
