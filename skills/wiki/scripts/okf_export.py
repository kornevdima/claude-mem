#!/usr/bin/env python3
"""Render the wiki vault as an Open Knowledge Format (OKF v0.1) bundle.

OKF (https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
is markdown + YAML frontmatter, one file per concept, cross-linked with normal
markdown links; ``type`` is the only required field. The vault already speaks
a superset of this, so the export is a mechanical transform:

  - copies ``wiki/**/*.md`` into the bundle, preserving folder structure
  - ensures ``type`` (defaulted from the parent folder), ``title`` (from the
    filename), ``description`` (first body paragraph when missing), and
    ``timestamp`` (mapped from ``updated:``/``created:``)
  - rewrites ``[[wikilinks]]`` to relative markdown links; unresolved targets
    degrade to plain text
  - skips loop-state artifacts (``_plan *``, ``_run *``) and ``wiki/meta/``
    (derived views: dashboards, lint reports, usage ledgers)

Attachments are not copied; the bundle is text-only. Stdlib only — no PyYAML.

Usage:
    python3 okf_export.py [vault_root] [-o OUTPUT_DIR]

Default output: <vault_root>/.raw/exports/okf/
"""

import argparse
import json
import os
import re
import sys

WIKILINK = re.compile(r"\[\[([^\]|#]+)(#[^\]|]*)?(?:\|([^\]]+))?\]\]")
SKIP_PREFIXES = ("_plan ", "_run ")

FOLDER_TYPES = {
    "concepts": "concept",
    "entities": "entity",
    "sources": "source",
    "questions": "question",
    "comparisons": "comparison",
    "requirements": "requirement",
    "user-stories": "user-story",
    "features": "feature",
    "decisions": "decision",
    "bugs": "bug",
}


def split_frontmatter(text):
    """Return (frontmatter_lines_or_None, body). Lossless: lines kept verbatim."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    fm = text[4:end].split("\n")
    body = text[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    return fm, body


def fm_value(fm_lines, key):
    for line in fm_lines:
        m = re.match(rf"^{key}:\s*(.*)$", line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return None


def first_paragraph(body):
    for raw in body.split("\n"):
        line = raw.strip()
        if not line or line.startswith(("#", ">", "```", "|", "---", "![", "- [[")):
            continue
        line = WIKILINK.sub(lambda m: (m.group(3) or m.group(1)).strip(), line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"[*_`]", "", line).strip()
        if len(line) > 20:
            return (line[:177] + "...") if len(line) > 180 else line
    return None


def build_page_map(vault, wiki_dir):
    """filename-stem (and frontmatter title) -> bundle-relative path."""
    pages = {}
    aliases = {}
    for root, dirs, files in os.walk(wiki_dir):
        dirs[:] = [d for d in dirs if d != "meta"]
        for f in sorted(files):
            if not f.endswith(".md") or f.startswith(SKIP_PREFIXES):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, wiki_dir)
            stem = f[:-3]
            pages.setdefault(stem, rel)
            try:
                with open(full, encoding="utf-8") as fh:
                    fm, _ = split_frontmatter(fh.read())
                title = fm_value(fm, "title") if fm else None
                if title and title != stem:
                    aliases.setdefault(title, rel)
            except OSError:
                pass
    # titles never shadow filenames
    for k, v in aliases.items():
        pages.setdefault(k, v)
    return pages


def rewrite_links(body, page_map, self_rel, stats):
    self_dir = os.path.dirname(self_rel)

    def repl(m):
        target, alias = m.group(1).strip(), (m.group(3) or m.group(1)).strip()
        rel = page_map.get(target)
        if rel is None:
            stats["unresolved"] += 1
            return alias
        stats["rewritten"] += 1
        href = os.path.relpath(rel, self_dir) if self_dir else rel
        return f"[{alias}]({href.replace(os.sep, '/')})"

    return WIKILINK.sub(repl, body)


def export_page(src, rel, out_dir, page_map, stats):
    with open(src, encoding="utf-8") as fh:
        text = fh.read()
    fm, body = split_frontmatter(text)
    if fm is None:
        fm = []
    added = []
    folder = rel.split(os.sep)[0] if os.sep in rel else ""
    stem = os.path.basename(rel)[:-3]
    if fm_value(fm, "type") is None:
        added.append(f"type: {FOLDER_TYPES.get(folder, folder or 'page')}")
    if fm_value(fm, "title") is None:
        added.append(f"title: {json.dumps(stem)}")
    if fm_value(fm, "description") is None:
        desc = first_paragraph(body)
        if desc:
            added.append(f"description: {json.dumps(desc)}")
    if fm_value(fm, "timestamp") is None:
        ts = fm_value(fm, "updated") or fm_value(fm, "created")
        if ts:
            added.append(f"timestamp: {ts}")
    stats["fields_added"] += len(added)
    fm_out = "\n".join(fm + added)
    body_out = rewrite_links(body, page_map, rel, stats)
    dest = os.path.join(out_dir, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(f"---\n{fm_out}\n---\n\n{body_out}" if fm_out else body_out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("vault", nargs="?", default=".", help="vault root (default: .)")
    ap.add_argument("-o", "--output", default=None, help="output dir (default: <vault>/.raw/exports/okf)")
    args = ap.parse_args()

    vault = os.path.abspath(args.vault)
    wiki_dir = os.path.join(vault, "wiki")
    if not os.path.isdir(wiki_dir):
        sys.exit(f"No wiki/ under {vault} — not a vault root?")
    out_dir = os.path.abspath(args.output or os.path.join(vault, ".raw", "exports", "okf"))

    page_map = build_page_map(vault, wiki_dir)
    stats = {"pages": 0, "rewritten": 0, "unresolved": 0, "fields_added": 0}
    for stem_rel in sorted(set(page_map.values())):
        export_page(os.path.join(wiki_dir, stem_rel), stem_rel, out_dir, page_map, stats)
        stats["pages"] += 1

    print(f"OKF bundle: {out_dir}")
    print(
        f"  pages: {stats['pages']}  links rewritten: {stats['rewritten']}  "
        f"unresolved (kept as text): {stats['unresolved']}  frontmatter fields added: {stats['fields_added']}"
    )
    print("  skipped: wiki/meta/, _plan/_run artifacts, attachments (text-only bundle)")


if __name__ == "__main__":
    main()
