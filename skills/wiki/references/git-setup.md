# Git Setup

Initialize git in the vault to get full history and protect against bad writes.

---

## Initialize

```bash
cd "$VAULT_PATH"
git init
git add -A
git commit -m "Initial vault scaffold"
```

---

## .gitattributes (always)

Create a `.gitattributes` in the vault root as part of the scaffold:

```gitattributes
wiki/log.md merge=union
**/wiki/log.md merge=union
```

`log.md` is append-only with newest entries at the top, so concurrent sessions (teammates, parallel agents, a wrap-up racing an ingest) both prepend — a normal merge conflicts every time, while `merge=union` keeps both entries automatically. The `**/` pattern covers co-located code wikis under `services/`. The team-sync protocol (`team-sync.md`) depends on this being present before the second concurrent session ever runs.

---

## .gitignore

The root `.gitignore` in this repo already covers the right exclusions:

```
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.smart-connections/
.obsidian-git-data
.trash/
.DS_Store
```

`workspace.json` changes constantly as you move panes around. Excluding it keeps the diff clean.

---

## Obsidian Git Plugin (optional)

Install via Settings → Community Plugins → Browse → "Obsidian Git". Then:

Settings > Obsidian Git:
- Auto backup interval: **15 minutes**
- Auto backup after file change: on
- Push on backup: on (if you have a remote)
- Commit message: `vault: auto backup {{date}}`

This runs silently in the background. You get a full history of every note without thinking about it.

---

## Remote (Optional)

To back up to GitHub:

```bash
git remote add origin https://github.com/yourname/your-vault
git push -u origin main
```

Keep the repo private if the vault contains personal notes.
