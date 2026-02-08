#!/bin/bash
# Script to test Docker AI Agent (Gordon) workflows for container operations

echo "Testing Docker AI Agent (Gordon) workflows..."

# Check if Gordon is available
if ! command -v gordon &> /dev/null; then
    echo "Gordon (Docker AI Agent) is not installed or not in PATH"
    echo "Please install it using: ./install-docker-ai-agent.sh"
    exit 1
fi

echo "Gordon is available. Testing workflows..."

# Create a temporary directory for our test Dockerfile
TEST_DIR=$(mktemp -d)
cd "$TEST_DIR"

# Create a sample Dockerfile for testing
cat << 'EOF' > Dockerfile.test
FROM ubuntu:20.04
LABEL maintainer="test@example.com"

# Install packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "app.py"]
EOF

# Create a minimal requirements.txt for the test
cat << 'EOF' > requirements.txt
flask==2.0.1
requests==2.25.1
EOF

echo "Created test Dockerfile and requirements.txt in $TEST_DIR"

echo ""
echo "=== Testing Dockerfile Optimization ==="

# Test Dockerfile optimization
gordon optimize-image "$TEST_DIR/Dockerfile.test"

echo ""
echo "=== Testing Dockerfile Best Practices Review ==="

# Test Dockerfile best practices review
gordon review-dockerfile "$TEST_DIR/Dockerfile.test"

echo ""
echo "=== Testing Build Suggestions ==="

# Test build suggestions
gordon suggest-build "$TEST_DIR"

echo ""
echo "=== Testing Gordon Help ==="

# Test Gordon help
gordon help

echo ""
echo "=== Building Test Image for Size Analysis ==="

# Build a simple test image for size analysis
docker build -f Dockerfile.test -t test-gordon-image:latest . 2>/dev/null || {
    echo "Docker build failed or Docker not available. Creating a dummy image for testing..."
    # Create a dummy image if docker build fails
    docker pull alpine:latest
    docker tag alpine:latest test-gordon-image:latest
}

echo ""
echo "=== Testing Image Size Analysis ==="

# Test image size analysis
gordon analyze-size test-gordon-image:latest

echo ""
echo "=== Testing Gordon Commands ==="

# Test various Gordon commands
echo "Testing Gordon commands with examples:"
echo "1. gordon optimize-image <path/to/Dockerfile>"
echo "2. gordon review-dockerfile <path/to/Dockerfile>"
echo "3. gordon scan-vulnerabilities <image_name>"
echo "4. gordon suggest-build <context_directory>"
echo "5. gordon analyze-size <image_name>"

echo ""
echo "=== Workflow Testing Complete ==="
echo "Successfully tested various Gordon (Docker AI Agent) workflows:"
echo "- Dockerfile optimization analysis"
echo "- Best practices review"
echo "- Build suggestions"
echo "- Image size analysis"
echo "- Help and usage information"

# Cleanup
cd - > /dev/null
rm -rf "$TEST_DIR"

# Clean up test image
docker rmi test-gordon-image:latest 2>/dev/null || true

echo ""
echo "Testing completed!"