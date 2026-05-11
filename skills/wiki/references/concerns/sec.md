# Concern: Security

Add when: the project has formal security review, threat modeling, or compliance frameworks (SOC 2, ISO 27001, HIPAA, PCI). Skip when security is purely "follow good practice" without recorded artifacts.

## Folders

```
wiki/
├── threat-models/        # Per-feature or per-system threat models (STRIDE, attack trees)
├── compliance/           # Compliance evidence and control mappings
└── security-decisions/   # Security ADRs separate from engineering ADRs
```

## Frontmatter — `wiki/threat-models/*.md`

```yaml
---
type: threat-model
title: "..."
system: "..."                   # what's being modeled
methodology: STRIDE             # STRIDE | PASTA | attack-tree | DREAD
date: YYYY-MM-DD
reviewers: []
threats_identified: 0
mitigations: []                 # wikilinks to ADRs / runbooks / code modules
residual_risk: low              # low | medium | high
status: current                 # draft | current | superseded
tags: [threat-model, security]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/compliance/*.md`

```yaml
---
type: compliance-control
title: "..."
framework: SOC2                 # SOC2 | ISO27001 | HIPAA | PCI | GDPR | other
control_id: "..."               # e.g. CC6.1, A.9.2.1
status: implemented             # not-started | in-progress | implemented | reviewed
evidence: []                    # wikilinks or external links
last_audit: YYYY-MM-DD
next_review: YYYY-MM-DD
owner: "..."
tags: [compliance]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Frontmatter — `wiki/security-decisions/*.md`

```yaml
---
type: security-decision
title: "..."
date: YYYY-MM-DD
status: accepted                # proposed | accepted | superseded
context: ""
decision: ""
consequences: ""
related_threat_models: []
related_compliance: []
supersedes: ""
tags: [security-decision, adr]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Key wiki pages to create

`[[Security Posture Overview]]`, `[[Threat Model Index]]`, `[[Compliance Status]]`, `[[Security Incident Playbook]]`.

## Patterns

- **Why split from `decisions/`**: engineering ADRs in `wiki/decisions/` (Mode B) and security decisions both follow the ADR format, but auditors and security reviewers want a single, separate folder. Keeping them split makes audit prep tractable.
- **Compliance evidence**: each control links to evidence (config screenshots, code commits, runbooks). The `evidence` array is what an auditor walks during review.
- **Cross-link with `ops`**: security incidents (data breach, auth compromise) live in `wiki/incidents/` (ops) but link to `wiki/security-decisions/` and `wiki/threat-models/` for context.
- **Threat models age out**: review when the system materially changes. The `status: superseded` flag keeps history without misleading new readers.
