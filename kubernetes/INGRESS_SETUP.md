# NGINX Ingress Controller Setup

## For Docker Desktop with Kubernetes

Docker Desktop comes with the NGINX Ingress Controller pre-installed and enabled. You don't need to install it separately.

### Verify Ingress Controller

Check if the ingress controller is running:

```bash
kubectl get pods -n kube-system | grep ingress
```

You should see ingress controller pods running.

### Enable Ingress (if not already enabled)

If ingress is not enabled in Docker Desktop:

1. Open Docker Desktop
2. Go to Settings > Kubernetes
3. Ensure "Enable Kubernetes" is checked
4. The NGINX Ingress Controller should be available by default

### Test Ingress Functionality

Create a simple test ingress to verify functionality:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-ingress
  namespace: default
spec:
  rules:
  - host: hello-world.info
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hello-service
            port:
              number: 80
```

### Configure DNS for Local Development

For local development, add entries to your hosts file:

On Windows:
```
C:\Windows\System32\drivers\etc\hosts
```

Add:
```
127.0.0.1 localhost
127.0.0.1 hello-world.info
```

### Access Applications via Ingress

Once ingress is configured, your applications will be accessible via the configured hostnames on port 80/443.

### Troubleshooting

If ingress is not working:
1. Verify that Docker Desktop Kubernetes is running
2. Check ingress controller status: `kubectl get pods -n kube-system`
3. Check ingress resources: `kubectl get ingress`
4. Check ingress controller logs if needed