#!/bin/bash
# Script to deploy the Todo Chatbot application to Kubernetes using Helm

echo "Starting deployment of Todo Chatbot application..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo "helm is not installed or not in PATH"
    exit 1
fi

# Verify kubectl can connect to cluster
echo "Checking kubectl connection to cluster..."
kubectl cluster-info &> /dev/null
if [ $? -ne 0 ]; then
    echo "Cannot connect to Kubernetes cluster. Please ensure Docker Desktop with Kubernetes is running."
    exit 1
fi

echo "Kubernetes cluster connection verified."

# Check if the release already exists
if helm status todo-chatbot-release &> /dev/null; then
    echo "Todo Chatbot release already exists. Upgrading..."
    helm upgrade todo-chatbot-release ./helm/todo-chatbot/ -f ./helm/todo-chatbot/values-dev.yaml
else
    echo "Installing Todo Chatbot Helm chart..."
    helm install todo-chatbot-release ./helm/todo-chatbot/ -f ./helm/todo-chatbot/values-dev.yaml
fi

if [ $? -eq 0 ]; then
    echo "Helm chart installed/updated successfully!"

    # Wait for pods to be ready
    echo "Waiting for pods to be ready..."
    kubectl wait --for=condition=Ready pods -l app.kubernetes.io/name=todo-chatbot --timeout=300s

    # Show deployment status
    echo "Deployment status:"
    kubectl get pods -l app.kubernetes.io/name=todo-chatbot
    kubectl get services -l app.kubernetes.io/name=todo-chatbot

    # Show ingress if it exists
    kubectl get ingress

    echo "Deployment completed successfully!"
    echo "Access the application at: http://localhost (if ingress is configured)"
    echo "Or use port forwarding to access services directly"
else
    echo "Helm chart installation failed!"
    exit 1
fi