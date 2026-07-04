#!/usr/bin/env python3
"""Generate wiki/meta/usage.md — token-usage rollup from Claude Code session transcripts.

Zero-dep. Scans the project's transcript directory (~/.claude/projects/<slug>/),
aggregates per-session token usage (main context + subagents, deduped by requestId),
and writes a derived wiki page. The ledger is cumulative: rows for sessions whose
transcripts were garbage-collected are preserved from the existing page, so history
survives transcript retention limits.

Host-local: transcripts exist only on the machine (and host app) that ran the
sessions. On hosts without ~/.claude/projects/ the script exits 0 with a notice.

Usage:
    python3 usage_report.py [project_root] [--transcripts DIR] [--out FILE]
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

MAX_LABEL = 70


def transcript_dir_for(project_root: Path) -> Path:
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(project_root.resolve()))
    return Path.home() / ".claude" / "projects" / slug


def iter_jsonl(path: Path):
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return


def usage_of(entry: dict) -> dict | None:
    msg = entry.get("message") or {}
    u = msg.get("usage")
    if not isinstance(u, dict):
        return None
    return {
        "input": u.get("input_tokens", 0) or 0,
        "output": u.get("output_tokens", 0) or 0,
        "cache_w": u.get("cache_creation_input_tokens", 0) or 0,
        "cache_r": u.get("cache_read_input_tokens", 0) or 0,
        "model": msg.get("model") or "?",
    }


def aggregate_file(path: Path):
    """Sum usage over one transcript file, deduping streamed chunks by requestId
    (the same requestId repeats with identical usage; last entry wins)."""
    by_request = {}
    first_ts = last_ts = None
    branch = ""
    label = ""
    for entry in iter_jsonl(path):
        ts = entry.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts
        branch = entry.get("gitBranch") or branch
        if not label and entry.get("type") == "user":
            content = (entry.get("message") or {}).get("content")
            if isinstance(content, list):
                content = next(
                    (b.get("text", "") for b in content
                     if isinstance(b, dict) and b.get("type") == "text"), "")
            if isinstance(content, str):
                text = content.strip()
                cmd = re.search(r"<command-name>([^<]+)</command-name>", text)
                if cmd:
                    args = re.search(r"<command-args>([^<]*)</command-args>", text)
                    label = re.sub(r"\s+", " ", f"{cmd.group(1)} {args.group(1) if args else ''}").strip()[:MAX_LABEL]
                elif text and not text.startswith("<") and not text.startswith("Caveat"):
                    label = re.sub(r"\s+", " ", text)[:MAX_LABEL]
        if entry.get("type") != "assistant":
            continue
        u = usage_of(entry)
        if u is None:
            continue
        key = entry.get("requestId") or entry.get("uuid")
        by_request[key] = u
    totals = {"input": 0, "output": 0, "cache_w": 0, "cache_r": 0}
    models = {}
    requests = 0
    for u in by_request.values():
        if u["model"] == "<synthetic>" or not any(u[k] for k in totals):
            continue  # harness-internal placeholder entries carry no usage
        requests += 1
        for k in totals:
            totals[k] += u[k]
        m = models.setdefault(u["model"], dict.fromkeys(totals, 0))
        for k in totals:
            m[k] += u[k]
    return {
        "totals": totals, "models": models, "requests": requests,
        "first_ts": first_ts, "last_ts": last_ts, "branch": branch, "label": label,
    }


def scan_sessions(tdir: Path):
    sessions = []
    agent_types = {}
    for f in sorted(tdir.glob("*.jsonl")):
        sid = f.stem
        main = aggregate_file(f)
        sub_totals = {"input": 0, "output": 0, "cache_w": 0, "cache_r": 0}
        sub_requests = 0
        for af in sorted((tdir / sid / "subagents").glob("agent-*.jsonl")):
            agg = aggregate_file(af)
            for k in sub_totals:
                sub_totals[k] += agg["totals"][k]
            sub_requests += agg["requests"]
            meta_path = af.with_name(af.stem + ".meta.json")
            atype = "unknown"
            if meta_path.exists():
                try:
                    atype = json.load(open(meta_path)).get("agentType") or "unknown"
                except (OSError, json.JSONDecodeError):
                    pass
            slot = agent_types.setdefault(atype, {"runs": 0, **dict.fromkeys(sub_totals, 0)})
            slot["runs"] += 1
            for k in sub_totals:
                slot[k] += agg["totals"][k]
        if main["requests"] == 0 and sub_requests == 0:
            continue
        sessions.append({
            "sid": sid, "main": main,
            "sub": {"totals": sub_totals, "requests": sub_requests},
        })
    return sessions, agent_types


def fmt(n: int) -> str:
    return f"{n:,}"


def parse_existing_ledger(out_path: Path):
    """Keep rows for sessions no longer on disk. Rows are keyed by the short sid
    in the second column; numeric columns are re-parsed for cumulative totals."""
    rows = {}
    if not out_path.exists():
        return rows
    in_ledger = False
    for line in out_path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "<!-- ledger -->":
            in_ledger = True
            continue
        if in_ledger:
            if not line.startswith("|"):
                if line.strip():
                    in_ledger = False
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 10 or cells[0] in ("date", ":---", "---") or set(cells[0]) <= {"-", ":"}:
                continue
            sid = cells[1].strip("`")
            rows[sid] = line
    return rows


def ledger_row(s: dict) -> str:
    main, sub = s["main"], s["sub"]
    date = (main["first_ts"] or "")[:10]
    t = {k: main["totals"][k] + sub["totals"][k] for k in main["totals"]}
    out_total = t["output"]
    sub_share = f"{sub['totals']['output'] * 100 // out_total}%" if out_total else "0%"
    models = ", ".join(sorted(m.split("-2")[0] for m in main["models"])) or "?"
    label = (s["main"]["label"] or "—").replace("|", "\\|")
    return (
        f"| {date} | `{s['sid'][:8]}` | {label} | {main['branch'] or '—'} | {models} "
        f"| {main['requests'] + sub['requests']} | {fmt(t['input'])} | {fmt(t['output'])} "
        f"| {fmt(t['cache_w'])} | {fmt(t['cache_r'])} | {sub_share} |"
    )


NUM_COLS = ("input", "output", "cache_w", "cache_r")


def totals_from_rows(rows: list[str]) -> dict:
    totals = dict.fromkeys(NUM_COLS, 0)
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        try:
            for key, cell in zip(NUM_COLS, cells[6:10]):
                totals[key] += int(cell.replace(",", ""))
        except (ValueError, IndexError):
            continue
    return totals


def render(sessions, agent_types, kept_rows, tdir):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fresh = {s["sid"][:8]: ledger_row(s) for s in sessions}
    all_rows = {**kept_rows, **fresh}
    rows_sorted = sorted(
        (r for r in all_rows.values() if any(totals_from_rows([r]).values())),
        key=lambda r: r.split("|")[1].strip(), reverse=True)
    totals = totals_from_rows(rows_sorted)

    per_model = {}
    for s in sessions:
        for m, u in s["main"]["models"].items():
            slot = per_model.setdefault(m, dict.fromkeys(NUM_COLS, 0))
            for k in NUM_COLS:
                slot[k] += u[k]

    top = sorted(sessions, key=lambda s: s["main"]["totals"]["output"] + s["sub"]["totals"]["output"],
                 reverse=True)[:5]

    lines = [
        "---",
        "type: meta",
        'title: "Token Usage"',
        f"updated: {now}",
        "tags:",
        "  - meta",
        "  - usage",
        "  - derived-view",
        "status: evergreen",
        "---",
        "",
        "# Token Usage",
        "",
        "> [!note] Derived, host-local view — regenerate, don't hand-edit.",
        f"> Built by `usage_report.py` from Claude Code transcripts (`{tdir}`).",
        "> Transcripts exist only on the machine that ran the sessions; teammates regenerate their own",
        "> (team-sync rule: regenerate-don't-merge). Ledger rows outlive transcript garbage-collection.",
        "> Reading the numbers: **output** and **cache write** are the expensive classes;",
        "> **cache read** is high-volume but ~10x cheaper than input; a high **sub %** means",
        "> subagent fan-out (not the main context) drove the spend.",
        "",
        "## Totals (cumulative, all ledger rows)",
        "",
        "| input | output | cache write | cache read |",
        "|---|---|---|---|",
        f"| {fmt(totals['input'])} | {fmt(totals['output'])} | {fmt(totals['cache_w'])} | {fmt(totals['cache_r'])} |",
        "",
        "## Top sessions by output tokens (transcripts currently on disk)",
        "",
        "| session | label | output (main+sub) |",
        "|---|---|---|",
    ]
    for s in top:
        out_sum = s["main"]["totals"]["output"] + s["sub"]["totals"]["output"]
        label = (s["main"]["label"] or "—").replace("|", "\\|")
        lines.append(f"| `{s['sid'][:8]}` | {label} | {fmt(out_sum)} |")
    lines += [
        "",
        "## By model (main context; transcripts currently on disk)",
        "",
        "| model | input | output | cache write | cache read |",
        "|---|---|---|---|---|",
    ]
    for m, u in sorted(per_model.items(), key=lambda kv: kv[1]["output"], reverse=True):
        lines.append(f"| {m} | {fmt(u['input'])} | {fmt(u['output'])} | {fmt(u['cache_w'])} | {fmt(u['cache_r'])} |")
    lines += [
        "",
        "## By subagent type (transcripts currently on disk)",
        "",
        "| agent type | runs | input | output | cache write | cache read |",
        "|---|---|---|---|---|---|",
    ]
    for atype, u in sorted(agent_types.items(), key=lambda kv: kv[1]["output"], reverse=True):
        lines.append(f"| {atype} | {u['runs']} | {fmt(u['input'])} | {fmt(u['output'])} "
                     f"| {fmt(u['cache_w'])} | {fmt(u['cache_r'])} |")
    if not agent_types:
        lines.append("| — | 0 | 0 | 0 | 0 | 0 |")
    lines += [
        "",
        "## Session ledger (cumulative; newest first)",
        "",
        "<!-- ledger -->",
        "| date | session | label | branch | models | requests | input | output | cache write | cache read | sub % |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
        *rows_sorted,
        "",
    ]
    return "\n".join(lines)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    project_root = Path(args[0]) if args else Path(".")
    tdir = None
    out_path = project_root / "wiki" / "meta" / "usage.md"
    for i, a in enumerate(argv):
        if a == "--transcripts" and i + 1 < len(argv):
            tdir = Path(argv[i + 1])
        if a == "--out" and i + 1 < len(argv):
            out_path = Path(argv[i + 1])
    tdir = tdir or transcript_dir_for(project_root)
    if not tdir.is_dir():
        print(f"No transcript dir at {tdir} — nothing to report (non-Claude-Code host?). Skipping.")
        return 0
    sessions, agent_types = scan_sessions(tdir)
    kept = parse_existing_ledger(out_path)
    for s in sessions:
        kept.pop(s["sid"][:8], None)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(sessions, agent_types, kept, tdir), encoding="utf-8")
    print(f"Wrote {out_path}: {len(sessions)} sessions on disk, {len(kept)} historic rows kept.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
