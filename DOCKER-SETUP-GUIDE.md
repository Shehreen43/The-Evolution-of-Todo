# Docker Setup Guide for Todo AI Chatbot Project

## Overview
This guide provides step-by-step instructions to build Docker images and run containers for the entire Todo AI Chatbot project with all its components (frontend, backend, MCP server, database, Kafka, Dapr, etc.).

## Prerequisites
- Docker installed (version 20.10 or higher)
- Docker Compose installed
- At least 8GB RAM available
- Internet connection for pulling base images

## Project Structure
```
The-Evolution-of-Todo/
├── backend/                    # FastAPI backend
├── frontend/                   # Next.js frontend
├── docker/
│   ├── frontend/
│   │   └── Dockerfile        # Frontend Dockerfile
│   ├── backend/
│   │   └── Dockerfile        # Backend Dockerfile
│   ├── mcp/
│   │   └── Dockerfile        # MCP Server Dockerfile
│   └── docker-compose.yml    # Main orchestration
├── docker-compose.yml        # Production-ready compose file
└── ...
```

## Part 1: Building Individual Docker Images

### 1. Build Frontend Image
```bash
# Navigate to project root
cd /path/to/The-Evolution-of-Todo

# Build frontend image
docker build -f docker/frontend/Dockerfile . -t todo-frontend:latest

# Verify the image was built
docker images | grep todo-frontend
```

### 2. Build Backend Image
```bash
# Build backend image
docker build -f docker/backend/Dockerfile . -t todo-backend:latest

# Verify the image was built
docker images | grep todo-backend
```

### 3. Build MCP Server Image
```bash
# Build MCP server image
docker build -f docker/mcp/Dockerfile . -t todo-mcp-server:latest

# Verify the image was built
docker images | grep todo-mcp-server
```

## Part 2: Running Individual Containers (Optional)

### 1. Run PostgreSQL Container (Required for Backend)
```bash
# Run PostgreSQL database
docker run -d \
  --name todo-postgres \
  -e POSTGRES_DB=todo_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15-alpine

# Verify PostgreSQL is running
docker ps | grep postgres
```

### 2. Run Backend Container
```bash
# Run backend container (after PostgreSQL is running)
docker run -d \
  --name todo-backend \
  --link todo-postgres \
  -e DATABASE_URL=postgresql://postgres:password@todo-postgres:5432/todo_db \
  -e BETTER_AUTH_SECRET=your-super-secret-key-here \
  -p 8000:8000 \
  todo-backend:latest
```

### 3. Run Frontend Container
```bash
# Run frontend container (after backend is running)
docker run -d \
  --name todo-frontend \
  --link todo-backend \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  -p 3000:3000 \
  todo-frontend:latest
```

## Part 3: Running Complete Application with Docker Compose (Recommended)

### 1. Quick Start with Docker Compose
```bash
# Navigate to project root
cd /path/to/The-Evolution-of-Todo

# Start all services using docker-compose
docker-compose up -d

# Check the status of all containers
docker-compose ps
```

### 2. Understanding the Services
The docker-compose.yml file starts these services:

| Service | Port | Description |
|---------|------|-------------|
| `postgres` | 5432 | PostgreSQL database for the application |
| `zookeeper` | 2181 | Kafka dependency |
| `kafka` | 9092 | Apache Kafka for event streaming |
| `dapr-placement` | 50005 | Dapr placement service |
| `backend` | 8000 | FastAPI backend with MCP integration |
| `frontend` | 3000 | Next.js frontend application |
| `prometheus` | 9090 | Monitoring and metrics |
| `grafana` | 3001 | Visualization dashboard |

### 3. Checking Service Status
```bash
# View all running containers
docker-compose ps

# View logs for a specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# View logs in real-time
docker-compose logs -f backend
```

## Part 4: Environment Variables Setup

### 1. Create Environment File
Create a `.env` file in the project root:
```bash
# In the project root directory
cat > .env << EOF
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENAI_DOMAIN_KEY=your-openai-domain-key-here
DATABASE_URL=postgresql://postgres:password@postgres:5432/todo_db
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
EOF
```

### 2. Using the Environment File
```bash
# Start services with environment file
docker-compose --env-file .env up -d
```

## Part 5: Testing the Application

### 1. Verify All Services Are Running
```bash
# Check all containers are healthy
docker-compose ps

# Expected result: All services should show "Up" status
```

### 2. Test Application Endpoints
```bash
# Test backend health
curl http://localhost:8000/health

# Test frontend (should return HTML)
curl http://localhost:3000 | head -10

# Test database connection (inside backend container)
docker-compose exec backend curl -f http://localhost:8000/health
```

### 3. Access the Applications
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

## Part 6: Managing the Containers

### 1. Stopping the Application
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This will delete database data!)
docker-compose down -v
```

### 2. Restarting the Application
```bash
# Restart all services
docker-compose up -d

# Restart specific service
docker-compose restart backend
```

### 3. Updating Images and Restarting
```bash
# Rebuild images
docker-compose build

# Pull latest images (if using external images)
docker-compose pull

# Restart with new images
docker-compose up -d --force-recreate
```

### 4. Viewing Logs
```bash
# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f frontend

# View logs for last N lines
docker-compose logs --tail 50 backend
```

## Part 7: Troubleshooting

### 1. Common Issues and Solutions

#### Issue: Port Already in Use
```bash
# Check what's using the port
netstat -tulpn | grep :3000
# or
lsof -i :3000

# Kill the process using the port
kill -9 $(lsof -t -i:3000)
```

#### Issue: Database Connection Failed
```bash
# Check if PostgreSQL is running
docker-compose ps | grep postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Test database connection from backend
docker-compose exec backend ping postgres
```

#### Issue: Frontend Cannot Connect to Backend
```bash
# Check if backend is running
docker-compose ps | grep backend

# Test connection from frontend to backend
docker-compose exec frontend curl -v http://backend:8000/health
```

### 2. Debugging Commands
```bash
# Enter backend container
docker-compose exec backend sh

# Enter frontend container
docker-compose exec frontend sh

# Check container environment variables
docker-compose exec backend env

# Check network connectivity between containers
docker-compose exec backend nslookup postgres
docker-compose exec frontend nslookup backend
```

## Part 8: Production Considerations

### 1. Resource Limits
The Docker Compose file includes basic resource limits. For production:

```yaml
# In docker-compose.yml
services:
  backend:
    # ... other config
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 512M
```

### 2. Security Considerations
- Never commit actual API keys to version control
- Use secrets management for production
- Ensure all containers run as non-root users (already configured)
- Regularly update base images

### 3. Backup Strategy
```bash
# Backup database
docker-compose exec postgres pg_dump -U postgres todo_db > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U postgres -d todo_db
```

## Part 9: Development Workflow

### 1. Development with Hot Reload
For development, you can mount source code as volumes:

```bash
# Start with development configuration
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### 2. Building Specific Images
```bash
# Build only frontend
docker-compose build frontend

# Build only backend
docker-compose build backend

# Build all images
docker-compose build
```

## Part 10: Cleaning Up

### 1. Remove All Containers
```bash
# Stop and remove all containers
docker-compose down

# Remove all images related to the project
docker-compose down --rmi all

# Remove all volumes
docker-compose down -v
```

### 2. Clean Docker System
```bash
# Remove unused containers, networks, images
docker system prune -a

# Remove only unused volumes
docker volume prune

# Check disk usage
docker system df
```

## Quick Start Command Summary
```bash
# 1. Navigate to project root
cd /path/to/The-Evolution-of-Todo

# 2. Create .env file with your API keys
# (see Part 4 for .env file format)

# 3. Start all services
docker-compose up -d

# 4. Check status
docker-compose ps

# 5. Access applications
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
# Grafana: http://localhost:3001 (admin/admin)

# 6. Stop all services
docker-compose down
```

## Next Steps
Once you have successfully built and run the Docker containers, you can proceed to:
1. Test the application functionality
2. Verify MCP server integration
3. Test AI chatbot features
4. Monitor application with Grafana/Prometheus
5. Prepare for Kubernetes deployment (Phase 4)