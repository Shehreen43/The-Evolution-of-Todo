# AI Agent Troubleshooting Guide

## Overview
This guide provides troubleshooting steps for common issues with AI agents including kubectl-ai, Docker AI Agent (Gordon), and CI/CD AI assistants.

## Common Issues and Solutions

### 1. Connection and Authentication Issues

#### Issue: AI agent cannot connect to API
**Symptoms**:
- Error messages about connection timeouts
- Authentication failures
- API key errors

**Solutions**:
1. Verify API key is set correctly:
   ```bash
   echo $OPENAI_API_KEY
   ```
2. Check network connectivity:
   ```bash
   curl -X POST https://api.openai.com/v1/chat/completions \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}]}'
   ```
3. Verify API endpoint is accessible:
   ```bash
   curl -I https://api.openai.com/v1/chat/completions
   ```

#### Issue: Permission denied errors
**Symptoms**:
- Access denied messages
- Unauthorized responses
- Insufficient permissions

**Solutions**:
1. Check API key permissions in the provider's dashboard
2. Verify the account has sufficient quota/credits
3. For Kubernetes, ensure proper RBAC permissions:
   ```bash
   kubectl auth can-i '*' '*'
   ```

### 2. Installation Issues

#### Issue: kubectl-ai installation fails
**Symptoms**:
- Plugin installation errors
- Binary not found
- Permission errors

**Solutions**:
1. Ensure kubectl is in PATH:
   ```bash
   kubectl version
   ```
2. Check kubectl plugins directory:
   ```bash
   ls ~/.kube/plugins/
   ```
3. Manual installation:
   ```bash
   # Download binary directly
   OS=$(uname -s | tr '[:upper:]' '[:lower:]')
   ARCH=$(uname -m | sed 's/x86_64/amd64/' | sed 's/aarch64/arm64/')
   curl -L -o kubectl-ai "https://github.com/itaysk/kubectl-ai/releases/latest/download/kubectl-ai_${OS}_${ARCH}"
   chmod +x kubectl-ai
   mv kubectl-ai ~/.kube/plugins/
   ```

#### Issue: Gordon (Docker AI Agent) not found
**Symptoms**:
- Command not found
- Script execution errors
- Permission denied

**Solutions**:
1. Verify installation:
   ```bash
   which gordon
   ```
2. Check if in PATH:
   ```bash
   echo $PATH
   ```
3. Reinstall:
   ```bash
   ./tools/ai-integration/install-docker-ai-agent.sh
   ```

### 3. Performance Issues

#### Issue: Slow response times
**Symptoms**:
- Long delays in AI responses
- Timeout errors
- High latency

**Solutions**:
1. Check internet connection quality
2. Verify API provider status
3. Adjust timeout settings:
   ```bash
   export KUBECTL_AI_TIMEOUT=30s  # if supported
   ```
4. Use a different API endpoint if available
5. Check if rate limits are being hit

#### Issue: High error rates
**Symptoms**:
- Frequent failures
- Invalid responses
- Parsing errors

**Solutions**:
1. Increase retry attempts in configuration
2. Check prompt complexity - simplify if needed
3. Verify API key has sufficient quota
4. Use a more capable model if available

### 4. Kubernetes-Specific Issues

#### Issue: kubectl-ai gives incorrect commands
**Symptoms**:
- Commands that don't work as expected
- Invalid kubectl syntax
- Wrong resource names

**Solutions**:
1. Verify the request is specific enough:
   ```bash
   # Instead of: kubectl ai "fix my pods"
   # Use: kubectl ai "get pods in namespace production that are in Error state"
   ```
2. Check cluster context:
   ```bash
   kubectl config current-context
   kubectl config get-contexts
   ```
3. Ensure proper permissions for requested operations

#### Issue: kubectl-ai suggests unsupported operations
**Symptoms**:
- Commands that don't exist
- Unsupported flags or options
- Deprecated functionality

**Solutions**:
1. Update kubectl and kubectl-ai to latest versions
2. Verify Kubernetes version compatibility
3. Report issues to the kubectl-ai project

### 5. Docker-Specific Issues

#### Issue: Gordon gives bad Dockerfile advice
**Symptoms**:
- Dockerfile suggestions that don't work
- Security recommendations that break functionality
- Optimization suggestions that cause issues

**Solutions**:
1. Verify the Dockerfile format and syntax
2. Check if the suggestions are appropriate for your specific use case
3. Test changes in a non-production environment first
4. Report issues to the Gordon project if applicable

#### Issue: Gordon cannot scan images
**Symptoms**:
- Image scanning fails
- Vulnerability scanning errors
- Missing security tools

**Solutions**:
1. Install required security tools:
   ```bash
   # Install Trivy for vulnerability scanning
   brew install aquasecurity/trivy/trivy  # macOS
   # or
   sudo apt-get install trivy  # Ubuntu
   ```
2. Ensure Docker daemon is running
3. Verify image exists locally:
   ```bash
   docker images | grep your-image-name
   ```

### 6. CI/CD Integration Issues

#### Issue: AI agents not available in CI/CD pipeline
**Symptoms**:
- Commands not found in pipeline
- Installation failures in pipeline
- Permission errors in CI/CD

**Solutions**:
1. Install AI agents in pipeline setup:
   ```yaml
   - name: Install kubectl-ai
     run: |
       # Install script here
   ```
2. Ensure proper environment variables are set
3. Check if the runner has required tools (kubectl, docker, etc.)

#### Issue: Different behavior in CI vs local
**Symptoms**:
- Works locally but fails in CI
- Different outputs between environments
- Environment-specific errors

**Solutions**:
1. Match environment versions between local and CI
2. Use the same base images in CI
3. Ensure consistent configuration files
4. Log more detailed output for debugging

## Diagnostic Commands

### Check kubectl-ai status:
```bash
kubectl ai --help
kubectl ai "show me cluster info" --dry-run
```

### Check Gordon status:
```bash
gordon help
gordon analyze-size alpine:latest
```

### Check API connectivity:
```bash
curl -s https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.data[0].id'
```

### Check system resources:
```bash
# Memory and CPU
top
# Disk space
df -h
# Network
ping google.com
```

## Logging and Monitoring

### Enable verbose logging:
```bash
# For kubectl-ai (if supported)
kubectl ai --v=5 "your command"

# For Docker operations
export DEBUG=gordon:*
```

### Check logs:
```bash
# Kubernetes events
kubectl get events --all-namespaces

# Docker logs
docker logs container_name
```

## Prevention Strategies

1. **Regular Updates**: Keep AI agents updated to the latest versions
2. **Environment Consistency**: Maintain similar environments across dev/staging/prod
3. **Monitoring**: Set up alerts for AI agent failures
4. **Fallback Procedures**: Have manual processes when AI agents fail
5. **Testing**: Test AI agent outputs before applying to production
6. **Documentation**: Keep troubleshooting steps updated

## When to Escalate

Escalate issues to:
- Development team if AI agent is causing incorrect operations
- Infrastructure team if connectivity/performance issues persist
- Security team if AI agent raises security concerns
- Vendor/provider if API-related issues occur

## Useful Resources

- kubectl-ai GitHub: https://github.com/itaysk/kubectl-ai
- Docker documentation: https://docs.docker.com
- Kubernetes documentation: https://kubernetes.io/docs/
- AI provider documentation (OpenAI, Anthropic, etc.)

## Contact Support

If issues persist:
1. Collect relevant logs and error messages
2. Document the exact steps to reproduce
3. Check if others have reported similar issues
4. Report to the appropriate project or vendor