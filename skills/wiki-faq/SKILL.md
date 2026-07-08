---
name: wiki-faq
description: >
  In-session guided help for claude-mem. Answers questions about requirements
  (host tools, Python, Obsidian), the workflow (which skill when, end-to-end
  flows), troubleshooting (common errors and fixes), and terminology
  (glossary of claude-mem concepts). Reference docs hold canonical content;
  this skill routes the user's question to the right one and synthesizes a
  focused chat answer.
  Triggers on: "/wiki-faq", "how do I get started", "I'm new", "where do I start",
  "first time setup", "what is claude-mem", "what's the workflow",
  "explain the workflow", "what are the requirements", "what do I need",
  "why is X broken", "graphify isn't working", "hot cache not loading",
  "skills not appearing", "edge drop", "labels.json mismatch", "what is hot cache",
  "what is .raw", "what is a vault", "explain mode B", "explain mode ADLC", "what are concerns", "what is wrap-up", "agentic mode",
  "what is graphify", "wiki-faq", "claude-mem faq".
---

# wiki-faq: Guided Help for claude-mem

Help users understand what claude-mem is, what it requires, how the skills compose, and what to do when something breaks. Reference docs hold the canonical content; this skill routes the user's question to the right one and gives a distilled chat answer.

## Routing

Map the question to ONE of these reference files (or two for an open-ended overview):

| Question shape | Reference file |
|---|---|
| "How do I get started?", "what do I need?", "Python version?", "host tools?", "Obsidian setup?" | [`references/requirements.md`](references/requirements.md) |
| "What's the workflow?", "which skill when?", "end-to-end example", "how does this fit together?", "explain the layers" | [`references/workflow.md`](references/workflow.md) |
| "Why is graphify broken?", "hot cache not loading", "graphifyy not installed", "edge drop too high", "labels.json mismatch", "Python 3.14 issue" | [`references/troubleshooting.md`](references/troubleshooting.md) |
| "What is X?" where X is a claude-mem term (vault, .raw, hot cache, base mode, concerns, ADLC, wrap-up, community, label, AST, subagent, skill) | [`references/glossary.md`](references/glossary.md) |
| Open-ended overview ("explain claude-mem", "what is this", "I just installed it") | requirements + workflow combined |

If the question doesn't fit any of these, fall back to `wiki-query` for content questions, or ask the user to clarify.

## Steps

1. Classify the question (one of the five above).
2. Read the matching reference file (or two for an overview).
3. Synthesize a focused answer in chat. **Don't paste the reference verbatim** — distill it to what the user asked.
4. Cite the canonical source (skill file path, wiki concept page wikilink, or upstream doc URL) so the user can drill in.
5. If the answer points to an action ("run `/wiki`", "run `bin/setup-graphify.sh`"), name the skill or command so the user knows what to invoke next.

## Don't

- Don't ingest content into the wiki (that's `wiki-ingest`).
- Don't search the wiki for project-specific answers (that's `wiki-query`).
- Don't run diagnostic commands. Each operational skill (`/graphify-ingest`, `/graphify-update`, etc.) does its own checks; this skill is content-only. If a user asks "is graphify installed on this machine?", suggest they run `/graphify-ingest` or `bash bin/setup-graphify.sh` — those tools check and report.

## Output style

- **Short.** 5–15 lines for typical questions. The reference files are detailed; the chat answer is the distillation.
- **Specific.** "Run `bash bin/setup-graphify.sh /path/to/project`" beats "install graphify."
- **Linked.** Every claim points at a file path, skill name, or wikilink.
- **Directive.** Tell the user the next action, not just the explanation.

## When to update the references

The reference docs go stale when:

- A new skill is added or removed (update `workflow.md` skill grouping).
- A new requirement appears (Python version pin change, new host tool — update `requirements.md`).
- A new common failure mode emerges in user reports (add to `troubleshooting.md`).
- A new concept enters the project vocabulary (add to `glossary.md`).

Update the reference doc when you encounter the gap. The skill is meta — it documents the rest of claude-mem and needs to track its evolution.
