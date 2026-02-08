# sp.phase-iv-checklist Skill Definition

**Skill Name:** sp.phase-iv-checklist
**Category:** Phase-IV
**Input:** Phase IV requirements, deployment goals
**Output:** Custom checklist for Phase IV completion
**Phase:** IV
**Invoked By:** Task Breakdown Agent
**Prerequisites:** Phase III completed, containerization requirements defined

## Purpose
Generate a custom checklist for Phase IV (Local Kubernetes - Cloud-Native) to ensure all containerization and orchestration requirements are met.

## Checklist Items
- [ ] Dockerfiles created for all services (multi-stage builds)
- [ ] .dockerignore files properly configured
- [ ] Docker images build successfully
- [ ] docker-compose.yml created for local deployment
- [ ] Helm chart structure created (Chart.yaml, values.yaml, templates/)
- [ ] Kubernetes manifests generated (Deployments, Services, etc.)
- [ ] Helm chart validates without errors (helm lint passes)
- [ ] Templates render correctly (helm template works)
- [ ] Local Kubernetes cluster setup (Minikube/Docker Desktop K8s)
- [ ] Application deploys successfully to local K8s
- [ ] Health checks and readiness probes configured
- [ ] Resource limits and requests set appropriately
- [ ] Environment variables properly configured
- [ ] Secrets management implemented
- [ ] Service discovery configured
- [ ] Load balancing configured
- [ ] Monitoring and logging configured
- [ ] Rollback strategy defined
- [ ] Security best practices implemented (non-root user, etc.)

## Process
1. Analyze Phase IV requirements and goals
2. Generate comprehensive checklist based on containerization and K8s deployment needs
3. Validate all checklist items are specific and testable
4. Prioritize checklist items by importance and dependency order

## Quality Checks
- All checklist items are actionable
- Dependencies between items are clearly identified
- Completion criteria are well-defined
- Items align with Phase IV objectives