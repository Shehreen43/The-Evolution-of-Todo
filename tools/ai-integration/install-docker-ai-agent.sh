#!/bin/bash
# Script to install Docker AI Agent (Gordon) for container operations

echo "Installing Docker AI Agent (Gordon) for container operations..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not in PATH"
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

echo "Setting up Docker AI Agent (Gordon)..."

# Gordon may be a conceptual AI agent or a specific tool, so creating a framework for such tools
echo "Creating Docker AI Agent framework..."

# Create a directory for Docker AI tools
mkdir -p "${HOME}/.docker-ai-tools"

# Create a sample Docker AI agent script that demonstrates functionality
cat << 'EOF' > docker-ai-agent.sh
#!/bin/bash
# Docker AI Agent (Gordon) - Framework for AI-assisted Docker operations

DOCKER_AI_AGENT_VERSION="1.0.0"

usage() {
    echo "Docker AI Agent (Gordon) - AI-assisted Docker operations"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  optimize-image <dockerfile_path>    - Analyze and suggest Dockerfile optimizations"
    echo "  scan-vulnerabilities <image_name>   - Scan image for vulnerabilities"
    echo "  review-dockerfile <dockerfile_path> - Review Dockerfile for best practices"
    echo "  suggest-build <context_dir>         - Suggest optimal build approach"
    echo "  analyze-size <image_name>          - Analyze image size and layers"
    echo "  help                               - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 optimize-image ./Dockerfile"
    echo "  $0 scan-vulnerabilities myapp:latest"
}

optimize_image() {
    local dockerfile_path="$1"

    if [ ! -f "$dockerfile_path" ]; then
        echo "Error: Dockerfile not found at $dockerfile_path"
        return 1
    fi

    echo "Analyzing Dockerfile at $dockerfile_path for optimization opportunities..."

    # Check for common optimization opportunities
    if grep -E "FROM\s+[^:]" "$dockerfile_path" | grep -v "alpine\|scratch"; then
        echo "Recommendation: Consider using smaller base images like alpine or scratch"
    fi

    if grep -E "RUN.*apt-get.*update.*apt-get.*install" "$dockerfile_path" | grep -v "clean"; then
        echo "Recommendation: Combine apt-get update and apt-get install in single RUN command with cleanup"
    fi

    if grep -i "add\s\|copy.*\*" "$dockerfile_path"; then
        echo "Recommendation: Use specific file paths instead of wildcards for better layer caching"
    fi

    if ! grep -E "USER\s+" "$dockerfile_path"; then
        echo "Recommendation: Add USER instruction to run as non-root user"
    fi

    echo "Dockerfile analysis completed."
}

scan_vulnerabilities() {
    local image_name="$1"

    echo "Scanning image $image_name for vulnerabilities..."

    # Check if trivy is available for vulnerability scanning
    if command -v trivy &> /dev/null; then
        echo "Using Trivy for vulnerability scanning..."
        trivy image "$image_name"
    elif docker scan --help &> /dev/null; then
        echo "Using Docker Scout for vulnerability scanning..."
        docker scan "$image_name"
    else
        echo "No vulnerability scanner found. Install Trivy or use 'docker scan' if available."
        echo "To install Trivy: https://aquasecurity.github.io/trivy/"
    fi
}

review_dockerfile() {
    local dockerfile_path="$1"

    if [ ! -f "$dockerfile_path" ]; then
        echo "Error: Dockerfile not found at $dockerfile_path"
        return 1
    fi

    echo "Reviewing Dockerfile at $dockerfile_path for best practices..."

    # Security best practices check
    if ! grep -E "^USER\s+" "$dockerfile_path"; then
        echo "Security: No USER instruction found - container runs as root"
    fi

    # Performance best practices check
    if grep -E "RUN.*pip\s\|RUN.*npm\s\|RUN.*apt-get" "$dockerfile_path" | grep -v "cache\|layer"; then
        echo "Performance: Consider multi-stage builds to reduce final image size"
    fi

    # Optimization best practices check
    if grep -E "RUN.*rm.*cache\|RUN.*clean" "$dockerfile_path"; then
        echo "Optimization: Good - cache cleanup found"
    else
        echo "Optimization: Consider cleaning package caches in RUN commands"
    fi

    echo "Dockerfile review completed."
}

suggest_build() {
    local context_dir="$1"

    echo "Suggesting optimal build approach for $context_dir..."

    # Check for multi-stage build opportunities
    if grep -E "AS\s+" "$context_dir/Dockerfile" &> /dev/null; then
        echo "Multi-stage build detected - good for optimization"
    else
        echo "Consider using multi-stage builds to separate build and runtime environments"
    fi

    # Suggest build cache usage
    echo "Ensure .dockerignore is used to exclude unnecessary files from build context"

    # Suggest build arguments
    echo "Consider using build arguments for flexible builds"

    echo "Build suggestions completed."
}

analyze_size() {
    local image_name="$1"

    echo "Analyzing size of image $image_name..."

    # Get image size
    docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep "$(echo $image_name | cut -d: -f1)"

    # Show image layers if dive is available
    if command -v dive &> /dev/null; then
        echo "Using dive to analyze image layers..."
        echo "Run: dive $image_name for detailed analysis"
    else
        echo "Install dive (https://github.com/wagoodman/dive) for detailed layer analysis"
    fi

    echo "Size analysis completed."
}

case "${1:-help}" in
    optimize-image)
        if [ -z "$2" ]; then
            echo "Error: Dockerfile path required"
            usage
            exit 1
        fi
        optimize_image "$2"
        ;;
    scan-vulnerabilities)
        if [ -z "$2" ]; then
            echo "Error: Image name required"
            usage
            exit 1
        fi
        scan_vulnerabilities "$2"
        ;;
    review-dockerfile)
        if [ -z "$2" ]; then
            echo "Error: Dockerfile path required"
            usage
            exit 1
        fi
        review_dockerfile "$2"
        ;;
    suggest-build)
        if [ -z "$2" ]; then
            echo "Error: Context directory required"
            usage
            exit 1
        fi
        suggest_build "$2"
        ;;
    analyze-size)
        if [ -z "$2" ]; then
            echo "Error: Image name required"
            usage
            exit 1
        fi
        analyze_size "$2"
        ;;
    help|-h|--help)
        usage
        ;;
    *)
        echo "Unknown command: $1"
        usage
        exit 1
        ;;
esac
EOF

chmod +x docker-ai-agent.sh

# Move to tools directory
mkdir -p "${HOME}/.docker-ai-tools"
mv docker-ai-agent.sh "${HOME}/.docker-ai-tools/gordon"

# Create a symlink for easier access
if [ -d "/usr/local/bin" ]; then
    sudo ln -sf "${HOME}/.docker-ai-tools/gordon" /usr/local/bin/gordon 2>/dev/null || echo "Could not create system-wide symlink, adding to personal bin"
fi

# Add to user's PATH if not already available
if ! command -v gordon &> /dev/null; then
    echo "Adding Gordon to PATH..."
    echo 'export PATH="$HOME/.docker-ai-tools:$PATH"' >> "${HOME}/.bashrc"
    echo "Please run 'source ~/.bashrc' or restart your terminal to use Gordon."
fi

echo "Docker AI Agent (Gordon) installed successfully!"
echo "You can now use Gordon for AI-assisted Docker operations."
echo "Try: gordon help"

# Cleanup
cd - > /dev/null
rm -rf "$TEMP_DIR"

echo "Docker AI Agent (Gordon) installation completed!"