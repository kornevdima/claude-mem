---
name: project-profile
description: >
  Build or refresh AGENTS.md for a project. Combines mechanical extraction
  (build/test/lint commands, configs) via the mechanical-scanner subagent with a
  short structured tribal-knowledge interview. Output is AGENTS.md-spec compatible
  so it works across Codex, Cursor, Copilot, Aider, and Claude Code. Designed for
  brownfield repos where new code should match existing conventions. Trigger phrases:
  /project-profile, set up agents.md, build project profile, init project context,
  create AGENTS.md, scan project conventions, brownfield setup.
---

# project-profile: Build the Calibration Artifact

This skill creates `AGENTS.md` (and the `.agents/rules/` scaffolding) for a project. The output is the **calibration layer** that helps coding agents — Claude Code, Codex, Cursor, Copilot, Aider, etc. — produce code that fits the host project's conventions.

The design is informed by the [[Project Profile Skill Suite]] and the empirical findings in [[evaluating-agents-md-eth]]. Key load-bearing constraints:

- **AGENTS.md auto-generated from configs is net-positive only when content is concrete.** Repository overviews are net-negative. Cut them.
- **Tribal knowledge is the only consistent positive.** Interview the human; don't guess.
- **Specific actionable directives outperform descriptive prose 1.6×** in agent compliance.
- **Cross-tool standard is AGENTS.md.** Don't invent a claude-mem-specific format.

## When to invoke

- A project has no `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or `CONVENTIONS.md` and the user wants agent context set up.
- A brownfield repo where new code should match existing conventions.
- The user says "/project-profile", "set up AGENTS.md", "init project context", "scan project conventions".

Do NOT invoke for:
- Greenfield empty repos (no conventions exist yet — wait until there's something to capture).
- Pure docs-only repos (no build/test commands to extract).

## Modes (this version implements first-run only)

| Mode | What runs | Status |
|---|---|---|
| **first-run** | Full setup: mechanical scan + tribal interview + write (or **augment**, non-destructively) AGENTS.md and `.agents/rules/_index.md` | **Implemented** |
| **refresh** | Re-scan mechanical sections only, show diff, leave tribal sections untouched | Not yet (deferred) |
| **status** | Show rule count, pruning candidates, conflicts | Not yet (deferred) |

## Steps to follow when invoked

### Step 0 — Resolve target path

If the user gave a path, use it. Otherwise use the current working directory.

```bash
TARGET="${1:-$PWD}"
TARGET=$(cd "$TARGET" && pwd)  # absolutize
```

If `$TARGET` isn't a directory, abort with a clear error.

### Step 1 — Detect existing context files

Check for any of:

- `$TARGET/AGENTS.md`
- `$TARGET/CLAUDE.md`
- `$TARGET/.cursorrules` or `$TARGET/.cursor/rules/`
- `$TARGET/CONVENTIONS.md` (Aider's format)

If `AGENTS.md` already exists, **stop** and ask the user:

> "AGENTS.md already exists at $TARGET. First-run can **augment** it non-destructively: I'll back it up to `AGENTS.md.bak`, refresh the mechanical sections from a fresh scan, merge in your tribal answers, and preserve verbatim every section I don't own. Options: (1) back up and augment, (2) cancel."

Default to (2) cancel unless the user explicitly says proceed. When the user proceeds, **hold onto the existing file's full contents** — Step 5 merges the composed sections *into* it rather than replacing it, and Step 7 backs it up before writing. Never discard the existing content on this path.

If `CLAUDE.md` / `.cursorrules` / `CONVENTIONS.md` exist but no `AGENTS.md`, note them in the output and proceed — we'll cross-reference and not duplicate their content.

### Step 2 — Dispatch mechanical-scanner subagent

Dispatch ONE `mechanical-scanner-subagent` (defined in `agents/mechanical-scanner-subagent.md`):

```
Agent tool call:
  subagent_type: "mechanical-scanner-subagent"
  description: "Scan project configs for AGENTS.md mechanical sections"
  prompt: |
    target_path: <TARGET absolute path>
    existing_agents_md: <"none" or contents of existing AGENTS.md if any>
```

Wait for the subagent's response. It returns a structured markdown summary in its message — there's no file output for this scanner.

Parse the response. Extract:
- The "Detected stack" block (for the user's situational awareness)
- The "Proposed AGENTS.md sections" block (for composition into the final file)
- "Notes for the main agent" (surface to the user before the interview)

### Step 3 — Show the user what was detected

Print a brief summary to the user, like:

```
Detected: TypeScript / Next.js / pnpm / vitest / eslint
Test command (from CI): pnpm test --reporter verbose
Lint command: pnpm lint
Build: pnpm build
Notes from scanner:
  - Two test commands found (unit + e2e). Recommend noting both.
  - .nvmrc pins Node 22.
```

Then prompt:

> "Mechanical sections look right? [y / edit]"

If the user wants to edit, accept their inline edits before proceeding. Don't write to disk yet.

### Step 4 — Tribal interview

Conduct a SHORT structured interview. Ask one question at a time, accept free-form answers, allow "skip" or "n/a" for each. Limit to these four questions — do not extend:

> Q1: **Anything I should never touch?** (Examples: legacy modules, generated code, vendored libs. Free-form, or "none".)
>
> Q2: **Use X not Y rules?** (Examples: "use httpx not requests", "Result types not exceptions", "no print() in production code". Free-form list, or "none".)
>
> Q3: **Code generations to mark?** (For brownfield repos with multiple eras of code. Format: `current: <glob>; legacy: <glob>; transitional: <glob>`. Or "none".)
>
> Q4: **Style for new code (vs legacy)?** (One or two sentences on what new code should look like. Or "none".)

If the user gives "none" / "skip" to all four, that's fine — proceed with mechanical-only AGENTS.md. The point of asking is to give the human a chance to add the only kind of content empirically known to help.

### Step 5 — Compose AGENTS.md

Build the file in this exact structure. **Do not add a "Project overview" section** (AGENTbench: net-negative). **Do not paraphrase README.**

```markdown
# AGENTS.md

> Cross-tool agent context for this project. Read by Codex, Cursor, Copilot, Aider, Claude Code, and other AGENTS.md-compatible agents.

## Build & Test

[mechanical-scanner output, exact commands]

## Linting & Formatting

[mechanical-scanner output, exact commands]

## Language Version

[from mechanical-scanner if detected; omit section otherwise]

## Code Generations

[from Q3 if user provided; omit section otherwise]

Example:
- Current style: src/api/v3/**, src/services/v3/**
- Legacy (do not copy patterns from): src/legacy/**, src/api/v1/**
- Transitional: src/api/v2/** (reference only, not as analogue)

## Conventions

[combined from Q1, Q2, Q4 if user provided; omit section if all "none"]

Format each as a concrete directive. Examples:
- Never modify src/legacy/* — being deprecated.
- Use httpx, not requests.
- Use Result types in src/api/v3/**, not exceptions.
- New components go in src/components/v3/. Match the patterns there, not in src/legacy/components/.

## Rules

Detailed rules live in `.agents/rules/` (one rule per file, see `_index.md`). Use the `/capture-rule` skill to add a new rule from a productive chat.

## Cross-references

[only include if other context files were detected in Step 1]

- `CLAUDE.md` — Claude Code tool-specific notes
- `.cursor/rules/` — Cursor tool-specific rules
- `CONVENTIONS.md` — superseded; consider migrating into this file
```

The seven headings above are the **skill-owned sections** — the only ones this skill generates or rewrites: `Build & Test`, `Linting & Formatting`, `Language Version`, `Code Generations`, `Conventions`, `Rules`, `Cross-references`.

**If there is NO existing AGENTS.md** (the clean-slate case), write exactly the template above and skip to Step 6.

**If an existing AGENTS.md was detected in Step 1** (the augment path), do NOT emit the bare template — it would drop the user's custom content (this is [[Project Profile Skill Suite]] DEFECT-001). Instead **merge** the composed sections into the existing file:

1. Split the existing file into a preamble (the title line and anything above the first `##`) plus its `##` sections, keeping their original order.
2. **Skill-owned sections** that appear in the existing file: replace the body.
   - Mechanical sections (`Build & Test`, `Linting & Formatting`, `Language Version`) → the fresh scan output (configs are the source of truth; the scan wins).
   - `Conventions` and `Code Generations` → the **union** of the existing directives and the new interview answers, deduplicated, existing directives preserved. Never silently drop a directive the user already had.
3. **Skill-owned sections missing** from the existing file → append them (only the non-empty ones), following the template's section order.
4. **Every other `##` section** — anything not in the skill-owned set (e.g. `wiki/` topology, ADLC, project-specific sections) — **preserve verbatim, in its original position and order.** These are the sections the scan can't reproduce; losing them is the defect. When unsure whether a heading is skill-owned, treat it as foreign and preserve it.
5. Keep the preamble; if the existing preamble differs from the template's one-line banner, keep the existing one.

Target length: under 2K tokens total for the **skill-owned** content. If the file exceeds 3K tokens, push back: AGENTbench shows costs ramping without benefits beyond ~2K. On the augment path the cap applies to skill-owned sections only — never truncate a preserved foreign section to hit a token target.

### Step 6 — Create .agents/rules/ scaffolding

```bash
mkdir -p "$TARGET/.agents/rules"
```

Write `$TARGET/.agents/rules/_index.md` as an empty index:

```markdown
---
type: index
title: "Project Rules Index"
updated: <YYYY-MM-DD today>
---

# Project Rules Index

Rules captured via `/capture-rule`. One rule per file. The evaluator reads this index to detect conflicts cheaply.

| Rule | Scope | Created | One-line summary |
|---|---|---|---|
| (none yet) | | | |
```

### Step 7 — Show the user the proposed AGENTS.md

Print the full proposed AGENTS.md to the user. Prompt:

> "Looks good? [Accept / Edit / Reject]"

- **Accept**: on the augment path, first back up the existing file — copy `$TARGET/AGENTS.md` to `$TARGET/AGENTS.md.bak` (if `.bak` already exists, use `.bak.1`, `.bak.2`, … so no prior backup is clobbered). Then write the composed/merged content to `$TARGET/AGENTS.md`. Confirm both paths (and the backup) on the augment path; just the path on the clean-slate path.
- **Edit**: accept inline edits, then write (same backup step on the augment path).
- **Reject**: don't write anything; report "AGENTS.md not created." (No backup is made — nothing was touched.)

### Step 8 — Append to wiki/log.md (if claude-mem wiki present)

If `$TARGET/wiki/log.md` exists, prepend a log entry:

```markdown
## [YYYY-MM-DD] project-profile | First-run setup
- Type: skill execution
- Created: AGENTS.md, .agents/rules/_index.md          # clean-slate path
- Detected stack: <one-line summary from scanner>
- Tribal answers given: <count of non-"none" responses>
- Existing context files cross-referenced: <CLAUDE.md, .cursorrules, etc., or "none">
```

On the augment path, record it as a merge instead of a creation:

```markdown
## [YYYY-MM-DD] project-profile | First-run augment
- Type: skill execution
- Augmented: AGENTS.md (backed up to AGENTS.md.bak); created .agents/rules/_index.md
- Detected stack: <one-line summary from scanner>
- Tribal answers given: <count of non-"none" responses>
- Skill-owned sections refreshed: <list>
- Foreign sections preserved: <list, or "none">
```

If no claude-mem wiki present, skip this step. The skill is useful in projects without a wiki too.

### Step 9 — Report to the user

Brief confirmation:

```
project-profile complete:
  $TARGET/AGENTS.md (NN tokens)
  $TARGET/.agents/rules/_index.md (empty)

Next steps:
  - Use the project normally; agents will read AGENTS.md upfront.
  - When you correct an agent's behavior in chat into the right pattern,
    run /capture-rule to crystallize the lesson.
```

## Hard rules

1. **Never write AGENTS.md without explicit user accept.** Step 7 is mandatory.
2. **Never paraphrase README into AGENTS.md.** AGENTbench: net-negative.
3. **Never invent commands.** If the scanner reports "(not detected)", leave the slot honest.
4. **Cap at 4 tribal questions.** Adding more burns user patience without proportional gain.
5. **Default to "skip" being acceptable.** Mechanical-only AGENTS.md is still useful.
6. **Never drop a section you don't own.** When augmenting an existing AGENTS.md, preserve every foreign `##` section verbatim and back the file up before writing. Overwriting custom sections with a mechanical-only template is DEFECT-001 — the exact regression this skill must not reintroduce.

## Known limitations (intentional, deferred)

- **No dedicated refresh mode yet.** When configs drift, re-running first-run now **augments** safely (mechanical sections refresh from the fresh scan; foreign sections are preserved; the prior file is backed up to `.bak`) — no hand-merge required. A dedicated `--refresh` that shows a section-level diff and leaves tribal sections untouched is still deferred to step 4 of the implementation sequence.
- **No status mode yet.** No `--status` flag for rule-count/health output.
- **No per-subdirectory AGENTS.md.** Monorepos with multiple subprojects get only a root-level file.
- **No CLAUDE.md @path imports.** If user wants Claude Code to specifically link to AGENTS.md, they add the import manually.

## Connections

- [[Project Profile Skill Suite]] — design doc this implements
- [[Project Profile]] — broader concept
- [[AGENTS.md]] — output format spec
- [[evaluating-agents-md-eth]] — empirical caveats baked into this skill
- `agents/mechanical-scanner-subagent.md` — the subagent this skill dispatches
