# Concern: Operations / SRE / DevOps

Add when: the project has production deployments, on-call rotation, or formal incident response. Skip when ops is informal and produces no structured artifacts.

## Folders

```
wiki/
├── runbooks/        # Step-by-step procedures for known operational tasks
├── incidents/       # Postmortems with blameless review structure
├── services/        # Service catalog: ownership, dependencies, on-call, SLOs
└── observability/   # Dashboard links, alert definitions, log queries
```

## Frontmatter — `wiki/runbooks/*.md`

```yaml
---
type: runbook
title: "..."
service: "..."                 # which service this runbook covers
severity: P0                   # P0 | P1 | P2 | P3
linked_alert: "..."            # alert/page that triggers this runbook
last_tested: YYYY-MM-DD
owner: "..."
status: active                 # active | deprecated | draft
tags: [runbook]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/incidents/*.md`

```yaml
---
type: incident
title: "..."                   # short, factual; avoid blame
date: YYYY-MM-DD
duration_min: 0
severity: P1
services_affected: []
trigger: "..."                 # what kicked it off
status: resolved               # investigating | mitigated | resolved
postmortem_status: published   # draft | reviewed | published
related_runbooks: []
related_decisions: []          # ADRs in wiki/decisions/ if a follow-up was filed
tags: [incident, postmortem]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/services/*.md`

```yaml
---
type: service
name: "..."
owner_team: "..."
on_call_rotation: "..."        # link to PagerDuty / Opsgenie / wiki page
dependencies: []               # wikilinks or service names
slos: []                       # short list, e.g. "99.9% availability", "p99 latency <200ms"
runbooks: []                   # wikilinks to relevant runbooks
status: active                 # active | sunsetting | deprecated
tags: [service]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/observability/*.md`

```yaml
---
type: observability
title: "..."
service: "..."
artifact_type: dashboard       # dashboard | alert | query | runbook-link
external_url: "..."            # link to Grafana / Datadog / Splunk
tags: [observability]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Key wiki pages to create

`[[Service Catalog]]`, `[[On-Call Rotation]]`, `[[Incident Response Playbook]]`, `[[Severity Definitions]]`, `[[Deployment Procedure]]`.

## Patterns

- **Alert → runbook link**: every paging alert should reference a runbook by wikilink. The runbook contains debugging steps, blast radius, and rollback procedure. (Source: [[sdlc-team-documentation-research]] / Google SRE Workbook.)
- **Blameless postmortems**: incidents go in `wiki/incidents/` regardless of root cause. The `postmortem_status` field tracks review lifecycle.
- **Service catalog as source of truth**: each service has one `wiki/services/<name>.md` page with ownership, dependencies, runbooks, SLOs. Cross-link from `wiki/modules/` (Mode B) where the code lives.
