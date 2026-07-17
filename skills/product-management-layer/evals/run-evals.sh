#!/usr/bin/env bash
# run-evals.sh — E1–E8 eval runner for the product-management-layer skill.
#
# Each case in cases/E*.md defines a Prompt plus Must match / Must not match
# regex assertions (one POSIX extended regex per line; HTML comments ignored).
# The runner builds a throwaway workspace with the fixture registry (dates
# substituted relative to today), drives one non-interactive `claude -p` turn
# in it, then grades the transcript + the registry diff.
#
# Usage:
#   ./run-evals.sh                 # run and grade all 8 cases
#   ./run-evals.sh E1 E5           # run a subset
#   ./run-evals.sh --dry-run       # print substituted prompts, no API calls
#   ./run-evals.sh --grade-only E3 # re-grade existing results/ output
#
# Env knobs:
#   CLAUDE_CMD      command to invoke (default: claude) — add flags here if needed
#   EVAL_MODEL      optional --model override
#   EVAL_MAX_TURNS  --max-turns cap per case (default: 25)
#
# Precondition: the adlc plugin (product-management-layer skill) must be
# installed for the invoking user — the scratch workspace has no plugin config.
# Running all 8 cases makes 8 real model calls; expect cost and a few minutes.

set -uo pipefail

EVALS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CASES_DIR="$EVALS_DIR/cases"
FIXTURES_DIR="$EVALS_DIR/fixtures/governance"
RESULTS_DIR="$EVALS_DIR/results"
CLAUDE_CMD="${CLAUDE_CMD:-claude}"
EVAL_MAX_TURNS="${EVAL_MAX_TURNS:-25}"

DRY_RUN=0
GRADE_ONLY=0
REQUESTED=()

for arg in "$@"; do
  case "$arg" in
    -n|--dry-run) DRY_RUN=1 ;;
    -g|--grade-only) GRADE_ONLY=1 ;;
    E[1-8]) REQUESTED+=("$arg") ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

# --- dates (BSD/macOS and GNU) -------------------------------------------
date_offset() { # $1 = signed day count, e.g. +45 or -90
  if date -v+1d +%F >/dev/null 2>&1; then
    date -v"${1}d" +%F
  else
    date -d "${1} days" +%F
  fi
}
TODAY="$(date +%F)"
PLUS_30D="$(date_offset +30)"
PLUS_45D="$(date_offset +45)"
PLUS_60D="$(date_offset +60)"
PLUS_400D="$(date_offset +400)"
MINUS_90D="$(date_offset -90)"
MINUS_320D="$(date_offset -320)"

subst_dates() { # stdin -> stdout
  sed -e "s/{{TODAY}}/$TODAY/g" \
      -e "s/{{PLUS_30D}}/$PLUS_30D/g" \
      -e "s/{{PLUS_45D}}/$PLUS_45D/g" \
      -e "s/{{PLUS_60D}}/$PLUS_60D/g" \
      -e "s/{{PLUS_400D}}/$PLUS_400D/g" \
      -e "s/{{MINUS_90D}}/$MINUS_90D/g" \
      -e "s/{{MINUS_320D}}/$MINUS_320D/g"
}

# --- case-file parsing -----------------------------------------------------
extract_section() { # $1 = case file, $2 = section heading text
  awk -v h="## $2" '
    $0 == h { on = 1; next }
    /^## /  { if (on) exit }
    on      { print }
  ' "$1"
}

# Emit assertion regexes: skip blanks and <!-- ... --> comment blocks.
assertion_lines() { # $1 = case file, $2 = section heading
  local in_comment=0 line
  while IFS= read -r line; do
    if (( in_comment )); then
      [[ "$line" == *"-->"* ]] && in_comment=0
      continue
    fi
    if [[ "$line" == *"<!--"* ]]; then
      [[ "$line" != *"-->"* ]] && in_comment=1
      continue
    fi
    line="${line#"${line%%[![:space:]]*}"}"  # ltrim
    [[ -z "$line" ]] && continue
    printf '%s\n' "$line"
  done < <(extract_section "$1" "$2")
}

case_file_for() { # $1 = case id (E1..E8)
  local match
  match=$(find "$CASES_DIR" -maxdepth 1 -name "${1}-*.md" | head -1)
  [[ -n "$match" ]] && printf '%s\n' "$match"
}

# --- grading ---------------------------------------------------------------
grade_case() { # $1 = case id, $2 = blob file, $3 = case file; returns 0 on pass
  local ok=0
  while IFS= read -r rx; do
    if ! grep -Eq -- "$rx" "$2"; then
      echo "    MISS (must match): $rx"
      ok=1
    fi
  done < <(assertion_lines "$3" "Must match")
  while IFS= read -r rx; do
    if grep -Eq -- "$rx" "$2"; then
      echo "    HIT (must NOT match): $rx"
      ok=1
    fi
  done < <(assertion_lines "$3" "Must not match")
  return $ok
}

# --- main loop ---------------------------------------------------------------
mkdir -p "$RESULTS_DIR"
[[ ${#REQUESTED[@]} -eq 0 ]] && REQUESTED=(E1 E2 E3 E4 E5 E6 E7 E8)

declare -a PASSED FAILED SKIPPED
for id in "${REQUESTED[@]}"; do
  case_file="$(case_file_for "$id")"
  if [[ -z "$case_file" ]]; then
    echo "== $id: no case file found, skipping"
    SKIPPED+=("$id")
    continue
  fi

  prompt="$(extract_section "$case_file" "Prompt" | subst_dates | awk 'NF {found=1} found')"

  if (( DRY_RUN )); then
    echo "== $id — $(basename "$case_file") =="
    echo "$prompt"
    echo
    continue
  fi

  out="$RESULTS_DIR/$id.out.md"
  diff_file="$RESULTS_DIR/$id.governance.diff"
  blob="$RESULTS_DIR/$id.blob.txt"

  if (( ! GRADE_ONLY )); then
    ws="$(mktemp -d "${TMPDIR:-/tmp}/pm-eval-$id.XXXXXX")"
    mkdir -p "$ws/docs/governance" "$ws/.pristine-governance"
    while IFS= read -r f; do
      rel="${f#"$FIXTURES_DIR"/}"
      mkdir -p "$ws/docs/governance/$(dirname "$rel")" "$ws/.pristine-governance/$(dirname "$rel")"
      subst_dates < "$f" > "$ws/docs/governance/$rel"
      cp "$ws/docs/governance/$rel" "$ws/.pristine-governance/$rel"
    done < <(find "$FIXTURES_DIR" -type f -name '*.md')

    echo "== $id: running (workspace: $ws)"
    (
      cd "$ws" &&
      $CLAUDE_CMD -p "$prompt" \
        --permission-mode acceptEdits \
        --max-turns "$EVAL_MAX_TURNS" \
        ${EVAL_MODEL:+--model "$EVAL_MODEL"}
    ) > "$out" 2> "$RESULTS_DIR/$id.err.log"
    rc=$?
    if (( rc != 0 )); then
      echo "    claude exited $rc — see $RESULTS_DIR/$id.err.log"
    fi
    diff -ru "$ws/.pristine-governance" "$ws/docs/governance" > "$diff_file" 2>/dev/null
  fi

  if [[ ! -s "$out" ]]; then
    echo "== $id: no transcript at $out — cannot grade"
    FAILED+=("$id")
    continue
  fi
  cat "$out" "$diff_file" 2>/dev/null > "$blob"

  echo "== $id: grading"
  if grade_case "$id" "$blob" "$case_file"; then
    echo "   PASS"
    PASSED+=("$id")
  else
    echo "   FAIL"
    FAILED+=("$id")
  fi
done

(( DRY_RUN )) && exit 0

echo
echo "==== Summary ===="
echo "PASS: ${PASSED[*]:-—}"
echo "FAIL: ${FAILED[*]:-—}"
[[ ${#SKIPPED[@]} -gt 0 ]] && echo "SKIP: ${SKIPPED[*]}"
[[ ${#FAILED[@]} -eq 0 ]]
