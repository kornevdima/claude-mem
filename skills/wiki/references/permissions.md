# ADLC permissions profile

Mode ADLC is agent-operated: the human operates the agents and should not be prompted for routine work, while destructive operations stay gated. This profile encodes that. Scaffold it into the ADLC vault's `.claude/settings.json` (project scope) at setup, then tune per project.

Principle: allow routine project work, ask on medium-risk, deny hard-destructive and anything outside the project.

## Mechanism

Claude Code permissions support three lists: `allow` (run without prompt), `ask` (confirm first), `deny` (block outright). Precedence is `deny` > `ask` > `allow`. Keep destructive patterns in `deny` / `ask`; put everything routine in `allow`. Scope `Write` / `Edit` to the project path so nothing outside is touched silently. Bash entries use prefix matching (`Bash(git commit:*)` matches any `git commit ...`).

## Template `.claude/settings.json`

Replace `<VAULT_PATH>` with the project root. Trim patterns the project does not use.

```json
{
  "permissions": {
    "allow": [
      "Read(//<VAULT_PATH>/**)",
      "Write(//<VAULT_PATH>/**)",
      "Edit(//<VAULT_PATH>/**)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git switch:*)",
      "Bash(git checkout -b:*)",
      "Bash(rg:*)",
      "Bash(grep:*)",
      "Bash(ls:*)",
      "Bash(find:*)",
      "Bash(cat:*)",
      "Bash(awk:*)",
      "Bash(jq:*)",
      "Bash(md5sum:*)",
      "Bash(npm run:*)",
      "Bash(npm test:*)",
      "Bash(npx:*)",
      "Task(ba-suite-subagent)",
      "Task(architecture-subagent)",
      "Task(ba-export-subagent)",
      "Task(feature-builder)",
      "Task(feature-tester)",
      "Task(feature-reviewer)",
      "Task(feature-verifier)",
      "Task(doc-writer)",
      "Task(wiki-ingest-subagent)",
      "Bash(docker compose up:*)",
      "Bash(docker compose ps:*)",
      "Bash(docker compose logs:*)",
      "mcp__clickup__get_task",
      "mcp__chrome-devtools__navigate_page",
      "mcp__chrome-devtools__evaluate_script",
      "mcp__chrome-devtools__take_screenshot",
      "mcp__chrome-devtools__list_console_messages",
      "mcp__chrome-devtools__list_network_requests",
      "mcp__plantuml__render_plantuml"
    ],
    "ask": [
      "Bash(git push:*)",
      "Bash(rm:*)",
      "Bash(docker compose down:*)",
      "Bash(npm install:*)",
      "Bash(gh pr:*)",
      "mcp__clickup__create_task"
    ],
    "deny": [
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Bash(git reset --hard:*)",
      "Bash(git clean:*)",
      "Bash(docker compose down -v:*)",
      "Bash(docker volume rm:*)",
      "Bash(mongosh:*drop:*)",
      "Bash(gcloud:*)",
      "Bash(rm -rf /:*)",
      "Write(//etc/**)",
      "Read(//<VAULT_PATH>/.env)"
    ]
  }
}
```

Notes:

- `Task(ba-suite-subagent)` lets the ADLC ingest pass dispatch the BA worker without a prompt. Add other `Task(...)` workers the vault uses.
- Bash prefix matching cannot express every dangerous shape (for example "rm -rf anywhere outside the project"). `ask` on bare `rm` plus the guard hook below covers the rest.
- Keep secrets out of `allow`: `.env` reads are denied here as an example.
- MCP: reads (`mcp__clickup__get_task`) and local verification (`mcp__chrome-devtools__*`, `mcp__plantuml__render_plantuml`, `docker compose up`) are pre-allowed; outward-facing tracker writes (`mcp__clickup__create_task`) are in `ask` because they leave the repo.

## Optional guard hook (deterministic backstop)

Pattern lists miss novel command shapes. For a hard backstop, add a `PreToolUse` hook on `Bash|Write` that blocks dangerous commands and writes to untracked or outside-project paths. The outreach app uses a `guard-untracked.py` of this kind. Document it; do not require it.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write",
        "hooks": [
          { "type": "command", "command": "python3 .claude/hooks/guard.py", "statusMessage": "Guarding destructive ops..." }
        ]
      }
    ]
  }
}
```

## What stays the human's call

Sign-off, production deploys, force pushes, schema drops, and anything that leaves the repo. The agent proposes; the human approves. This is the gate that keeps ADLC safe to run unattended-ish.
