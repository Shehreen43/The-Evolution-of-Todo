# Quick Start Guide - Todo AI Chatbot Docker Setup

## Prerequisites
- Docker Desktop installed and running
- At least 8GB RAM available
- Internet connection

## Step 1: Build Docker Images
```bash
# Make the build script executable
chmod +x build-all-images.sh

# Build all Docker images
./build-all-images.sh
```

## Step 2: Run the Application
```bash
# Make the run script executable
chmod +x run-containers.sh

# Start all services
./run-containers.sh
```

## Step 3: Access the Applications
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9000

## Useful Commands
```bash
# View all services
docker-compose ps

# View logs
docker-compose logs

# View specific service logs
docker-compose logs backend

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart backend
```

## Troubleshooting
If services don't start properly:
1. Check if Docker is running
2. Verify you have enough system resources
3. Look at the logs: `docker-compose logs`
4. Check if ports 3000, 8000, 3001, 9090 are available

## Clean Up
```bash
# Stop and remove all containers
docker-compose down

# Remove all images (optional)
docker-compose down --rmi all
```