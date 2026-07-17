#!/usr/bin/env bash
# run-evals.sh — G1–G5 eval runner for the graphify skill suite
# (graphify-ingest, -query, -path, -explain, -update).
#
# Builds one persistent workspace from fixtures/demo-app, runs the pipeline in
# order (G2–G5 depend on G1's graph), grades via file checks + transcript regex.
#
# Usage:
#   ./run-evals.sh              # run all: G1 ingest, G2 query, G3 path, G4 explain, G5 update
#   ./run-evals.sh G1 G3        # subset (G1 must have run at least once before G2-G5)
#   ./run-evals.sh --dry-run    # print prompts, no API calls
#
# Env knobs:
#   CLAUDE_CMD      command to invoke (default: claude)
#   EVAL_MODEL      optional --model override
#   EVAL_MAX_TURNS  --max-turns cap (default: 80 for G1/G5, 25 for queries)
#   EVAL_WS         reuse an existing workspace instead of creating one
#   EVAL_PERMS      permission flags (default: --dangerously-skip-permissions —
#                   required because -p mode cannot answer approval prompts and the
#                   pipeline runs bash + plugin scripts. The workspace is a throwaway
#                   temp dir and the fixture is inert, so the blast radius is nil;
#                   set EVAL_PERMS="" to restore gates and watch it deadlock.)
#
# Preconditions: adlc plugin installed for the invoking user; graphifyy
# installed (bash bin/setup-graphify.sh). G1 makes heavy model calls (subagent
# extraction) — expect several minutes and real cost.

set -uo pipefail

EVALS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$EVALS_DIR/../../.." && pwd)"
FIXTURE="$EVALS_DIR/fixtures/demo-app"
RESULTS_DIR="$EVALS_DIR/results"
CLAUDE_CMD="${CLAUDE_CMD:-claude}"
EVAL_PERMS="${EVAL_PERMS---dangerously-skip-permissions}"
DRY_RUN=0
GRADE_ONLY=0
REQUESTED=()

for arg in "$@"; do
  case "$arg" in
    -n|--dry-run) DRY_RUN=1 ;;
    --grade-only) GRADE_ONLY=1 ;;
    G[1-5]) REQUESTED+=("$arg") ;;
    *) echo "unknown arg: $arg"; exit 2 ;;
  esac
done
[ ${#REQUESTED[@]} -eq 0 ] && REQUESTED=(G1 G2 G3 G4 G5)

mkdir -p "$RESULTS_DIR"

# ── workspace ─────────────────────────────────────────────────────────────────
if [ -n "${EVAL_WS:-}" ]; then
  WS="$EVAL_WS"
else
  WS_STATE="$RESULTS_DIR/.workspace"
  if [[ " ${REQUESTED[*]} " == *" G1 "* ]] || [ ! -f "$WS_STATE" ]; then
    WS=$(mktemp -d "${TMPDIR:-/tmp}/graphify-eval.XXXXXX")
    cp -R "$FIXTURE/." "$WS/"
    (cd "$WS" && git init -q && git add -A && git commit -qm "fixture baseline")
    echo "$WS" > "$WS_STATE"
    echo "workspace: $WS"
    bash "$REPO_ROOT/bin/setup-graphify.sh" "$WS" >/dev/null || { echo "graphifyy setup failed"; exit 1; }
  else
    WS=$(cat "$WS_STATE")
    echo "reusing workspace: $WS"
  fi
fi

run_case() { # id prompt max_turns
  local id="$1" prompt="$2" turns="${3:-25}" t="$RESULTS_DIR/$1.transcript.txt"
  if [ "$GRADE_ONLY" = 1 ]; then echo "== $id: grade-only (reusing $t)"; return 0; fi
  echo "== $id: running (turns<=$turns)"
  if [ "$DRY_RUN" = 1 ]; then echo "--- prompt ---"; echo "$prompt"; return 0; fi
  ( cd "$WS" && $CLAUDE_CMD -p "$prompt" --max-turns "$turns" \
      --add-dir "$REPO_ROOT" $EVAL_PERMS \
      ${EVAL_MODEL:+--model "$EVAL_MODEL"} ) > "$t" 2>&1
}

PASS=(); FAIL=()
ok()  { echo "   ✓ $1"; }
bad() { echo "   ✗ $1"; CASE_OK=0; }
tmatch() { grep -Eiq "$1" "$RESULTS_DIR/$2.transcript.txt"; }

grade_G1() {
  CASE_OK=1
  local g="$WS/graphify-out/graph.json"
  [ -f "$g" ] && python3 -c "
import json,sys
d=json.load(open('$g'))
nodes=d.get('nodes',[]); edges=d.get('links',d.get('edges',[]))
sys.exit(0 if len(nodes)>=10 and len(edges)>=8 else 1)" \
    && ok "graph.json valid with >=10 nodes / >=8 edges" || bad "graph.json missing/too small"
  [ -f "$WS/graphify-out/labels.json" ] && ok "labels.json written" || bad "labels.json missing"
  [ -f "$WS/graphify-out/GRAPH_REPORT.md" ] && ok "GRAPH_REPORT.md written" || bad "GRAPH_REPORT.md missing"
  ls "$WS/wiki/code/"_COMMUNITY_*.md >/dev/null 2>&1 && ok "community pages in wiki/code/" || bad "no _COMMUNITY_*.md pages"
}

grade_G2() {
  CASE_OK=1
  local hits=0
  for n in PaymentService process_payment PaymentRepo PaymentGateway charge refund; do
    tmatch "$n" G2 && hits=$((hits+1)); done
  [ $hits -ge 2 ] && ok "names >=2 payment-cluster nodes ($hits)" || bad "payment nodes not surfaced ($hits)"
  tmatch "ingest.*first|graph\.json (doesn'?t|not) exist" G2 && bad "claimed graph missing" || ok "used existing graph"
}

grade_G3() {
  CASE_OK=1
  tmatch "ingest.*first|graph\.json (doesn'?t|not) exist|graph doesn'?t exist" G3 && bad "claimed graph missing" || ok "used existing graph"
  tmatch "create_order" G3 && tmatch "send_email" G3 && ok "endpoints named" || bad "endpoints missing"
  tmatch "order_confirmation|Notifier|notification" G3 && ok "plausible intermediate hop shown" || bad "no intermediate hop"
}

grade_G4() {
  CASE_OK=1
  tmatch "ingest.*first|graph\.json (doesn'?t|not) exist|graph doesn'?t exist" G4 && bad "claimed graph missing" || ok "used existing graph"
  tmatch "OrderService" G4 && ok "node named" || bad "node not named"
  local hits=0
  for n in OrderRepo PaymentService Notifier create_order cancel_order; do
    tmatch "$n" G4 && hits=$((hits+1)); done
  [ $hits -ge 2 ] && ok "neighbors listed ($hits)" || bad "neighbors missing ($hits)"
}

grade_G5() {
  CASE_OK=1
  grep -q "LoyaltyService" "$WS/graphify-out/graph.json" 2>/dev/null \
    && ok "new node LoyaltyService in graph" || bad "LoyaltyService not in graph.json"
  # Inheritance mechanism check, not name immutability: the skill explicitly tells
  # Claude to CORRECT inherited labels whose members drifted, and a small graph
  # legitimately re-partitions when nodes are added. So require: >=1 old label
  # carried over verbatim (proves Jaccard inheritance executed) AND no bare
  # "Cluster N" placeholders left in labels.json (proves labeling completed).
  python3 -c "
import json,sys
old=json.load(open('$RESULTS_DIR/.labels_before.json'))
new=json.load(open('$WS/graphify-out/labels.json'))
oldn={str(v) for v in (old.values() if isinstance(old,dict) else old)}
newn={str(v) for v in (new.values() if isinstance(new,dict) else new)}
placeholders=[v for v in newn if v.startswith('Cluster ')]
sys.exit(0 if newn and len(oldn & newn) >= 1 and not placeholders else 1)" 2>/dev/null \
    && ok "label inheritance executed (>=1 carried over, no placeholders)" || bad "label inheritance broken or labeling incomplete"
  tmatch "restored [1-9][0-9]* cross-boundary edges|snapshotted.*restored" G5 \
    && ok "cross-boundary edge restoration ran" || bad "no evidence of edge restoration"
}

for id in "${REQUESTED[@]}"; do
  case "$id" in
    G1) run_case G1 "Build the code graph for this project: /graphify-ingest ." 80 ;;
    G2) run_case G2 "/graphify-query \"what touches the payment module?\"" 25 ;;
    G3) run_case G3 "/graphify-path \"create_order\" \"send_email\"" 25 ;;
    G4) run_case G4 "/graphify-explain \"OrderService\"" 25 ;;
    G5)
      if [ "$GRADE_ONLY" = 1 ]; then run_case G5 "" 0;
      else
      # Reset any degraded graph artifacts from a previous failed update attempt, so
      # each G5 run starts from the last committed (G1) graph and manifest.
      (cd "$WS" && git checkout -- graphify-out 2>/dev/null)
      cp "$WS/graphify-out/labels.json" "$RESULTS_DIR/.labels_before.json" 2>/dev/null || echo '{}' > "$RESULTS_DIR/.labels_before.json"
      if grep -q "LoyaltyService" "$WS/services/order_service.py" 2>/dev/null; then
        # Rerun on a reused workspace: loyalty already landed (and a prior aborted
        # update may have saved the manifest) — force a fresh detectable delta.
        echo "# touched for eval rerun $(date +%s)" >> "$WS/services/loyalty_service.py"
        (cd "$WS" && git add -A && git commit -qm "chore: touch loyalty for eval rerun")
      else
        cat > "$WS/services/loyalty_service.py" <<'PYEOF'
from repos.order_repo import OrderRepo

class LoyaltyService:
    def __init__(self):
        self.orders = OrderRepo()

    def award_points(self, user_id, order):
        return int(order.total() // 10)
PYEOF
        python3 - <<PYEOF
p="$WS/services/order_service.py"
s=open(p).read().replace("from services.notification_service import Notifier",
 "from services.notification_service import Notifier\nfrom services.loyalty_service import LoyaltyService")
s=s.replace("self.notifier = Notifier()","self.notifier = Notifier()\n        self.loyalty = LoyaltyService()")
s=s.replace("self.notifier.order_confirmation(order, charge)","self.notifier.order_confirmation(order, charge)\n        self.loyalty.award_points(order.user_id, order)")
open(p,"w").write(s)
PYEOF
        (cd "$WS" && git add -A && git commit -qm "feat: loyalty points")
      fi
      run_case G5 "The loyalty feature just landed. Update the code graph: /graphify-update ." 80
      fi ;;
  esac
  [ "$DRY_RUN" = 1 ] && continue
  echo "== $id: grading"
  "grade_$id"
  if [ "$CASE_OK" = 1 ]; then echo "   PASS"; PASS+=("$id"); else echo "   FAIL"; FAIL+=("$id"); fi
done

[ "$DRY_RUN" = 1 ] && exit 0
echo
echo "==== Summary ===="
echo "PASS: ${PASS[*]:-—}"
echo "FAIL: ${FAIL[*]:-—}"
echo "workspace kept at: $WS (transcripts in $RESULTS_DIR)"
[ ${#FAIL[@]} -eq 0 ]
