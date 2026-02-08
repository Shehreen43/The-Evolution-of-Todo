# Monitoring Setup for Todo AI Chatbot

This directory contains configuration files for monitoring and observability of the Todo AI Chatbot application.

## Components

### 1. Prometheus
Prometheus is used for metric collection from various services in the application stack.

#### Configuration
- `prometheus.yml`: Main Prometheus configuration file that defines scraping targets
- Scrapes metrics from:
  - Todo backend service
  - Dapr sidecars
  - Kafka (via JMX exporter)

### 2. Grafana
Grafana is used for visualization and dashboard creation.

#### Configuration
- Provisioning files for automatic dashboard setup
- Pre-built dashboards for:
  - Application performance
  - Dapr runtime metrics
  - Kafka performance
  - System resources

### 3. Dapr Observability
Dapr provides built-in observability features including:
- Distributed tracing
- Metrics collection
- Health checks

## Setup Instructions

### Local Development
1. Start services with docker-compose:
   ```bash
   docker-compose up -d prometheus grafana
   ```

2. Access Prometheus at `http://localhost:9090`
3. Access Grafana at `http://localhost:3001` (admin/admin)

### Production
The monitoring stack is deployed as part of the Helm chart when `monitoring.enabled` is set to `true`.

## Key Metrics

### Application Metrics
- Request rate and latency
- Error rates
- Active users
- Task creation/completion rates

### Dapr Metrics
- Sidecar health
- Component health (state store, pub/sub)
- Service invocation metrics
- Actor metrics (if used)

### Kafka Metrics
- Topic partition lag
- Broker health
- Throughput metrics
- Consumer group status

## Alerts

The monitoring system includes pre-configured alerts for:
- High error rates
- Increased latency
- Service unavailability
- Resource exhaustion
- Dapr component failures

## Dashboards

Pre-built dashboards include:
1. **Application Performance**: Shows key application metrics
2. **Dapr Runtime**: Visualizes Dapr component health and performance
3. **Event Processing**: Tracks Kafka streams and event processing
4. **System Resources**: Monitors infrastructure resources