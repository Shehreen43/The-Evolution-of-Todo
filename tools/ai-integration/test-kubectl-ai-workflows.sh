#!/bin/bash
# Script to test kubectl-ai workflows for common Kubernetes operations

echo "Testing kubectl-ai workflows..."

# Check if kubectl-ai is available
if ! kubectl ai --help &> /dev/null; then
    echo "kubectl-ai is not installed or not accessible"
    echo "Please install it using: ./install-kubectl-ai.sh"
    exit 1
fi

echo "kubectl-ai is available. Testing workflows..."

# Create a test namespace for our experiments
TEST_NAMESPACE="ai-test-$(date +%s)"
echo "Creating test namespace: $TEST_NAMESPACE"
kubectl create namespace "$TEST_NAMESPACE"

# Function to cleanup test resources
cleanup() {
    echo "Cleaning up test resources..."
    kubectl delete namespace "$TEST_NAMESPACE" --ignore-not-found=true
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Change to test namespace
kubectl config set-context --current --namespace="$TEST_NAMESPACE"

echo ""
echo "=== Testing Pod Debugging Workflows ==="

# Test basic pod listing
echo "1. Testing: List all pods"
kubectl ai "get pods" || echo "Command failed, but this is expected if no pods exist"

# Create a test pod to work with
kubectl run test-pod --image=nginx --restart=Never
sleep 5

echo "2. Testing: Describe problematic pod"
kubectl ai "describe pod test-pod"

echo "3. Testing: Get pod logs"
kubectl ai "get logs for pod test-pod"

echo ""
echo "=== Testing Deployment Operations ==="

# Create a test deployment
kubectl create deployment test-deployment --image=nginx
sleep 10

echo "4. Testing: Scale deployment"
kubectl ai "scale deployment test-deployment --replicas=3"

echo "5. Testing: Check deployment status"
kubectl ai "check deployment test-deployment status"

echo ""
echo "=== Testing Network Troubleshooting ==="

echo "6. Testing: Get services"
kubectl ai "show me all services"

echo "7. Testing: Get ingress"
kubectl ai "list ingress resources"

echo ""
echo "=== Testing Resource Optimization ==="

echo "8. Testing: Show resource usage"
kubectl ai "show me resource usage by pods"

echo "9. Testing: Get nodes with resource info"
kubectl ai "show nodes with CPU and memory capacity"

echo ""
echo "=== Testing Troubleshooting Queries ==="

echo "10. Testing: Check for failed pods"
kubectl ai "find pods that are not running"

echo "11. Testing: Get events"
kubectl ai "show recent events in namespace $TEST_NAMESPACE"

# Scale down deployment
kubectl scale deployment test-deployment --replicas=1

echo ""
echo "=== Workflow Testing Complete ==="
echo "Successfully tested various kubectl-ai workflows:"
echo "- Pod debugging and inspection"
echo "- Deployment scaling and management"
echo "- Network resource queries"
echo "- Resource optimization queries"
echo "- Troubleshooting and event queries"

echo ""
echo "Example commands that work well with kubectl-ai:"
echo "- kubectl ai 'show me pods with high memory usage'"
echo "- kubectl ai 'restart deployment my-app'"
echo "- kubectl ai 'find pods that have crashed'"
echo "- kubectl ai 'explain the error in pod my-pod'"
echo "- kubectl ai 'show me resource quotas in namespace default'"

echo ""
echo "Testing completed in namespace: $TEST_NAMESPACE"