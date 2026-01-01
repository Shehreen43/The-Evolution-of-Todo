---
name: sp.implement
description: Execute implementation based on approved specs and plans. Use when translating tasks.md into working code, infrastructure, or deliverables. Part of the spec-driven development workflow.
---

# Implementation Skill

Execute implementation following approved specifications, plans, and tasks.

## Preconditions

Before implementation begins, verify:
- `specs/<feature>/spec.md` exists and is approved
- `specs/<feature>/plan.md` exists and is approved
- `specs/<feature>/tasks.md` exists and is approved
- No pending clarification on requirements

## Implementation Workflow

### 1. Review Scope

Read the approved artifacts:
- spec.md: Requirements and constraints
- plan.md: Architectural decisions and phases
- tasks.md: Ordered, atomic tasks

Identify phase boundaries and task dependencies.

### 2. Start Tasks

Execute tasks in dependency order:
- Begin with phase 1 tasks
- Complete tasks before moving to dependents
- Mark tasks in_progress when work begins
- Mark tasks completed when acceptance criteria are met

### 3. Maintain Fidelity

When implementing:
- Follow spec.md requirements exactly
- Respect architectural decisions in plan.md
- Complete all acceptance criteria for each task
- Flag deviations from approved artifacts

### 4. Handle Deviations

If requirements conflict with implementation:
- Do not invent workarounds
- Document the conflict
- Request clarification before proceeding
- Do not expand scope without approval

### 5. Integrate Incrementally

Follow plan.md phase structure:
- Complete phase before beginning next
- Validate integration at phase boundaries
- Address integration issues before proceeding

### 6. Request Intervention

Stop and request clarification when:
- Requirements are ambiguous
- Tasks are not testable
- Dependencies create blockers
- Architectural decisions conflict
- Scope creep is requested

## Guardrails

### Do
- Implement exactly what specs require
- Follow architectural decisions
- Complete all acceptance criteria
- Flag conflicts immediately
- Maintain phase boundaries

### Do Not
- Add features not in spec
- Change architectural decisions
- Skip acceptance criteria
- Defer blockers without escalation
- Expand scope unilaterally

### Escalate
- Ambiguous requirements
- Missing specifications
- Conflicting decisions
- Scope change requests
- Technical blockers

## Outputs

Implementation produces:
- Working code in appropriate directories
- Updated task status
- Test coverage for acceptance criteria
- Documentation updates as specified

## Triggers

Use this skill when:
- User requests implementation
- Tasks exist and need execution
- User asks "implement this feature"
- Transitioning from task breakdown to code execution
