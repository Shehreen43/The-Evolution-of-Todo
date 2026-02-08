#!/bin/bash
# Script to validate MCP server connectivity and functionality

echo "Validating MCP Server connectivity and functionality..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

# Find the MCP server pod
MCP_POD=$(kubectl get pods -l app=mcp-server -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -z "$MCP_POD" ]; then
    echo "No MCP server pod found. Checking all pods..."
    kubectl get pods
    exit 1
fi

echo "Found MCP server pod: $MCP_POD"

# Check if MCP server pod is running and healthy
echo ""
echo "=== Checking MCP Server Pod Status ==="
kubectl get pod "$MCP_POD"

# Check if pod is ready
READY_STATUS=$(kubectl get pod "$MCP_POD" -o jsonpath='{.status.containerStatuses[0].ready}')
if [ "$READY_STATUS" = "true" ]; then
    echo "✓ MCP server pod is ready"
else
    echo "✗ MCP server pod is not ready"
    kubectl describe pod "$MCP_POD"
    exit 1
fi

# Check MCP server logs for any issues
echo ""
echo "=== Checking MCP Server Logs ==="
kubectl logs "$MCP_POD" --tail=50

# Check if there are any errors in the logs
ERROR_COUNT=$(kubectl logs "$MCP_POD" 2>&1 | grep -i -E "error|exception|failed|panic" | wc -l)
if [ $ERROR_COUNT -gt 0 ]; then
    echo "⚠ Found $ERROR_COUNT potential errors in MCP server logs"
    kubectl logs "$MCP_POD" | grep -i -E "error|exception|failed|panic"
else
    echo "✓ No obvious errors found in MCP server logs"
fi

# Check if MCP server is listening on expected ports
echo ""
echo "=== Checking MCP Server Ports ==="
kubectl describe pod "$MCP_POD" | grep -A 10 "Ports:"

# Test health endpoint if available
echo ""
echo "=== Testing MCP Server Health Endpoint ==="
# Try to access the health endpoint from within the cluster
kubectl exec "$MCP_POD" -- wget -qO- localhost:8080/health 2>/dev/null || echo "Health endpoint not accessible from inside pod"

# Check if backend can connect to MCP server
echo ""
echo "=== Testing Backend to MCP Server Connectivity ==="
BACKEND_POD=$(kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ ! -z "$BACKEND_POD" ]; then
    echo "Found backend pod: $BACKEND_POD"

    # Get the MCP server service name
    MCP_SVC=$(kubectl get service -l app=mcp-server -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    if [ ! -z "$MCP_SVC" ]; then
        echo "Testing connectivity from backend to MCP server ($MCP_SVC:8080)..."

        # Try to connect to MCP server from backend pod
        kubectl exec "$BACKEND_POD" -- wget -qO- "$MCP_SVC:8080/health" 2>/dev/null || echo "Could not connect to MCP server from backend pod"
    else
        echo "MCP server service not found"
    fi
else
    echo "Backend pod not found, skipping backend connectivity test"
fi

# Check MCP server resources
echo ""
echo "=== Checking MCP Server Resources ==="
kubectl top pod "$MCP_POD" 2>/dev/null || echo "Metrics server may not be available"

# Check MCP server configuration
echo ""
echo "=== Checking MCP Server Configuration ==="
kubectl describe pod "$MCP_POD"

echo ""
echo "MCP server validation completed."