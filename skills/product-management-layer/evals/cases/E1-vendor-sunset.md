# E1 — Vendor sunset (golden case)

- **Traces:** FR-2 (vendor lifecycle governance)
- **Mode exercised:** VENDOR-REVIEW
- **Why golden:** the vendor-sunset retrospective is the scenario that motivated the skill.

## Prompt

Our governance registry is in docs/governance/. Embrace.ai just announced they are
shutting the product down at the end of the year. We use it for session replay on the
web app. What do we do?

## Must match

sunset
RT-
under-review
AP-UC002-TL001
[Mm]igration
(never transfer|not transfer|do not reuse|new ApprovalEntry|NEW ApprovalEntry)

## Must not match

<!-- The approval must not silently stay approved after the trigger. -->

## Grader notes

Passing behavior: a `sunset` ReviewTrigger is recorded (new RT-id), the dependent
approval AP-UC002-TL001 is set to `under-review`, a Migration Checklist is attached,
and the response states that approvals never transfer — the replacement needs a NEW
ApprovalEntry. Bonus (not asserted): the checklist includes retiring AS-003 to avoid
shelfware, and the exit-plan gap ([TBD] on the scorecard) is called out.
