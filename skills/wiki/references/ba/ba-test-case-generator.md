---
name: ba-test-case-generator
description: >
  Generates structured test cases from user stories, acceptance criteria, or requirement
  statements — covering happy path, negative, boundary, exception, and NFR scenarios.
  Produces an Excel test case register with traceability matrix and a YAML BDD spec for
  automation handoff. Trigger this skill whenever a user says "write test cases",
  "generate tests", "test case register", "UAT plan", "UAT script", "test scenarios",
  "acceptance testing", "BDD test spec", "Gherkin test cases", "test coverage", "QA handoff",
  "traceability matrix", "test from these stories", or "help me test this". Also triggers on
  "I need to verify this requirement", "what should we test for this story", "generate edge
  cases", "negative testing", "boundary value analysis", or any request to convert user
  stories or requirements into testable scenarios. Use after ba-user-story-factory when
  backlog stories have Gherkin acceptance criteria ready for test expansion.
---

# BA Test Case Generator

Expands user story acceptance criteria into full test case suites covering all scenario types.
Produces an Excel register for UAT coordination and a YAML BDD spec for automation handoff.

## Reference File

Read before processing any input:
- `references/test-case-patterns.md` — scenario type definitions, boundary value analysis rules,
  negative test patterns, and NFR test design

---

## Input Handling

### Minimum Viable Input
One or more of:
- User stories with Gherkin acceptance criteria (from ba-user-story-factory or provided directly)
- Requirement statements (FR or NFR)
- A feature description with stated business rules

### Optimal Input
| Input | Effect |
|-------|--------|
| Full backlog register (from ba-user-story-factory) | Enables complete traceability matrix |
| NFR register | Generates dedicated NFR test scenarios with measurable thresholds |
| Test type tag | UAT / Regression / Smoke / Edge Case / Integration / Performance |
| Test environment description | Adds pre-condition context to test steps |
| Definition of Done (team's) | Aligns pass criteria with what the team considers Done |

### Clarification Rule
If the input has no acceptance criteria (just a feature description), ask one question:
> "Who will be executing these tests — business users for UAT, or QA engineers for automated testing?"

This determines the language level and step granularity of the output.

---

## Processing Steps

### Step 1 — Parse Inputs
For each user story or requirement:
- Extract the actor, the action, and the outcome
- Extract each Gherkin scenario as a test seed
- Note any data conditions, thresholds, or business rules embedded in the criteria

### Step 2 — Classify Scenario Types
Read `references/test-case-patterns.md`. For each acceptance criterion and each business rule,
derive the following scenario types:

| Type Code | Type | Source |
|-----------|------|--------|
| HP | Happy Path | The Gherkin scenario as written |
| NP | Negative Path | What happens if the actor provides invalid input or takes an invalid action |
| BC | Boundary Condition | Values at and around numeric, date, or character thresholds |
| EC | Exception Condition | System errors, unavailable services, concurrent access issues |
| NFR | Non-Functional | Performance, security, accessibility, reliability test |
| INT | Integration | Cross-system data flow and trigger verification |
| REG | Regression | Existing functionality that must still work after this change |

Each acceptance criterion must produce at minimum: one HP and one NP.
Numeric or date-based criteria must also produce one BC.

### Step 3 — Write Test Cases
For each scenario, write a complete test case. Format:

**Test Case fields:**
| Field | Content |
|-------|---------|
| Test Case ID | TC-{STORY-ID}-{TYPE}-{NNN} e.g. TC-PAY-001-HP-001 |
| Story / Requirement Reference | Source story or FR ID |
| Test Type | HP / NP / BC / EC / NFR / INT / REG |
| Test Objective | One sentence: what this test verifies |
| Pre-conditions | System state, data state, logged-in role, environment required |
| Test Steps | Numbered steps — each step is one action only |
| Test Data | Specific values to use (or "[use dataset X]" reference) |
| Expected Result | Observable, specific, pass/fail determinable outcome |
| Pass Criteria | The exact condition that constitutes a pass |
| Priority | Critical / High / Medium / Low |
| Automation Candidate | Yes / No / Partial |

### Step 4 — Apply Boundary Value Analysis (for numeric/date criteria)
Read `references/test-case-patterns.md` §2.
For every criterion with a numeric threshold or date boundary, generate three test cases:
- Value at the boundary (e.g. exactly 50 characters)
- Value one unit below the boundary (49 characters)
- Value one unit above the boundary (51 characters)

For range criteria (between X and Y):
- Generate five cases: below minimum, at minimum, inside range, at maximum, above maximum

### Step 5 — Generate Negative Test Cases
For each happy path test case, derive the primary negative case:
- Invalid data type or format
- Missing required field
- Unauthorised actor attempting the action
- Action attempted in wrong system state (e.g. editing a locked record)
- Duplicate submission

### Step 6 — Generate NFR Test Cases
For each NFR in the input:
- Performance: define load conditions and measure response time against threshold
- Security: attempt unauthorised access, injection, privilege escalation
- Accessibility: screen reader navigation, keyboard-only navigation, colour contrast
- Availability: test behaviour during planned maintenance window scenarios

Each NFR test must reference the measurable threshold from the NFR statement.
If no threshold exists, flag `[NO MEASURE — threshold required before this test is executable]`.

### Step 7 — Build Traceability Matrix
Map every test case ID back to its source story or requirement ID.
Identify coverage gaps: any story or FR with no test case is a coverage gap — flag it.

### Step 8 — Write YAML BDD Spec
For automation candidates, translate the test case into Gherkin YAML format suitable
for handoff to a QA engineer using Cucumber, SpecFlow, Behave, or equivalent.

---

## Output Specification

### Output 1 — Excel Test Case Register
Filename: `{project}_test_cases.xlsx`
Location: `/mnt/user-data/outputs/`

**Sheet 1: Test Case Register**
All columns from Step 3. Sortable by Type, Priority, Story ID, Automation Candidate.

**Sheet 2: Traceability Matrix**
| Story / Req ID | Story Title | Test Case IDs | Coverage Status |
|----------------|-------------|--------------|-----------------|
| | | | Full / Partial / None |

**Sheet 3: Coverage Summary**
- Total stories / requirements in scope
- Total test cases generated (by type)
- Stories with full coverage / partial / none
- Automation candidate count

**Sheet 4: NFR Test Cases**
Dedicated sheet for NFR test cases with threshold references

### Output 2 — YAML BDD Spec
Filename: `{project}_bdd_spec.yaml`
Location: `/mnt/user-data/outputs/`

Format per feature:
```yaml
feature: "[Epic or Feature Name]"
  story_id: "PAY-001"
  scenarios:
    - id: "TC-PAY-001-HP-001"
      name: "[Descriptive scenario name]"
      type: "happy_path"
      tags: ["@smoke", "@regression"]
      steps:
        given: "[Precondition]"
        when: "[User action]"
        then: "[Expected outcome]"
        and: "[Additional outcome if needed]"
      test_data:
        field_name: "value"
      automation_candidate: true
```

### Output 3 — Word UAT Script
Filename: `{project}_uat_script.docx`
Location: `/mnt/user-data/outputs/`
Audience: Business users executing UAT. Plain English only. No technical jargon.

Format per test case:
- Test number and name
- What you are testing (one sentence, business language)
- Before you start (pre-conditions in plain English)
- Steps to follow (numbered, each one action)
- What you expect to see
- Pass / Fail checkbox + Comments field

### Output 4 — Inline Summary (in conversation)
- Stories/requirements covered, total test cases generated
- Breakdown by type (HP/NP/BC/EC/NFR)
- Coverage gaps (stories with no test cases)
- Automation candidate count
- NFR cases without measurable thresholds (if any)

---

## Quality Gates

Before delivering any output:
- [ ] Every story has at minimum one HP and one NP test case
- [ ] Every numeric or date threshold has boundary value test cases
- [ ] Every NFR test case references a measurable threshold — flag if absent
- [ ] Traceability matrix has no stories with zero test cases (unless explicitly excluded)
- [ ] Expected result for every test case is observable and pass/fail determinable — no "system works correctly"
- [ ] YAML BDD spec is syntactically valid
- [ ] UAT script has no technical jargon — written for a business user

---

## Downstream Handoff

| This Output | Used By |
|-------------|---------|
| Test Case Register | QA team, UAT coordinator, Development Team verification |
| YAML BDD Spec | QA engineer for automation framework implementation |
| Traceability Matrix | `ba-scrum-events-pack` — Sprint Review evidence that stories meet acceptance criteria |
| Coverage gaps | `ba-user-story-factory` — missing test coverage signals incomplete acceptance criteria |
