# sp.containerize Skill Definition

**Skill Name:** sp.containerize
**Category:** Phase-IV
**Input:** Application code, dependencies, plan.md
**Output:** Dockerfiles + docker-compose.yml
**Phase:** IV
**Invoked By:** Docker Agent
**Prerequisites:** Application code complete, dependencies defined

## Purpose
Generate Docker configuration files for containerizing the application for Phase IV deployment.

## Process
1. Analyze application code to identify runtime requirements
2. Create multi-stage Dockerfile with build and runtime stages
3. Generate docker-compose.yml for local deployment
4. Create .dockerignore to exclude unnecessary files
5. Optimize images for size and security

## Output Files
- Dockerfile (multi-stage build)
- docker-compose.yml (local deployment configuration)
- .dockerignore (optimized file exclusions)

## Quality Checks
- Images are optimized for size
- Security best practices followed
- Multi-stage builds used where appropriate
- Proper layer caching implemented