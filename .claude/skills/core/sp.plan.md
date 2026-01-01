---
name: sp.plan
description: Convert specifications into executable architectural plans. Use when transforming a spec.md into a plan.md for implementation. Part of the spec-driven development workflow.
---

# Planning Skill

Convert specifications into actionable, ordered plans.

## Inputs Required

- `specs/<feature>/spec.md` — The specification to plan
- Any referenced artifacts from the spec
- Project constitution if available

## Planning Principles

### Determinism
Plans must be reproducible. Same spec, same context, same plan.

### Explicit Assumptions
State all assumptions made during planning. Do not assume unstated requirements.

### Dependency Ordering
Identify what must happen before what. Order tasks to minimize blockers.

### Planning vs Execution
Planning determines what to do and in what order. Execution determines how to do it. Do not decide implementation details during planning.

## Plan Output Structure

```
# Architectural Plan: <Feature>

## Scope and Dependencies
- In Scope: Key features being planned
- Out of Scope: Explicit exclusions
- External Dependencies: Systems, services, teams

## Key Decisions
### Decision: <Title>
- Options Considered
- Trade-offs
- Rationale

## Interfaces and API Contracts
- Public APIs and their contracts
- Error taxonomy

## Non-Functional Requirements
- Performance requirements
- Security requirements
- Reliability requirements

## Implementation Phases
Ordered, dependency-resolved phases with clear boundaries

## Data Management
- Schema evolution
- Migration strategy

## Operational Readiness
- Observability requirements
- Deployment strategy

## Risk Analysis
- Top 3 risks with mitigation strategies

## Evaluation Criteria
- Definition of done
- Acceptance tests
```

## Planning Workflow

### 1. Analyze Specification

Read the full spec. Identify:
- Core requirements (Must Have)
- Constraints stated or implied
- Dependencies within and outside the system
- Success criteria

### 2. Identify Architectural Decisions

For each significant choice, document:
- What decision is required
- Options available
- Trade-offs between options
- Recommended approach with rationale

Significant decisions meet three criteria:
- Long-term consequences
- Multiple viable alternatives
- Cross-cutting impact

### 3. Structure Implementation Phases

Group related work into phases. Each phase:
- Is independently testable
- Has clear completion criteria
- Minimizes integration risk
- Delivers value incrementally

Order phases to:
- Establish foundations first
- Resolve dependencies early
- Defer optional enhancements

### 4. Define Interfaces

For external contracts:
- Specify inputs and outputs
- Define error conditions and codes
- State versioning approach
- Document idempotency requirements

### 5. Document Constraints

Record:
- Technology constraints
- Integration requirements
- Compliance requirements
- Resource constraints

### 6. Assess Risks

Identify top risks:
- Technical risks
- Dependency risks
- Scope risks

For each risk:
- Describe impact
- Propose mitigation
- Identify kill switches if needed

### 7. Validate Completeness

Check:
- All Must Have requirements have implementation approach
- Dependencies are ordered correctly
- Interfaces are defined for external interactions
- Risks are identified with mitigations
- Success criteria are testable

## Guardrails

### Do
- Document decisions with rationale
- Order tasks by dependency
- Identify external dependencies explicitly
- Define clear phase boundaries
- State assumptions explicitly

### Do Not
- Include code or implementation details
- Specify tool commands or scripts
- Decide implementation order beyond dependencies
- Assume unavailable resources
- Skip risk identification

### Defer to Execution
- Exact file locations
- Specific library versions
- Detailed code structure
- Tool-specific commands
- Environment configuration

## Outputs

Write plans to `specs/<feature>/plan.md`.

## Triggers

Use this skill when:
- User requests "create a plan" or "plan this feature"
- A spec.md exists and needs architectural planning
- User asks "what's the implementation approach?"
