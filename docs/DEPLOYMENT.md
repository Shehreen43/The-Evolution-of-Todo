# Deployment Guide

## Prerequisites
- Docker Desktop with Kubernetes enabled OR Minikube
- Helm 3.x
- kubectl
- Node.js 20.x
- Python 3.11

## Local Development Setup
1. Clone the repository
2. Navigate to the project directory
3. Build Docker images using build scripts
4. Deploy to local Kubernetes cluster using Helm

## Building Containers
```bash
# Build all containers
./build-containers.sh

# Or build individual containers
docker build -t todo-frontend:latest -f docker/frontend/Dockerfile .
docker build -t todo-backend:latest -f docker/backend/Dockerfile .
docker build -t todo-mcp-server:latest -f backend/Dockerfile.mcp .
```

## Deploying with Helm
```bash
# Add the Helm repository (if remote)
helm repo add todo-chatbot .

# Install the chart
helm install todo-chatbot-release helm/todo-chatbot/ -f helm/todo-chatbot/values-dev.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

## Accessing the Application
- Frontend: http://localhost:3000 (or via ingress)
- Backend API: http://localhost:8000
- MCP Server: http://localhost:8080