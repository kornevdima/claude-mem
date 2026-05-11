# claude-mem

Claude + Obsidian knowledge companion. A running notetaker that builds and maintains a persistent, compounding wiki vault. Every source you add gets integrated. Every question you ask pulls from everything that has been read.

Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Code-graph layer powered by [graphify](https://github.com/safishamsi/graphify). Zero manual filing.

## What It Does

Drop sources into `.raw/`. Claude reads them, extracts entities and concepts, updates cross-references, and files everything into a structured Obsidian vault.

Ask questions. Claude reads the hot cache, scans the index, drills into relevant pages, and cites specific wiki pages.

Run `lint the wiki` to find orphans, dead links, stale claims, and missing cross-references.

At the end of every session, Claude updates a hot cache so the next session starts with full recent context.

## Install

Pick the method that matches your goal.

### Persistent install — every Claude Code session

Local-marketplace install. The plugin is registered globally; skills appear under the `claude-mem:` namespace in every session.

```bash
claude plugin marketplace add /path/to/claude-mem
claude plugin install claude-mem@claude-obsidian-marketplace
claude plugin list
```

After editing source files: `claude plugin marketplace update claude-obsidian-marketplace` then `/reload-plugins` in-session.

### Active development — fastest edit-test loop

Per-session, no install. Edits picked up by `/reload-plugins` immediately.

```bash
claude --plugin-dir /path/to/claude-mem
```

### Other options

- **Cowork zip upload** — zip the repo and upload via Cowork UI (no CLI required).
- **GitHub-hosted marketplace** — push to GitHub, then `claude plugin marketplace add <github-url>` in any project.

### Vault setup

Open the project folder in Obsidian (Obsidian creates a fresh `.obsidian/` config on first open), then run `/wiki` (or `/claude-mem:wiki` when installed as a plugin) inside Claude Code. The wiki skill scaffolds the vault structure on first use. No bundled plugins or themes — install whatever you want from Obsidian's community marketplace.

### Code-graph setup (optional, for code projects)

If you plan to use `graphify-ingest` / `graphify-update` on a codebase, install the Python backend once. The skills will detect and pin it on first use, but running this upfront is faster and gives clear errors if your Python is incompatible (`graphifyy` requires `>=3.10,<3.14`):

```bash
bash bin/setup-graphify.sh                     # install graphifyy globally
bash bin/setup-graphify.sh /path/to/your-app   # also pin to a specific code project
```

## Skills

| Skill | Trigger |
|---|---|
| `/wiki` | Setup, scaffold, route to sub-skills |
| `ingest [source]` | Single or batch source ingestion |
| `query: [question]` | Answer from wiki content |
| `lint the wiki` | Health check |
| `/wiki-faq` | In-session help: requirements, workflow, troubleshooting, glossary |
| `/save` | File the current conversation as a wiki note |
| `/autoresearch [topic]` | Autonomous research loop: search, fetch, synthesize, file |
| `obsidian-markdown` | Reference for correct Obsidian Flavored Markdown |
| `obsidian-bases` | Create and edit `.base` files (Obsidian's database layer) |
| `graphify-ingest` | Build a structural code graph for a project, file summaries into `wiki/code/` |
| `graphify-update` | Incrementally rebuild the code graph after a feature; preserves community labels via Jaccard matching |
| `graphify-query` | Free-form BFS/DFS traversal of the code graph (no LLM cost) |
| `graphify-path` | Shortest path between two named graph nodes |
| `graphify-explain` | One node + immediate neighbors with edge confidences |

## Commands

| You say | Claude does |
|---|---|
| `/wiki` | Setup check, scaffold, or continue where you left off |
| `ingest [file]` | Read source, create wiki pages, update index and log |
| `ingest all of these` | Batch process multiple sources, then cross-reference |
| `what do you know about X?` | Read index, drill into relevant pages, synthesize answer |
| `/save` | File the current conversation as a wiki note |
| `/autoresearch [topic]` | Run the autonomous research loop |
| `lint the wiki` | Health check: orphans, dead links, gaps, suggestions |
| `/wiki-faq` | "How do I...?", "what's the workflow?", "why is X broken?" — guided help |
| `/graphify-ingest` | Build code structure graph (AST + semantic), file into `wiki/code/` |
| `/graphify-update` | Incremental update: re-extract changed files only, preserve labels |
| `/graphify-query "..."` | BFS/DFS the code graph — "what touches X", "explore the auth area" |
| `/graphify-path "A" "B"` | Shortest path between two graph nodes |
| `/graphify-explain "X"` | Node summary + edges (cheapest first-look query) |

## Cross-Project Access

Point any other project at this vault. Add to that project's `AGENTS.md`:

```markdown
## Wiki Knowledge Base
Path: ~/path/to/vault

When you need context not already in this project:
1. Read wiki/hot.md first (recent context cache)
2. If not enough, read wiki/index.md
3. If you need domain details, read the relevant domain sub-index
4. Only then drill into specific wiki pages
```

## Vault Structure

```
.raw/           source documents (immutable)
wiki/           Claude-generated knowledge base
_attachments/   images and PDFs referenced by wiki pages
```

## Wiki Modes and Concerns

A vault has **one base mode** plus **zero or more opt-in concerns**.

### Base modes

| Mode | Use when |
|---|---|
| **B: Repository** | Code projects: architecture, modules, flows, ADRs, dependencies |
| **C: Business / Project** | Product docs: stakeholders, decisions, deliverables, intel, comms |
| **B+C** | A repo that's also the working surface for product/business documentation (developers + BA on the same project) |

### Concerns (opt-in folder kits for SDLC roles)

| Concern | Folders added | Role |
|---|---|---|
| `ops` | `runbooks/`, `incidents/`, `services/`, `observability/` | DevOps / SRE |
| `qa` | `test-plans/`, `test-cases/`, `bugs/`, `coverage/` | QA / QC / Test |
| `sec` | `threat-models/`, `compliance/`, `security-decisions/` | Security |
| `design` | `designs/`, `user-research/` | UX |
| `writing` | `user-docs/`, `api-docs/`, `tutorials/` | Technical writers |

A solo dev picks `B`. A platform team picks `B + ops + qa`. A regulated SaaS picks `B+C + ops + qa + sec`. Concerns are about **artifacts**, not roles — skip a concern if the role exists informally without producing structured documentation. Per-concern reference docs (folder map, frontmatter, key pages) live in [`skills/wiki/references/concerns/`](skills/wiki/references/concerns/). Design rationale at [`wiki/concepts/SDLC Wiki Concerns.md`](wiki/concepts/SDLC%20Wiki%20Concerns.md).

The original LLM Wiki pattern by Andrej Karpathy defined six modes (also covering Website, Personal, Research, Book / Course). The full pattern is preserved at [`.raw/llm-wiki-pattern-spec.md`](.raw/llm-wiki-pattern-spec.md); only B and C are actively scaffolded by the `wiki` skill.

## License

MIT. See [LICENSE](LICENSE) and [ATTRIBUTION.md](ATTRIBUTION.md).
