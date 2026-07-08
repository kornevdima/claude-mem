---
name: wiki-ingest
description: "Ingest sources into the Obsidian wiki vault. Reads a source, extracts entities and concepts, creates or updates wiki pages, cross-references, and logs the operation. Supports files, URLs, and batch mode. Triggers on: ingest, process this source, add this to the wiki, read and file this, batch ingest, ingest all of these, ingest this url."
---

# wiki-ingest: Source Ingestion

Read the source. Write the wiki. Cross-reference everything. A single source typically touches 8-15 wiki pages.

**Syntax standard**: Write all Obsidian Markdown using proper Obsidian Flavored Markdown. Wikilinks as `[[Note Name]]`, callouts as `> [!type] Title`, embeds as `![[file]]`, properties as YAML frontmatter. If the kepano/obsidian-skills plugin is installed, prefer its canonical obsidian-markdown skill for Obsidian syntax reference. Otherwise, follow the guidance in this skill.

---

## Delta Tracking

Before ingesting any file, check `.raw/.manifest.json` to avoid re-processing unchanged sources.

```bash
# Check if manifest exists
[ -f .raw/.manifest.json ] && echo "exists" || echo "no manifest yet"
```

**Manifest format** (create if missing):
```json
{
  "sources": {
    ".raw/articles/article-slug-2026-04-08.md": {
      "hash": "abc123",
      "ingested_at": "2026-04-08",
      "pages_created": ["wiki/sources/article-slug.md", "wiki/entities/Person.md"],
      "pages_updated": ["wiki/index.md"]
    }
  }
}
```

**Before ingesting a file:**
1. Compute a hash: `md5sum [file] | cut -d' ' -f1` (or `sha256sum` on Linux).
2. Check if the path exists in `.manifest.json` with the same hash.
3. If hash matches, skip. Report: "Already ingested (unchanged). Use `force` to re-ingest."
4. If missing or hash differs, proceed with ingest.

**After ingesting a file:**
1. Record `{hash, ingested_at, pages_created, pages_updated}` in `.manifest.json`.
2. Write the updated manifest back.

Skip delta checking if the user says "force ingest" or "re-ingest".

---

## URL Ingestion

Trigger: user passes a URL starting with `https://`.

Steps:

1. **Fetch** the page using WebFetch (or your host's web-fetch tool).
2. **Derive slug** from the URL path (last segment, lowercased, spaces→hyphens, strip query strings).
3. **Save** to `.raw/articles/[slug]-[YYYY-MM-DD].md` with a frontmatter header:
   ```markdown
   ---
   source_url: [url]
   fetched: [YYYY-MM-DD]
   ---
   ```
4. Proceed with **Single Source Ingest** starting at step 2 (file is now in `.raw/`).

---

## Video / YouTube Ingestion

Trigger: user passes a YouTube (or other video) URL, or says "ingest this talk".

1. **Capture the transcript** with yt-dlp (subtitles only, never the video):
   ```bash
   yt-dlp --skip-download --write-subs --write-auto-subs --sub-lang "en.*" --sub-format vtt \
     -o ".raw/videos/%(title)s" "<url>"
   ```
   Uploaded subs (`--write-subs`) beat auto-subs when both exist.
2. **Clean the VTT**: strip cue numbers and timestamps; auto-subs repeat each line across overlapping cues — dedupe consecutive repeats; collapse into plain paragraphs.
3. **Save** the cleaned text to `.raw/yt-[slug].md` with frontmatter: `source_url`, `source_type: video-transcript`, `speaker`, `event` (if known), `fetched`, `source_language`.
4. Proceed with **Single Source Ingest** step 1. Caveat: auto-subs lack punctuation and mis-hear proper nouns — verify speaker / product / project names against the video page before creating entity pages, and mark uncertain ones `(sp?)` rather than guessing.

---

## Canonical Language

Wiki pages are authored in the vault's canonical language (the language of the existing wiki; default English), regardless of the source's language. `.raw/` files stay in their original language — never translate sources. Translate at the wiki layer: keep proper nouns and technical terms in original form where translation loses meaning, record `source_language:` in the source page frontmatter, and when exact wording matters, quote the original with a translation beside it. A vault that mixes page languages splits its search space and its wikilink graph.

---

## Image / Vision Ingestion

Trigger: user passes an image file path (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.avif`).

Steps:

1. **Read** the image file using the Read tool when your host supports vision on images.
2. **Describe** the image contents: extract all text (OCR), identify key concepts, entities, diagrams, and data visible in the image.
3. **Save** the description to `.raw/images/[slug]-[YYYY-MM-DD].md`:
   ```markdown
   ---
   source_type: image
   original_file: [original path]
   fetched: YYYY-MM-DD
   ---
   # Image: [slug]

   [Full description of image contents, transcribed text, entities visible, etc.]
   ```
4. Copy the image to `_attachments/images/[slug].[ext]` if it's not already in the vault.
5. Proceed with **Single Source Ingest** on the saved description file.

Use cases: whiteboard photos, screenshots, diagrams, infographics, document scans.

---

## Single Source Ingest

Trigger: user drops a file into `.raw/` or pastes content.

Steps:

1. **Read** the source completely. Do not skim.
2. **Discuss** key takeaways with the user. Ask: "What should I emphasize? How granular?" Skip this if the user says "just ingest it."
3. **Create** source summary in `wiki/sources/`. Use the source frontmatter schema from `references/frontmatter.md`.
4. **Create or update** entity pages for every person, org, product, and repo mentioned. One page per entity.
5. **Create or update** concept pages for significant ideas and frameworks.
6. **Update** relevant domain page(s) and their `_index.md` sub-indexes.
7. **Update** `wiki/overview.md` if the big picture changed.
8. **Update** `wiki/index.md`. Add entries for all new pages.
9. **Update** `wiki/hot.md` with this ingest's context.
10. **Append** to `wiki/log.md` (new entries at the TOP):
    ```markdown
    ## [YYYY-MM-DD] ingest | Source Title
    - Source: `.raw/articles/filename.md`
    - Summary: [[Source Title]]
    - Pages created: [[Page 1]], [[Page 2]]
    - Pages updated: [[Page 3]], [[Page 4]]
    - Key insight: One sentence on what is new.
    ```
11. **Check for contradictions.** If new info conflicts with existing pages, add `> [!contradiction]` callouts on both pages.

**Mode B (repository) vaults:** If `wiki/modules/`, `wiki/flows/`, or `wiki/decisions/` exist, link new or updated `concepts/` and `entities/` pages to the best-matching module, flow, or ADR, and add a short paragraph to those pages when the source is about code layout or behavior.

**Mode ADLC vaults:** If the vault is Mode ADLC (`wiki/requirements/`, `wiki/user-stories/`, etc. exist), do NOT flatten BA sources into generic `entities/` + `concepts/`. Still write the raw-source summary to `sources/` as usual, then route the structured deliverables to the BA workers: `ba-suite-subagent` for requirements / stories / gaps / tests, and `architecture-subagent` for per-service technical specs. They preserve stable IDs and traceability. See `skills/wiki/references/ba-suite-pipeline.md` and `technical-planning.md`.

---

## Batch Ingest

Trigger: user drops multiple files or says "ingest all of these" / "batch ingest" / "process everything in `.raw/`".

For 3 or more sources, **dispatch parallel subagents** instead of processing sequentially. Each `wiki-ingest-subagent` (defined in `agents/wiki-ingest-subagent.md`) handles one source fully in its own isolated context. This protects the main thread from N file reads and runs in roughly the time of the slowest single ingest.

### Steps

1. **List** all files to process. Confirm with user before starting (especially for >10 files).
2. **Filter** via the manifest. Skip files whose hash is unchanged in `.raw/.manifest.json`. Report the count skipped.
3. **Dispatch** one Agent tool call per remaining source — **all in a single message** so they run concurrently. For each source:
   - `subagent_type: "wiki-ingest-subagent"`
   - `description`: `"Ingest <filename>"`
   - `prompt`: pass the absolute source path, the vault path, and any user-requested emphasis. The subagent already knows its job (see `agents/wiki-ingest-subagent.md`).
4. **Wait** for all subagents. Each returns a summary block: `Source / Created / Updated / Contradictions / Key insight`.
5. **Cross-reference pass** (caller / main thread): scan the summaries for entities/concepts that appeared in multiple sources. Add wikilinks between the new pages where appropriate.
6. **Update** `wiki/index.md` once with all new pages from all subagent summaries.
7. **Update** `wiki/hot.md` once with the batch's combined context and key insights.
8. **Append** ONE consolidated entry to `wiki/log.md` (not one per source):
   ```markdown
   ## [YYYY-MM-DD] batch ingest | N sources
   - Sources: [filenames]
   - Pages created: [aggregate list]
   - Pages updated: [aggregate list]
   - Cross-source connections: [discoveries from step 5]
   ```
9. **Update** `.raw/.manifest.json` with the new hashes for each ingested source.
10. **Report**: "Processed N sources. Created X pages, updated Y pages. Key cross-source connections: [list]."

### Why parallel

- Each subagent reads ~5-15 wiki pages + the source. Doing 5 sources sequentially in main context = 25-75 file reads worth of tokens. Subagents return only the summary block (~150 tokens each).
- Subagents fail in isolation. If one source fails to read, the other 4 still complete.

### When NOT to dispatch subagents

- **1-2 sources**: just do them inline in the main thread. The dispatch overhead isn't worth it.
- **Sources that need user input mid-ingest** (e.g. emphasis decisions). Subagents have no way to ask the user. Use single-source mode for interactive work.
- **30+ sources**: still dispatch in parallel, but cap at 10 concurrent. Process in waves of 10 to avoid overwhelming the host's parallel Task queue.

---

## Context Window Discipline

Token budget matters. Follow these rules during ingest:

- Read `wiki/hot.md` first. If it contains the relevant context, don't re-read full pages.
- Read `wiki/index.md` to find existing pages before creating new ones.
- Read only 3-5 existing pages per ingest. If you need 10+, you are reading too broadly.
- Use PATCH for surgical edits. Never re-read an entire file just to update one field.
- Keep wiki pages short. 100-300 lines max. If a page grows beyond 300 lines, split it.
- Use search (`/search/simple/`) to find specific content without reading full pages.

---

## Contradictions

> [!note] Custom callout dependency
> The `[!contradiction]` callout used below uses Obsidian's default callout rendering. It works as-is in any vault.

When new info contradicts an existing wiki page:

On the existing page, add:
```markdown
> [!contradiction] Conflict with [[New Source]]
> [[Existing Page]] claims X. [[New Source]] says Y.
> Needs resolution. Check dates, context, and primary sources.
```

On the new source summary, reference it:
```markdown
> [!contradiction] Contradicts [[Existing Page]]
> This source says Y, but existing wiki says X. See [[Existing Page]] for details.
```

Do not silently overwrite old claims. Flag and let the user decide.

---

## What Not to Do

- Do not modify anything in `.raw/`. These are immutable source documents.
- Do not create duplicate pages. Always check the index and search before creating.
- Do not skip the log entry. Every ingest must be recorded.
- Do not skip the hot cache update. It is what keeps future sessions fast.
