#!/bin/bash
# Script to build all Docker images for the Todo AI Chatbot project

echo "==========================================="
echo "Building Docker Images for Todo AI Chatbot"
echo "==========================================="

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "Current directory: $PWD"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    echo "Please install Docker Desktop or Docker Engine first"
    exit 1
fi

# Check Docker Compose availability
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  Docker Compose is not available, but this is OK for individual builds"
fi

echo "✅ Docker is available"
echo ""

# Build frontend image
echo "📦 Building Frontend Image..."
docker build -f docker/frontend/Dockerfile . -t todo-frontend:latest
if [ $? -eq 0 ]; then
    echo "✅ Frontend image built successfully"
else
    echo "❌ Frontend image build failed"
    exit 1
fi
echo ""

# Build backend image
echo "📦 Building Backend Image..."
docker build -f docker/backend/Dockerfile . -t todo-backend:latest
if [ $? -eq 0 ]; then
    echo "✅ Backend image built successfully"
else
    echo "❌ Backend image build failed"
    exit 1
fi
echo ""

# Build MCP server image
echo "📦 Building MCP Server Image..."
docker build -f docker/mcp/Dockerfile . -t todo-mcp-server:latest
if [ $? -eq 0 ]; then
    echo "✅ MCP Server image built successfully"
else
    echo "❌ MCP Server image build failed"
    exit 1
fi
echo ""

# Show built images
echo "🖼️  Built Images:"
docker images | grep -E "(todo-frontend|todo-backend|todo-mcp-server)"
echo ""

# Suggest next steps
echo "==========================================="
echo "✅ All Docker images built successfully!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Run the application with Docker Compose:"
echo "   docker-compose up -d"
echo ""
echo "2. Check running containers:"
echo "   docker-compose ps"
echo ""
echo "3. View logs:"
echo "   docker-compose logs backend"
echo "   docker-compose logs frontend"
echo ""
echo "4. Access the applications:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000/docs"
echo "   - Health check: http://localhost:8000/health"
echo ""
echo "5. Stop the application:"
echo "   docker-compose down"
echo ""