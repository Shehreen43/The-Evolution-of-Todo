# =========================
# Builder stage
# =========================
FROM node:20-slim AS builder

WORKDIR /app

# Improve npm network stability (CRITICAL for your error)
RUN npm config set fetch-retries 5 \
    && npm config set fetch-retry-mintimeout 20000 \
    && npm config set fetch-retry-maxtimeout 120000 \
    && npm config set registry https://registry.npmjs.org/

# Copy only dependency manifests first (cache-friendly)
COPY frontend/package.json frontend/package-lock.json ./

# Use npm install (more resilient than npm ci in Docker)
RUN npm install --legacy-peer-deps

# Copy rest of the frontend source
COPY frontend/ .

# Build Next.js app
RUN npm run build


# =========================
# Runner stage
# =========================
FROM node:20-slim AS runner

WORKDIR /app

# Create non-root user (security best practice)
RUN groupadd -g 1001 nextjs \
    && useradd -u 1001 -g nextjs -m nextjs

ENV NODE_ENV=production

# Copy only required runtime files
COPY --from=builder /app/package.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.* ./

USER nextjs

EXPOSE 3000

CMD ["npm", "start"]
