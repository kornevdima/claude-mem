# Concern: Technical Writing / User Documentation

Add when: the project produces public-facing or external-user documentation (API reference, tutorials, end-user guides) maintained as a discipline distinct from engineering ADRs and code comments. Skip when all documentation is README-level or auto-generated only.

## Folders

```
wiki/
├── user-docs/    # End-user-facing guides, walkthroughs, conceptual explanations
├── api-docs/     # API reference, endpoint specs, SDK usage
└── tutorials/    # Step-by-step tutorials, getting-started guides, recipes
```

## Frontmatter — `wiki/user-docs/*.md`

```yaml
---
type: user-doc
title: "..."
audience: end-user              # end-user | admin | integrator | developer
artifact_type: guide            # guide | concept | reference | troubleshooting
status: published               # draft | review | published | retired
last_reviewed: YYYY-MM-DD
maintainer: "..."
related_features: []            # wikilinks to wiki/modules/ or wiki/flows/ (Mode B)
release: ""                     # if tied to a specific version
tags: [user-doc]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/api-docs/*.md`

```yaml
---
type: api-doc
title: "..."
endpoint: "..."                 # /api/v1/widgets, GET https://...
api_version: ""
auth_required: true
status: stable                  # alpha | beta | stable | deprecated
deprecation_date: ""            # if applicable
related_modules: []             # wikilinks to wiki/modules/ (Mode B)
example_request: ""
example_response: ""
tags: [api-doc]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/tutorials/*.md`

```yaml
---
type: tutorial
title: "..."
audience: end-user
difficulty: beginner            # beginner | intermediate | advanced
duration_min: 0
prerequisites: []               # wikilinks to other tutorials or user-docs
related_features: []
last_validated: YYYY-MM-DD      # when the steps were last actually run
status: published               # draft | published | retired
tags: [tutorial]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Key wiki pages to create

`[[User Documentation Overview]]`, `[[API Reference Index]]`, `[[Getting Started]]`, `[[Glossary]]`.

## Patterns

- **Audience drives folder choice**: `user-docs` and `tutorials` target end-users; `api-docs` target integrators. Don't mix — keep navigation predictable.
- **Cross-link to code**: every API doc references `wiki/modules/` (Mode B) where the code lives. When a module changes, agents looking at the module page see linked API docs that may need refresh.
- **`last_validated` matters more than `updated`**: tutorials drift fastest. The `last_validated` field tracks when someone actually ran the steps end-to-end. Lint can flag tutorials past a stale threshold.
- **Don't duplicate the source**: API specs may live in OpenAPI / GraphQL schema files alongside code. `wiki/api-docs/` is for the human-friendly companion (when to use, gotchas, examples), not a re-render of the schema.
- **Public vs internal**: this concern targets public-facing docs. Internal engineering wikis (Mode B's `decisions/`, `flows/`) stay where they are. If you also need internal product docs, that's Mode C, not this concern.
