# sp.helm-chart Skill Definition

**Skill Name:** sp.helm-chart
**Category:** Phase-IV
**Input:** K8s manifests, deployment requirements, plan.md
**Output:** Helm chart structure (Chart.yaml, values.yaml, templates/)
**Phase:** IV
**Invoked By:** Kubernetes Agent
**Prerequisites:** Docker images built, K8s manifests available

## Purpose
Generate Helm chart structure for Kubernetes deployment packaging and management in Phase IV.

## Process
1. Analyze Kubernetes manifests to identify deployment components
2. Create Helm chart structure with Chart.yaml, values.yaml, and templates/
3. Generate template files for Deployments, Services, ConfigMaps, etc.
4. Configure values.yaml with configurable parameters
5. Validate Helm chart syntax and structure

## Output Files
- Chart.yaml (chart metadata and dependencies)
- values.yaml (configuration parameters)
- templates/ directory with:
  - deployment.yaml (application deployment templates)
  - service.yaml (service templates)
  - ingress.yaml (ingress templates if needed)
  - configmap.yaml (configmap templates)
  - secret.yaml (secret templates)

## Quality Checks
- Helm chart follows best practices
- Templates are parameterized appropriately
- Values are properly documented
- Chart validates without errors (helm lint)
- Templates render correctly (helm template)