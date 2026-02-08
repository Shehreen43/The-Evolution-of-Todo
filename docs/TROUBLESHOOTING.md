# Troubleshooting Guide

## Common Issues

### Container Build Issues
- **Issue**: Docker build fails due to missing dependencies
- **Solution**: Verify Dockerfile dependencies and ensure base images exist

- **Issue**: Permission denied errors in containers
- **Solution**: Check non-root user configuration in Dockerfiles

### Kubernetes Deployment Issues
- **Issue**: Pods stuck in Pending state
- **Solution**: Check resource limits and node availability
- **Commands**:
  ```bash
  kubectl describe pod <pod-name>
  kubectl get nodes
  ```

- **Issue**: Services not accessible
- **Solution**: Verify service configuration and ingress rules
- **Commands**:
  ```bash
  kubectl get services
  kubectl get ingress
  ```

### Application Issues
- **Issue**: Frontend cannot connect to backend
- **Solution**: Check service discovery and network policies
- **Commands**:
  ```bash
  kubectl logs <frontend-pod>
  kubectl logs <backend-pod>
  ```

## Debugging Commands
```bash
# Check all resources
kubectl get all

# Get detailed pod information
kubectl describe pod <pod-name>

# Check logs for all containers
kubectl logs -l app=todo-frontend
kubectl logs -l app=todo-backend

# Port forward to test services locally
kubectl port-forward svc/todo-frontend 3000:3000
kubectl port-forward svc/todo-backend 8000:8000
```

## Monitoring
- Check resource usage: `kubectl top nodes` and `kubectl top pods`
- Monitor events: `kubectl get events --sort-by=.metadata.creationTimestamp`
- Check health endpoints: Each service has a `/health` endpoint