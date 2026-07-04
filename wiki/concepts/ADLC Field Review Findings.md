---
type: concept
title: "ADLC Field Review Findings"
created: 2026-07-04
updated: 2026-07-04
confidence: high
tags:
  - concept
  - adlc
  - field-evidence
  - review
  - metrics
status: mature
related:
  - "[[Grilling Session]]"
  - "[[Validation Contract]]"
  - "[[Vertical Slices for Agent Tasks]]"
  - "[[Wiki Sharing Patterns]]"
  - "[[RLM-Optimized Wiki Querying]]"
---

# ADLC Field Review Findings

End-to-end review (2026-07-04) of a production **two-wiki ADLC setup**: one product/delivery vault (Mode ADLC, `qa` + `ops` concerns) with `services/` symlinks to two Mode-B code wikis — a backend service carrying an embedded admin SPA, and a mobile app. An entire admin-panel subsystem (~24 feature plans) had been delivered through the agent pipeline; the review traced the flow through both wiki logs, measured content duplication across the wikis, and correlated with per-session token-usage data. Findings are genericized; they ground several harness rules in field evidence.

## 1. The pipeline ships — and inverts

The build → test → verify loop genuinely worked: verifier rejections were real gates (an SPA phase was REJECTED twice before passing), the tester stage repeatedly caught bugs the unit gates missed (a timestamp-serialization bug, a circular import that reddened 163 tests, a blocking publish hang), and every FAIL was routed to a fix in-session.

But the intended flow (requirements → spec → plan → build) **inverted for the core subsystem**: the code shipped first, grounded in a legacy-tool export rather than a product plan, and the BA layer (an epic of ~16 FRs, stories, test cases, RTM) was registered **after** the subsystem was live — sanctioned by a standing governance stance ("everything in shipped code is approved"). Product BA acted as catch-up, not driver. Code-first can be the right trade (it shipped in ~2 days of pipeline sessions); the failure mode is the *unregistered interval* — later features invented ad-hoc local requirement IDs that existed nowhere in the register at build time.

**Rule grounded:** register in the same session you build, or accept that the register lags reality and schedule the reconcile explicitly. Never let local IDs float unregistered.

## 2. The handoff seam is where cost hides

The practiced handoff: product session authors a plan and pushes it into the service code wiki; a repo-level session picks it up and does detailed implementation planning + dispatch. This worked because the plans were strong — file-by-file steps, a **"Grounded facts (verified in code — don't re-discover)"** section, and their own acceptance criteria in every plan.

Two measured seam costs:

- **Zero traceability.** Not one of ~24 plans referenced a registered requirement ID. The plan→register link was one-directional and lagging; drift was discovered later by grep, not prevented.
- **Re-derivation.** The repo-level agent re-read source (a scoring-weights implementation, a data-gate condition) to rebuild context the plan should have carried; the product side later reconciled stale beliefs ("chart X is live" — it wasn't). Context not carried across the seam is paid for twice.

**Rules grounded:** a pushed-down plan must carry requirement IDs, the verification contract, and grounded facts (this is the `architecture-subagent` job description — it ran exactly **once** in 16 repo sessions; the manual substitute worked but leaked exactly the things the template enforces).

## 3. Records must be pages, not prose

During the delivered work: **no review stage existed** (the reviewer agent and the loop-cap rule postdate it), and PASS/REJECTED verdicts lived only in log narrative + plan frontmatter — real but not queryable. Two code-wiki pages (a module note and an auth-flow note) still said "not implemented — no code exists yet" weeks after the subsystem was live in production: the exact plan-rot trap the wrap-up archive rule targets, found live in the field.

**Rules grounded:** verification/review records as their own pages with one-line log pointers; the wrap-up "archive delivered plans / flip stale flags" step; `wiki-lint` staleness checks. All were added to the harness before this review — the review confirmed each corresponds to a real observed failure.

## 4. Duplication: low overall, concentrated in the shared layer

- **~6–8% by volume** across both wikis' subsystem documentation — because the code wiki's implementation detail (~10× the product wiki's volume) has no product-side counterpart. The two-wiki split earns its keep.
- In the **shared conceptual layer** (~450 lines that *could* overlap): ~25–30% hard duplication (a weighted-scoring formula table maintained verbatim in both wikis; population statistics; an options-considered rejection rationale maintained in **three** places; a status enum in four), ~35–40% summarized overlap (route lists, auth model — same facts, independent phrasing: acceptable), rest clean.
- Bidirectional wikilinks between the wikis existed and were used — the healthy pattern.

**Rules grounded:** single-source detailed tables/formulas (one wiki owns it, the other links); a comparison page and an ADR should not both maintain the alternatives analysis. Duplication itself was *not* the main risk — the two genuinely contradictory pages (drift) were.

## 5. Efficiency is set by the operator, bounded by the harness

Token-usage ledgers (per-repo `meta/usage.md`, generated by the wrap-up usage rollup) quantified what interaction style costs:

- A pipelined feature: **~250–460K output tokens** at the repo level, running at **48–66% subagent share** (workers read in their own contexts).
- Interactive main-thread marathons: a branch review hit **~600K output at 4% delegation with 136M cache-read tokens**; a long iterative session reached 455 requests / 105M cache reads. Same repo, same model — the difference is the shape of the ask.
- Product-vault sessions before the ADLC migration ran at ~0% delegation; after, ~30%+.

The levers, in observed order of impact: **granularity of the ask** (scoped feature + plan → pipeline; open-ended review → marathon), **session locality** (start repo-level sessions for app work — the right hot cache and conventions load by default), **handoff completeness** (§2), and **session hygiene** (wrap up and restart instead of pushing one session past ~400 requests). The harness rules reduce *variance* (gates, records, re-verification stop silent failure modes); the operator sets the *mean*. This is the ADLC premise made measurable: agents produce, humans operate, and how the human operates is the multiplier.

## 6. What the multi-wiki + symlink topology proved

- Per-service bounded contexts work: the repo-level pipeline ran entire features without the product vault in context.
- The seams are the weak points — traceability and staleness accumulate at wiki boundaries unless wrap-up runs on **both** sides; the checks (lint, records, board) are detective, not preventive.
- Session transcripts key on the launch directory, so usage ledgers are naturally per-repo — useful (product-level vs repo-level spend separates cleanly), but there is no single cross-repo cost view without aggregation.

## Review method (repeatable)

Two parallel read-only explorations (flow-trace over both wiki logs + plans; duplication analysis with a/b/c classification: hard copy / summarized overlap / clean pointer) plus the per-repo usage ledgers. ~240K subagent output tokens total; the main context received only the two condensed reports.
