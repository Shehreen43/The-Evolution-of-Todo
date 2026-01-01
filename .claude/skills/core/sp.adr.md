---
name: sp.adr
description: Document architecturally significant decisions. Use when creating, updating, or reviewing ADRs for significant technical choices.
---

# ADR Skill

Document architecturally significant decisions.

## ADR Output Structure

```markdown
# ADR: <Title>

## Status
Proposed | Accepted | Deprecated | Rejected

## Context
What is the issue or decision required?

## Decision
The chosen approach.

## Consequences
### Positive
- Benefits of this decision

### Negative
- Drawbacks and trade-offs

### Neutral
- Side effects requiring attention
```

## ADR Significance Test

A decision requires an ADR when ALL criteria are met:

1. **Impact**: Long-term consequences (affects architecture, data model, security, or platform)
2. **Alternatives**: Multiple viable options exist
3. **Scope**: Cross-cutting impact (affects multiple components or phases)

If any criterion is false, document inline without ADR.

## ADR Workflow

### 1. Identify Decision

Detect decisions during planning:
- Technology selection
- Architecture patterns
- Integration approaches
- Security or compliance choices

### 2. Test Significance

Apply significance test. If not significant, document inline.

### 3. Document Decision

Write ADR with:
- Clear title reflecting the decision
- Context explaining the problem
- Options considered
- Trade-offs between options
- Chosen option with rationale
- Consequences (positive, negative, neutral)

### 4. Link Artifacts

Reference from:
- plan.md for architectural decisions
- tasks.md for implementation guidance
- spec.md for requirement traceability

### 5. Review and Finalize

ADRs are typically:
- Proposed during planning
- Accepted when plan is approved
- Deprecated when superseded
- Rejected when alternative is chosen

## Guardrails

### Do
- Test significance before creating ADR
- Document alternatives and trade-offs
- Link ADRs to planning artifacts
- Use consistent naming: `adr/<ID>-<slug>.md`

### Do Not
- ADR every decision
- Skip alternatives section
- Document trivial choices
- Create ADRs without approval context

### Defer
- Detailed implementation steps
- Code examples
- Configuration details

## Outputs

Write ADRs to `history/adr/<ID>-<slug>.md`.

Naming convention:
- Increment ID (001, 002, ...)
- Slug is kebab-case title

## Triggers

Use this skill when:
- Planning reveals significant decisions
- User requests "create ADR" or "document this decision"
- Significant trade-offs need recording
- Architectural choices have long-term impact
