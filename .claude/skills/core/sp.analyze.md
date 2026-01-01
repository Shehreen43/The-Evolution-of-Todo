---
name: sp.analyze
description: Validate consistency across spec-driven development artifacts. Use when checking alignment between spec.md, plan.md, and tasks.md, or when verifying implementation fidelity.
---

# Analysis Skill

Validate consistency across SDD artifacts and implementation.

## Analysis Scope

Validate these artifact relationships:
- spec.md ↔ plan.md alignment
- plan.md ↔ tasks.md decomposition
- tasks.md ↔ implementation fidelity
- spec.md ↔ implementation requirements

## Analysis Workflow

### 1. Load Artifacts

Read available artifacts:
- spec.md for requirements
- plan.md for architectural decisions
- tasks.md for implementation tasks
- implementation files for verification

### 2. Trace Requirements

For each requirement in spec.md:
- Verify plan.md addresses it
- Verify tasks.md implements it
- Verify implementation satisfies it

### 3. Trace Decisions

For each decision in plan.md:
- Verify tasks implement the decision
- Verify implementation follows decision
- Flag deviations with rationale

### 4. Trace Tasks

For each task in tasks.md:
- Verify task relates to requirement
- Verify task has acceptance criteria
- Verify task is complete or in progress

### 5. Generate Report

Produce validation report:

```markdown
# Analysis: <Feature>

## Summary
- Artifacts analyzed
- Issues found
- Severity distribution

## Requirement Coverage
- Requirements traced
- Gaps identified

## Decision Compliance
- Decisions implemented
- Deviations found

## Task Completeness
- Tasks with criteria
- Tasks complete/incomplete

## Issues
### Critical
- [List]

### Warning
- [List]

### Info
- [List]
```

## Validation Checkpoints

### spec→plan alignment
- All Must Have requirements have implementation approach
- Constraints are addressed in plan
- Dependencies are identified

### plan→tasks alignment
- All phases have tasks
- Dependencies are ordered correctly
- Acceptance criteria exist

### tasks→implementation alignment
- Code files exist
- Tests cover acceptance criteria
- Documentation is updated

## Guardrails

### Do
- Trace requirements through all layers
- Flag gaps and deviations
- Distinguish severity levels
- Suggest remediation for critical issues

### Do Not
- Fix issues during analysis
- Add requirements not in spec
- Change architectural decisions
- Approve incomplete work

### Escalate
- Missing artifacts
- Significant deviations
- Scope gaps
- Unresolved blockers

## Outputs

Write analysis reports to `specs/<feature>/analysis.md`.

## Triggers

Use this skill when:
- User requests analysis or validation
- Approaching phase transition (e.g., before implementation)
- Reviewing implementation against spec
- Investigating gaps or misalignments
- Preparing for commit or PR
