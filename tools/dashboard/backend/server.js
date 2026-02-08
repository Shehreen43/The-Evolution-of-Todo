// Dashboard API server
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(cors());
app.use(express.json());

// Mock data for AI agent metrics
let aiAgentMetrics = {
  timestamp: new Date().toISOString(),
  agents: [
    {
      id: 'kubectl-ai',
      name: 'Kubectl AI',
      status: 'active',
      requests: 142,
      successRate: 98.5,
      avgResponseTime: 1250,
      lastActivity: new Date(Date.now() - 30000).toISOString()
    },
    {
      id: 'docker-ai',
      name: 'Docker AI Agent (Gordon)',
      status: 'active',
      requests: 87,
      successRate: 96.2,
      avgResponseTime: 980,
      lastActivity: new Date(Date.now() - 15000).toISOString()
    },
    {
      id: 'ci-cd-ai',
      name: 'CI/CD AI Assistant',
      status: 'warning',
      requests: 56,
      successRate: 89.3,
      avgResponseTime: 2100,
      lastActivity: new Date(Date.now() - 60000).toISOString()
    }
  ],
  totalRequests: 285,
  overallSuccessRate: 94.7,
  systemHealth: 'operational'
};

// API Routes
app.get('/api/metrics', (req, res) => {
  aiAgentMetrics.timestamp = new Date().toISOString();
  res.json(aiAgentMetrics);
});

app.get('/api/agents', (req, res) => {
  res.json(aiAgentMetrics.agents);
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

app.get('/api/logs', (req, res) => {
  // Mock logs data
  const mockLogs = [
    { id: 1, timestamp: new Date(Date.now() - 300000).toISOString(), level: 'info', message: 'Kubectl AI agent started successfully', agent: 'kubectl-ai' },
    { id: 2, timestamp: new Date(Date.now() - 240000).toISOString(), level: 'info', message: 'Docker AI agent analyzed Dockerfile optimization', agent: 'docker-ai' },
    { id: 3, timestamp: new Date(Date.now() - 180000).toISOString(), level: 'warning', message: 'CI/CD AI assistant had slow response time', agent: 'ci-cd-ai' },
    { id: 4, timestamp: new Date(Date.now() - 120000).toISOString(), level: 'info', message: 'All agents operational', agent: 'system' },
    { id: 5, timestamp: new Date(Date.now() - 60000).toISOString(), level: 'info', message: 'Kubectl AI processed deployment query', agent: 'kubectl-ai' }
  ];
  res.json(mockLogs);
});

app.get('/api/config', (req, res) => {
  const config = {
    kubectlAiEnabled: true,
    dockerAiEnabled: true,
    cicdAiEnabled: true,
    aiProvider: 'openai',
    maxRetries: 3,
    timeoutMs: 10000
  };
  res.json(config);
});

app.put('/api/config', (req, res) => {
  // In a real implementation, this would update the configuration
  console.log('Configuration update requested:', req.body);
  res.status(200).json({ message: 'Configuration updated successfully' });
});

// Serve static files in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, 'client/build')));

  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`AI Agent Dashboard server running on port ${PORT}`);
});