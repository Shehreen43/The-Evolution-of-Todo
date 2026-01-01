---
name: sp.tasks
description: Break plans into atomic, testable tasks. Use when converting a plan.md into tasks.md for implementation. Part of the spec-driven development workflow.
---

# Task Breakdown Skill

Convert architectural plans into executable, ordered tasks.

## Inputs Required

- `specs/<feature>/plan.md` — The architectural plan
- `specs/<feature>/spec.md` — The original specification
- Any ADRs or referenced decisions

## Task Format

Each task MUST have:

```yaml
id: unique-id
title: Brief task title
description: What this task accomplishes
status: pending | in_progress | completed
dependencies: []
phase: phase-name
testable: true | false
```

## Task Properties

### Atomicity
One task, one outcome. If a task has "and", split it.

### Testability
Each task must have clear completion criteria. Non-testable tasks are invalid.

### Traceability
Tasks MUST link to requirements in spec.md and decisions in plan.md.

### Independence
Tasks should minimize external dependencies. Group dependent tasks in phases.

## Task Breakdown Workflow

### 1. Review Plan

Read plan.md. Identify:
- Implementation phases
- Key decisions with rationale
- Non-functional requirements
- Dependencies and ordering constraints

### 2. Extract Work Items

For each phase, list all work required:
-基础设施搭建
- 核心功能实现
- 集成和测试
- 文档和验证

### 3. Decompose Into Tasks

Break each work item into atomic tasks.

Rules:
- Task completes one discrete unit
- Task has single, measurable outcome
- Task takes hours to days, not weeks
- Task can be tested independently

### 4. Define Dependencies

For each task:
- List tasks that must complete first
- Identify cross-phase dependencies
- Flag tasks that unblock others

### 5. Order Tasks

Arrange tasks to:
- Minimize idle time
- Put prerequisites first
- Group related work
- Enable parallel work where safe

### 6. Validate Completeness

Check:
- All plan phases have tasks
- All requirements are covered
- All decisions are implemented
- Dependencies are accurate
- Tasks are testable

## Task Output Structure

```markdown
# Tasks: <Feature>

## Phase 1: <Name>

### Task ID-001
**Title:** Brief title

**Description:** What this task accomplishes

**Dependencies:** []
**Phase:** phase-1
**Testable:** true

**Acceptance Criteria:**
- Criterion 1
- Criterion 2

**References:**
- Requirement: spec.md#section
- Decision: plan.md#decision-id
```

## Guardrails

### Do
- Create atomic, independent tasks
- Link tasks to requirements and decisions
- Define clear acceptance criteria
- Order by dependency
- Keep tasks under 8 hours where possible

### Do Not
- Create tasks spanning weeks
- Omit acceptance criteria
- Skip dependency links
- Mix implementation in task descriptions
- Create non-testable tasks

### Defer
- Exact file paths (defer to implementation)
- Specific library choices (defer to execution)
- Environment details (defer to implementation)
- Tool commands (defer to implementation)

## Outputs

Write tasks to `specs/<feature>/tasks.md`.

## Triggers

Use this skill when:
- User requests "create tasks" or "break down this plan"
- A plan.md exists and needs task decomposition
- User asks "what are the implementation tasks?"
- Transitioning from planning to implementation phase
