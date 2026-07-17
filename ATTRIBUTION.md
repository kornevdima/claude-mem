# Attributions

adlc is an original work. The following third-party patterns, tools, and creators informed its design.

---

## LLM Wiki Pattern

**Author:** Andrej Karpathy
**Source:** https://github.com/karpathy
**Use:** The core architecture of adlc — using an LLM to build and maintain a structured wiki from raw sources — is based on the LLM Wiki pattern Karpathy described publicly. adlc is an independent implementation; no code or content from Karpathy's repositories was copied. A reference specification is included as a source document at [`.raw/llm-wiki-pattern-spec.md`](.raw/llm-wiki-pattern-spec.md).

---

## BA method set (ba-suite)

**Author:** dmytro (the ba-suite skill set)
**Use:** The BA methodology docs under `skills/wiki/references/ba/` are bundled from the author's own ba-suite skill set so adlc's Mode ADLC is self-contained and does not require installing the separate ba-suite plugin. They are applied by `ba-suite-subagent` and `ba-export-subagent`.

---

## Shift-Left Engineering Advisor

**Source:** the `anthropic-skills:shift-left-engineering-advisor` skill
**Use:** The shift-left methodology under `skills/wiki/references/shift-left/` is bundled so adlc's Mode ADLC `architecture-subagent` produces per-service technical specs without requiring an external skill.

