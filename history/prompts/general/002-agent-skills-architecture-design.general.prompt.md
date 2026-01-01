---
id: 002
title: Design Agent and Skills Architecture for All Phases
stage: general
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: system
command: analysis
labels: ["architecture", "agents", "skills", "phase-planning", "ai-native"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - AGENTS-AND-SKILLS-ARCHITECTURE.md
tests:
  - N/A (architectural design)
---

## Prompt

Analyze "Hackathon II - Todo Spec-Driven Development.md" and constitution.md to design a comprehensive set of agents and skills for completing all 5 phases of "The Evolution of Todo" project.

**Requirements:**
- Design agent architecture (strategic, execution, support, infrastructure)
- Define skills catalog (core, phase-specific, integration)
- Map agents/skills to each phase (I: Console, II: Web, III: Chatbot, IV: K8s, V: Cloud)
- Ensure constitutional compliance (agent authority boundaries, stateless skills)
- Provide phase-based progression gates
- Create implementation roadmap

**Context:**
- Project progresses from console app → web app → AI chatbot → local K8s → cloud production
- Human operates as orchestrator, AI agents execute via Claude Code CLI
- Constitution defines governance, spec-driven workflow, agentic architecture
- All agents must operate within authority boundaries (no direct DB access, no constitution modification without approval)

## Response snapshot

Successfully designed comprehensive agent and skills architecture:

**Agent Architecture (14 Agents):**
- **Strategic (4)**: Constitution, Specification, Planning, Task Breakdown
- **Execution (3)**: Implementation, Testing, Git
- **Support (4)**: PHR, ADR, Analysis, Reverse Engineering
- **Infrastructure (3)**: Docker, Kubernetes, Event-Driven

**Skills Catalog (28 Skills):**
- **Core (12)**: sp.constitution, sp.specify, sp.plan, sp.tasks, sp.implement, sp.phr, sp.adr, sp.analyze, sp.clarify, sp.checklist, sp.git.commit_pr, sp.reverse-engineer
- **Phase-Specific (10)**: sp.console-setup, sp.web-scaffold, sp.auth-setup, sp.mcp-server, sp.chatbot-setup, sp.containerize, sp.helm-chart, sp.kafka-setup, sp.dapr-components, sp.ci-cd-setup
- **Integration (6)**: sp.api-contract, sp.db-migration, sp.test-contract, sp.test-integration, sp.taskstoissues

**Phase Distribution:**
- Phase I: 7 agents, 8 skills (establish workflow)
- Phase II: 9 agents, 14 skills (add web + auth)
- Phase III: 10 agents, 16 skills (add AI chatbot)
- Phase IV: 12 agents, 18 skills (add containerization + K8s)
- Phase V: 14 agents, 28 skills (add events + production)

**Key Design Principles:**
- Clear separation: Strategic agents separate from execution agents
- Constitutional compliance: Every agent operates within defined boundaries
- Phase-agnostic core: Core skills work across all phases
- Stateless design: All skills are idempotent and stateless
- Human orchestration: Agents execute, humans approve
- Audit trail: PHR Agent records all interactions
- Progressive complexity: Start minimal, scale incrementally

**Authority Matrix:**
- Constitution Agent: Only agent that can write constitution (with human approval)
- Specification Agent: Read-write on spec.md only
- Planning Agent: Read-write on plan artifacts only
- Implementation Agent: Read-write on code files
- All agents: Must read constitution before acting, cannot bypass spec workflow

**Implementation Roadmap:**
1. Create agent configuration files (`.claude/agents/*.yaml`)
2. Create skill definition files (`.claude/skills/{core,phase-specific,integration}/*.md`)
3. Build MCP server for skills (optional - can use existing `.claude/commands/`)
4. Test Phase I workflow (minimal agents)
5. Iterate based on learnings
6. Scale to Phase II-V incrementally

**Directory Structure:**
- Agents: `.claude/agents/*.yaml` (14 agent configurations)
- Skills: `.claude/skills/{core,phase-specific,integration}/*.md` (28 skill definitions)
- Commands: `.claude/commands/*.md` (existing sp.* commands)

**Deliverable:**
- Comprehensive architecture document: `AGENTS-AND-SKILLS-ARCHITECTURE.md`
- Agent authority matrix with invocation patterns
- Skill dependency graph
- Phase-based mapping with triggers and frequencies
- Orchestration workflow examples (complete Phase I walkthrough)
- Agent invocation decision tree
- When agents/skills invoke tables (core, phase-specific, integration)
- Complete directory structure summary

## Outcome

- ✅ Impact: Provided clear blueprint for implementing 14 agents and 28 skills across all 5 phases; architecture ensures constitutional compliance, spec-driven workflow, and human orchestration
- 🧪 Tests: N/A (architectural design document)
- 📁 Files: Created AGENTS-AND-SKILLS-ARCHITECTURE.md (comprehensive agent/skill architecture proposal)
- 🔁 Next prompts:
  - Create agent configuration files in `.claude/agents/`
  - Create skill definition files in `.claude/skills/`
  - Build MCP server for skills (optional)
  - Begin Phase I: `/sp.specify "In-Memory Python Console Todo App with Basic features"`
- 🧠 Reflection: Architecture successfully balances simplicity (minimal agents in Phase I) with scalability (14 agents by Phase V); clear authority boundaries prevent constitutional violations; phase-agnostic core skills (sp.specify, sp.plan, sp.tasks, sp.implement) work across all phases with phase-specific skills adding functionality incrementally; human-as-orchestrator model maintained throughout; added comprehensive invocation patterns showing WHEN each agent/skill triggers, preconditions, postconditions, and frequencies; complete Phase I workflow example demonstrates agent orchestration flow; decision tree helps determine which agent to invoke based on user input

## Evaluation notes (flywheel)

- Failure modes observed: None - architecture design completed successfully
- Graders run and results (PASS/FAIL):
  - Constitutional compliance: PASS (all agents respect authority boundaries)
  - Phase alignment: PASS (agents/skills map correctly to hackathon phases)
  - Separation of concerns: PASS (strategic/execution/support/infrastructure clearly separated)
  - Stateless design: PASS (all skills are idempotent and stateless)
  - Human orchestration: PASS (agents execute, humans approve significant decisions)
- Prompt variant (if applicable): N/A (initial architecture design)
- Next experiment (smallest change to try): Test Phase I workflow with minimal agents (Constitution, Specification, Planning, Task Breakdown, Implementation, PHR, Git) to validate architecture before scaling to Phase II-V
