---
name: sp.specify
description: Transform vague ideas into structured specifications. Use when users provide high-level feature requests, product concepts, or problem statements that need formalization before planning or implementation.
---

# Specification Generator

Generate clear, structured, testable specifications from user ideas.

## Inputs

Accept these input forms:
- Vague feature requests ("I want a better dashboard")
- Product concepts ("A todo app that evolves through phases")
- Problem statements ("Users need to track tasks efficiently")
- Partial requirements ("Like X but with Y")

## Specification Output Structure

Produce specs with this structure:

```
# Feature Name

## Overview
One-sentence description of the feature.

## Problem Statement
What problem does this solve? Why does it matter?

## Requirements
### Must Have
- Essential requirements without which the feature fails

### Should Have
- Important requirements deferred only if necessary

### Could Have
- Nice-to-have enhancements

### Out of Scope
Explicit exclusions

## Acceptance Criteria
Each requirement has testable, observable outcomes.

## Constraints
- Technical constraints
- Business constraints
- Dependencies

## Success Metrics
How is success measured?
```

## Workflow

### 1. Clarify Intent

If input is ambiguous, ask focused questions:
- "What problem are you solving?"
- "Who is the user?"
- "What does success look like?"
- "What exists today?"

Ask 2-3 questions maximum. Iterate as needed.

### 2. Extract Core Concept

Identify:
- Primary user action
- Value delivered
- Success condition

### 3. Structure Requirements

Categorize into Must/Should/Could/Out of Scope.

Rules:
- Must Have: Feature is useless without
- Should Have: Feature is diminished without
- Could Have: Nice to have, deferrable
- Out of Scope: Explicitly NOT included

### 4. Define Acceptance Criteria

For each Must Have requirement:
- Write observable outcome
- State conditions and inputs
- State expected result

Avoid: "Works correctly" — use specific, testable language.

### 5. Identify Constraints

Document:
- Technology constraints
- Integration requirements
- Compliance or policy requirements
- External dependencies

### 6. Validate Completeness

Check:
- Each requirement has acceptance criteria
- Ambiguity is resolved or marked for clarification
- Out of scope is clearly stated
- Constraints are documented

## Guardrails

### Clarity
- Use precise language over vague terms
- Replace "fast", "better", "user-friendly" with measurable attributes
- Define subjective terms explicitly

### Completeness
- Do not skip Out of Scope section
- Do not defer critical requirements to "future"
- Do not leave acceptance criteria as "TBD"

### Testability
- Acceptance criteria must be observable
- Avoid internal implementation details in requirements
- State what, not how

### Ambiguity
- Resolve ambiguity through questions
- Mark unresolved ambiguity explicitly
- Do not assume unstated requirements

## Outputs

Write specifications to `specs/<feature-name>/spec.md`.

If directory does not exist, create it.

## Triggers

Use this skill when:
- User requests a feature without detailed requirements
- Feature concept is vague or high-level
- Requirements need formalization before planning
- User asks "create a spec" or "write requirements"
