---
name: wiki-query
description: "Answer questions using the Obsidian wiki vault and (when present) the graphify code graph. Reads hot cache first, routes code-structural questions to graphify-out/graph.json via graphify CLI, narrative questions to wiki pages. Synthesizes answers with citations. Files good answers back as wiki pages. Supports quick, standard, and deep modes. Triggers on: what do you know about, query:, what is, explain, summarize, find in wiki, search the wiki, based on the wiki, wiki query quick, wiki query deep, what calls X, where is X defined, how does A connect to B."
---

# wiki-query: Query the Wiki

The wiki has already done the synthesis work. Read strategically, answer precisely, and file good answers back so the knowledge compounds.

---

## Query Modes

Three depths. Choose based on the question complexity.

| Mode | Trigger | Reads | Token cost | Best for |
|------|---------|-------|------------|---------|
| **Quick** | `query quick: ...` or simple factual Q | hot.md + index.md only | ~1,500 | "What is X?", date lookups, quick facts |
| **Standard** | default (no flag) | hot.md + index + 3-5 pages (or graph commands) | ~3,000 | Most questions |
| **Deep** | `query deep: ...` or "thorough", "comprehensive" | Full wiki + optional web | ~8,000+ | "Compare A vs B across everything", synthesis, gap analysis |

---

## Code-Structural Questions: Consult the Graph First

**If `graphify-out/graph.json` exists in the project AND the question is code-structural, route to graphify before reading wiki pages.**

The graph carries the truth about *what calls what* — at a fraction of the token cost of reading source files. The wiki carries the truth about *why decisions were made*. Both layers, different purposes.

### Routing decision

A question is **code-structural** (consult the graph) if it asks about:

- **Calls / dependencies**: "what calls X?", "what does X depend on?", "where is Y used?"
- **Connections**: "how does A connect to B?", "what's between auth and the database?"
- **Definitions / locations**: "where is X defined?", "what file holds Y?"
- **Cluster / module questions**: "what's in the auth module?", "what does the contact form pipeline include?"

A question is **narrative** (skip the graph, go straight to wiki) if it asks about:

- "Why did we pick X?" — rationale lives in `wiki/decisions/`
- "What's our consent strategy?" — concepts in `wiki/concepts/`
- "What's the project about?" — context in `wiki/index.md`, `wiki/sources/`
- "What changed last week?" — operational state in `wiki/log.md`, git history

When in doubt, check `wiki/hot.md` first — its graph snapshot lists god nodes and community labels, which tells you whether the entities mentioned in the question even exist in the graph.

### Three graph primitives — prefer the dedicated skills

claude-mem ships three skills that wrap graphify's query side. **Use them when the user invokes them directly** (or when the question maps cleanly to one shape):

| User question shape | Skill to dispatch |
|---|---|
| "What is X?" / "What does X touch?" / single-node lookup | [`graphify-explain`](../graphify-explain/SKILL.md) |
| "How does A reach B?" / two-node trace | [`graphify-path`](../graphify-path/SKILL.md) |
| Open-ended: "what's in the auth area?" / "what touches the database?" | [`graphify-query`](../graphify-query/SKILL.md) |

Each skill handles its own interpreter resolution and graph-existence checks. **From `wiki-query`, you can shell out directly** when ambient routing makes sense (no need to invoke the skill machinery for a single CLI call):

```bash
# Resolve interpreter (same pattern the dedicated skills use)
PYTHON=""
PIN_FILE="graphify-out/.graphify_python"
if [ -f "$PIN_FILE" ]; then
    PINNED=$(cat "$PIN_FILE")
    [ -x "$PINNED" ] && "$PINNED" -c "import graphify" 2>/dev/null && PYTHON="$PINNED"
fi
[ -z "$PYTHON" ] && for cand in python3 python; do
    command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import graphify" 2>/dev/null && { PYTHON="$cand"; break; }
done
[ -z "$PYTHON" ] && { echo "graphify not installed. Install: pip install graphifyy"; exit 1; }

# Pick one of the three primitives based on the question shape
$PYTHON -m graphify explain "submitToHubSpot"
$PYTHON -m graphify query "auth refresh" --budget 1500
$PYTHON -m graphify path "ContactForm" "HubSpot Forms API v3"
```

Read the output as plain text — graphify formats it for an LLM to consume directly.

### After consulting the graph

The graph tells you the **structure**. To explain *what it means*, also read:

1. The relevant `wiki/code/_COMMUNITY_NN_*.md` page — community summary with cluster context
2. Any `wiki/decisions/*.md` that mentions the entities — the *why* behind the structure
3. Raw source files — last resort, when the graph + wiki page lack detail

### Citation format

When the answer used the graph, cite it explicitly:

> `submitToHubSpot()` is called by `onSubmit` in `ContactForm.tsx`. The function lives in cluster *Contact Form Submission Pipeline* (community 14, cohesion 0.25).
>
> _(Sources: `graphify-out/graph.json` via `graphify explain "submitToHubSpot"`; cluster: [[code/_COMMUNITY_14_contact_form_submission_pipeline]])_

---

## Quick Mode

Use when the answer is likely in the hot cache or index summary.

1. Read `wiki/hot.md`. If it answers the question, respond immediately.
2. If not, read `wiki/index.md`. Scan descriptions for the answer.
3. If found in index summary, respond and do not open any pages.
4. If not found, say "Not in quick cache. Run as standard query?"

Do not open individual wiki pages in quick mode.

---

## Standard Query Workflow

1. **Read** `wiki/hot.md` first. It may already have the answer, AND its graph snapshot tells you which entities exist in the code graph.
2. **Decide**: code-structural or narrative? (See routing decision above.)
3a. If **code-structural** AND `graphify-out/graph.json` exists:
    - Run the appropriate `graphify explain | query | path` command
    - Read the relevant `wiki/code/_COMMUNITY_*.md` for cluster context
    - Read `wiki/decisions/` only if the question asks *why*, not *what*
3b. If **narrative**:
    - Read `wiki/index.md`, scan for relevant pages
    - Read 3–5 wiki pages, follow wikilinks to depth 2 for key entities
4. **Synthesize** the answer in chat. Cite sources — wikilinks for wiki pages, command output for graph queries.
5. **Offer to file** the answer: "This analysis seems worth keeping. Should I save it as `wiki/questions/answer-name.md`?"
6. If the question reveals a **gap**: say "I don't have enough on X. Want to find a source?"

---

## Deep Mode

Use for synthesis questions, comparisons, or "tell me everything about X."

1. Read `wiki/hot.md` and `wiki/index.md`.
2. Identify all relevant sections (concepts, entities, sources, comparisons).
3. Read every relevant page. No skipping.
4. If wiki coverage is thin, offer to supplement with web search.
5. Synthesize a comprehensive answer with full citations.
6. Always file the result back as a wiki page. Deep answers are too valuable to lose.

---

## Token Discipline

Read the minimum needed:

| Start with | Cost (approx) | When to stop |
|------------|---------------|--------------|
| hot.md | ~500 tokens | If it has the answer |
| `graphify explain "X"` | ~50–200 tokens | For "what is X / what touches X" — almost always enough |
| `graphify path "A" "B"` | ~100 tokens | When the question is about a specific dependency chain |
| `graphify query "..."` | up to `--budget` (default 2000) | For broader code-structural questions; lower budget when possible |
| index.md | ~1000 tokens | If you can identify 3-5 relevant pages |
| `wiki/code/_COMMUNITY_*.md` | ~200 tokens each | After a graph query, for cluster context |
| 3-5 narrative wiki pages | ~300 tokens each | Usually sufficient for *why* questions |
| 10+ wiki pages | expensive | Only for synthesis across the entire wiki |

If hot.md has the answer, respond without reading further. If a `graphify` command answers a code-structural question with a single cluster summary, do not also read source files — the graph already cited them.

---

## Index Format Reference

The master index (`wiki/index.md`) looks like:

```markdown
## Domains
- [[Domain Name]]: description (N sources)

## Entities
- [[Entity Name]]: role (first: [[Source]])

## Concepts
- [[Concept Name]]: definition (status: developing)

## Sources
- [[Source Title]]: author, date, type

## Questions
- [[Question Title]]: answer summary
```

Scan the section headers first to determine which sections to read.

---

## Domain Sub-Index Format

Each domain folder has a `_index.md` for focused lookups:

```markdown
---
type: meta
title: "Entities Index"
updated: YYYY-MM-DD
---
# Entities

## People
- [[Person Name]]: role, org

## Organizations
- [[Org Name]]: what they do

## Products
- [[Product Name]]: category
```

Use sub-indexes when the question is scoped to one domain. Avoid reading the full master index for narrow queries.

---

## Filing Answers Back

Good answers compound into the wiki. Don't let insights disappear into chat history.

When filing an answer:

```yaml
---
type: question
title: "Short descriptive title"
question: "The exact query as asked."
answer_quality: solid
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [question, <domain>]
related:
  - "[[Page referenced in answer]]"
sources:
  - "[[wiki/sources/relevant-source.md]]"
status: developing
---
```

Then write the answer as the page body. Include citations. Link every mentioned concept or entity.

After filing, add an entry to `wiki/index.md` under Questions and append to `wiki/log.md`.

---

## Gap Handling

If the question cannot be answered from the wiki:

1. Say clearly: "I don't have enough in the wiki to answer this well."
2. Identify the specific gap: "I have nothing on [subtopic]."
3. Suggest: "Want to find a source on this? I can help you search or process one."
4. Do not fabricate. Do not answer from training data if the question is about the specific domain in this wiki.
