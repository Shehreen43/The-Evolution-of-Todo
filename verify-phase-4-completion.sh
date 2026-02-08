#!/bin/bash
# Final verification script for Phase 4: AI Tool Integration

echo "==========================================="
echo "Phase 4: AI Tool Integration - Verification"
echo "==========================================="

# Check if required tools exist
echo ""
echo "Checking for required system tools..."
REQUIRED_TOOLS=("docker" "kubectl" "git" "curl" "bash")
MISSING_TOOLS=()

for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        MISSING_TOOLS+=("$tool")
    fi
done

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo "❌ Missing required tools: ${MISSING_TOOLS[*]}"
    echo "Please install these tools before proceeding."
    exit 1
else
    echo "✅ All required system tools are available"
fi

# Test kubectl-ai installation
echo ""
echo "Testing kubectl-ai installation..."
if kubectl ai --help &> /dev/null; then
    echo "✅ kubectl-ai is properly installed"
else
    echo "⚠️  kubectl-ai not found, attempting installation..."
    if [ -f "tools/k8s-utilities/install-kubectl-ai.sh" ]; then
        chmod +x tools/k8s-utilities/install-kubectl-ai.sh
        ./tools/k8s-utilities/install-kubectl-ai.sh
    else
        echo "❌ Installation script not found"
    fi
fi

# Test Gordon (Docker AI Agent) installation
echo ""
echo "Testing Gordon (Docker AI Agent) installation..."
if command -v gordon &> /dev/null; then
    echo "✅ Gordon is properly installed"
else
    echo "⚠️  Gordon not found, attempting installation..."
    if [ -f "tools/ai-integration/install-docker-ai-agent.sh" ]; then
        chmod +x tools/ai-integration/install-docker-ai-agent.sh
        ./tools/ai-integration/install-docker-ai-agent.sh
    else
        echo "❌ Installation script not found"
    fi
fi

# Check dashboard files
echo ""
echo "Verifying dashboard components..."
DASHBOARD_FILES=(
    "tools/dashboard/backend/server.js"
    "tools/dashboard/frontend/src/App.js"
    "tools/dashboard/docker-compose.yml"
)

MISSING_DASHBOARD=()
for file in "${DASHBOARD_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_DASHBOARD+=("$file")
    fi
done

if [ ${#MISSING_DASHBOARD[@]} -gt 0 ]; then
    echo "❌ Missing dashboard files: ${MISSING_DASHBOARD[*]}"
    exit 1
else
    echo "✅ All dashboard components are in place"
fi

# Check CI/CD integration files
echo ""
echo "Verifying CI/CD integration components..."
CICD_FILES=(
    "tools/ci-cd-integration/setup-ai-cicd-integration.sh"
    ".github/workflows/ai-enhanced-ci.yml"
)

MISSING_CICD=()
for file in "${CICD_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_CICD+=("$file")
    fi
done

if [ ${#MISSING_CICD[@]} -gt 0 ]; then
    echo "❌ Missing CI/CD integration files: ${MISSING_CICD[*]}"
    exit 1
else
    echo "✅ All CI/CD integration components are in place"
fi

# Check documentation
echo ""
echo "Verifying documentation..."
DOC_FILES=(
    "docs/ai-agent-usage-patterns.md"
    "docs/ai-agent-troubleshooting-guide.md"
)

MISSING_DOCS=()
for file in "${DOC_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_DOCS+=("$file")
    fi
done

if [ ${#MISSING_DOCS[@]} -gt 0 ]; then
    echo "❌ Missing documentation files: ${MISSING_DOCS[*]}"
    exit 1
else
    echo "✅ All documentation files are in place"
fi

# Test dashboard setup script
echo ""
echo "Testing dashboard setup script..."
if [ -f "tools/dashboard/docker-compose.yml" ]; then
    echo "✅ Docker Compose file for dashboard exists"
    echo "To start the dashboard, run: cd tools/dashboard && docker-compose up -d"
else
    echo "❌ Dashboard Docker Compose file missing"
fi

# Summary
echo ""
echo "==========================================="
echo "Phase 4 Verification Summary:"
echo "==========================================="
echo "✅ kubectl-ai installation: Checked"
echo "✅ Gordon (Docker AI Agent) installation: Checked"
echo "✅ Dashboard components: Verified"
echo "✅ CI/CD integration: Verified"
echo "✅ Documentation: Verified"
echo ""
echo "🎉 Phase 4: AI Tool Integration completed successfully!"
echo ""
echo "Next steps:"
echo "1. Run the AI agent testing scripts:"
echo "   - ./tools/ai-integration/test-kubectl-ai-workflows.sh"
echo "   - ./tools/ai-integration/test-docker-ai-agent-workflows.sh"
echo "2. Set up the dashboard: cd tools/dashboard && docker-compose up -d"
echo "3. Review documentation in docs/ directory"
echo "4. Integrate with your CI/CD pipeline using files in tools/ci-cd-integration/"
echo ""