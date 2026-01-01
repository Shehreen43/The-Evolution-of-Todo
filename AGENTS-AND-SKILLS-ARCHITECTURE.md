# Agent & Skills Architecture Proposal
## The Evolution of Todo - AI-Native Development System

**Version:** 1.0.0
**Date:** 2025-12-28
**Status:** Proposal
**Based on:** Hackathon II requirements + Constitution v1.0.0

---

## Executive Summary

**14 Agents** + **28 Skills** designed to complete all 5 phases of the project through spec-driven, AI-native development.

**Core Principle:** Human orchestrates, AI agents execute within constitutional boundaries.

---

## 1. AGENT ARCHITECTURE (14 Agents)

### 1.1 Strategic Agents (4) - Planning & Architecture

#### A. Constitution Agent
- **Purpose**: Manage project governance and constitutional compliance
- **Tools**: Claude Code CLI, Read/Write, Grep
- **Phases**: All (I-V)
- **Authority**: Read-write on constitution.md only

#### B. Specification Agent
- **Purpose**: Transform requirements into structured specifications
- **Tools**: sp.specify, sp.clarify, templates
- **Phases**: All (I-V)
- **Authority**: Read-write on spec.md

#### C. Planning Agent
- **Purpose**: Design technical architecture from specifications
- **Tools**: sp.plan, sp.adr (suggest only), LSP
- **Phases**: All (I-V)
- **Authority**: Read-write on plan.md, research.md, data-model.md, contracts/

#### D. Task Breakdown Agent
- **Purpose**: Convert plans into atomic, testable work units
- **Tools**: sp.tasks, sp.checklist
- **Phases**: All (I-V)
- **Authority**: Read-write on tasks.md

---

### 1.2 Execution Agents (3) - Implementation & Testing

#### E. Implementation Agent
- **Purpose**: Execute code generation from tasks
- **Tools**: sp.implement, Edit/Write, Bash (tests)
- **Phases**: All (I-V)
- **Authority**: Read-write on code files

#### F. Testing Agent
- **Purpose**: Write and validate tests (TDD)
- **Tools**: Bash (pytest/jest), Edit/Write (test files)
- **Phases**: All (when tests required)
- **Authority**: Read-write on test files

#### G. Git Agent
- **Purpose**: Manage version control and PRs
- **Tools**: sp.git.commit_pr, Bash (git)
- **Phases**: All (I-V)
- **Authority**: Git operations only

---

### 1.3 Support Agents (4) - Documentation & Validation

#### H. PHR Agent
- **Purpose**: Create Prompt History Records
- **Tools**: sp.phr, templates, Write
- **Phases**: All (I-V)
- **Authority**: Read-write on history/prompts/

#### I. ADR Agent
- **Purpose**: Document architectural decisions
- **Tools**: sp.adr, templates
- **Phases**: II-V (especially architectural changes)
- **Authority**: Read-write on history/adr/

#### J. Analysis Agent
- **Purpose**: Validate cross-artifact consistency
- **Tools**: sp.analyze, Grep
- **Phases**: All (phase transition gates)
- **Authority**: Read-only (generates reports)

#### K. Reverse Engineering Agent
- **Purpose**: Extract specifications from code
- **Tools**: sp.reverse-engineer, LSP, Grep
- **Phases**: All (when inheriting code)
- **Authority**: Read code, write spec artifacts

---

### 1.4 Infrastructure Agents (3) - Phase IV+

#### L. Docker Agent
- **Purpose**: Containerization and local deployment
- **Tools**: Bash (docker), Docker AI (Gordon)
- **Phases**: IV-V
- **Authority**: Read-write on Dockerfiles, docker-compose.yml

#### M. Kubernetes Agent
- **Purpose**: Orchestration and deployment
- **Tools**: Bash (kubectl/helm), kubectl-ai, kagent
- **Phases**: IV-V
- **Authority**: Read-write on K8s manifests, Helm charts

#### N. Event-Driven Agent
- **Purpose**: Kafka and Dapr integration
- **Tools**: Bash (kafka/dapr), Edit (configs)
- **Phases**: V only
- **Authority**: Read-write on event schemas, Dapr components

---

## 2. SKILLS CATALOG (28 Skills)

### 2.1 Core Skills (12) - Multi-Phase

| Skill | Input | Output | Phases |
|-------|-------|--------|--------|
| **sp.constitution** | Project requirements | constitution.md | I |
| **sp.specify** | Natural language requirements | spec.md | I-V |
| **sp.plan** | spec.md | plan.md + research.md + data-model.md + contracts/ | I-V |
| **sp.tasks** | plan.md, spec.md | tasks.md | I-V |
| **sp.implement** | tasks.md, task IDs | Code files | I-V |
| **sp.phr** | Prompt, response, stage | PHR file in history/prompts/ | I-V |
| **sp.adr** | Decision title, context | ADR file in history/adr/ | II-V |
| **sp.analyze** | Spec, plan, tasks | Consistency report | I-V |
| **sp.clarify** | spec.md | Clarification questions (max 5) | I-V |
| **sp.checklist** | Feature requirements | Custom checklist | I-V |
| **sp.git.commit_pr** | Code changes | Commit + PR | I-V |
| **sp.reverse-engineer** | Codebase | Spec + plan + tasks | I-V |

---

### 2.2 Phase-Specific Skills (10)

| Skill | Input | Output | Phase |
|-------|-------|--------|-------|
| **sp.console-setup** | Project name | Python project (uv-based) | I |
| **sp.web-scaffold** | Project name | Monorepo (frontend/, backend/) | II |
| **sp.auth-setup** | Auth requirements | Better Auth + JWT middleware | II |
| **sp.mcp-server** | Tool definitions | MCP server code | III |
| **sp.chatbot-setup** | OpenAI API key | Agents SDK + ChatKit | III |
| **sp.containerize** | Application code | Dockerfiles + docker-compose | IV |
| **sp.helm-chart** | K8s manifests | Helm chart structure | IV |
| **sp.kafka-setup** | Event schemas | Kafka producers/consumers | V |
| **sp.dapr-components** | Dapr requirements | Dapr component YAML | V |
| **sp.ci-cd-setup** | Deployment targets | GitHub Actions workflows | V |

---

### 2.3 Integration Skills (6)

| Skill | Input | Output | Phases |
|-------|-------|--------|--------|
| **sp.api-contract** | Spec requirements | OpenAPI/AsyncAPI contracts | II-V |
| **sp.db-migration** | Data model changes | SQLModel migration scripts | II-V |
| **sp.test-contract** | API contracts | Contract test files (pytest) | II-V* |
| **sp.test-integration** | User journeys | Integration test files | I-V* |
| **sp.taskstoissues** | tasks.md | GitHub issues | I-V |

**Note:** Skills marked with * are optional (only when tests required in success criteria)

---

## 3. PHASE-BASED MAPPING

### Phase I: Console App (Basic Features)

**Agents:** Constitution, Specification, Planning, Task Breakdown, Implementation, PHR, Git
**Skills:** sp.constitution, sp.specify, sp.plan, sp.tasks, sp.implement, sp.console-setup, sp.phr, sp.git.commit_pr

**Key Focus:** Establish spec-driven workflow and governance foundation

---

### Phase II: Web App (Full-Stack + Auth)

**Agents:** All Phase I + Testing (if required), Analysis
**Skills:** All Phase I + sp.web-scaffold, sp.auth-setup, sp.api-contract, sp.db-migration, sp.test-contract*, sp.test-integration*

**Key Focus:** Add web layer, multi-user support, persistent storage, authentication

---

### Phase III: AI Chatbot (Conversational Interface)

**Agents:** All Phase II + ADR
**Skills:** All Phase II + sp.mcp-server, sp.chatbot-setup, sp.adr

**Key Focus:** Add conversational interface via MCP, document stateless architecture decisions

---

### Phase IV: Local Kubernetes (Cloud-Native)

**Agents:** All Phase III + Docker, Kubernetes
**Skills:** All Phase III + sp.containerize, sp.helm-chart

**Key Focus:** Containerization, local K8s deployment, AIOps (kubectl-ai, kagent, Docker AI)

---

### Phase V: Cloud Deployment (Production)

**Agents:** All Phase IV + Event-Driven
**Skills:** All Phase IV + sp.kafka-setup, sp.dapr-components, sp.ci-cd-setup

**Key Focus:** Advanced features, event-driven architecture, production deployment

---

## 4. AGENT AUTHORITY MATRIX

| Agent | Read Constitution | Write Constitution | Read Specs | Write Specs | Read Code | Write Code | Execute Tests | Git Ops |
|-------|:-----------------:|:------------------:|:----------:|:-----------:|:---------:|:----------:|:-------------:|:-------:|
| Constitution Agent | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Specification Agent | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Planning Agent | ✅ | ❌ | ✅ | ✅* | ✅ | ❌ | ❌ | ❌ |
| Task Breakdown Agent | ✅ | ❌ | ✅ | ✅* | ✅ | ❌ | ❌ | ❌ |
| Implementation Agent | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| Testing Agent | ✅ | ❌ | ✅ | ❌ | ✅ | ✅** | ✅ | ❌ |
| Git Agent | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
| PHR Agent | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| ADR Agent | ✅ | ❌ | ✅ | ✅*** | ✅ | ❌ | ❌ | ❌ |
| Analysis Agent | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Reverse Engineering | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Docker Agent | ✅ | ❌ | ✅ | ❌ | ✅ | ✅**** | ❌ | ❌ |
| Kubernetes Agent | ✅ | ❌ | ✅ | ❌ | ✅ | ✅***** | ❌ | ❌ |
| Event-Driven Agent | ✅ | ❌ | ✅ | ❌ | ✅ | ✅****** | ❌ | ❌ |

**Legend:**
- *Plan artifacts only (plan.md, research.md, data-model.md, contracts/)
- **Test files only
- ***ADR files only
- ****Dockerfiles, docker-compose.yml only
- *****Kubernetes manifests, Helm charts only
- ******Event handlers, Dapr components only

**Critical Rule:** NO agent may modify constitution without explicit human approval.

---

## 5. SKILL DEPENDENCY GRAPH

```
sp.constitution (root)
    │
    ├─> sp.specify (requires constitution)
    │   ├─> sp.clarify (clarifies spec)
    │   └─> sp.plan (consumes spec)
    │       ├─> sp.adr (suggests ADRs from plan)
    │       └─> sp.tasks (consumes plan)
    │           ├─> sp.checklist (generates checklists)
    │           ├─> sp.implement (executes tasks)
    │           │   ├─> sp.test-contract (writes tests)
    │           │   ├─> sp.test-integration (writes tests)
    │           │   └─> sp.git.commit_pr (version control)
    │           └─> sp.taskstoissues (converts to GitHub issues)
    │
    └─> sp.analyze (validates all artifacts)

Phase-Specific Skills (parallel branches):
├─> sp.console-setup → sp.specify (Phase I)
├─> sp.web-scaffold → sp.specify (Phase II)
├─> sp.auth-setup → sp.plan (Phase II)
├─> sp.api-contract → sp.plan (Phase II+)
├─> sp.db-migration → sp.plan (Phase II+)
├─> sp.mcp-server → sp.plan (Phase III)
├─> sp.chatbot-setup → sp.plan (Phase III)
├─> sp.containerize → sp.implement (Phase IV)
├─> sp.helm-chart → sp.containerize (Phase IV)
├─> sp.kafka-setup → sp.plan (Phase V)
├─> sp.dapr-components → sp.kafka-setup (Phase V)
└─> sp.ci-cd-setup → sp.helm-chart (Phase V)
```

---

## 6. AGENT ORCHESTRATION WORKFLOW

### Example: Phase I Console App

```
User: "Create console todo app with Basic features (add, delete, update, view, mark complete)"
    ↓
Constitution Agent: Create constitution.md (governance)
    ↓
Specification Agent: sp.specify → spec.md (WHAT to build)
    ↓
Planning Agent: sp.plan → plan.md + research.md + data-model.md (HOW to build)
    ↓
Task Breakdown Agent: sp.tasks → tasks.md (atomic work units)
    ↓
Implementation Agent: sp.implement → Python code files
    ↓
PHR Agent: sp.phr → 001-console-todo-implementation.spec.prompt.md
    ↓
Git Agent: sp.git.commit_pr → Commit + PR
    ↓
Analysis Agent: sp.analyze → Consistency report
    ↓
Human Approval: Verify Phase I deliverables
    ↓
[Phase I Complete ✅]
```

---

## 7. PHASE PROGRESSION GATES

Before moving to next phase, execute:

1. **sp.analyze** - Validate cross-artifact consistency
2. **sp.checklist** - Generate phase completion checklist
3. **Human approval** - Orchestrator verifies phase deliverables
4. **sp.git.commit_pr** - Create phase completion PR
5. **sp.phr** - Record phase completion

---

## 8. AGENT & SKILL INVOCATION PATTERNS

### 8.1 When Each Agent Invokes

#### Constitution Agent
**Triggers:**
- Project initialization (first time only)
- Constitution amendment requests (human approval required)
- Constitutional compliance validation (during planning phase)

**Invocation Pattern:**
```
User: "Initialize project with constitution"
→ Constitution Agent invokes sp.constitution
→ Reads: Hackathon requirements, project goals
→ Writes: .specify/memory/constitution.md
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Once per project + amendments (rare)

---

#### Specification Agent
**Triggers:**
- User provides feature requirements in natural language
- Start of any new phase
- New feature requests during a phase

**Invocation Pattern:**
```
User: "Create console todo app with Basic features"
→ Specification Agent invokes sp.specify
→ Reads: Constitution, spec template, user input
→ May invoke sp.clarify if requirements ambiguous
→ Writes: specs/<phase>/spec.md
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Once per phase + per new feature

---

#### Planning Agent
**Triggers:**
- After spec.md is approved by user
- When architecture needs to be designed
- When significant technical decisions required

**Invocation Pattern:**
```
User: "Generate plan for the spec"
→ Planning Agent invokes sp.plan
→ Reads: Constitution, spec.md, plan template
→ Writes: plan.md, research.md, data-model.md, contracts/
→ May suggest sp.adr if significant decisions detected
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Once per phase (after spec.md)

---

#### Task Breakdown Agent
**Triggers:**
- After plan.md is approved by user
- When tasks need to be broken down into atomic units

**Invocation Pattern:**
```
User: "Generate tasks from the plan"
→ Task Breakdown Agent invokes sp.tasks
→ Reads: Constitution, spec.md, plan.md, tasks template
→ Writes: tasks.md (with phases: Setup → Foundational → User Stories → Polish)
→ May invoke sp.checklist for validation
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Once per phase (after plan.md)

---

#### Implementation Agent
**Triggers:**
- After tasks.md is approved by user
- User requests implementation of specific task(s)
- Sequential or parallel task execution

**Invocation Pattern:**
```
User: "Implement task T001"
→ Implementation Agent invokes sp.implement
→ Reads: Constitution, spec.md, plan.md, tasks.md, task T001
→ Writes: Code files with task/spec reference comments
→ May invoke Testing Agent first (if TDD required)
→ Runs tests after implementation (if tests exist)
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Multiple times per phase (once per task or task group)

---

#### Testing Agent
**Triggers:**
- When tasks.md explicitly requires tests
- Before implementation (Red phase in TDD)
- After implementation (Green phase in TDD)

**Invocation Pattern:**
```
User: "Implement task T010 (write tests first)"
→ Testing Agent invokes sp.test-contract or sp.test-integration
→ Reads: Constitution, spec.md, tasks.md, contracts/
→ Writes: Test files (tests/contract/ or tests/integration/)
→ Runs tests to ensure they FAIL (Red phase)
→ Postcondition: Implementation Agent proceeds with code
```

**Frequency:** Only when tests required in success criteria

---

#### Git Agent
**Triggers:**
- After completing one or more tasks
- User requests commit + PR creation
- Phase completion (final commit)

**Invocation Pattern:**
```
User: "Commit the changes and create PR"
→ Git Agent invokes sp.git.commit_pr
→ Reads: Git status, git diff, recent commits (for style)
→ Analyzes: Staged changes to draft commit message
→ Writes: Commit with task/spec references + co-authored by Claude
→ Creates PR via gh CLI (if requested)
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Multiple times per phase (after task completion)

---

#### PHR Agent
**Triggers:**
- After EVERY significant AI interaction (mandatory)
- Automatically invoked by other agents
- Except when running sp.phr itself

**Invocation Pattern:**
```
[Any Agent completes work]
→ PHR Agent invokes sp.phr automatically
→ Reads: PHR template, prompt/response, stage, feature context
→ Writes: history/prompts/<constitution|feature|general>/<ID>-<slug>.<stage>.prompt.md
→ Validates: No unresolved placeholders
→ Postcondition: Audit trail created
```

**Frequency:** After every agent interaction (mandatory)

---

#### ADR Agent
**Triggers:**
- Planning Agent detects architecturally significant decision (3-part test)
- User explicitly requests ADR documentation
- Never auto-creates (only suggests)

**Invocation Pattern:**
```
Planning Agent detects: "Choosing stateless MCP architecture"
→ ADR Agent suggests: "📋 Architectural decision detected: Stateless MCP vs Stateful. Document? Run /sp.adr 'Stateless MCP Architecture'"
→ User approves: "Yes, create ADR"
→ ADR Agent invokes sp.adr
→ Reads: plan.md, context, alternatives
→ Writes: history/adr/<NNN>-<title>.md
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Rare (only for significant architectural decisions)

---

#### Analysis Agent
**Triggers:**
- Phase transition gates (before moving to next phase)
- User requests consistency validation
- After major changes to spec/plan/tasks

**Invocation Pattern:**
```
User: "Validate phase I artifacts before moving to phase II"
→ Analysis Agent invokes sp.analyze
→ Reads: Constitution, spec.md, plan.md, tasks.md, code files
→ Validates: Cross-artifact consistency, constitutional compliance
→ Generates: Consistency report with violations/warnings
→ Postcondition: PHR Agent records interaction
```

**Frequency:** At phase boundaries + on-demand validation

---

#### Reverse Engineering Agent
**Triggers:**
- Inheriting legacy code without specifications
- Mid-project entry (need to extract existing specs)
- Code-first projects transitioning to spec-driven

**Invocation Pattern:**
```
User: "Extract specifications from existing codebase"
→ Reverse Engineering Agent invokes sp.reverse-engineer
→ Reads: Codebase (via LSP, Grep)
→ Writes: spec.md, plan.md, tasks.md, intelligence artifacts
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Once (only when starting from existing code)

---

#### Docker Agent (Phase IV+)
**Triggers:**
- Phase IV begins (containerization required)
- User requests Dockerfile generation
- Local deployment setup

**Invocation Pattern:**
```
User: "Containerize the application for Phase IV"
→ Docker Agent invokes sp.containerize
→ Reads: Application code, dependencies, plan.md
→ Writes: Dockerfiles (multi-stage), docker-compose.yml
→ May use Docker AI (Gordon) for optimization
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Once per phase (IV and V)

---

#### Kubernetes Agent (Phase IV+)
**Triggers:**
- After Docker images are built
- User requests K8s manifests or Helm charts
- Deployment to Minikube or cloud K8s

**Invocation Pattern:**
```
User: "Generate Kubernetes manifests for deployment"
→ Kubernetes Agent invokes sp.helm-chart
→ Reads: Docker images, plan.md, K8s requirements
→ Writes: Helm charts (Chart.yaml, values.yaml, templates/)
→ May use kubectl-ai/kagent for intelligent operations
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Once per phase (IV and V)

---

#### Event-Driven Agent (Phase V)
**Triggers:**
- Phase V begins (event-driven architecture required)
- User requests Kafka or Dapr setup
- Advanced features (recurring tasks, reminders) need events

**Invocation Pattern:**
```
User: "Setup Kafka event-driven architecture"
→ Event-Driven Agent invokes sp.kafka-setup
→ Reads: Event schemas, plan.md, data-model.md
→ Writes: Kafka producers/consumers, Strimzi manifests
→ Then invokes sp.dapr-components
→ Writes: Dapr component YAML files
→ Postcondition: PHR Agent records interaction
```

**Frequency:** Once (Phase V only)

---

### 8.2 When Each Skill Invokes

#### Core Skills Invocation Table

| Skill | Invoked By | When | Prerequisites | Output |
|-------|-----------|------|---------------|--------|
| **sp.constitution** | Constitution Agent | Project init | None | constitution.md |
| **sp.specify** | Specification Agent | User provides requirements | Constitution exists | spec.md |
| **sp.plan** | Planning Agent | After spec.md approved | spec.md approved | plan.md, research.md, data-model.md, contracts/ |
| **sp.tasks** | Task Breakdown Agent | After plan.md approved | plan.md approved | tasks.md |
| **sp.implement** | Implementation Agent | User requests task execution | tasks.md approved | Code files |
| **sp.phr** | PHR Agent (automatic) | After every agent interaction | Agent completes work | PHR file in history/prompts/ |
| **sp.adr** | ADR Agent | Human approves ADR suggestion | Significant decision detected | ADR file in history/adr/ |
| **sp.analyze** | Analysis Agent | Phase transition or on-demand | spec/plan/tasks exist | Consistency report |
| **sp.clarify** | Specification Agent | Ambiguous requirements detected | spec.md draft exists | Clarification questions (max 5) |
| **sp.checklist** | Task Breakdown Agent | After tasks.md generated | tasks.md exists | Custom checklist |
| **sp.git.commit_pr** | Git Agent | User requests commit/PR | Code changes exist | Git commit + PR |
| **sp.reverse-engineer** | Reverse Engineering Agent | Existing code without specs | Codebase exists | spec.md, plan.md, tasks.md |

---

#### Phase-Specific Skills Invocation Table

| Skill | Invoked By | Phase | When | Prerequisites |
|-------|-----------|-------|------|---------------|
| **sp.console-setup** | Implementation Agent | I | Project scaffold needed | spec.md approved |
| **sp.web-scaffold** | Implementation Agent | II | Monorepo setup needed | spec.md approved |
| **sp.auth-setup** | Implementation Agent | II | Authentication required | plan.md includes auth |
| **sp.mcp-server** | Implementation Agent | III | MCP tools needed | plan.md includes MCP architecture |
| **sp.chatbot-setup** | Implementation Agent | III | Chatbot interface needed | MCP server ready |
| **sp.containerize** | Docker Agent | IV | Dockerization needed | Application code complete |
| **sp.helm-chart** | Kubernetes Agent | IV | K8s deployment needed | Docker images built |
| **sp.kafka-setup** | Event-Driven Agent | V | Event-driven arch needed | plan.md includes Kafka |
| **sp.dapr-components** | Event-Driven Agent | V | Dapr abstraction needed | Kafka setup complete |
| **sp.ci-cd-setup** | Implementation Agent | V | Deployment automation needed | Helm charts ready |

---

#### Integration Skills Invocation Table

| Skill | Invoked By | When | Prerequisites |
|-------|-----------|------|---------------|
| **sp.api-contract** | Planning Agent | API design phase | plan.md includes API endpoints |
| **sp.db-migration** | Implementation Agent | Database changes needed | Data model changes in plan.md |
| **sp.test-contract** | Testing Agent | Contract tests required | API contracts defined |
| **sp.test-integration** | Testing Agent | Integration tests required | User journeys in spec.md |
| **sp.taskstoissues** | Task Breakdown Agent | GitHub issues needed | tasks.md approved |

---

### 8.3 Complete Workflow Example (Phase I)

**User Goal:** Create console todo app with Basic features

```
Step 1: Constitution Creation
User: "Initialize project with constitution"
→ Constitution Agent invokes sp.constitution
→ Output: .specify/memory/constitution.md
→ PHR Agent auto-invokes sp.phr
→ Output: history/prompts/constitution/001-create-master-constitution.constitution.prompt.md

Step 2: Specification
User: "Create console todo app with add, delete, update, view, mark complete"
→ Specification Agent invokes sp.specify
→ Reads: Constitution, spec template, user input
→ Output: specs/phase-I-console/spec.md
→ PHR Agent auto-invokes sp.phr
→ Output: history/prompts/phase-I-console/002-console-todo-spec.spec.prompt.md

Step 3: Planning
User: "Generate plan from spec"
→ Planning Agent invokes sp.plan
→ Reads: Constitution, spec.md, plan template
→ Output: specs/phase-I-console/plan.md, research.md, data-model.md
→ PHR Agent auto-invokes sp.phr
→ Output: history/prompts/phase-I-console/003-console-todo-plan.plan.prompt.md

Step 4: Task Breakdown
User: "Generate tasks from plan"
→ Task Breakdown Agent invokes sp.tasks
→ Reads: Constitution, spec.md, plan.md, tasks template
→ Output: specs/phase-I-console/tasks.md
→ Task Breakdown Agent invokes sp.checklist (optional)
→ Output: Custom checklist for Phase I
→ PHR Agent auto-invokes sp.phr
→ Output: history/prompts/phase-I-console/004-console-todo-tasks.tasks.prompt.md

Step 5: Project Setup
User: "Setup Python console project structure"
→ Implementation Agent invokes sp.console-setup
→ Output: Project structure with uv, src/, tests/
→ PHR Agent auto-invokes sp.phr

Step 6: Implementation (Task-by-Task)
User: "Implement tasks T001-T005"
→ Implementation Agent invokes sp.implement (5 times)
→ Reads: tasks.md, task T001-T005
→ Output: src/models/task.py, src/services/todo_service.py, src/cli/main.py, etc.
→ PHR Agent auto-invokes sp.phr (after each task group)
→ Output: history/prompts/phase-I-console/005-implement-tasks.implement.prompt.md

Step 7: Git Commit
User: "Commit Phase I implementation"
→ Git Agent invokes sp.git.commit_pr
→ Reads: git status, git diff
→ Output: Git commit with task references + PR
→ PHR Agent auto-invokes sp.phr

Step 8: Phase Validation
User: "Validate Phase I completion"
→ Analysis Agent invokes sp.analyze
→ Reads: Constitution, spec.md, plan.md, tasks.md, code
→ Output: Consistency report (✅ Phase I complete)
→ PHR Agent auto-invokes sp.phr

[Phase I Complete → Ready for Phase II]
```

---

### 8.4 Agent Invocation Decision Tree

```
User provides input
    ↓
Is it a new project? → YES → Constitution Agent (sp.constitution)
    ↓ NO
Is it feature requirements? → YES → Specification Agent (sp.specify)
    ↓ NO
Does spec.md exist and approved? → YES → Planning Agent (sp.plan)
    ↓ NO
Does plan.md exist and approved? → YES → Task Breakdown Agent (sp.tasks)
    ↓ NO
Does tasks.md exist and approved? → YES → Implementation Agent (sp.implement)
    ↓ NO
Are there code changes uncommitted? → YES → Git Agent (sp.git.commit_pr)
    ↓ NO
Is phase validation needed? → YES → Analysis Agent (sp.analyze)
    ↓ NO
Is there existing code without specs? → YES → Reverse Engineering Agent (sp.reverse-engineer)
    ↓ NO
Is significant decision detected? → YES → ADR Agent (sp.adr) [suggest only]
    ↓ NO
Phase IV containerization needed? → YES → Docker Agent (sp.containerize)
    ↓ NO
Phase IV K8s deployment needed? → YES → Kubernetes Agent (sp.helm-chart)
    ↓ NO
Phase V events needed? → YES → Event-Driven Agent (sp.kafka-setup, sp.dapr-components)
```

---

## 9. IMPLEMENTATION ROADMAP

### Step 1: Create Agent Configurations (Next Action)

Create agent definition files in `.claude/agents/`:

```
.claude/
├── agents/
│   ├── constitution-agent.yaml
│   ├── specification-agent.yaml
│   ├── planning-agent.yaml
│   ├── task-breakdown-agent.yaml
│   ├── implementation-agent.yaml
│   ├── testing-agent.yaml
│   ├── git-agent.yaml
│   ├── phr-agent.yaml
│   ├── adr-agent.yaml
│   ├── analysis-agent.yaml
│   ├── reverse-engineering-agent.yaml
│   ├── docker-agent.yaml
│   ├── kubernetes-agent.yaml
│   └── event-driven-agent.yaml
├── skills/
│   ├── core/
│   │   ├── sp.constitution.md
│   │   ├── sp.specify.md
│   │   ├── sp.plan.md
│   │   ├── sp.tasks.md
│   │   ├── sp.implement.md
│   │   ├── sp.phr.md
│   │   ├── sp.adr.md
│   │   ├── sp.analyze.md
│   │   ├── sp.clarify.md
│   │   ├── sp.checklist.md
│   │   ├── sp.git.commit_pr.md
│   │   └── sp.reverse-engineer.md
│   ├── phase-specific/
│   │   ├── sp.console-setup.md
│   │   ├── sp.web-scaffold.md
│   │   ├── sp.auth-setup.md
│   │   ├── sp.mcp-server.md
│   │   ├── sp.chatbot-setup.md
│   │   ├── sp.containerize.md
│   │   ├── sp.helm-chart.md
│   │   ├── sp.kafka-setup.md
│   │   ├── sp.dapr-components.md
│   │   └── sp.ci-cd-setup.md
│   └── integration/
│       ├── sp.api-contract.md
│       ├── sp.db-migration.md
│       ├── sp.test-contract.md
│       ├── sp.test-integration.md
│       └── sp.taskstoissues.md
└── commands/
    └── [existing command files]
```

**Example `specification-agent.yaml`:**
```yaml
agent:
  name: specification-agent
  type: strategic
  purpose: Transform user requirements into structured specifications

  responsibilities:
    - Create spec.md from natural language
    - Define user stories and acceptance criteria
    - Identify edge cases and error scenarios
    - Ensure WHAT/HOW separation

  tools:
    - sp.specify
    - sp.clarify
    - Read (templates)
    - Write (spec files)

  authority:
    read:
      - .specify/memory/constitution.md
      - .specify/templates/spec-template.md
      - specs/**/*
    write:
      - specs/<phase>/spec.md
    prohibited:
      - .specify/memory/constitution.md (no modifications)
      - code files (no implementation)

  phases:
    - phase-I
    - phase-II
    - phase-III
    - phase-IV
    - phase-V

  invocation:
    trigger: User provides feature requirements in natural language
    when: At the start of any phase or when new features are requested
    preconditions:
      - Constitution must exist
      - User requirements must be clear (use sp.clarify if ambiguous)
    postconditions:
      - spec.md created with user stories, requirements, success criteria
      - PHR created documenting the interaction
    example: "User says: 'Create console todo app with add, delete, update, view, mark complete features'"
```

### Step 2: Build MCP Server

Convert `.claude/commands/*.md` to MCP prompts:

```
specifyplus-mcp-server/
├── src/
│   ├── server.py (MCP server entry point)
│   ├── prompts/
│   │   ├── constitution.py
│   │   ├── specify.py
│   │   ├── plan.py
│   │   ├── tasks.py
│   │   ├── implement.py
│   │   └── ... (one per skill)
│   └── tools/
│       ├── validate_constitution.py
│       ├── create_phr.py
│       └── ... (helper tools)
├── pyproject.toml
└── README.md
```

### Step 3: Test Phase I Workflow

Run minimal workflow:
1. Constitution Agent → constitution.md ✅ (already done)
2. Specification Agent → spec.md
3. Planning Agent → plan.md
4. Task Breakdown Agent → tasks.md
5. Implementation Agent → Python code
6. PHR Agent → Audit trail
7. Git Agent → Version control

### Step 4: Iterate & Refine

Based on Phase I learnings:
- Refine agent boundaries
- Adjust skill dependencies
- Update authority matrix
- Improve orchestration workflow

### Step 5: Scale to Phases II-V

Add phase-specific agents and skills incrementally:
- Phase II: Add Testing Agent, web-scaffold, auth-setup
- Phase III: Add ADR Agent, mcp-server, chatbot-setup
- Phase IV: Add Docker Agent, Kubernetes Agent
- Phase V: Add Event-Driven Agent, kafka-setup, dapr-components

---

## 9. BENEFITS OF THIS ARCHITECTURE

✅ **Clear Separation of Concerns**: Strategic agents separate from execution agents
✅ **Constitutional Compliance**: Every agent operates within defined boundaries
✅ **Phase-Agnostic Core**: Core skills work across all phases
✅ **Stateless Design**: All skills are idempotent and stateless
✅ **Human Orchestration**: Agents execute, humans approve and orchestrate
✅ **Audit Trail**: PHR Agent records every interaction
✅ **Architectural Documentation**: ADR Agent captures decisions
✅ **Version Control Traceability**: Git Agent ensures spec-to-code traceability
✅ **Progressive Complexity**: Minimal agents in Phase I, scale to 14 by Phase V
✅ **Tool-Mediated Actions**: No direct DB access, no hardcoded secrets

---

## 10. SUMMARY STATISTICS

**Total Agents:** 14
- Strategic: 4
- Execution: 3
- Support: 4
- Infrastructure: 3

**Total Skills:** 28
- Core (multi-phase): 12
- Phase-specific: 10
- Integration: 6

**Phase Distribution:**
- Phase I: 7 agents, 8 skills
- Phase II: 9 agents, 14 skills
- Phase III: 10 agents, 16 skills
- Phase IV: 12 agents, 18 skills
- Phase V: 14 agents, 28 skills

---

## 11. DIRECTORY STRUCTURE SUMMARY

```
The-Evolution-of-Todo/
├── .claude/
│   ├── agents/                      # Agent configurations (YAML)
│   │   ├── constitution-agent.yaml
│   │   ├── specification-agent.yaml
│   │   ├── planning-agent.yaml
│   │   ├── task-breakdown-agent.yaml
│   │   ├── implementation-agent.yaml
│   │   ├── testing-agent.yaml
│   │   ├── git-agent.yaml
│   │   ├── phr-agent.yaml
│   │   ├── adr-agent.yaml
│   │   ├── analysis-agent.yaml
│   │   ├── reverse-engineering-agent.yaml
│   │   ├── docker-agent.yaml
│   │   ├── kubernetes-agent.yaml
│   │   └── event-driven-agent.yaml
│   ├── skills/                      # Skill definitions (Markdown)
│   │   ├── core/
│   │   │   ├── sp.constitution.md
│   │   │   ├── sp.specify.md
│   │   │   ├── sp.plan.md
│   │   │   ├── sp.tasks.md
│   │   │   ├── sp.implement.md
│   │   │   ├── sp.phr.md
│   │   │   ├── sp.adr.md
│   │   │   ├── sp.analyze.md
│   │   │   ├── sp.clarify.md
│   │   │   ├── sp.checklist.md
│   │   │   ├── sp.git.commit_pr.md
│   │   │   └── sp.reverse-engineer.md
│   │   ├── phase-specific/
│   │   │   ├── sp.console-setup.md
│   │   │   ├── sp.web-scaffold.md
│   │   │   ├── sp.auth-setup.md
│   │   │   ├── sp.mcp-server.md
│   │   │   ├── sp.chatbot-setup.md
│   │   │   ├── sp.containerize.md
│   │   │   ├── sp.helm-chart.md
│   │   │   ├── sp.kafka-setup.md
│   │   │   ├── sp.dapr-components.md
│   │   │   └── sp.ci-cd-setup.md
│   │   └── integration/
│   │       ├── sp.api-contract.md
│   │       ├── sp.db-migration.md
│   │       ├── sp.test-contract.md
│   │       ├── sp.test-integration.md
│   │       └── sp.taskstoissues.md
│   └── commands/                    # Existing command files
│       └── [sp.*.md commands]
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # Project constitution
│   ├── templates/                   # Spec, plan, tasks templates
│   └── scripts/                     # PHR creation scripts
├── specs/                           # Phase-specific specifications
│   └── <phase-name>/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── contracts/
├── history/
│   ├── prompts/                     # Prompt History Records
│   │   ├── constitution/
│   │   ├── <feature-name>/
│   │   └── general/
│   └── adr/                         # Architecture Decision Records
├── src/                             # Phase I source code
├── backend/                         # Phase II+ backend
├── frontend/                        # Phase II+ frontend
├── CLAUDE.md                        # Agent instructions
├── README.md                        # User documentation
└── AGENTS-AND-SKILLS-ARCHITECTURE.md  # This file
```

---

## 12. NEXT ACTIONS

1. ✅ Constitution created (done)
2. ✅ Agent architecture proposed with invocation patterns (this document)
3. ⏳ Create agent configuration files (`.claude/agents/*.yaml`)
4. ⏳ Create skill definition files (`.claude/skills/{core,phase-specific,integration}/*.md`)
5. ⏳ Build MCP server for skills (optional - can use existing `.claude/commands/`)
6. ⏳ Test Phase I workflow with agent invocation patterns
7. ⏳ Begin Phase I specification: `/sp.specify "In-Memory Python Console Todo App with Basic features"`

---

**Document Version:** 1.0.0
**Last Updated:** 2025-12-28
**Status:** Ready for implementation
**Next Review:** After Phase I completion

---

*This architecture ensures spec-driven, AI-native development where humans orchestrate and AI agents execute within constitutional boundaries, progressing from simple console app to production-grade cloud-native AI chatbot.*
