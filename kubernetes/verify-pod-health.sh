#!/bin/bash
# Script to verify pod health and resource allocation for Todo Chatbot deployment

echo "Verifying pod health for Todo Chatbot application..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

# Get all pods with the todo-chatbot label
echo "Checking pods status..."
kubectl get pods -l app.kubernetes.io/name=todo-chatbot

echo ""
echo "Checking pod details..."
kubectl get pods -l app.kubernetes.io/name=todo-chatbot -o wide

echo ""
echo "Checking pod readiness..."
kubectl wait --for=condition=Ready pods -l app.kubernetes.io/name=todo-chatbot --timeout=30s

if [ $? -eq 0 ]; then
    echo "All pods are in Running and Ready state."
else
    echo "Some pods are not ready. Checking status..."
    kubectl get pods -l app.kubernetes.io/name=todo-chatbot
fi

echo ""
echo "Checking resource allocation..."
kubectl top pods -l app.kubernetes.io/name=todo-chatbot 2>/dev/null || echo "Metrics server may not be available, skipping resource allocation check"

echo ""
echo "Checking pod logs for errors..."
for pod in $(kubectl get pods -l app.kubernetes.io/name=todo-chatbot -o jsonpath='{.items[*].metadata.name}'); do
    echo "=== Logs for $pod ==="
    kubectl logs "$pod" --tail=20
    echo ""
done

echo ""
echo "Checking health checks in pod descriptions..."
kubectl describe pods -l app.kubernetes.io/name=todo-chatbot | grep -A 10 -B 5 "Health"

echo ""
echo "Verifying containers are running as non-root users..."
kubectl describe pods -l app.kubernetes.io/name=todo-chatbot | grep -i "RunAsUser\|RunAsGroup"

echo ""
echo "Pod health verification completed."