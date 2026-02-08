# kubectl-ai Guide

## Overview
kubectl-ai is a Kubernetes plugin that enables AI-assisted operations using natural language queries. It translates human-readable commands into kubectl commands.

## Installation
The installation script `install-kubectl-ai.sh` will automatically detect your OS and architecture and install the appropriate binary.

## Configuration
kubectl-ai uses OpenAI-compatible API endpoints. You can configure it with:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_ENDPOINT="https://api.openai.com/v1/chat/completions"
```

For Claude integration, you might need to use an OpenRouter endpoint or similar service.

## Usage Examples
- `kubectl ai get pods` - Get all pods in the current namespace
- `kubectl ai describe pod with high memory usage` - Describe pods with high memory usage
- `kubectl ai create deployment nginx --image=nginx` - Create an nginx deployment
- `kubectl ai explain service` - Explain Kubernetes service objects

## Best Practices
- Always verify AI-generated commands before executing them in production
- Use in development and testing environments first
- Review the translated kubectl commands to understand what will be executed

## Security Considerations
- API keys should be stored securely
- Be cautious about sending sensitive cluster information to AI services
- Consider using on-premise AI solutions for sensitive environments