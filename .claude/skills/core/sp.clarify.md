---
name: sp.clarify
description: Identify and resolve underspecified areas in specs. Use when spec.md has gaps, ambiguities, or missing details that prevent planning.
---

# Clarification Skill

Identify and resolve underspecified areas in specifications.

## Preconditions

Verify:
- A spec.md exists with content to clarify
- No user-provided clarification is available
- Planning cannot proceed without resolution

## Clarification Workflow

### 1. Scan Spec

Read spec.md and identify:
- Missing sections (Overview, Requirements, Constraints, etc.)
- Vague language (better, faster, user-friendly)
- Undefined terms or acronyms
- Assumptions not stated
- Edge cases not covered

### 2. Generate Questions

Form targeted questions (2-5 maximum):
- Each question addresses one gap
- Questions are specific and actionable
- Questions have bounded answers

Question patterns:
- "What is the expected behavior when [condition]?"
- "Who is the primary user for [feature]?"
- "What are the performance requirements for [component]?"
- "How should [edge case] be handled?"

### 3. Present Questions

Present questions to user:
- List each question clearly
- Request focused responses
- Avoid overwhelming with too many questions

### 4. Encode Responses

Once user responds:
- Update spec.md with clarifications
- Mark previously ambiguous sections as resolved
- Document any new constraints or requirements

### 5. Validate Updated Spec

Verify:
- All questions are answered
- Ambiguity is resolved
- Planning can now proceed

## Guardrails

### Do
- Limit questions to most critical gaps
- Ask for specific, actionable responses
- Update spec.md with answers
- Re-scan after encoding responses

### Do Not
- Ask more than 5 questions at once
- Proceed with planning despite ambiguity
- Make assumptions without user input
- Skip edge case identification

### Defer
- Minor clarifications that don't block planning
- Nice-to-know information
- Implementation details

## Outputs

Updated `specs/<feature>/spec.md` with:
- Ambiguous sections clarified
- New requirements documented
- Constraints added
- Edge cases addressed

## Triggers

Use this skill when:
- User requests clarification or asks "what's missing?"
- Spec contains vague language
- Planning reveals unanswerable questions
- User asks "what do you need to know?"
- Transitioning from spec to plan phase
