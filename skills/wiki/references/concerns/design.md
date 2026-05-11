# Concern: Design / UX

Add when: the team has dedicated UX/UI designers producing structured design artifacts (specs, prototypes, user research). Skip when design is informal or lives entirely in external tools (Figma, Miro) without companion documentation.

## Folders

```
wiki/
├── designs/         # Design specs, component decisions, design system notes
└── user-research/   # Research synthesis, personas, usability findings
```

## Frontmatter — `wiki/designs/*.md`

```yaml
---
type: design
title: "..."
artifact_type: spec             # spec | component | flow | system | redline
status: in-review               # draft | in-review | approved | implemented | retired
designer: "..."
external_link: ""               # Figma / Miro / Sketch URL
related_modules: []             # wikilinks to wiki/modules/ or wiki/components/ (Mode B)
related_flows: []               # wikilinks to wiki/flows/ (Mode B)
release: ""                     # if tied to a specific release
tags: [design]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/user-research/*.md`

```yaml
---
type: user-research
title: "..."
method: interview               # interview | survey | usability-test | analytics-review | diary-study
date: YYYY-MM-DD
participants: 0
researcher: "..."
key_findings: []
related_designs: []
related_decisions: []           # decisions that cite this research
status: synthesized             # raw | synthesized | shared | archived
tags: [user-research]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Key wiki pages to create

`[[Design System Overview]]`, `[[Personas]]`, `[[Research Insights Summary]]`, `[[Design Decisions Log]]`.

## Patterns

- **Wiki holds the rationale, Figma holds the pixels**: design specs in `wiki/designs/` capture the "why" (decisions, trade-offs, constraints). The `external_link` points to the visual source-of-truth (Figma, etc.). Don't try to reproduce visuals in the wiki — link out.
- **Research as input to decisions**: `wiki/user-research/` findings should be cited in `wiki/decisions/` (Mode B) and `wiki/business-decisions/` (Mode C) when they shaped the choice. Bidirectional wikilinks make the impact traceable.
- **Cross-link to flows**: a design spec for a checkout flow links to `wiki/flows/checkout.md` (Mode B). Reading either side surfaces the other.
- **Skip raw transcripts**: ingest interview transcripts into `.raw/` and let wiki-ingest produce the synthesis page in `wiki/user-research/`. The transcript stays in `.raw/` (immutable source).
