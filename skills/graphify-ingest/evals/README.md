# Graphify Suite Evals (G1–G5)

Covers all five graphify skills against one fixture project (`fixtures/demo-app`, 13-file Python shop app with deliberate clusters: routes → services → repos/models/utils).

| Case | Skill | What it proves | Key assertions |
|---|---|---|---|
| G1 | graphify-ingest | End-to-end graph build | `graph.json` (≥10 nodes, ≥8 edges), `labels.json`, `GRAPH_REPORT.md`, `wiki/code/_COMMUNITY_*.md` |
| G2 | graphify-query | BFS over payment cluster | ≥2 payment-cluster node names surfaced |
| G3 | graphify-path | `create_order` → `send_email` | endpoints + plausible intermediate hop (Notifier / order_confirmation) |
| G4 | graphify-explain | Node + neighbors | OrderService + ≥2 real neighbors |
| G5 | graphify-update | Incremental update, label preservation | new `LoyaltyService` node appears; ≥50% of old community labels carried over |

Run locally (needs installed adlc plugin + `bash bin/setup-graphify.sh` done once):

```bash
bash skills/graphify-ingest/evals/run-evals.sh            # full pipeline, G1 is the slow/expensive one
bash skills/graphify-ingest/evals/run-evals.sh G2 G3 G4   # re-query an existing workspace
bash skills/graphify-ingest/evals/run-evals.sh --dry-run  # inspect prompts only
```

G2–G5 reuse G1's workspace (path cached in `results/.workspace`). Transcripts land in `results/`. The sandbox can't run this suite — `graphifyy` isn't installable there — which is why this runner exists.
