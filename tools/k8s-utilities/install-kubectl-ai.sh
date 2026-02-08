#!/bin/bash
# Script to install kubectl-ai plugin for AI-assisted Kubernetes operations

echo "Installing kubectl-ai plugin..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

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

# Download the appropriate kubectl-ai binary
echo "Detected OS: $OS, Architecture: $ARCH"

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "Downloading kubectl-ai for ${OS}/${ARCH}..."

# Get the latest release information
if command -v curl &> /dev/null; then
    RELEASE_INFO=$(curl -s https://api.github.com/repos/itaysk/kubectl-ai/releases/latest)
    DOWNLOAD_URL=$(echo "$RELEASE_INFO" | grep "browser_download_url.*${OS}_${ARCH}" | cut -d '"' -f 4)
elif command -v wget &> /dev/null; then
    RELEASE_INFO=$(wget -qO- https://api.github.com/repos/itaysk/kubectl-ai/releases/latest)
    DOWNLOAD_URL=$(echo "$RELEASE_INFO" | grep "browser_download_url.*${OS}_${ARCH}" | cut -d '"' -f 4)
else
    echo "Neither curl nor wget is available. Please install one of them."
    exit 1
fi

if [ -z "$DOWNLOAD_URL" ]; then
    echo "Could not find download URL for ${OS}/${ARCH}"
    exit 1
fi

echo "Download URL: $DOWNLOAD_URL"

# Download the binary
if command -v curl &> /dev/null; then
    curl -L -o kubectl-ai "$DOWNLOAD_URL"
elif command -v wget &> /dev/null; then
    wget -O kubectl-ai "$DOWNLOAD_URL"
fi

# Make it executable
chmod +x kubectl-ai

# Find kubectl plugins directory
KUBECTL_PLUGINS_DIR="${HOME}/.kube/plugins"

# Create plugins directory if it doesn't exist
mkdir -p "$KUBECTL_PLUGINS_DIR"

# Move the binary to the plugins directory
mv kubectl-ai "$KUBECTL_PLUGINS_DIR/"

# Test the installation
echo "Testing kubectl-ai installation..."
kubectl ai --help

if [ $? -eq 0 ]; then
    echo "kubectl-ai installed successfully in $KUBECTL_PLUGINS_DIR"
    echo "You can now use kubectl ai for AI-assisted Kubernetes operations"
    echo "Example: kubectl ai get pods, kubectl ai describe deployment my-deployment"
else
    echo "Installation may have failed. Please check manually."
    exit 1
fi

# Cleanup
cd - > /dev/null
rm -rf "$TEMP_DIR"

echo "kubectl-ai installation completed!"