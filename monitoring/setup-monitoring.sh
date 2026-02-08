#!/bin/bash
# Script to set up basic monitoring for the Todo Chatbot application

echo "Setting up monitoring for Todo Chatbot application..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    echo "helm is not installed or not in PATH"
    exit 1
fi

# Create monitoring namespace
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# Add prometheus-community repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack (includes Prometheus, Grafana, Alertmanager)
echo "Installing kube-prometheus-stack..."

# Create values file for monitoring
cat << EOF > /tmp/monitoring-values.yaml
prometheus:
  enabled: true
  service:
    type: NodePort
  prometheusSpec:
    serviceMonitorSelectorNilUsesHelmValues: false
    podMonitorSelectorNilUsesHelmValues: false
grafana:
  enabled: true
  service:
    type: NodePort
  adminPassword: prom-operator
  persistence:
    enabled: false
  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
      - name: 'default'
        orgId: 1
        folder: '/'
        type: file
        disableDeletion: false
        editable: true
        options:
          path: /var/lib/grafana/dashboards/default
  dashboards:
    default:
      todo-app-dashboard:
        gnetId: 1860
        revision: 1
        datasource: Prometheus
alertmanager:
  enabled: true
  service:
    type: NodePort
EOF

# Install the monitoring stack
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values /tmp/monitoring-values.yaml \
  --create-namespace

if [ $? -eq 0 ]; then
    echo "kube-prometheus-stack installed successfully!"

    echo "Waiting for pods to be ready..."
    kubectl wait --for=condition=Ready pods -n monitoring -l app.kubernetes.io/instance=kube-prometheus-stack --timeout=300s

    echo "Monitoring services:"
    kubectl get svc -n monitoring

    echo ""
    echo "To access Grafana: kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3000:80"
    echo "Grafana credentials: admin/prom-operator"
    echo ""
    echo "To access Prometheus: kubectl port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090"
    echo ""
    echo "To access Alertmanager: kubectl port-forward -n monitoring svc/kube-prometheus-stack-alertmanager 9093:9093"
else
    echo "Failed to install kube-prometheus-stack"
    exit 1
fi

# Clean up temporary file
rm /tmp/monitoring-values.yaml

echo "Monitoring setup completed!"