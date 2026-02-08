# ADR-0003: Kubernetes Networking Strategy

## Status
Accepted

## Context
We need to determine how our application components will communicate both internally within the cluster and externally with users and external services. The networking strategy impacts security, performance, scalability, and accessibility of our application.

## Decision
We will use ClusterIP services for internal communication combined with Ingress for external access:
- Frontend: ClusterIP service with external access via Ingress
- Backend: ClusterIP service for internal access only
- MCP Server: ClusterIP service for internal access only
- External access: NGINX Ingress Controller with TLS termination
- Internal communication: Direct service-to-service communication via ClusterIP services

## Considered Options
A) ClusterIP + Ingress - Internal services with external access through ingress
B) NodePort - Direct access to services via node IP and port
C) LoadBalancer - Cloud provider load balancer for external access

## Rationale
Option A (ClusterIP + Ingress) was chosen because:
- Provides proper service isolation within the cluster
- Enables centralized external access management through ingress
- Supports TLS termination at the ingress layer
- Allows for path-based routing and host-based routing
- Enables advanced features like rate limiting, authentication at ingress level
- Follows Kubernetes best practices for service exposure
- Works well in both local (Minikube) and cloud environments
- Proper separation of internal and external traffic

Option B (NodePort) was rejected because it exposes services directly on the node, reducing security and making it harder to manage external access patterns.

Option C (LoadBalancer) was rejected because it's not suitable for local Minikube deployment and creates unnecessary cloud dependencies for a local deployment phase.

## Consequences
### Positive Impacts
- Proper service isolation and security within the cluster
- Centralized external access management
- Support for TLS and advanced routing features
- Consistent networking pattern that works in local and cloud environments
- Better security posture with internal services not exposed externally
- Flexible routing options (path-based, host-based)

### Negative Impacts
- Additional complexity with ingress controller setup
- Extra configuration for external access
- Dependency on ingress controller availability
- Slight increase in request latency due to ingress layer

## Trade-offs
- Security vs. Simplicity: More secure isolation but additional configuration complexity
- Flexibility vs. Overhead: Advanced routing features but requires ingress management
- Standardization vs. Direct Access: Standard Kubernetes pattern but adds a network hop

## References
- plan.md: Section on service connectivity and external access
- spec.md: Networking requirements and security considerations