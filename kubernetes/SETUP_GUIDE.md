# Kubernetes Setup Guide for Phase IV

## Prerequisites

Before deploying the Todo Chatbot application to Kubernetes, you need to set up your local Kubernetes cluster using Docker Desktop with Kubernetes enabled.

## Setting Up Docker Desktop with Kubernetes

### Step 1: Install Docker Desktop
1. Download and install Docker Desktop from https://www.docker.com/products/docker-desktop
2. Make sure you have sufficient resources allocated:
   - At least 4 CPUs
   - At least 8GB RAM
   - At least 20GB disk space

### Step 2: Enable Kubernetes
1. Open Docker Desktop
2. Go to Settings > Kubernetes
3. Check "Enable Kubernetes"
4. Click "Apply & Restart"
5. Wait for Kubernetes to start (this may take a few minutes)

### Step 3: Verify Kubernetes Setup
Once Docker Desktop has restarted with Kubernetes enabled, verify that it's working:

```bash
kubectl cluster-info
kubectl get nodes
```

### Step 4: Enable Required Addons
Some Kubernetes features may need to be enabled:

```bash
# For Windows/Linux, ingress is typically available by default
# For ingress controller, you might need to enable it through Docker Desktop settings
```

## Alternative: Minikube Setup (if Docker Desktop is not available)
If Docker Desktop is not available, you can use Minikube instead:

```bash
# Install minikube
minikube start --driver=docker --memory=8192 --cpus=4

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server
```

## Verify Setup
Once Kubernetes is running, verify your setup:

```bash
kubectl cluster-info
kubectl get nodes
kubectl get pods --all-namespaces
```

You should see that the cluster is running and nodes are ready before proceeding with the deployment.

## Configuration
Make sure your kubectl context is pointing to the local cluster:

```bash
kubectl config get-contexts
kubectl config current-context
```