# ADR-0001: Container Base Images Selection

## Status
Accepted

## Context
We need to select base images for the frontend (Next.js) and backend (FastAPI) applications that will be deployed in Kubernetes. The choice of base images impacts security, image size, performance, and maintenance. We must balance between minimal footprint and functionality needed for our applications.

## Decision
We will use Alpine-based images for both frontend and backend:
- Frontend: `node:20-alpine`
- Backend: `python:3.11-alpine`
- MCP Server: `python:3.11-alpine`

## Considered Options
A) node:20-alpine + python:3.11-alpine - Minimal base images with small attack surface
B) node:20-slim + python:3.11-slim - Debian-based with slightly larger footprint but more tools
C) distroless/nodejs + distroless/python - Minimal images with only runtime and application

## Rationale
Option A (Alpine-based) was chosen because:
- Alpine images are significantly smaller than slim images, reducing download time and storage
- Smaller attack surface compared to Debian-based images
- Still provides necessary package managers (apk) for installing additional dependencies if needed
- Good community support and stability
- Consistent with industry best practices for container security
- Compatible with multi-stage builds to further reduce final image size

Option B (slim) was rejected due to larger image size and attack surface, though it would provide more debugging tools.

Option C (distroless) was rejected because it would make debugging more difficult during development and requires more complex build processes, which adds overhead for a local deployment phase.

## Consequences
### Positive Impacts
- Smaller image sizes lead to faster pull times and less storage usage
- Reduced attack surface improves security posture
- Lower bandwidth usage for image distribution
- Faster container startup times due to smaller image size

### Negative Impacts
- Alpine uses musl libc instead of glibc, which can cause compatibility issues with some native packages
- Fewer debugging tools available in the container (though this is also a security advantage)
- Potential issues with certain binary dependencies that expect glibc

## Trade-offs
- Security vs. Convenience: Smaller, more secure images but potentially more debugging complexity
- Size vs. Compatibility: Smaller images but potential compatibility issues with native modules
- Build simplicity vs. Runtime security: Slightly more complex build process to achieve better runtime security

## References
- plan.md: Section on container preparation and security considerations
- spec.md: Security specifications and container requirements