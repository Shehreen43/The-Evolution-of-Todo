# Todo Chatbot Helm Chart

A Helm chart for deploying the Todo Chatbot application to Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installing the Chart

To install the chart with the release name `todo-chatbot`:

```bash
helm install todo-chatbot ./todo-chatbot/ -f values-dev.yaml
```

## Uninstalling the Chart

To uninstall/delete the `todo-chatbot` release:

```bash
helm delete todo-chatbot
```

## Configuration

The following table lists the configurable parameters of the todo-chatbot chart and their default values.

### Global parameters

| Parameter | Description | Default |
|-----|-----|-----|
| `global.imagePullPolicy` | Image pull policy | `"IfNotPresent"` |
| `global.imageTag` | Overrides the image tag whose default is the chart appVersion | `""` |

### Frontend parameters

| Parameter | Description | Default |
|-----|-----|-----|
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `frontend.image.repository` | Frontend image repository | `"todo-frontend"` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `"IfNotPresent"` |
| `frontend.image.tag` | Frontend image tag | `""` |
| `frontend.service.type` | Frontend service type | `"ClusterIP"` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.resources.limits.cpu` | Frontend CPU limit | `"500m"` |
| `frontend.resources.limits.memory` | Frontend memory limit | `"512Mi"` |
| `frontend.resources.requests.cpu` | Frontend CPU request | `"250m"` |
| `frontend.resources.requests.memory` | Frontend memory request | `"256Mi"` |

### Backend parameters

| Parameter | Description | Default |
|-----|-----|-----|
| `backend.replicaCount` | Number of backend replicas | `1` |
| `backend.image.repository` | Backend image repository | `"todo-backend"` |
| `backend.image.pullPolicy` | Backend image pull policy | `"IfNotPresent"` |
| `backend.image.tag` | Backend image tag | `""` |
| `backend.service.type` | Backend service type | `"ClusterIP"` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.resources.limits.cpu` | Backend CPU limit | `"500m"` |
| `backend.resources.limits.memory` | Backend memory limit | `"512Mi"` |
| `backend.resources.requests.cpu` | Backend CPU request | `"250m"` |
| `backend.resources.requests.memory` | Backend memory request | `"256Mi"` |

### MCP Server parameters

| Parameter | Description | Default |
|-----|-----|-----|
| `mcpServer.replicaCount` | Number of MCP server replicas | `1` |
| `mcpServer.image.repository` | MCP server image repository | `"todo-mcp-server"` |
| `mcpServer.image.pullPolicy` | MCP server image pull policy | `"IfNotPresent"` |
| `mcpServer.image.tag` | MCP server image tag | `""` |
| `mcpServer.service.type` | MCP server service type | `"ClusterIP"` |
| `mcpServer.service.port` | MCP server service port | `8080` |
| `mcpServer.metricsPort` | MCP server metrics port | `8001` |
| `mcpServer.resources.limits.cpu` | MCP server CPU limit | `"500m"` |
| `mcpServer.resources.limits.memory` | MCP server memory limit | `"512Mi"` |
| `mcpServer.resources.requests.cpu` | MCP server CPU request | `"250m"` |
| `mcpServer.resources.requests.memory` | MCP server memory request | `"256Mi"` |

### Database parameters

| Parameter | Description | Default |
|-----|-----|-----|
| `database.postgresql.enabled` | Enable PostgreSQL | `true` |
| `database.postgresql.auth.postgresPassword` | PostgreSQL admin password | `"secure-postgres-password"` |
| `database.postgresql.auth.username` | PostgreSQL user | `"todo_user"` |
| `database.postgresql.auth.password` | PostgreSQL user password | `"secure-user-password"` |
| `database.postgresql.auth.database` | PostgreSQL database | `"todo_database"` |

## Values Files

- `values.yaml` - Default values
- `values-dev.yaml` - Development environment values
- `values-test.yaml` - Test environment values
- `values-prod.yaml` - Production environment values