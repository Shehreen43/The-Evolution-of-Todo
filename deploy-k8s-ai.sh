#!/bin/bash
# AI-Assisted Kubernetes Deployment Script for Todo Chatbot
# Uses kubectl-ai and kagent for intelligent deployment operations

set -e  # Exit on any error

echo "🚀 Starting AI-Assisted Deployment of Todo Chatbot to Kubernetes..."

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed or not in PATH"
    exit 1
fi

# Check if kubectl-ai is available
if command -v kubectl-ai &> /dev/null; then
    echo "🤖 kubectl-ai is available - will use AI-assisted kubectl commands"
    KUBECTL_CMD="kubectl-ai"
else
    echo "⚠️  kubectl-ai not found - using standard kubectl"
    KUBECTL_CMD="kubectl"
fi

# Check if kagent is available
if command -v kagent &> /dev/null; then
    echo "🤖 kagent is available - will use AI-assisted operations"
    KAGENT_AVAILABLE=true
else
    echo "⚠️  kagent not found - using standard operations"
    KAGENT_AVAILABLE=false
fi

# Verify kubectl can connect to cluster
echo "📡 Verifying cluster connection..."
$KUBECTL_CMD cluster-info &> /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Cannot connect to Kubernetes cluster"
    echo "💡 Make sure Minikube is running: minikube start"
    exit 1
fi

echo "✅ Cluster connection verified"

# Check if ingress-nginx is enabled (needed for the application)
echo "🔍 Checking ingress controller..."
if ! $KUBECTL_CMD get pods -n ingress-nginx &> /dev/null; then
    echo "📦 Installing ingress-nginx controller..."
    if [ "$KAGENT_AVAILABLE" = true ]; then
        kagent "install ingress-nginx controller for kubernetes"
    else
        $KUBECTL_CMD create namespace ingress-nginx
        helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
        helm repo update
        helm install ingress-nginx ingress-nginx/ing-ress-nginx -n ingress-nginx --set controller.service.type=NodePort
    fi
else
    echo "✅ Ingress controller is available"
fi

# Build and push Docker images if not already done
echo "🐳 Checking Docker images..."
if [ "$KAGENT_AVAILABLE" = true ]; then
    kagent "check if docker images exist: todo-frontend, todo-backend, todo-mcp-server"
fi

# Check if images exist locally
if ! docker images | grep -q "todo-frontend"; then
    echo "🏗️  Building frontend Docker image..."
    cd ../frontend
    docker build -t todo-frontend:latest .
    cd ../backend
fi

if ! docker images | grep -q "todo-backend"; then
    echo "🏗️  Building backend Docker image..."
    docker build -t todo-backend:latest .
fi

if ! docker images | grep -q "todo-mcp-server"; then
    echo "🏗️  Building MCP server Docker image..."
    docker build -t todo-mcp-server:latest -f Dockerfile.mcp .
fi

# For Minikube, load images into the cluster
if command -v minikube &> /dev/null; then
    echo "🔄 Loading images into Minikube..."
    minikube image load todo-frontend:latest
    minikube image load todo-backend:latest
    minikube image load todo-mcp-server:latest
fi

# Create namespace if it doesn't exist
NAMESPACE="todo-chatbot"
echo "🌐 Creating namespace: $NAMESPACE..."
if ! $KUBECTL_CMD get namespace $NAMESPACE &> /dev/null; then
    $KUBECTL_CMD create namespace $NAMESPACE
    echo "✅ Namespace $NAMESPACE created"
else
    echo "✅ Namespace $NAMESPACE already exists"
fi

# Check if the release already exists
RELEASE_NAME="todo-chatbot-release"
echo "🔍 Checking for existing release: $RELEASE_NAME..."
if helm status $RELEASE_NAME &> /dev/null; then
    ACTION="upgrade"
    echo "🔄 Release exists, preparing for upgrade..."
else
    ACTION="install"
    echo "🆕 Release does not exist, preparing for fresh install..."
fi

# Get current context for AI deployment assistance
if [ "$KAGENT_AVAILABLE" = true ]; then
    echo "🤖 Analyzing cluster state with kagent..."
    kagent "analyze the current kubernetes cluster state and provide recommendations for the todo chatbot deployment"
fi

# Deploy using Helm
echo "🚢 Deploying application with Helm..."
if [ "$ACTION" = "install" ]; then
    echo "📦 Installing Helm chart..."
    if [ "$KAGENT_AVAILABLE" = true ]; then
        kagent "install the todo chatbot helm chart with development values"
    fi
    helm install $RELEASE_NAME ./helm/todo-chatbot/ -f ./helm/todo-chatbot/values-dev.yaml --namespace $NAMESPACE
else
    echo "🔄 Upgrading Helm chart..."
    if [ "$KAGENT_AVAILABLE" = true ]; then
        kagent "upgrade the todo chatbot helm chart with development values"
    fi
    helm upgrade $RELEASE_NAME ./helm/todo-chatbot/ -f ./helm/todo-chatbot/values-dev.yaml --namespace $NAMESPACE
fi

if [ $? -eq 0 ]; then
    echo "✅ Helm chart $ACTION completed successfully!"

    # Wait for pods to be ready
    echo "⏳ Waiting for pods to be ready..."
    if [ "$KAGENT_AVAILABLE" = true ]; then
        kagent "wait for all pods in the todo-chatbot namespace to be ready"
    fi
    $KUBECTL_CMD wait --for=condition=Ready pods -l app.kubernetes.io/name=todo-chatbot --timeout=300s -n $NAMESPACE

    # Show deployment status
    echo "📊 Deployment status:"
    $KUBECTL_CMD get pods -n $NAMESPACE
    $KUBECTL_CMD get services -n $NAMESPACE
    $KUBECTL_CMD get ingress -n $NAMESPACE

    # Get the application URL
    if $KUBECTL_CMD get ingress -n $NAMESPACE &> /dev/null; then
        echo "🌐 Ingress is available"
        if command -v minikube &> /dev/null; then
            MINIKUBE_IP=$(minikube ip)
            echo "🔗 Access the application at: http://$MINIKUBE_IP (or http://localhost if using tunnel)"
        fi
    else
        echo "💡 To access the application, use port forwarding:"
        echo "   kubectl port-forward -n $NAMESPACE svc/$(helm list -n $NAMESPACE -o json | jq -r '.[0].name')-frontend 3000:3000"
    fi

    # Perform health checks
    echo "🧪 Performing health checks..."
    if [ "$KAGENT_AVAILABLE" = true ]; then
        kagent "perform health checks on the deployed todo chatbot application"
    fi

    # Wait a bit for services to be fully ready
    sleep 10

    # Check pod status
    $KUBECTL_CMD get pods -n $NAMESPACE

    # Check service endpoints
    $KUBECTL_CMD get endpoints -n $NAMESPACE

    echo "🎉 Deployment completed successfully!"
    echo ""
    echo "📚 Next steps:"
    echo "   1. Configure AI API keys: kubectl create secret generic todo-chatbot-ai-secrets --from-literal=OPENROUTER_API_KEY=your-key -n $NAMESPACE"
    echo "   2. Access the application via the URL above or use port forwarding"
    echo "   3. Monitor the application: kubectl get pods,svc -n $NAMESPACE"
    echo "   4. Check logs: kubectl logs -l app.kubernetes.io/name=todo-chatbot -n $NAMESPACE"

    if [ "$KAGENT_AVAILABLE" = true ]; then
        echo "🤖 Use kagent to troubleshoot: kagent 'analyze any issues with the todo chatbot deployment'"
        echo "🤖 Use kubectl-ai for management: kubectl-ai 'describe the todo chatbot pods'"
    fi

else
    echo "❌ Helm chart $ACTION failed!"
    echo "🔍 Troubleshooting tips:"
    echo "   - Check if all required images exist: docker images | grep todo"
    echo "   - Verify cluster connection: kubectl cluster-info"
    echo "   - Check for resource constraints: kubectl describe nodes"
    if [ "$KAGENT_AVAILABLE" = true ]; then
        kagent "analyze why the todo chatbot deployment failed and provide troubleshooting steps"
    fi
    exit 1
fi