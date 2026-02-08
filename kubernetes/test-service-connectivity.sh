#!/bin/bash
# Script to test service connectivity between components of Todo Chatbot application

echo "Testing service connectivity for Todo Chatbot application..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

RELEASE_NAME=${1:-todo-chatbot-release}

echo "Using release name: $RELEASE_NAME"

# Get the fullname of the services (based on Helm template)
FULLNAME=$(kubectl get deployments -l app.kubernetes.io/name=todo-chatbot -o jsonpath='{.items[0].metadata.labels.app\.kubernetes\.io\/instance}-{.items[0].metadata.labels.app\.kubernetes\.io\/name}' 2>/dev/null | head -1)

if [ -z "$FULLNAME" ]; then
    echo "Could not determine the Helm release fullname. Using default pattern..."
    FULLNAME="${RELEASE_NAME}-todo-chatbot"
fi

echo "Using service pattern: $FULLNAME"

# Test internal service connectivity
echo ""
echo "=== Testing Service Discovery ==="
kubectl get services -l app.kubernetes.io/name=todo-chatbot

# Check if services exist
FRONTEND_SVC="${FULLNAME}-frontend"
BACKEND_SVC="${FULLNAME}-backend"
MCP_SERVER_SVC="${FULLNAME}-mcp-server"

echo ""
echo "Checking frontend service: $FRONTEND_SVC"
kubectl get service "$FRONTEND_SVC" 2>/dev/null || echo "Frontend service not found with name $FRONTEND_SVC"

echo ""
echo "Checking backend service: $BACKEND_SVC"
kubectl get service "$BACKEND_SVC" 2>/dev/null || echo "Backend service not found with name $BACKEND_SVC"

echo ""
echo "Checking MCP server service: $MCP_SERVER_SVC"
kubectl get service "$MCP_SERVER_SVC" 2>/dev/null || echo "MCP server service not found with name $MCP_SERVER_SVC"

# Test service accessibility
echo ""
echo "=== Testing Service Accessibility ==="
if kubectl get service "$BACKEND_SVC" &>/dev/null; then
    echo "Backend service $BACKEND_SVC exists and is accessible"
    kubectl describe service "$BACKEND_SVC"
else
    echo "Backend service not found, checking for any backend service..."
    kubectl get services -l app=backend
fi

if kubectl get service "$FRONTEND_SVC" &>/dev/null; then
    echo "Frontend service $FRONTEND_SVC exists and is accessible"
    kubectl describe service "$FRONTEND_SVC"
else
    echo "Frontend service not found, checking for any frontend service..."
    kubectl get services -l app=frontend
fi

if kubectl get service "$MCP_SERVER_SVC" &>/dev/null; then
    echo "MCP server service $MCP_SERVER_SVC exists and is accessible"
    kubectl describe service "$MCP_SERVER_SVC"
else
    echo "MCP server service not found, checking for any mcp-server service..."
    kubectl get services -l app=mcp-server
fi

# Check pods to see environment variables and connectivity
echo ""
echo "=== Checking Pod Environment Variables ==="
FRONTEND_POD=$(kubectl get pods -l app=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ ! -z "$FRONTEND_POD" ]; then
    echo "Checking frontend pod environment for API URL: $FRONTEND_POD"
    kubectl exec "$FRONTEND_POD" -- env | grep -i api_url
fi

BACKEND_POD=$(kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ ! -z "$BACKEND_POD" ]; then
    echo "Checking backend pod environment for database connection: $BACKEND_POD"
    kubectl exec "$BACKEND_POD" -- env | grep -i database
fi

MCP_POD=$(kubectl get pods -l app=mcp-server -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ ! -z "$MCP_POD" ]; then
    echo "Checking MCP server pod: $MCP_POD"
    kubectl describe pod "$MCP_POD"
fi

# Test external ingress access if available
echo ""
echo "=== Testing External Access ==="
kubectl get ingress

echo ""
echo "Service connectivity testing completed."