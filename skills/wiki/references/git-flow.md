# Git Flow: branch topology for agent sessions

How wiki changes and code changes ride branches when agents work a feature, so that (a) engineer PRs stay code-only, (b) wiki changes merge to main automatically once the feature lands, and (c) parallel delivery loops don't conflict. Complements [`git-setup.md`](git-setup.md) (repo init, `.gitattributes`) and [`team-sync.md`](team-sync.md) (operating protocol, merge hotspots). The `adlc` skill applies this at Step 0 (run policy); `wrap-up` applies it when the operator asks to commit.

## Principles

1. **Wiki commits and code commits never mix.** Separate commits always; separate branches where the topology allows. A commit that touches both `wiki/` and `src/` is a flow violation — split it.
2. **Review by reading, not merging.** The engineer and the orchestrator session review wiki changes by *reading the wiki branch's working copy* (point Obsidian at it) — never by merging the wiki branch into the feature branch. Merging wiki → feature re-couples them and puts the wiki diff back into the code PR; the two goals "code-only PRs" and "wiki merged into the feature branch" are mutually exclusive. Don't try to have both.
3. **Records ride anywhere; singletons ride with the dispatcher.** Parallel workers may write record pages concurrently (one new file each — conflict-free by construction, see `team-sync.md` § merge hotspots). The singletons (`log.md`, `hot.md`, `index.md`, `meta/` boards, the `_run` ledger) are single-writer: only the dispatcher touches them, only on the session's wiki branch.

## Topology A — multi-repo ADLC vault (default)

The product vault and the service repos are separate repositories, so the split is free:

- **Session start:** cut `wiki/<epic-id>` in the vault. Each service repo gets its feature branch per its own convention (`feat/<epic-id>` if none). The `_run` ledger frontmatter records the pairing (`wiki_branch:`, `code_branch:` per service).
- **During the run:** all wiki writes — dispatcher and workers — land in the vault checkout on the wiki branch. Code writes land in `services/<svc>` on the feature branch. Service PRs are code-only by construction.
- **Feature lands:** when the feature branch merges to main, merge `wiki/<epic-id>` to the vault's main — operator action at wrap-up, or a CI job that matches branches by epic ID. Merge order across concurrent epics doesn't matter: `log.md` is `merge=union` (git-setup), and `hot.md` / `meta/` boards are regenerate-on-conflict, never hand-merged (team-sync).
- **Abandoned feature:** the wiki branch is *not* automatically abandoned — specs, findings, and bug pages usually outlive a dropped implementation. Cherry-pick keepers to main, then delete the branch.

## Topology B — co-located Mode B wiki (single repo)

The wiki lives inside the service repo, so a session on feature branch A can't also be on a wiki branch. Two levels, by how strict the team's PR policy is:

- **Default (cheap):** one branch. Wiki edits go in dedicated `wiki:`-prefixed commits, never mixed with code. Add to the repo's `.gitattributes`:

  ```gitattributes
  wiki/** linguist-generated=true
  ```

  The PR still carries wiki changes, but GitHub collapses them in the diff — reviewers see code only, history stays linear, nothing can desynchronize. This solves the actual problem (reviewer noise) for most teams.

- **Strict (code-only PRs mandated):** worktree seam. Cut `wiki/<epic-id>` from the same base as the feature branch and check it out as a second worktree:

  ```bash
  git worktree add ../<repo>-wiki-<epic-id> -b wiki/<epic-id> main
  ```

  The harness routes wiki writes to the worktree path and code writes to the main checkout; Obsidian opens the worktree. Per principle 2, the wiki branch never merges into A — it merges to main *after* A's PR does. Cost: one extra checkout to keep in mind per session; use only when the team genuinely mandates code-only PRs.

## Parallel loops

Splitting an epic across parallel story dispatches composes with either topology:

- Builders may run in per-story worktrees of the *service* repo; their branches fold into the epic's feature branch as they finish.
- Wiki writes stay funneled: workers file their record pages in the single wiki checkout (distinct new files — safe concurrently); the dispatcher alone updates ledger, board, log, and index between dispatches. Never give two parallel dispatchers the same wiki branch.

## Naming and pairing

- Vault / wiki branches: `wiki/<epic-id>`. Code branches: repo convention, else `feat/<epic-id>`.
- The epic ID is the join key — branch names, ledger frontmatter, trace IDs in commit messages. A CI auto-merge job needs nothing else to pair a merged feature branch with its wiki branch.
- Wiki-only commits in co-located repos: `wiki:` prefix, so `git log --grep` and PR-splitting tooling can find them mechanically.
