# Phase IV: Todo Chatbot Kubernetes Deployment Architecture

## System Overview

The Todo Chatbot application is designed as a microservices architecture deployed on Kubernetes. The system consists of frontend, backend, and MCP server components that communicate through internal Kubernetes services, with external access provided via ingress controllers.

### High-Level Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                        KUBERNETES CLUSTER                                            │
│                                                                                      │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────┐   │
│  │   Frontend      │    │    Backend      │    │   Neon DB       │    │  MCP    │   │
│  │   Pod           │    │    Pod          │    │  (External)     │    │ Server  │   │
│  │  ┌───────────┐  │    │  ┌───────────┐  │    │                 │    │ Pod     │   │
│  │  │ Next.js   │  │    │  │ FastAPI   │  │    │                 │    │         │   │
│  │  │ Container │  │    │  │ Container │  │    │                 │    │         │   │
│  │  └───────────┘  │    │  └───────────┘  │    │                 │    │         │   │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────┘   │
│         │                        │                        │               │           │
│         ▼                        ▼                        │               ▼           │
│  ┌─────────────────┐    ┌─────────────────┐              │    ┌─────────────────┐    │
│  │   Frontend      │    │    Backend      │              │    │   MCP Server    │    │
│  │   Service       │    │    Service      │              │    │   Service       │    │
│  └─────────────────┘    └─────────────────┘              │    └─────────────────┘    │
│         │                        │                        │               │           │
│         └────────────────────────┼────────────────────────┼───────────────┼───────────┘
│                                  │                        │               │
│                                  ▼                        ▼               ▼
│                         ┌─────────────────┐    ┌─────────────────┐    ┌─────────┐
│                         │    Ingress      │    │   Internal      │    │External │
│                         │    Controller   │    │   Communication │    │Services │
│                         └─────────────────┘    └─────────────────┘    └─────────┘
│                                  │                        │               │
│                                  ▼                        ▼               ▼
│                         External Access (HTTP/HTTPS)  MCP Communication  LLM APIs
└──────────────────────────────────────────────────────────────────────────────────────┘
```

### Component List

1. **Frontend Component**
   - Technology: Next.js 14 application
   - Container: Node.js runtime in Alpine Linux
   - Port: 3000
   - Purpose: User interface and chatbot UI

2. **Backend Component**
   - Technology: FastAPI application
   - Container: Python 3.11 runtime in Alpine Linux
   - Port: 8000
   - Purpose: API layer, business logic, authentication

3. **MCP Server Component**
   - Technology: Model Context Protocol server
   - Container: Python 3.11 runtime in Alpine Linux
   - Port: 8080
   - Purpose: Extend AI models with external tools and services

4. **External Database**
   - Technology: Neon PostgreSQL
   - Location: External to cluster
   - Purpose: Persistent data storage

5. **Kubernetes Infrastructure**
   - Orchestration: Minikube (local), will transition to cloud platforms
   - Networking: Ingress controller for external access
   - Service Discovery: Internal service communication

### Technology Stack

- **Container Runtime**: Docker
- **Orchestration**: Kubernetes (Minikube for local development)
- **Package Management**: Helm 3.x
- **Frontend Framework**: Next.js 14
- **Backend Framework**: FastAPI
- **Programming Languages**: JavaScript/TypeScript (frontend), Python (backend)
- **Database**: PostgreSQL (Neon hosted)
- **API Gateway**: NGINX Ingress Controller
- **Monitoring**: Prometheus, Grafana
- **AI Tools**: kubectl-ai, Kagent, Docker AI Agent (Gordon)

## Component Architecture

### Frontend Component

**Image Configuration:**
- Base: `node:20-alpine`
- Build Stage: Uses multi-stage build with `node:20-alpine` for production
- Production Stage: Runs from minimal image with only necessary files
- Size Target: <100MB compressed

**Port Configuration:**
- Container Port: 3000
- Service Port: 3000
- Protocol: TCP

**Resources:**
- CPU Request: 100m
- CPU Limit: 200m
- Memory Request: 128Mi
- Memory Limit: 256Mi

**Health Checks:**
- Readiness Probe: HTTP GET `/api/health`
- Liveness Probe: HTTP GET `/api/health`
- Initial Delay: 10 seconds
- Period: 10 seconds

**Security Context:**
- Run as Non-root: Enabled
- User ID: 1000
- File System Group: 2000

### Backend Component

**Image Configuration:**
- Base: `python:3.11-alpine`
- Dependencies: FastAPI, Uvicorn, SQLAlchemy, authentication libraries
- Size Target: <150MB compressed

**Port Configuration:**
- Container Port: 8000
- Service Port: 8000
- Protocol: TCP

**Resources:**
- CPU Request: 150m
- CPU Limit: 300m
- Memory Request: 256Mi
- Memory Limit: 512Mi

**Health Checks:**
- Readiness Probe: HTTP GET `/health`
- Liveness Probe: HTTP GET `/health`
- Initial Delay: 15 seconds
- Period: 15 seconds

**Security Context:**
- Run as Non-root: Enabled
- User ID: 1000
- File System Group: 2000

**Environment Variables:**
- `DATABASE_URL`: Database connection string (from secret)
- `BETTER_AUTH_SECRET`: Authentication secret (from secret)
- `OPENROUTER_API_KEY`: LLM API key (from secret)
- `MCP_SERVER_URL`: MCP server URL (from secret)

### MCP Server Component

**Image Configuration:**
- Base: `python:3.11-alpine`
- Dependencies: MCP server libraries, communication protocols
- Size Target: <100MB compressed

**Port Configuration:**
- Container Port: 8080
- Service Port: 8080
- Protocol: TCP

**Resources:**
- CPU Request: 100m
- CPU Limit: 200m
- Memory Request: 128Mi
- Memory Limit: 256Mi

**Health Checks:**
- Readiness Probe: HTTP GET `/health`
- Liveness Probe: HTTP GET `/health`
- Initial Delay: 10 seconds
- Period: 10 seconds

**Security Context:**
- Run as Non-root: Enabled
- User ID: 1000
- File System Group: 2000

**Environment Variables:**
- `OPENROUTER_API_KEY`: LLM API key (from secret)
- `MCPSERVER_HOST`: Internal service hostname
- `MCPSERVER_PORT`: Service port

### Kubernetes Resources

**Deployments:**
- Frontend Deployment: Manages frontend pods with scaling and updates
- Backend Deployment: Manages backend pods with scaling and updates
- MCP Server Deployment: Manages MCP server pods with scaling and updates

**Services:**
- Frontend Service: ClusterIP service for frontend access
- Backend Service: ClusterIP service for backend access
- MCP Server Service: ClusterIP service for MCP server access

**Ingress:**
- External access to frontend application
- TLS termination for secure connections
- Path-based routing for API endpoints

**ConfigMaps:**
- Application configuration parameters
- Feature flags and settings
- Non-sensitive configuration data

**Secrets:**
- Database connection strings
- API keys and authentication secrets
- TLS certificates

## Data Flow

### Request Flow from User to Backend

1. **User Request**: User sends HTTP request to frontend via browser
2. **Frontend Processing**: Next.js handles static assets and client-side routing
3. **API Call**: Frontend makes API call to backend service
4. **Backend Processing**: FastAPI receives request, performs authentication/validation
5. **Database Interaction**: Backend queries Neon PostgreSQL database
6. **Response Generation**: Backend constructs response and returns to frontend
7. **Client Response**: Frontend receives data and updates UI

### MCP Server Communication Flow

1. **AI Request**: Backend receives request requiring AI processing
2. **MCP Request**: Backend makes internal service call to MCP server
3. **Tool Execution**: MCP server executes external tools/services
4. **Response Processing**: MCP server formats response for AI model
5. **AI Response**: Backend receives processed response from MCP server
6. **Client Delivery**: Backend delivers AI-generated content to frontend

### External Service Interactions

**Neon PostgreSQL Database:**
- Connection: TLS-encrypted PostgreSQL protocol
- Authentication: Username/password from Kubernetes secret
- SSL Mode: Require for security

**OpenRouter API:**
- Authentication: API key from Kubernetes secret
- Protocol: HTTPS REST API
- Rate Limiting: Handled by OpenRouter

**ChatKit Service:**
- Authentication: Domain key from configuration
- Protocol: HTTPS API calls
- Purpose: Frontend chat functionality

### Error Handling Flows

**Service Unavailability:**
1. Health check detects unhealthy pod
2. Kubernetes removes pod from service endpoints
3. Traffic routed to healthy replicas
4. Kubernetes attempts to restart unhealthy pod

**Database Connection Failure:**
1. Backend detects database connection failure
2. Circuit breaker activates to prevent cascade failure
3. Graceful degradation or error response to client
4. Automatic retry with exponential backoff

**MCP Server Communication Failure:**
1. Backend detects MCP server unavailability
2. Graceful degradation of AI features
3. Error logging and alerting
4. Automatic retry with circuit breaker pattern

## Security Architecture

### Container Security

**Non-Root Execution:**
- All containers run as non-root user (UID 1000)
- File system group set to 2000 for consistency
- Limited permissions within container

**Minimal Base Images:**
- Using Alpine Linux for smaller attack surface
- Only essential packages installed
- Regular base image updates

**Image Scanning:**
- Automated vulnerability scanning during CI/CD
- Critical vulnerabilities block deployment
- Regular re-scanning of base images

**Multi-Stage Builds:**
- Build dependencies separated from runtime
- Production image contains only necessary files
- Reduced attack surface

### Kubernetes Security

**RBAC Configuration:**
- Principle of least privilege
- Role-based access controls for all resources
- Service accounts with minimal required permissions

**Network Policies:**
- Restrict traffic between namespaces
- Allow only necessary inter-service communication
- Block unauthorized external access

**Pod Security Standards:**
- Enforce security contexts
- Prevent privileged containers
- Limit capabilities and access

**TLS Encryption:**
- All internal communication encrypted
- External traffic uses HTTPS
- Certificate management for ingress

### Secret Management

**Kubernetes Secrets:**
- Store sensitive data separately from configuration
- Encrypted at rest in etcd
- Access controlled via RBAC

**Secret Injection:**
- Secrets mounted as volumes or environment variables
- No hardcoded credentials in images or code
- Rotation procedures documented

**Database Security:**
- SSL connections required
- Connection pooling for efficiency
- Audit logging for security monitoring

## Scalability Architecture

### Horizontal Pod Autoscaling

**CPU-Based Scaling:**
- Target CPU utilization: 70%
- Minimum: 1 replica
- Maximum: 5 replicas
- Scaling based on average CPU across all pods

**Memory-Based Scaling:**
- Target memory utilization: 80%
- Triggered when memory pressure detected
- Scaled separately from CPU-based scaling

**Custom Metrics Scaling:**
- Queue depth for backend processing
- Request rate for frontend
- Custom business metrics as needed

### Resource Constraints

**Request vs Limits:**
- Requests represent guaranteed resources
- Limits prevent resource exhaustion
- Ratio of 1:2 for CPU (request:limit)
- Ratio of 1:2 for memory (request:limit)

**Quality of Service Classes:**
- Guaranteed: Limits equal to requests
- Burstable: Limits higher than requests
- BestEffort: No requests or limits specified

### Multi-Pod Considerations

**Stateless Design:**
- All applications designed as stateless services
- External database for persistent state
- Session management via external services

**Load Balancing:**
- Built-in Kubernetes service load balancing
- Round-robin distribution of requests
- Health-check based traffic routing

**Data Consistency:**
- Database handles consistency requirements
- Eventual consistency where appropriate
- Distributed locking for critical operations