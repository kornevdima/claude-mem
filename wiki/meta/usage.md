---
type: meta
title: "Token Usage"
updated: 2026-07-04T10:06:44Z
tags:
  - meta
  - usage
  - derived-view
status: evergreen
---

# Token Usage

> [!note] Derived, host-local view — regenerate, don't hand-edit.
> Built by `usage_report.py` from Claude Code transcripts (`/Users/dmytro/.claude/projects/-Users-dmytro-IdeaProjects-claude-mem`).
> Transcripts exist only on the machine that ran the sessions; teammates regenerate their own
> (team-sync rule: regenerate-don't-merge). Ledger rows outlive transcript garbage-collection.
> Reading the numbers: **output** and **cache write** are the expensive classes;
> **cache read** is high-volume but ~10x cheaper than input; a high **sub %** means
> subagent fan-out (not the main context) drove the spend.

## Totals (cumulative, all ledger rows)

| input | output | cache write | cache read |
|---|---|---|---|
| 358,838 | 1,329,985 | 5,236,705 | 294,712,709 |

## Top sessions by output tokens (transcripts currently on disk)

| session | label | output (main+sub) |
|---|---|---|
| `8ccf9641` | Hi! I want to improve cloud-mem project. | 466,034 |
| `fd099c2f` | /claude-mem:wiki I want to run the skill re-avalutaion. I have a feedb | 398,967 |
| `2602cc6b` | /model | 224,983 |
| `42d7c8d5` | /login | 71,142 |
| `9ccdeca2` | /claude-mem:wiki let's continue work on the project, we have 2 planned | 55,865 |

## By model (main context; transcripts currently on disk)

| model | input | output | cache write | cache read |
|---|---|---|---|---|
| claude-opus-4-7 | 12,118 | 452,397 | 2,175,166 | 195,289,214 |
| claude-opus-4-8 | 78,768 | 449,202 | 997,226 | 56,784,888 |
| claude-fable-5 | 110,854 | 247,767 | 1,063,044 | 32,027,226 |

## By subagent type (transcripts currently on disk)

| agent type | runs | input | output | cache write | cache read |
|---|---|---|---|---|---|
| claude-mem:wiki-ingest-subagent | 5 | 108,006 | 101,477 | 403,208 | 6,384,183 |
| Explore | 6 | 31,372 | 65,176 | 518,500 | 4,061,898 |
| claude-mem:graphify-extract-subagent | 2 | 13 | 13,637 | 47,072 | 155,880 |
| general-purpose | 1 | 17,707 | 329 | 32,489 | 9,420 |

## Session ledger (cumulative; newest first)

<!-- ledger -->
| date | session | label | branch | models | requests | input | output | cache write | cache read | sub % |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-07-04 | `f43eac40` | /claude-mem:wiki let's check the latest changes in the project, starti | adlc | claude-fable-5 | 41 | 21,172 | 35,839 | 197,015 | 3,452,475 | 0% |
| 2026-07-03 | `2602cc6b` | /model | adlc | claude-fable-5 | 210 | 162,688 | 224,983 | 1,124,679 | 20,406,575 | 63% |
| 2026-07-03 | `42d7c8d5` | /login | adlc | claude-opus-4-8 | 64 | 38,194 | 71,142 | 166,422 | 6,929,895 | 0% |
| 2026-07-03 | `82c1164b` | /claude-mem:wiki let's continue build the harness. what next left in t | adlc | claude-fable-5 | 54 | 21,591 | 32,434 | 103,373 | 5,117,897 | 0% |
| 2026-07-03 | `9ccdeca2` | /claude-mem:wiki let's continue work on the project, we have 2 planned | adlc | claude-fable-5 | 47 | 22,362 | 55,865 | 196,320 | 5,020,203 | 0% |
| 2026-07-03 | `9d3c1083` | /claude-mem:wiki let's contniue building harness | adlc | claude-fable-5 | 63 | 21,859 | 42,117 | 118,857 | 6,178,250 | 0% |
| 2026-06-29 | `2e8d7fe4` | how to reinstall plugin to have update for aldc locally | adlc | claude-opus-4-8 | 4 | 19,341 | 2,604 | 28,586 | 121,910 | 0% |
| 2026-06-28 | `fd099c2f` | /claude-mem:wiki I want to run the skill re-avalutaion. I have a feedb | adlc-rlm | claude-opus-4-8 | 213 | 39,500 | 398,967 | 1,079,215 | 52,040,410 | 5% |
| 2026-05-09 | `8ccf9641` | Hi! I want to improve cloud-mem project. | master | claude-opus-4-7 | 530 | 12,131 | 466,034 | 2,222,238 | 195,445,094 | 2% |
