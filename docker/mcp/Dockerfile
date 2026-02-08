# Dockerfile for MCP (Model Context Protocol) Server
# Uses Python 3.11 slim (Debian-based, production stable)

# =========================
# Builder stage
# =========================
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements (shared with backend)
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# =========================
# Runner stage
# =========================
FROM python:3.11-slim AS runner

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Create non-root user (UID 1000 as required)
RUN groupadd -g 1000 python && \
    useradd -u 1000 -g python -m python

# Copy Python dependencies
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy only MCP-related components
COPY backend/app/mcp ./app/mcp
COPY backend/app/database ./app/database
COPY backend/app/models ./app/models
COPY backend/app/config.py ./app/config.py
COPY backend/test_mcp_start.py ./run_mcp_server.py


USER python

EXPOSE 8080 8001

# Safer default healthcheck
HEALTHCHECK CMD curl -f http://localhost:8080 || exit 1

# Start MCP server
CMD ["python", "run_mcp_server.py", "--host", "0.0.0.0", "--port", "8080"]
