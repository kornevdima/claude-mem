#!/usr/bin/env python3
"""Generate wiki/index.json — a machine-readable locator mirror of the wiki.

Walks wiki/**/*.md (and services/*/wiki/**/*.md when --services is passed),
extracts a small frontmatter subset per page, and writes wiki/index.json.
Zero dependencies: parses only the flat YAML subset the wiki conventions use
(scalar `key: value` lines and block lists of `- item` / - "[[item]]").

Usage:
    python3 build_index_json.py [vault_root] [--services]

vault_root defaults to the current directory; it must contain wiki/.
The output is a locator, not content: grep/jq it to find pages, then read
the pages themselves. Records always win over the generated view.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Frontmatter keys worth indexing: identity, lifecycle, and the greppable
# ADLC trace fields. Everything else stays in the page.
SCALAR_KEYS = {
    "type", "title", "status", "created", "updated", "confidence",
    "req_id", "feature", "produced_by", "effort_estimate", "answer_quality",
}
LIST_KEYS = {"tags", "traces_to", "related"}

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


def parse_frontmatter(text):
    """Parse the flat YAML subset used by wiki conventions. Returns a dict."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    current_list = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if current_list is not None and re.match(r"^\s+-\s+", line):
            item = line.split("-", 1)[1].strip().strip('"').strip("'")
            m = WIKILINK.search(item)
            fm[current_list].append(m.group(1) if m else item)
            continue
        current_list = None
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if key in LIST_KEYS and value == "":
            current_list = key
            fm[key] = []
        elif key in SCALAR_KEYS and value:
            fm[key] = value.strip('"').strip("'")
        elif key in LIST_KEYS and value.startswith("["):
            fm[key] = [v.strip().strip('"').strip("'")
                       for v in value.strip("[]").split(",") if v.strip()]
    return fm


def index_wiki(wiki_dir, root):
    pages = []
    for md in sorted(wiki_dir.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        try:
            head = md.read_text(encoding="utf-8", errors="replace")[:4096]
        except OSError as e:
            print(f"skip {rel}: {e}", file=sys.stderr)
            continue
        fm = parse_frontmatter(head)
        entry = {"path": rel, "name": md.stem}
        entry.update(fm)
        pages.append(entry)
    return pages


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    include_services = "--services" in sys.argv
    root = Path(args[0]).resolve() if args else Path.cwd()
    wiki = root / "wiki"
    if not wiki.is_dir():
        sys.exit(f"No wiki/ under {root}")

    pages = index_wiki(wiki, root)
    if include_services:
        for svc_wiki in sorted(root.glob("services/*/wiki")):
            pages.extend(index_wiki(svc_wiki, root))

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "page_count": len(pages),
        "pages": pages,
    }
    target = wiki / "index.json"
    target.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print(f"Wrote {target.relative_to(root)}: {len(pages)} pages")


if __name__ == "__main__":
    main()
