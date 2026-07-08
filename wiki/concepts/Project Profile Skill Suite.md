---
type: concept
title: "Project Profile Skill Suite"
complexity: advanced
domain: claude-mem
aliases:
  - "/project-profile design"
  - "Skill Suite Design"
created: 2026-05-09
updated: 2026-07-08
tags:
  - concept
  - design
  - skill-design
  - project-profile
  - implementation-plan
  - defect
status: developing
related:
  - "[[Project Profile]]"
  - "[[Feedback Loop for Project Profile]]"
  - "[[Rule Generation from Chat]]"
  - "[[Generator-Evaluator Pattern]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[AGENTS.md]]"
  - "[[Repo Map]]"
  - "[[graphify-integration]]"
  - "[[maintenance-triggers]]"
sources:
  - "[[evaluating-agents-md-eth]]"
  - "[[cursor-generate-rules]]"
  - "[[anthropic-context-engineering]]"
  - "[[anthropic-harness-design]]"
  - "[[reflexion-paper]]"
  - "[[agents-md-spec]]"
---

# Project Profile Skill Suite

End-to-end design for the skill suite that operationalizes the [[Project Profile]] concept. Five skills + three subagents + one hook. All open questions from the 2026-05-09 research passes resolved into concrete decisions. Status: design phase, ready for implementation sequencing.

## The suite at a glance

| Skill | Purpose | Cadence | Writes |
|---|---|---|---|
| `/project-profile` | First-time setup; refresh mechanical sections; show status | Once + occasional | `AGENTS.md`, `.agents/rules/_index.md` |
| `/capture-rule` | Turn a productive chat into a persistent rule | After each pattern emerges | `.agents/rules/<slug>.md`, updates index |
| `/list-rules` | Discover existing rules before proposing new ones | On demand | nothing (read-only) |
| `/prune-rules` | Remove stale, conflicting, or unused rules | Occasional | deletes / edits rule files |
| `/resolve-rule-conflicts` | (Optional) Multi-author conflict triage | When evaluator surfaces a conflict | edits rule files |

## File layout

```
project-root/
  AGENTS.md                         # canonical, root-level
  .agents/
    rules/
      _index.md                     # name + 1-line scope per rule (cheap discovery)
      use-pytest-not-unittest.md    # one rule per file, <80 lines
      no-cyclic-imports-v3.md
      legacy-modules-do-not-touch.md
      ...
  CLAUDE.md                         # tool-specific @path imports to AGENTS.md
  .cursor/rules/                    # tool-specific (if user has Cursor)
  graphify-out/                     # existing, optional
  wiki/                             # existing claude-mem narrative layer
```

**Why this layout**:

- `AGENTS.md` at root is the cross-tool standard ([[AGENTS.md]]).
- `.agents/rules/*.md` (one rule per file, <80 lines) follows the Cursor pattern ([[cursor-generate-rules]]) — each rule is PR-reviewable, length-capped, scoped.
- `_index.md` is the cheap discovery layer (~5 tokens per rule) the evaluator reads to detect conflicts at scale.
- Tool-specific files (`CLAUDE.md`, `.cursor/rules/`) only carry tool-specific extensions; the cross-tool truth is in `AGENTS.md`.

## Skill specs

### 1. `/project-profile`

**Modes** (auto-detected by what state exists):

- **First run** (no AGENTS.md): full setup flow.
- **Refresh** (AGENTS.md exists): re-scan mechanical sections only, show diff.
- **Status** (`--status` flag): rule count, pruning candidates, conflicts, drift signals.

**First-run flow**:

1. Detect existing `AGENTS.md` / `CLAUDE.md` / `.cursorrules` / `CONVENTIONS.md`. If any exist, augment rather than replace. ✅ **The shipped implementation now honors "augment": first-run on an existing `AGENTS.md` backs it up, refreshes the skill-owned sections, and preserves foreign sections verbatim — see [[#Known Defects]] → DEFECT-001 (Fixed).**
2. Dispatch `mechanical-scanner-subagent`: extracts build/test/lint commands from `package.json`, `Makefile`, `pyproject.toml`, CI configs, linter configs.
3. Show user the proposed mechanical sections of AGENTS.md. Edit / approve.
4. Conduct tribal interview (inline, not subagent):
   - "Anything I should never touch?"
   - "Use X not Y rules?" (free-form)
   - "Code generations to mark?" (current/legacy/transitional with glob patterns)
   - "Style for new code (vs legacy)?"
5. Write `AGENTS.md` + create empty `.agents/rules/_index.md`.

**Refresh flow**: steps 2, 3, 5 only.

**Status flow**: read `_index.md` and rule frontmatter, output a table.

### 2. `/capture-rule [optional description]`

**Trigger**: manual + retrospective. Engineer runs after a chat where they corrected agent behavior into the right pattern. Copies the Cursor model from [[cursor-generate-rules]].

**Flow**:

1. Read recent chat history.
2. Dispatch `rule-generator` subagent. Inputs: chat excerpt, `_index.md`, optional description. Outputs: proposed rule file (name, scope, body, motivating example).
3. Dispatch `rule-evaluator` subagent **in parallel**. Inputs: proposed rule + full rules index (cheap, ~5K tokens at 1000 rules) + relevant existing rule bodies (only those the index flags). Outputs: pass/fail/warn + critique.
4. Show engineer the diff: file path, rule body, motivating chat excerpt, evaluator critique. Three options: **Accept**, **Edit**, **Reject**.
5. If accepted: write `.agents/rules/<slug>.md`, update `_index.md`.

**Flags**: `--strict` / `--moderate` / `--permissive` (evaluator mode), `--dry-run` (preview without writing).

The Generator-Evaluator separation ([[Generator-Evaluator Pattern]]) is enforced by running them as **two separate subagent dispatches** with no shared context. Anthropic's harness-design article ([[anthropic-harness-design]]) labels this "a strong lever" against self-grading leniency.

### 3. `/list-rules [filter]`

Read-only. Reads `_index.md`. Optional filter by tag, file path glob, or text search. Output is a scannable table.

### 4. `/prune-rules`

**Trigger**: manual, when status command nudges or engineer wants cleanup.

**Flow**:

1. Read all rule files + `_index.md`.
2. Score each rule:
   - **Age**: when created? When last modified?
   - **Usage signal**: was it referenced in a chat in the last N days? (Requires opt-in tracking; default off.)
   - **Conflict**: is there a newer rule that supersedes it?
   - **Scope validity**: does the file pattern it scopes to still exist in the repo?
3. Output a list of candidates with reasons.
4. For each: engineer accepts deletion, rejects, or edits.
5. Update `_index.md` accordingly.

**Never automatic.** Engineer-confirmed every removal. This addresses the monotonic-growth problem identified in [[Feedback Loop for Project Profile]].

### 5. `/resolve-rule-conflicts`

Triggered by the evaluator surfacing a conflict during `/capture-rule`. Could also be standalone.

Shows both rules side-by-side with author and date. Engineer chooses:

- Scope each more narrowly
- Replace old (records `supersedes: rule-X` in new rule's frontmatter)
- Keep both with explicit precedence

## Subagents

| Subagent | Used by | Purpose |
|---|---|---|
| `mechanical-scanner-subagent` | `/project-profile` | Parse configs/CI/Makefile, extract commands |
| `rule-generator-subagent` | `/capture-rule` | Draft rule from chat context + index |
| `rule-evaluator-subagent` | `/capture-rule` | Independent quality/conflict check |

All three follow the existing claude-mem subagent pattern (isolated context, return condensed summary 1-2K tokens). `mechanical-scanner-subagent` could potentially run in parallel for monorepos (per-subdirectory).

## Hooks

| Hook | Action | Why |
|---|---|---|
| **SessionStart** | Load `AGENTS.md` and `_index.md` into context | Same pattern as `CLAUDE.md` autoload |
| (none) | No PostToolUse, no Stop, no PostCommit auto-rebuild | **Intentional**, matches existing claude-mem philosophy of explicit user control |

The SessionStart hook is the **only** automation. Everything else is explicit user trigger. This matches the existing `/graphify-update` design choice (manual control over auto-rebuild) noted in [[maintenance-triggers]].

## Cross-skill integration

- **`wiki-lint` extension**: add checks for AGENTS.md/rules consistency:
  - No duplication with wiki narrative
  - Rule scope globs still match real files
  - `_index.md` in sync with rule files
  - No content duplicated between `AGENTS.md` and individual rule files
- **`wiki-query` extension**: when answering convention questions, route to AGENTS.md + rules first, wiki narrative second.
- **`graphify` integration** (later): community labels can mark generation tags from AGENTS.md (`current` / `legacy` / `transitional`).

## Three key user flows

### Flow A — first time on a brownfield repo

```
$ /project-profile
  ▸ scanning configs...
  ▸ detected: pytest, ruff, npm scripts, GitHub Actions CI
  ▸ propose mechanical sections (shown)
  > [y/edit/n] y
  ▸ tribal interview:
    Q: Anything I should never touch?
    > src/legacy/* — being deprecated
    Q: Code generations? (current/legacy globs)
    > current: src/api/v3/**, legacy: src/api/v1/**, transitional: src/api/v2/**
    ...
  ▸ writing AGENTS.md (1.8K tokens)
  ▸ created .agents/rules/_index.md (empty)
  done
```

### Flow B — capture a rule mid-work

```
[in chat: engineer corrects agent to use Result types instead of exceptions]
[agent gets it right twice]
$ /capture-rule
  ▸ generator drafted: "Use Result types in src/api/v3/**, not exceptions"
  ▸ evaluator: PASS (no conflicts, 12 lines, scoped)
  ▸ proposed file: .agents/rules/use-result-types-v3.md
  ▸ motivating chat: [excerpt]
  > [Accept/Edit/Reject] a
  ▸ written; index updated
```

### Flow C — quarterly cleanup

```
$ /project-profile --status
  ▸ 47 rules, 3 unused >6mo, 1 potential conflict
  ▸ run /prune-rules to review
$ /prune-rules
  ▸ candidate 1: "use-typescript-strict" (created 2024-09, no chats reference it)
    > [delete/keep/skip] keep
  ...
```

## Resolved design decisions (recap)

From the discussion that produced this design:

| Question | Decision |
|---|---|
| AGENTS.md vs separate rule files | Hybrid: AGENTS.md root + `.agents/rules/*.md` (one per rule) |
| Evaluator token budget | Build `_index.md` (5 tokens per rule); evaluator reads index first |
| Evaluator failure handling | Fall back to human-only review; one auto-retry; never block engineer |
| Cross-skill consistency | AGENTS.md canonical, wiki references it, wiki-lint cross-checks |
| Prompt caching cost math | Caching changes "+20-23% per task" to ~"+2-3%"; design assumes caching on |
| Pruning trigger | Combined signals surfaced in `--status`; engineer-initiated only |
| Evaluator calibration | Three modes: strict / moderate (default) / permissive; per-call override |
| Multi-author conflict UX | Inline PR-review style; both rules surfaced, engineer resolves |
| Rule discoverability | `/list-rules` + inline overlap detection in `/capture-rule` proposal |
| Brownfield generation tagging | AGENTS.md `## Code generations` section + glob patterns now; graphify community tags later |

## Implementation sequence

Recommended order. Each ships independently.

1. **`/project-profile` first-run mode + `mechanical-scanner-subagent`.** Smallest useful skill; creates the artifact everything else builds on.
2. **`/list-rules` + `_index.md` writer.** Cheap. Needed before `/capture-rule` so the evaluator has something to read.
3. **`/capture-rule` + both subagents (`rule-generator-subagent`, `rule-evaluator-subagent`).** The big one; largest design surface.
4. **`/project-profile --status`.** Adds visibility once rules exist.
5. **`/prune-rules`.** Maintenance.
6. **`/resolve-rule-conflicts`.** Optional, deferrable until conflicts actually arise.
7. **SessionStart hook + wiki-lint / wiki-query integration.** Glue.

## Empirical caveats to remember during implementation

From [[evaluating-agents-md-eth]] (ETH Zurich AGENTbench, 2026):

- Repository overviews provide no measurable benefit. **Cut them from the AGENTS.md template.**
- LLM-generated content tends to duplicate README. **Mechanical scanner should focus on commands and configs, not prose.**
- Specific actionable directives (named tools, commands) outperform descriptive text. **Generator prompt should bias toward concrete.**
- Stronger models do not generate better context files. **Don't overthink the model choice for the generator subagent.**
- Agents re-read context they already have. **Mitigation deferred; not a blocker.**

## Open implementation questions

These remain open and will be resolved during implementation, not before:

1. Exact prompt for the tribal interview (length vs completeness trade-off).
2. Schema for rule frontmatter (scope, supersedes, author, created date).
3. Exact heuristics for the rule-evaluator's conflict detection (regex on scope globs? semantic comparison?).
4. Whether to add opt-in chat-reference tracking for the pruning "usage signal."
5. The `--status` output format (table, dashboard, summary).

None of these block the next step (implementation of `/project-profile` first-run).

## Known Defects

Defects found in the shipped implementation. Tracked here (this vault has no `defects/` folder) alongside the design they diverge from. Format: `DEFECT-NNN — one-line title`.

### DEFECT-001 — first-run overwrites an existing AGENTS.md instead of augmenting it

| Field | Value |
|---|---|
| Severity | **High** (data loss) |
| Status | **Fixed** — 2026-07-08, `skills/project-profile/SKILL.md` Step 5 augment path |
| Found | 2026-07-08, during a `/project-profile` first-run on a brownfield service repo whose `AGENTS.md` already carried `wiki/` + ADLC topology sections |
| Area | `skills/project-profile/SKILL.md` — first-run composition |

**Symptom.** On the "back up and proceed" path, first-run mode wrote a mechanical-only `AGENTS.md` (mechanical scan + tribal-interview output) and dropped the pre-existing custom sections.

**Root cause.** The design says first-run should *augment rather than replace* when a context file exists (this page's first-run flow, step 1). The skill's Step 1 guard even passes `existing_agents_md` into the `mechanical-scanner-subagent` — but the composition step writes from a fixed template and never merges that existing content back into the final file, so anything the scan + interview didn't reproduce is lost.

**Contradiction.** `skills/project-profile/SKILL.md` Step 1 correctly warns and defaults to *cancel*, but once the user chooses proceed the composed output silently ignores the "augment" intent recorded on this page — spec says augment, implementation replaces.

**Workaround.** Manual merge from the `.bak` file created by the "back up and proceed" option.

**Fix direction.** Composition must diff/merge the scanner + interview output into the existing `AGENTS.md`, preserving unrecognized sections — or, minimally, re-append them under a "Preserved from prior AGENTS.md" heading until the `--refresh` mode (implementation sequence step 4) lands.

**Fix (2026-07-08).** `skills/project-profile/SKILL.md` Step 5 now branches: with no existing file it writes the template as before; with an existing `AGENTS.md` it takes an **augment path** — split the existing file into `##` sections, replace the seven *skill-owned* sections (mechanical sections from the fresh scan; `Conventions` / `Code Generations` as a deduplicated union of old + new), and **preserve every foreign section verbatim in its original order**. Step 1 reframes the prompt as "back up and augment" (default cancel); Step 7 backs the file up to `AGENTS.md.bak` (`.bak.N` if taken) before writing; Step 8 logs it as an augment. Hard rule 6 encodes "never drop a section you don't own." The dedicated `--refresh` mode (section-level diff, tribal untouched) is still deferred, but the data-loss regression is closed — re-running first-run is now non-destructive.

## Connections

- [[Project Profile]] — the broader concept this implements
- [[Feedback Loop for Project Profile]] — the design synthesis for the feedback half
- [[Rule Generation from Chat]] — the pattern this skill suite operationalizes
- [[Generator-Evaluator Pattern]] — the trust-boundary architecture
- [[Context Engineering for Coding Agents]] — the principles
- [[AGENTS.md]] — the output format
- [[graphify-integration]] — the structural layer that complements this
- [[maintenance-triggers]] — the existing maintenance-trigger pattern this skill suite extends
