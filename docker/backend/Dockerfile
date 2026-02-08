# Multi-stage Dockerfile for FastAPI Backend Application
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

# Copy requirements
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

# Create non-root user (Debian syntax)
RUN groupadd -g 1001 python && \
    useradd -u 1001 -g python -m python

# Copy Python dependencies
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY backend/app ./app
COPY backend/requirements.txt .
COPY backend/alembic.ini .
COPY backend/test_mcp_start.py .
COPY backend/verify_chat_backend.py .
COPY backend/test_streaming_issue.py .
# Environment variables should be passed via docker-compose or kubernetes secrets


USER python

EXPOSE 8000

# Safer healthcheck (works even without custom endpoint)
HEALTHCHECK CMD curl -f http://localhost:8000 || exit 1

# Start FastAPI
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
