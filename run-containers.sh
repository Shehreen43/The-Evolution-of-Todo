#!/bin/bash
# Script to run the Todo AI Chatbot containers with Docker Compose

echo "==========================================="
echo "Running Todo AI Chatbot Containers"
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
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not available"
    echo "Please install Docker Compose or use Docker Desktop"
    exit 1
fi

# Check if images exist
echo "🔍 Checking for built images..."
IMAGES_EXIST=true
for img in todo-frontend:latest todo-backend:latest todo-mcp-server:latest; do
    if ! docker images | grep -q "$(echo $img | sed 's/:.*//')"; then
        echo "❌ Image $img does not exist"
        IMAGES_EXIST=false
    else
        echo "✅ Found image: $img"
    fi
done

if [ "$IMAGES_EXIST" = false ]; then
    echo ""
    echo "💡 Tip: Build the images first with:"
    echo "   ./build-all-images.sh"
    exit 1
fi

echo ""
echo "📊 Current Docker status:"
docker ps -q | wc -l | xargs -I {} sh -c 'if [ "{}" -eq 0 ]; then echo "No running containers"; else echo "{} containers currently running"; fi'
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file with default values..."
    cat > .env << EOF
# Todo AI Chatbot Environment Variables
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here
OPENAI_DOMAIN_KEY=your-openai-domain-key-here
DATABASE_URL=postgresql://postgres:password@postgres:5432/todo_db
BETTER_AUTH_SECRET=supersecretkeythatisatleast32characterslong
EOF
    echo "✅ Created .env file with default values (update with your actual keys!)"
    echo ""
fi

# Start the containers
echo "🚀 Starting all services..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services"
    exit 1
fi

echo "✅ Services started successfully!"
echo ""

# Wait a moment for services to start
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check the status of all containers
echo "📋 Service Status:"
echo "----------------"
docker-compose ps
echo ""

# Check if services are running properly
echo "🔍 Verifying service health..."
SERVICES_HEALTHY=true

# Check if backend is responding
echo "Checking backend health..."
if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend may still be starting up or has issues"
    SERVICES_HEALTHY=false
fi

# Check if frontend is responding
echo "Checking frontend availability..."
if curl -s -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "⚠️  Frontend may still be starting up or has issues"
    SERVICES_HEALTHY=false
fi

echo ""
if [ "$SERVICES_HEALTHY" = true ]; then
    echo "==========================================="
    echo "🎉 All services are running successfully!"
    echo "==========================================="
else
    echo "==========================================="
    echo "⚠️  Some services may still be starting up"
    echo "==========================================="
fi

echo ""
echo "🌐 Access the applications:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/docs"
echo "   Health check: http://localhost:8000/health"
echo "   Grafana: http://localhost:3001 (admin/admin)"
echo "   Prometheus: http://localhost:9090"
echo ""

echo "📋 Useful commands:"
echo "   View logs: docker-compose logs [service_name]"
echo "   View all logs: docker-compose logs"
echo "   Follow logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart service: docker-compose restart [service_name]"
echo ""

echo "💡 Note: The first startup may take 2-3 minutes as all services initialize."
echo "    If services don't become healthy, check logs with: docker-compose logs"