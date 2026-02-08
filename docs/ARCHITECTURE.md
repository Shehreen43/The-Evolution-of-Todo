# System Architecture

## Overview
This document outlines the architecture of the Todo Chatbot application for Phase IV: Local Kubernetes Deployment.

## Components
- Frontend: Next.js application running in Docker container
- Backend: FastAPI application running in Docker container
- MCP Server: Model Context Protocol server for AI integration
- Database: PostgreSQL for persistent storage
- Kubernetes: Orchestration layer
- Helm: Package management for Kubernetes

## Deployment Architecture
- Local Kubernetes cluster (Minikube/Docker Desktop)
- Service mesh for inter-service communication
- Ingress controller for external access
- Persistent volumes for data storage
- ConfigMaps and Secrets for configuration management

## Security Considerations
- Non-root containers for all services
- Network policies for service isolation
- RBAC for access control
- TLS termination at ingress