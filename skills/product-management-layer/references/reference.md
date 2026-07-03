# Product Management Layer — Artifact Templates

Canonical formats for every Gate 0 artifact. Copy the relevant block, fill it in, present it, and on approval write it to the `governance/` registry (see SKILL.md → Registry & Persistence). Keep IDs stable (SKILL.md → ID Scheme).

---

## 1. Intake Form (INTAKE mode)

```markdown
### Intake — <UC-id>: <use case name>

- **Use case:** <one sentence — what job is being done>
- **Requested tool / vendor:** <name>  (<TL-id>)
- **Requested by / owner:** <name>
- **Risk class:** low | medium | high            <!-- data sensitivity + blast radius -->
- **Data policy touched:** <e.g. customer PII, none, internal only>  [TBD]
- **Alternatives already considered:** <list or "none yet">
- **Target decision date:** <YYYY-MM-DD>
```

On approval, open an ApprovalEntry (§2, status `proposed`) and a compliance stub (§5, class `[TBD]`).

---

## 2. Approval Registry (INTAKE mode → `approval-registry.md`)

One row per **use case × tool** pair. An entry never transfers to another pair.

```markdown
| AP-id | UC-id | Tool (TL-id) | Use case | Status | Compliance (CC-id) | Reviewer | Approved | Expires |
|-------|-------|--------------|----------|--------|--------------------|----------|----------|---------|
| AP-UC001-TL003 | UC-001 | Arize (TL-003) | LLM eval dashboards | approved | CC-002 | <owner> | 2026-07-03 | 2027-07-03 |
```

**Status values:** `proposed` → `approved` → `under-review` → `expired` / `retired`.
- `under-review` is set automatically-by-rule when an acquisition/sunset ReviewTrigger fires (§7). Attach a Migration Checklist (§7a).
- An approval within 60 days of `Expires` shows in STATUS as "near expiry".

---

## 3. Vendor Viability Scorecard (VENDOR-REVIEW mode → `vendor-scorecards/<tool>.md`)

```markdown
### <TL-id> <tool> — viability <score>/100 · lifecycle: <active|at-risk|sunset|acquired>

| Dimension | Weight | Score (1-5) | Notes |
|-----------|--------|-------------|-------|
| Financial stability / funding runway | 20% | | |
| Adoption & community / customer base | 15% | | |
| Roadmap & release cadence | 15% | | |
| Support & SLA quality | 15% | | |
| Data portability / exit difficulty | 20% | | |
| Security & compliance posture | 15% | | |

- **Weighted viability score:** <0-100>
- **Lifecycle status:** active | at-risk | acquired | sunset
- **Exit plan (exitPlanRef):** <link or "none — [TBD]">  <!-- how we leave, and cost to leave -->
- **Re-review cadence:** <e.g. every 6 months>  ·  **Next review:** <YYYY-MM-DD> (owner: <name>)
```

Anti-Magic: "next review" is a dated, owned reminder — not automatic.

---

## 4. Buy-vs-Build TCO Comparison (BUY-VS-BUILD mode → `buy-vs-build/<BB-id>.md`)

Always include a **Do-Nothing** baseline and any **already-owned** asset as options.

```markdown
### <BB-id> — Buy vs Build: <capability> for <UC-id>

| Option | Type | Yr-1 cost | 3-yr TCO | Time to value | Key risk | Exit difficulty |
|--------|------|-----------|----------|---------------|----------|-----------------|
| Do nothing | baseline | 0 | 0 | n/a | gap persists | n/a |
| Use <owned tool> | adopt-owned | <sunk> | <sunk+ops> | days | feature fit | low |
| Buy <vendor> | buy | | | weeks | lock-in | med/high |
| Build in-house | build | | | months | maintenance load | low |

**TCO includes:** license/subscription + implementation + integration + ongoing ops/maintenance + exit/migration.

- **Recommendation:** <option> — <one-paragraph why, referencing the numbers>
- **If architectural,** the decision needs a shift-left **ADR** (route down; do not write it here). ADR ref: <ADR-NNN or [TBD]>
- **Owner decision:** <requested / <name> chose <option> on <YYYY-MM-DD>>
```

End by asking the owner to decide.

---

## 5. Compliance Classification Sheet (COMPLIANCE-SCOPE mode → `compliance/<UC-id>.md`)

One sheet **per use case × tool pair**. Two use cases on the same tool get two sheets.

```markdown
### <CC-id> — Compliance scope: <UC-id> × <TL-id>

- **Compliance class:** public | internal | confidential | regulated
- **Data-policy flags:** [ ] PII  [ ] PHI  [ ] payment  [ ] source-secrets  [ ] none
- **Residency / retention constraints:** <e.g. EU-only, 30-day retention> [TBD]
- **Sub-processor / data-sharing note:** <does the vendor process our data? where?>
- **Controls required before approval:** <e.g. DPA signed, SSO, audit log>
- **Scoped by:** <name> on <YYYY-MM-DD>
```

Never inherit a class across use cases — re-scope each pair.

---

## 6. Asset Register (REGISTRY-STATUS / INTAKE → `asset-register.md`)

```markdown
| AS-id | Subscription / license | Owner | Annual cost | Renews | Utilization | Approval (AP-id) | Flag |
|-------|------------------------|-------|-------------|--------|-------------|------------------|------|
| AS-004 | Arize seat ×5 | <owner> | $X | 2027-01-15 | 1/5 used | AP-UC001-TL003 | underused |
| AS-005 | <tool> | <owner> | $Y | <date> | none 90d | — | SHELFWARE |
```

**Rule:** an AssetRecord with no linked ApprovalEntry, or 0 utilization, is **shelfware** — attach a renewal or cancel action and surface it in STATUS.

---

## 7. Review Trigger Log (VENDOR-REVIEW mode → `review-triggers.md`)

```markdown
| RT-id | Tool (TL-id) | Type | Fired | Detail | Dependent approvals | Action |
|-------|--------------|------|-------|--------|---------------------|--------|
| RT-002 | TL-007 | sunset | 2026-07-03 | vendor EOL announced for 2026-12 | AP-UC004-TL007 | migrate before EOL |
```

**Trigger types:** `acquisition` · `sunset` · `newUseCase` · `expiry`.
- `acquisition` / `sunset` → set every dependent ApprovalEntry to `under-review` (§2) and attach a Migration Checklist (§7a).
- `newUseCase` → open a fresh intake (a new use case × tool pair is not covered by an existing approval).
- `expiry` → the approval must be re-reviewed before its `Expires` date.

### 7a. Migration Checklist (attached when acquisition/sunset fires)

```markdown
### Migration — <RT-id>: off <tool> for <UC-id>

- [ ] Confirm affected use cases and approvals (<AP-ids>)
- [ ] Export / secure our data (portability check from §3 exit plan)
- [ ] Shortlist replacements → run BUY-VS-BUILD (§4)
- [ ] Compliance re-scope for the replacement (§5)
- [ ] Cutover plan + drop-dead date <YYYY-MM-DD>
- [ ] Retire old subscription (update §6, cancel to avoid shelfware)
```

---

## 8. Decision Log (all modes → `decision-log.md`, append-only)

New entries at the **top**. Never edit past entries.

```markdown
## [YYYY-MM-DD] <DL-id> — <decision title>
- **Decision:** <what was decided>
- **Mode / trace:** <mode> · <AP/BB/CC/RT ids>
- **Owner:** <name>
- **Rationale:** <one or two sentences>
- **Follow-up:** <handoff to shift-left Gate 1 / migration / renewal / none>
```

---

## 9. Portfolio STATUS Report (REGISTRY-STATUS mode)

```markdown
### Governance portfolio status — <YYYY-MM-DD>

**Approvals near expiry (≤60d):**
| AP-id | Tool | Use case | Expires | Action |

**Open review triggers:**
| RT-id | Tool | Type | Fired | Action |

**Shelfware / underused assets:**
| AS-id | Subscription | Annual cost | Why flagged | Action |

**Recent decisions:** <last 3 DL-ids>

**Next best action:** <the single most important thing to do now>
```

---

## 10. Handoff Packet (down to shift-left Gate 1)

Produced when a use case × tool is approved. Give it to the shift-left advisor as a Gate 1 input.

```markdown
### Handoff → shift-left Gate 1

- **Use case (UC-id):** <name + one sentence>
- **Approved tool (TL-id):** <name>
- **Approval (AP-id):** <status approved, expires YYYY-MM-DD>
- **Compliance class (CC-id):** <class + data-policy flags that become security requirements>
- **Constraints to carry into requirements:** <residency, retention, controls>
- **Ask:** "Write Gate 1 requirements for <use case> using <tool>; treat the compliance controls as SRs; trace back to <AP-id>."
```

Keep the packet's language governance-side; shift-left turns it into FRs/NFRs/SRs.
