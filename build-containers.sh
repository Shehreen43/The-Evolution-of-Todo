#!/bin/bash
# Script to build Docker containers for Phase IV

echo "Building frontend container..."
docker build -t todo-frontend:latest -f docker/frontend/Dockerfile .

echo "Building backend container..."
docker build -t todo-backend:latest -f docker/backend/Dockerfile .

echo "Building MCP server container..."
docker build -t todo-mcp-server:latest -f docker/mcp/Dockerfile .

echo "All containers built successfully!"
echo "Images created:"
echo "- todo-frontend:latest"
echo "- todo-backend:latest"
echo "- todo-mcp-server:latest"

echo "To deploy with Helm:"
echo "helm install todo-chatbot-release helm/todo-chatbot/ -f helm/todo-chatbot/values-dev.yaml"
