<!--
SYNC IMPACT REPORT
===================
Version Change: 1.0.0 → 1.0.0 (Initial Constitution)
Modified Principles: N/A (Initial creation)
Added Sections: All sections (initial creation)
Removed Sections: None
Templates Requiring Updates:
  ✅ plan-template.md - Reviewed, aligns with constitution principles
  ✅ spec-template.md - Reviewed, aligns with constitution requirements
  ✅ tasks-template.md - Reviewed, aligns with constitution task structure
Follow-up TODOs: None
-->

# The Evolution of Todo - AI-Native Project Constitution

**Project Name**: The Evolution of Todo - Mastering Spec-Driven Development & Cloud Native AI
**Project Type**: Multi-Phase AI-Native Todo Application (Console → Web → AI Chatbot → Kubernetes Deployment)
**Technology Stack**: Python, Next.js, FastAPI, SQLModel, Neon DB, OpenAI Agents SDK, MCP, Docker, Kubernetes, Kafka, Dapr
**Development Paradigm**: AI-Native, Spec-Driven Development (SDD-RI), Agentic Architecture

---

## 1. Purpose & Scope

### Project Mission

This constitution governs the **entire lifecycle** of "The Evolution of Todo" project across all five phases:
- Phase I: In-Memory Python Console App
- Phase II: Full-Stack Web Application
- Phase III: AI-Powered Todo Chatbot
- Phase IV: Local Kubernetes Deployment
- Phase V: Advanced Cloud Deployment

This project serves as a **production-grade AI platform**, not a demo, where the human developer operates as an **ORCHESTRATOR** using Claude Code CLI and spec-kit as primary execution mechanisms.

### Scope Boundaries

**In Scope:**
- All todo management features (Basic, Intermediate, Advanced levels)
- User authentication and authorization
- Multi-user support with data isolation
- AI-powered conversational interface via MCP
- Event-driven architecture with Kafka
- Cloud-native deployment on Kubernetes
- Progressive feature evolution across phases

**Out of Scope:**
- Features not defined in phase specifications
- Manual code writing (spec-driven only)
- Direct database manipulation by AI agents
- Deployment to platforms other than specified (Minikube, DigitalOcean DOKS, or approved alternatives)

---

## 2. Non-Negotiable Principles

### I. Spec-Driven Development (Mandatory)

**All code MUST originate from specifications.**

**Rules:**
- NO manual code writing - all implementation through Claude Code executing specifications
- Constitution → Specification → Plan → Tasks → Implementation (strictly enforced order)
- Every line of code MUST trace back to a task ID, which traces to a spec requirement
- Specifications must be refined until Claude Code generates correct output
- Incomplete specifications block implementation (fail-fast principle)

**Enforcement:**
- Every code file must include header comments: `# Task: [TASK_ID] | Spec: [SPEC_SECTION] | Phase: [PHASE_NUMBER]`
- All PRs must reference task IDs and spec sections
- Agents cannot proceed without approved specification artifacts

### II. Agentic Architecture & AI-First Execution

**The system is AI-native and agentic by design.**

**Rules:**
- Claude Code CLI is the primary builder - humans orchestrate, not code
- All AI agents (Claude, subagents, skills) operate within defined authority boundaries
- Agent actions are mediated via approved tools (Claude Code CLI, MCP servers)
- Agents MUST NOT modify governance documents or specifications without explicit human approval
- Skills are stateless, reusable, and phase-agnostic

**Authority Boundaries:**
- Agents MAY: read specs, generate code from tasks, query databases via MCP tools, create PHRs, suggest ADRs
- Agents MUST NOT: bypass specifications, write unapproved features, modify constitution, access secrets directly, perform destructive database operations

### III. Separation of Concerns (Architecture)

**Clear boundaries between governance, specifications, planning, and implementation.**

**Rules:**
- **Constitution** (this file): WHY - Principles, constraints, non-negotiables (applies to ALL phases)
- **Specification** (spec.md): WHAT - Requirements, user stories, acceptance criteria (phase-specific)
- **Plan** (plan.md): HOW - Architecture, components, technical approach (phase-specific)
- **Tasks** (tasks.md): BREAKDOWN - Atomic, testable work units (phase-specific)
- **Implementation** (code): EXECUTION - Code generated from tasks (phase-specific)

**Enforcement:**
- No mixing of concerns across artifact types
- Each artifact type has a defined template and validation rules
- Changes to architecture require plan updates BEFORE code changes
- Changes to requirements require spec updates BEFORE plan changes

### IV. Test-Driven Development (TDD) - Conditional

**Tests are written BEFORE implementation when explicitly required.**

**Rules:**
- TDD is MANDATORY when specifications explicitly request tests
- Red-Green-Refactor cycle: Write failing tests → Approve tests → Implement → Pass tests → Refactor
- Test types: Contract tests (API boundaries), Integration tests (user journeys), Unit tests (if specified)
- Test files must exist and fail before implementation code is written
- Tests must be independently executable and deterministic

**Enforcement:**
- Task ordering: Test tasks precede implementation tasks in tasks.md
- Test validation: Verify tests fail before implementation begins
- Test coverage: Must align with success criteria in specifications

**Note:** Tests are OPTIONAL by default - only include when success criteria explicitly require verification.

### V. Phased Evolution & Backward Compatibility

**Each phase builds on previous phases without breaking existing functionality.**

**Rules:**
- Phase completion gates: All tasks complete → All tests pass (if tests exist) → Phase deliverables validated
- No phase may be skipped - sequential implementation required
- New phase features must not break previous phase functionality
- Database migrations must be forward-compatible
- API versioning required when Phase II+ introduces breaking changes

**Enforcement:**
- Phase validation checklist before proceeding to next phase
- Regression testing of previous phase features when adding new phase
- Deployment verification at each phase boundary

### VI. Cloud-Native & Production-Grade Standards

**The system must be production-ready, not a prototype.**

**Rules:**
- 12-Factor App compliance (config via environment, stateless processes, port binding, etc.)
- Observability: Structured logging, metrics, distributed tracing for Phase IV+
- Security: JWT-based authentication, secrets management via environment variables, no hardcoded credentials
- Scalability: Horizontal scaling support (stateless services), database connection pooling
- Resilience: Graceful degradation, error handling at system boundaries, retry logic with exponential backoff

**Enforcement:**
- Constitution check in plan.md validates 12-factor compliance
- Security review required for authentication/authorization changes
- Performance budgets defined per phase (e.g., <200ms p95 latency for API endpoints)

### VII. Documentation as Code

**All project knowledge resides in versioned artifacts.**

**Rules:**
- CLAUDE.md: Agent instructions (how to work with this project)
- README.md: User-facing documentation (how to use this project)
- Prompt History Records (PHRs): All AI interactions recorded in `history/prompts/`
- Architecture Decision Records (ADRs): Significant decisions documented in `history/adr/`
- Quickstart guides: Step-by-step setup and verification

**Enforcement:**
- PHR creation mandatory after every AI interaction (except /sp.phr itself)
- ADR suggestion mandatory for architecturally significant decisions (3-part test: impact, alternatives, scope)
- Documentation updates included in task definitions

---

## 3. Spec-Driven Development Rules

### Specification Hierarchy (Authority Order)

1. **Constitution** (this file) - Highest authority, applies to all phases
2. **Specification** (spec.md) - Defines WHAT to build per phase
3. **Plan** (plan.md) - Defines HOW to build per phase
4. **Tasks** (tasks.md) - Defines atomic work units per phase

**Conflict Resolution:** If artifacts conflict, higher authority overrides. Constitution supersedes all.

### Specification Lifecycle (Per Phase)

```
User Input → /sp.specify → spec.md (WHAT)
           ↓
spec.md → /sp.plan → plan.md + research.md + data-model.md + contracts/ (HOW)
        ↓
plan.md → /sp.tasks → tasks.md (BREAKDOWN)
         ↓
tasks.md → /sp.implement → Code (EXECUTION)
```

### Specification Requirements

**spec.md MUST contain:**
- User stories (prioritized P1, P2, P3... for independent testing)
- Functional requirements (FR-XXX format with MUST/SHOULD/MAY)
- Acceptance criteria (measurable, testable)
- Success criteria (observable outcomes)
- Edge cases and error scenarios

**plan.md MUST contain:**
- Technical context (language, dependencies, platform, constraints)
- Constitution check (pass/fail with justifications)
- Project structure (concrete paths, no placeholders)
- Complexity tracking (if constitution violations justified)
- Architecture decisions (with ADR references for significant decisions)

**tasks.md MUST contain:**
- Task ID, priority marker [P], user story marker [Story]
- Exact file paths in descriptions
- Phase grouping (Setup → Foundational → User Stories → Polish)
- Clear dependencies and execution order
- Test tasks BEFORE implementation tasks (if tests required)

---

## 4. Agentic Governance & Skill Reuse

### Agent Definition (Governance Level)

An **Agent** is an autonomous AI entity that:
- Operates within defined authority boundaries (Section 2.II)
- Executes tasks by reading specifications and producing artifacts
- Mediates ALL actions through approved tools (Claude Code CLI, MCP servers)
- Records all significant interactions via PHRs
- Suggests (not creates) ADRs when detecting architectural decisions

**Agent Types in This Project:**
- **Primary Agent:** Claude Code CLI (main builder)
- **Subagents:** Specialized agents for complex tasks (Explore, Plan, General-purpose)
- **Skills:** Reusable agent capabilities exposed as commands (sp.specify, sp.plan, sp.tasks, sp.implement, etc.)

### Skill Definition (Governance Level)

A **Skill** is a stateless, reusable capability that:
- Takes structured input (arguments, context) and produces structured output (files, reports)
- Operates phase-agnostically (same skill works across all phases with different inputs)
- Follows the specification hierarchy (cannot bypass constitution)
- Produces versioned, auditable artifacts (with PHRs)
- Has clear success/failure criteria

**Skill Requirements:**
- Stateless: No persistent state between invocations
- Idempotent: Running twice produces same result (unless inputs change)
- Composable: Skills can call other skills (via spec-driven workflow)
- Documented: Clear input/output contracts, usage examples

**Note:** Concrete agent lists and skill implementations are defined in separate documents (CLAUDE.md, skill definition files), NOT in this constitution.

### Agent Authority Boundaries (Enforcement)

**Agents MUST:**
- Read specifications before acting
- Request clarification when specifications are ambiguous
- Create PHRs after significant interactions
- Suggest ADRs (not create) when detecting architecturally significant decisions
- Operate only on files within project scope
- Respect phase boundaries (no skipping phases)

**Agents MUST NOT:**
- Modify constitution.md without explicit human approval
- Bypass specification workflow (no "vibe coding")
- Access databases directly (only via MCP tools which are stateless and store state in DB)
- Modify specifications without human approval
- Invent features not in specifications
- Store secrets or credentials (use environment variables)
- Perform destructive operations without confirmation (e.g., DELETE database operations)

### Agent Safety & Guardrails

**Pre-execution Checks:**
- Validate task ID exists in tasks.md
- Verify specification artifact exists (spec.md, plan.md)
- Check constitution compliance for proposed changes
- Confirm no conflicting tasks in progress

**Post-execution Validation:**
- Verify output matches task acceptance criteria
- Run tests (if tests exist) and validate they pass
- Create PHR with prompt/response captured
- Update task status to completed

**Failure Handling:**
- Stop immediately if specification conflict detected
- Request human intervention for ambiguous requirements
- Log all errors with context (task ID, spec section, error details)
- Rollback partial changes if task fails mid-execution

---

## 5. Agent Authority Boundaries

Covered comprehensively in Section 4 (Agentic Governance & Skill Reuse).

---

## 6. Tooling & Execution Constraints

### Approved Tools (Mandatory Usage)

**Primary Development Tools:**
- **Claude Code CLI** - Main agent execution environment
- **Spec-Kit Plus (specifyplus)** - Specification management (init, specify, plan, tasks, implement commands)
- **MCP Servers** - Model Context Protocol for tool exposure (Official MCP SDK for Phase III+)
- **Git** - Version control (with commit message conventions: spec-driven references)

**Language & Framework Stack (Per Phase):**
- Phase I: Python 3.13+, UV package manager
- Phase II: Python FastAPI (backend), Next.js 16+ (frontend), SQLModel (ORM), Neon Serverless PostgreSQL, Better Auth (authentication)
- Phase III: OpenAI Agents SDK, Official MCP SDK, OpenAI ChatKit (frontend)
- Phase IV: Docker, Minikube, Helm Charts, kubectl-ai, kagent, Docker AI (Gordon)
- Phase V: Kubernetes (DOKS/GKE/AKS), Kafka (Strimzi/Redpanda), Dapr

**Prohibited Actions:**
- Manual code writing (must use spec-driven generation)
- Direct database CLI access by agents (only via MCP tools)
- Hardcoding secrets in code (use environment variables)
- Using unapproved tools or frameworks without constitution amendment

### Execution Environment (Platform Constraints)

**Development Environment:**
- Windows users MUST use WSL 2 (Windows Subsystem for Linux)
- Linux/macOS users work natively
- All development inside project root (no external dependencies without justification)

**Deployment Targets (Per Phase):**
- Phase I: Local Python environment
- Phase II: Vercel (frontend) + local/cloud FastAPI (backend)
- Phase III: Vercel (ChatKit frontend) + FastAPI backend + Neon DB
- Phase IV: Minikube (local Kubernetes cluster)
- Phase V: DigitalOcean DOKS (or GKE/AKS with free credits), Kafka on Strimzi/Redpanda

### File Structure Conventions

**Repository Root Structure:**
```
The-Evolution-of-Todo/
├── .specify/                    # Spec-Kit configuration & templates
│   ├── memory/
│   │   └── constitution.md      # This file
│   ├── templates/               # Spec, plan, tasks templates
│   └── scripts/                 # PHR creation scripts
├── specs/                       # Phase-specific specifications
│   └── <phase-name>/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── contracts/           # API contracts
├── history/
│   ├── prompts/                 # Prompt History Records (PHRs)
│   │   ├── constitution/        # Constitution-related prompts
│   │   ├── <feature-name>/      # Feature-specific prompts
│   │   └── general/             # General prompts
│   └── adr/                     # Architecture Decision Records
├── src/                         # Phase I source code
├── backend/                     # Phase II+ backend
├── frontend/                    # Phase II+ frontend
├── CLAUDE.md                    # Agent instructions (references this constitution)
└── README.md                    # User documentation
```

**Path Conventions:**
- Single project (Phase I): `src/`, `tests/` at repository root
- Web app (Phase II+): `backend/src/`, `frontend/src/`
- Tests always mirror source structure: `tests/contract/`, `tests/integration/`, `tests/unit/`

---

## 7. Security & Authentication Governance

### Authentication Architecture (Phase II+)

**Requirements:**
- Better Auth for user authentication (JavaScript/TypeScript library on Next.js frontend)
- JWT (JSON Web Token) for stateless authentication between frontend and backend
- Shared secret key via `BETTER_AUTH_SECRET` environment variable (both services)
- Token expiry: 7 days (configurable via environment)

**Security Rules:**
- All API endpoints (Phase II+) require valid JWT token in `Authorization: Bearer <token>` header
- User data isolation: All queries MUST filter by authenticated user ID
- No session sharing: Frontend and backend verify JWT independently (stateless)
- Requests without token return 401 Unauthorized
- Task ownership enforced on every CRUD operation

### Secrets Management

**Rules:**
- NO secrets in code, specs, or configuration files committed to Git
- All secrets via environment variables (`.env` for local, platform secrets for cloud)
- Secret names use SCREAMING_SNAKE_CASE: `DATABASE_URL`, `OPENAI_API_KEY`, `BETTER_AUTH_SECRET`
- Phase IV+ uses Kubernetes Secrets (or Dapr Secrets API for multi-cloud)

**Prohibited:**
- Hardcoded API keys, database passwords, JWT secrets
- Secrets in log output or error messages
- Committing `.env` files (must be in `.gitignore`)

### Data Privacy & User Isolation (Phase II+)

**Rules:**
- Multi-tenant architecture: Each user sees ONLY their own data
- Database queries MUST include `WHERE user_id = <authenticated_user_id>`
- MCP tools MUST validate user_id parameter matches authenticated user
- No cross-user data leakage (enforce at API and database layers)

**Validation:**
- Security review required for any endpoint accessing user data
- Integration tests MUST verify user isolation
- Penetration testing encouraged (authorized only)

---

## 8. AI Agent Safety & Guardrails

Covered comprehensively in Section 4 (Agentic Governance & Skill Reuse - Agent Safety & Guardrails subsection).

**Additional Constraints:**

### Input Validation
- AI agents MUST validate all user inputs before processing
- Sanitize inputs to prevent injection attacks (SQL, command, XSS)
- Reject malformed inputs with clear error messages

### Output Validation
- All agent outputs (code, specs, plans) MUST pass validation before committing
- No unresolved placeholders (e.g., `[PLACEHOLDER]`, `TODO`) in deliverables
- Generated code MUST pass linting/formatting checks

### Rate Limiting & Cost Control
- Agents MUST NOT make unbounded API calls (implement retry limits)
- Token usage monitoring for OpenAI API (Phase III+)
- Alert on anomalous usage patterns

---

## 9. Infrastructure, Deployment & Cloud Readiness

### 12-Factor App Compliance (Mandatory for Phase II+)

**Required Factors:**
1. **Codebase:** Single repo, tracked in Git, multiple deploys (Vercel, DOKS)
2. **Dependencies:** Explicitly declared (requirements.txt, package.json, no implicit system deps)
3. **Config:** Environment variables, no hardcoded config
4. **Backing Services:** Attachable resources (Neon DB, Kafka) via URLs in config
5. **Build, Release, Run:** Strict separation (Phase IV+ with Docker images)
6. **Processes:** Stateless, share-nothing (conversation state in DB, not memory)
7. **Port Binding:** Self-contained services (FastAPI on port 8000, Next.js on 3000)
8. **Concurrency:** Horizontal scaling (Phase IV+ with Kubernetes replicas)
9. **Disposability:** Fast startup/shutdown, graceful termination
10. **Dev/Prod Parity:** Same dependencies, same backing services (Neon DB in both)
11. **Logs:** Treat as event streams (stdout/stderr, not log files)
12. **Admin Processes:** One-off tasks via CLI (database migrations via script)

### Containerization Standards (Phase IV+)

**Dockerfile Requirements:**
- Multi-stage builds (build stage + runtime stage for minimal images)
- Non-root user for security
- Health checks defined (HEALTHCHECK instruction)
- Explicit base image versions (no `latest` tags)
- Layer caching optimization (COPY dependencies first, then code)

**Docker Compose (Local Development Phase IV):**
- Services: frontend, backend, database (optional local Postgres)
- Networks: Isolated networks per service group
- Volumes: Persistent data for local database

### Kubernetes Standards (Phase IV+)

**Manifest Requirements:**
- Deployments: Replica count ≥ 2 for production, resource limits defined
- Services: LoadBalancer/NodePort for external access, ClusterIP for internal
- ConfigMaps: Non-secret configuration
- Secrets: Sensitive configuration (JWT secrets, database passwords)
- Health Probes: Liveness and readiness probes for all services

**Helm Charts (Phase IV+):**
- Chart structure: Chart.yaml, values.yaml, templates/
- Parameterization: Environment-specific values (dev, staging, prod)
- Dependencies: External charts declared (e.g., Kafka via Strimzi)

**AIOps Tools (Phase IV+):**
- kubectl-ai for natural language Kubernetes operations
- kagent for cluster health analysis
- Docker AI (Gordon) for Docker operations (if available)

### Event-Driven Architecture (Phase V)

**Kafka Integration:**
- Topics: `task-events`, `reminders`, `task-updates`
- Producer: Chat API (publishes task CRUD events)
- Consumers: Recurring Task Service, Notification Service, Audit Service
- Schema: Defined in ADRs, versioned

**Dapr Integration (Phase V):**
- Building Blocks: Pub/Sub (Kafka), State Management (PostgreSQL), Service Invocation, Jobs API (reminders), Secrets
- Sidecar Pattern: Dapr sidecar per service pod
- Component Configuration: YAML files in `dapr-components/`
- Portability: Swap Kafka for RabbitMQ via config (no code changes)

---

## 10. Observability, Reliability & Production Standards

### Logging Standards (All Phases)

**Requirements:**
- Structured logging: JSON format with `timestamp`, `level`, `message`, `context` fields
- Log levels: DEBUG (local only), INFO (normal operations), WARN (recoverable errors), ERROR (failures)
- Correlation IDs: Trace requests across services (Phase IV+ with Dapr)
- No sensitive data in logs (no passwords, tokens, PII)

**Python (FastAPI):**
```python
import logging
import json

logger = logging.getLogger(__name__)
logger.info("Task created", extra={"task_id": task.id, "user_id": user.id})
```

### Monitoring & Alerting (Phase IV+)

**Metrics (Required):**
- Application: Request rate, error rate, latency (p50, p95, p99)
- Infrastructure: CPU, memory, disk usage, pod restarts
- Business: Task creation rate, active users, chatbot usage

**Alerts (Critical):**
- Error rate > 5% for 5 minutes
- p95 latency > 500ms for 5 minutes
- Pod crash loop detected
- Database connection pool exhausted

**Tools:**
- Kubernetes metrics: kubectl top, Prometheus (optional Phase V)
- Logs aggregation: kubectl logs, ELK stack (optional Phase V)

### Error Handling Standards (All Phases)

**Rules:**
- Fail fast at system boundaries (validate user input immediately)
- Graceful degradation (if external service fails, return cached data or error message)
- Retry logic with exponential backoff (for transient failures like network timeouts)
- Circuit breaker pattern for external services (Phase V with Dapr)

**Error Response Format (Phase II+):**
```json
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 123 does not exist",
    "details": {
      "task_id": 123,
      "user_id": "user-456"
    }
  }
}
```

### Performance Budgets (Per Phase)

**Phase I (Console):** Instant response (<100ms for in-memory operations)

**Phase II (Web App):**
- API latency: p95 < 200ms
- Frontend load time: < 2 seconds (initial page)
- Database query time: < 50ms (indexed queries)

**Phase III (Chatbot):**
- AI response time: < 5 seconds (includes OpenAI API call)
- MCP tool invocation: < 100ms (each tool)
- Conversation history load: < 200ms

**Phase IV (Kubernetes):**
- Service startup: < 30 seconds
- Health check response: < 1 second
- Horizontal scaling: New pod ready in < 60 seconds

**Phase V (Production):**
- Maintain Phase II-IV budgets under load (1000 concurrent users)
- Kafka message throughput: 10,000 messages/second
- Event processing latency: < 1 second (from publish to consume)

### Reliability Targets (Phase V)

**Availability:**
- Target: 99.9% uptime (no more than 43 minutes downtime/month)
- Achieved via: Multi-replica deployments, health checks, automatic restarts

**Data Durability:**
- Database backups: Daily automated (Neon DB handles this)
- Recovery Point Objective (RPO): < 24 hours
- Recovery Time Objective (RTO): < 1 hour

---

## 11. Amendment Policy (Additive-Only)

### Amendment Principles

**This constitution is ADDITIVE-ONLY:**
- New principles may be ADDED to address emerging needs
- Existing principles may be CLARIFIED but NOT weakened or removed
- Amendments require human approval (AI agents cannot amend)
- All amendments documented with rationale and date

### Amendment Process

1. **Proposal:** Human or AI agent identifies need for amendment
2. **Justification:** Document why amendment needed (new phase requirements, technical constraints, lessons learned)
3. **Impact Analysis:** Review affected specifications, plans, tasks (all phases)
4. **Approval:** Human approves amendment (AI agents suggest, humans decide)
5. **Documentation:** Update constitution with version bump and amendment record
6. **Propagation:** Update dependent artifacts (specs, plans, CLAUDE.md) for consistency

### Versioning (Semantic Versioning)

**Format:** MAJOR.MINOR.PATCH (e.g., 1.2.3)

**Version Increment Rules:**
- **MAJOR:** Backward-incompatible changes (removing/redefining principles)
- **MINOR:** New principle/section added, materially expanded guidance
- **PATCH:** Clarifications, typo fixes, non-semantic refinements

**Current Version:** 1.0.0 (Initial Constitution)

### Amendment Record

**Version 1.0.0 - 2025-12-28 (Initial Ratification)**
- Created comprehensive constitution for The Evolution of Todo project
- Defined 11 core sections covering governance, principles, tooling, security, infrastructure, observability
- Established spec-driven development workflow for all 5 phases
- Documented agentic governance and agent authority boundaries

---

## Governance

### Enforcement

**Constitution Authority:**
- This constitution supersedes all other practices, guidelines, and preferences
- All specifications (spec.md, plan.md, tasks.md) MUST comply with this constitution
- Constitution violations require explicit justification in plan.md (Complexity Tracking section)

**Compliance Verification:**
- Every plan.md MUST include "Constitution Check" section (pass/fail per principle)
- Every pull request MUST reference task IDs and verify constitution compliance
- Agents MUST stop and request human intervention if constitution conflict detected

**Amendment Authority:**
- Only humans may amend this constitution
- AI agents may SUGGEST amendments but cannot execute them
- Amendments require impact analysis and version bump

**Runtime Guidance:**
- See **CLAUDE.md** for agent-specific instructions on how to work with this constitution
- See **README.md** for user-facing documentation on using the system
- See **history/adr/** for architectural decisions made during implementation

---

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28

---

## Appendix: Quick Reference

### Specification Workflow (One-Page Summary)

```
User Input
    ↓
/sp.specify → specs/<phase>/spec.md
    ↓
/sp.plan → specs/<phase>/plan.md + research.md + data-model.md + contracts/
    ↓
/sp.tasks → specs/<phase>/tasks.md
    ↓
/sp.implement → Code (backend/src/, frontend/src/, or src/)
    ↓
Tests Pass (if tests exist) + PHR Created + ADR Suggested (if significant decision)
    ↓
Phase Complete → Next Phase
```

### Phase Progression Checklist

**Phase I → Phase II:**
- [ ] Console app complete with all Basic features
- [ ] In-memory task management working
- [ ] Spec-driven workflow validated
- [ ] PHRs created for all interactions

**Phase II → Phase III:**
- [ ] Web app deployed (Vercel frontend + FastAPI backend)
- [ ] Authentication working (Better Auth + JWT)
- [ ] Multi-user support with data isolation
- [ ] RESTful API endpoints complete
- [ ] Neon DB integration working

**Phase III → Phase IV:**
- [ ] AI chatbot functional (ChatKit + Agents SDK)
- [ ] MCP server exposing task tools
- [ ] Natural language commands working
- [ ] Stateless chat endpoint with DB persistence
- [ ] Conversation history maintained

**Phase IV → Phase V:**
- [ ] Local Kubernetes deployment (Minikube)
- [ ] Docker containers built and tested
- [ ] Helm charts created and validated
- [ ] AIOps tools configured (kubectl-ai, kagent)
- [ ] Health checks and monitoring setup

**Phase V Complete:**
- [ ] Cloud Kubernetes deployment (DOKS/GKE/AKS)
- [ ] Advanced features implemented (recurring tasks, reminders, priorities, tags)
- [ ] Kafka event-driven architecture working
- [ ] Dapr integration complete (Pub/Sub, State, Jobs, Secrets)
- [ ] CI/CD pipeline functional
- [ ] Production observability and monitoring

### Agent Quick Commands

```bash
# Initialize project
specifyplus init <project-name>

# Specification workflow
/sp.specify "Feature description..."
/sp.plan
/sp.tasks
/sp.implement

# Documentation
/sp.phr --title "..." --stage <stage>
/sp.adr "Decision title..."

# Validation
/sp.analyze  # Cross-artifact consistency check
/sp.checklist  # Generate custom checklist
```

### Critical Files (Always Read First)

1. **.specify/memory/constitution.md** (this file) - Project principles
2. **CLAUDE.md** - Agent instructions
3. **specs/<current-phase>/spec.md** - What to build
4. **specs/<current-phase>/plan.md** - How to build
5. **specs/<current-phase>/tasks.md** - Work breakdown

---

*This constitution is a living document. As the project evolves through phases, amendments may be proposed to address new requirements while maintaining the core principles of spec-driven, AI-native development.*

**Next Steps:**
1. Review this constitution with project team
2. Create Phase I specification using `/sp.specify`
3. Begin spec-driven development workflow
4. Record all interactions via PHRs
5. Suggest ADRs for architectural decisions
