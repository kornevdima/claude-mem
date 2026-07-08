---
type: source
title: "After the AI Hype — What's Real, and What's Next (Richard Campbell, NDC 2026)"
source_type: conference-keynote-transcript
author: "Richard Campbell"
date_published: 2026-06-18
url: "https://youtu.be/uWnUnMphmPM"
created: 2026-07-03
updated: 2026-07-03
confidence: medium
tags:
  - source
  - keynote
  - ai-landscape
  - hype-cycle
  - agentic-sdlc
status: current
related:
  - "[[Generator-Evaluator Pattern]]"
  - "[[Product Management Layer Skill]]"
  - "[[Context Engineering for Coding Agents]]"
key_claims:
  - "2025 was the first year of real, demonstrable LLM product impact — and it was in software development: agents assigned GitHub issues, iterating to a PR you argue with before accepting"
  - "GPT-5's literary mode failed because it was evaluated by another GPT that green-lit nonsense — a public failure case of LLM-judges-LLM"
  - "Half the agentic-coding products of the 2025 proliferation have already disappeared; big companies gut startups by hiring the staff away"
  - "Restricting the training/problem domain (Copilot on code vs GPT-3 on all language) produced the first working LLM product"
  - "Vendor promises repeat month over month; the pipeline is filled with noise to simulate velocity"
---

# Source: After the AI Hype — What's Real, and What's Next (NDC 2026 keynote)

**Speaker**: Richard Campbell (podcaster, .NET Rocks / RunAs Radio) | **Venue**: NDC, Copenhagen, 2026-06-18
**Raw transcript**: `.raw/yt-campbell-after-ai-hype.md` (auto-transcript, ~9k words — quote wording approximate)

## Summary

A skeptic's history-and-forecast keynote: "artificial intelligence" is a fundraising-era misnomer riding on science fiction and two human biases (projected intelligence, pareidolia). Campbell traces the lineage — Eliza (1960s), Hinton's backprop nets, ImageNet 2012, Siri, Google Brain, OpenAI's founding-as-talent-raid, the neural scaling laws paper (2020) as "the hyperscalers' excuse," GPT-2→3→4, ChatGPT as an accidental cash-strapped RLHF experiment that hit 100M users in two months — then places the industry on the Gartner curve: **past the peak, descending into the trough of disillusionment, far from bottom**. Core financial claims: no AI company is profitable in this line of business; Magnificent-10 data-center spend is masking US economic decline; NVIDIA self-dealing; memory makers (TSMC, Micron) refusing to double RAM production was the pin that pricked the peak. Closing arc: the tech is nonetheless real and worth keeping (AlphaFold "changed medicine fundamentally"), regulation matters (EU leading), and developers should return to fundamentals — "our job was never to write code, it was to solve people's problems."

## What's relevant to agentic software delivery

### 2025: the first real products were agentic coding

> Teams are "wired into GitHub and are assigning issues to an agent model that can iterate on the code and produce the code results in a pull request. And then you can argue with the tool in the pull request to do further tuning before you accept it."

Campbell says this is the **first real, demonstrable LLM impact anywhere** — after years of refusing podcast guests with no product. Qualifiers: "It's not easy. You're still hand rolling a lot of stuff. It still can go badly wrong" — extraordinary results come from teams that build discipline around the tools, not from the tools alone.

### Domain restriction beats scale

GPT-3 on all human language "still wasn't that good"; GitHub's insight — "what if we restricted the set? What if we used programming languages instead of human languages?" — produced Copilot, the first LLM product. A durable argument for narrow, curated context over kitchen-sink context (see [[Context Engineering for Coding Agents]]).

### LLM-judges-LLM failure case (GPT-5 literary mode)

> The literary capability "was trained... by exercising against another GPT, and the fact that the sentences made no sense didn't bother GPT at all. It thought the results were great and gave it all green lights. Then humans used it and went, 'Wow, this isn't English.'"

A public production-scale confirmation of the evaluator-leniency problem behind [[Generator-Evaluator Pattern]]: a same-family model as sole evaluator rubber-stamps garbage. Independent/ grounded evaluation (humans, runtime observation) is the fix.

### Vendor volatility and noise

- "Half these products already have disappeared" from the 2025 agentic-tool proliferation; incumbents don't acquire startups, they "gut" them by hiring away staff, then leadership.
- Product proliferation itself signals "an unsolved problem with some potential in it."
- His monthly-notes practice: record every vendor's promises at the start of each month, compare next month — "they're the same promises every month. They aren't progressing that quickly." The pipeline is filled with noise to make it *feel* fast so you spend before thinking.
- None of these companies are profitable; they report **engagement** instead — hence sycophancy by design (the GPT-4o restoration episode), which for agents means self-reported success is untrustworthy.
- Netscape-or-Google framing for AI labs; "most people would pick Anthropic as the survivor at this particular moment. But wait a month."

### Accountability naming

Copilot is "a good name... cuz that means you're the pilot. It's still your fault." And Campbell's deliberate language discipline: never anthropomorphize — "this is simply software. Clever software, but software nonetheless."

### Common-sense gap

The car-wash scenario (walk 50 m to the car wash, forgetting you need the car there) — models lack embodied common sense, so plausible reasoning is not a substitute for checking outcomes.

## Predictions / claims to watch

- Trough of disillusionment continues; price increases and free-tier cuts as labs chase profitability.
- RAM/fab constraints cap the compute build-out ("there isn't enough RAM and there's not going to be").
- No AGI path: "no real evidence that the technology can ever deliver"; AGI chant is a recruiting/marketing engine. People who know the tool best trust it least.
- Second-highest PE ratios ever (below only dot-com 2000); a serious correction has systemic impact because 10 companies ≈ half the S&P 500's value.
- Radiology precedent (Hinton wrong in 2016): automation raised productivity, demand outran it, radiologist demand went *up* — jobs shift rather than vanish.
- Deepfake worry declining because population skepticism rose; regulation (EU) is where enforcement is needed.

## What this contributes to the vault

- Independent, practitioner-visible validation that the **issue → agent → PR → human argues → accept** loop is where real value landed — the exact shape of the claude-mem ADLC build→review→verify pipeline.
- Evidence for the [[Product Management Layer Skill]] vendor-lifecycle premise: tool churn, acqui-gutting, unprofitable vendors, and promise-noise justify Gate 0 approval registries and re-review triggers.
- A citable failure case for same-model evaluation, strengthening [[Generator-Evaluator Pattern]] and the harness rule that verifiers observe behavior rather than trust agent self-grades.

## Caveats

Auto-transcript of a keynote: numbers and quotes are approximate; financial figures (e.g., "$16M and eight Teslas," "$5T NVIDIA cash") are speaker's rhetoric, unverified. Confidence set to medium.

## Connections

- [[Generator-Evaluator Pattern]] — GPT-5 literary flop added as an external failure case
- [[Product Management Layer Skill]] — vendor volatility evidence added
- [[Context Engineering for Coding Agents]] — domain-restriction lesson (Copilot)
- [[anthropic-harness-design]] — same evaluator-leniency finding from the builder's side
