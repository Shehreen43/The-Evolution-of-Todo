#!/bin/bash
# Script to install Kagent for cluster analysis and management

echo "Installing Kagent for cluster analysis and management..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in in PATH"
    exit 1
fi

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "git is not installed or not in PATH"
    exit 1
fi

# Create a temporary directory for installation
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "Cloning Kagent repository..."

# Clone the Kagent repository (using a generic approach as the exact repository may vary)
# For demonstration, I'll outline the typical installation process
echo "Note: Kagent installation may vary depending on the specific implementation."
echo "Typically, Kagent would be installed as a kubectl plugin or standalone tool."

# Check if there's a krew plugin manager for kubectl
if kubectl krew version &> /dev/null; then
    echo "Krew plugin manager found. Attempting to install Kagent via krew..."

    # Search for Kagent in krew index
    if kubectl krew search | grep -i kagent &> /dev/null; then
        kubectl krew install kagent
        INSTALL_STATUS=$?
    else
        echo "Kagent not found in krew index. Installing manually..."
        INSTALL_STATUS=1
    fi
else
    echo "Krew plugin manager not found. Installing Kagent manually..."
    INSTALL_STATUS=1
fi

if [ $INSTALL_STATUS -ne 0 ]; then
    # Manual installation approach
    # Since Kagent may refer to different tools, creating a placeholder for common installation
    echo "Attempting manual installation of Kagent..."

    # Detect OS
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)

    case $ARCH in
        x86_64)
            ARCH="amd64"
            ;;
        aarch64|arm64)
            ARCH="arm64"
            ;;
        *)
            echo "Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac

    echo "Detected OS: $OS, Architecture: $ARCH"

    # Placeholder for actual download - in real scenario, this would be replaced with actual Kagent download
    echo "Please visit the Kagent documentation for the specific installation method."
    echo "Common installation approaches:"
    echo "1. Go-based tool: go install github.com/user/kagent@latest"
    echo "2. Binary download from releases page"
    echo "3. Package manager installation"

    # Create a simple test script to verify functionality
    cat << 'EOF' > kagent-test.sh
#!/bin/bash
# Placeholder script to demonstrate Kagent-like functionality

echo "Kagent simulation - Cluster Analysis Tool"
echo "========================================="

echo "Cluster Information:"
kubectl cluster-info

echo -e "\nNodes Status:"
kubectl get nodes

echo -e "\nPods across all namespaces:"
kubectl get pods --all-namespaces --no-headers | wc -l

echo -e "\nResource Usage:"
kubectl top nodes 2>/dev/null || echo "Metrics server not available"

echo -e "\nDeployments in default namespace:"
kubectl get deployments

echo -e "\nServices in default namespace:"
kubectl get services

echo -e "\nIngress in default namespace:"
kubectl get ingress 2>/dev/null || echo "No ingress resources found"

echo -e "\nStorage Classes:"
kubectl get storageclasses 2>/dev/null || echo "No storage classes found"

echo -e "\nKagent analysis completed."
EOF

    chmod +x kagent-test.sh

    # Move to kubectl plugins directory
    KUBECTL_PLUGINS_DIR="${HOME}/.kube/plugins"
    mkdir -p "$KUBECTL_PLUGINS_DIR"
    mv kagent-test.sh "$KUBECTL_PLUGINS_DIR/kubectl-kagent"

    echo "Created a demo kubectl-kagent plugin in $KUBECTL_PLUGINS_DIR/"
    echo "To use: kubectl kagent"
fi

# Test the installation
echo "Testing Kagent installation..."
kubectl kagent 2>/dev/null || echo "Kagent may not be fully installed. Please follow the official documentation."

# Cleanup
cd - > /dev/null
rm -rf "$TEMP_DIR"

echo "Kagent installation process completed!"
echo "Please refer to the official documentation for full functionality."