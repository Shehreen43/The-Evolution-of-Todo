# Phase IV: Local Kubernetes Deployment

## Overview
This document outlines the deployment of the Todo Chatbot application to a local Kubernetes cluster using Docker Desktop with Kubernetes enabled.

## Prerequisites
- Docker Desktop with Kubernetes enabled
- Helm 3.x
- kubectl
- Node.js 20.x
- Python 3.11

## Architecture
The deployment consists of:
- Frontend: Next.js application running in Docker container
- Backend: FastAPI application running in Docker container
- MCP Server: Model Context Protocol server for AI integration
- PostgreSQL: Database for persistent storage

## Containerization
All services are containerized using multi-stage Docker builds with security best practices:
- Non-root user execution
- Minimal base images (Alpine Linux)
- Optimized layer caching

## Kubernetes Deployment
The application is packaged as a Helm chart with:
- Environment-specific configurations (dev, test, prod)
- Resource limits and requests
- Health checks and readiness probes
- Network policies for security
- RBAC configurations

## Deployment Steps

### 1. Build Containers
```bash
./build-containers.sh
```

### 2. Deploy with Helm
```bash
# Navigate to the helm directory
cd helm/todo-chatbot/

# Install the chart with development values
helm install todo-chatbot-release . -f values-dev.yaml
```

### 3. Verify Deployment
```bash
# Check all resources
kubectl get all -n default

# Check pods
kubectl get pods

# Check services
kubectl get services
```

## Accessing the Application
- Frontend: http://localhost (via ingress) or the NodePort service
- Backend API: http://localhost:8000 (via port forward or service)
- MCP Server: http://localhost:8080 (via port forward or service)

## Troubleshooting
Refer to docs/TROUBLESHOOTING.md for common issues and solutions.

## Security Considerations
- All containers run as non-root users
- Network policies restrict pod communication
- RBAC configured with least-privilege access
- Secrets encrypted at rest

## Monitoring
- Prometheus service monitor configured for metrics collection
- Health endpoints available on all services
- Resource utilization tracked via Kubernetes metrics