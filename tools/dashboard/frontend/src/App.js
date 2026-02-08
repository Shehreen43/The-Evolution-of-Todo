// AI Agent Orchestration Dashboard
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState([]);
  const [config, setConfig] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [metricsRes, logsRes, configRes] = await Promise.all([
        fetch('http://localhost:5001/api/metrics'),
        fetch('http://localhost:5001/api/logs'),
        fetch('http://localhost:5001/api/config')
      ]);

      const [metricsData, logsData, configData] = await Promise.all([
        metricsRes.json(),
        logsRes.json(),
        configRes.json()
      ]);

      setMetrics(metricsData);
      setLogs(logsData);
      setConfig(configData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#4CAF50';
      case 'warning': return '#FF9800';
      case 'critical': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  const getLogLevelClass = (level) => {
    switch (level) {
      case 'error': return 'log-error';
      case 'warning': return 'log-warning';
      case 'info': return 'log-info';
      default: return 'log-default';
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <h2>Loading AI Agent Dashboard...</h2>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Agent Orchestration Dashboard</h1>
        <p>Real-time monitoring of AI agents across your development and deployment pipeline</p>
      </header>

      <main className="dashboard-container">
        {/* Overall Metrics */}
        <section className="overview-section">
          <h2>System Overview</h2>
          <div className="overview-cards">
            <div className="card">
              <h3>Total Requests</h3>
              <p className="metric-value">{metrics?.totalRequests || 0}</p>
            </div>
            <div className="card">
              <h3>Overall Success Rate</h3>
              <p className="metric-value">{metrics?.overallSuccessRate ? `${metrics.overallSuccessRate}%` : 'N/A'}</p>
            </div>
            <div className="card">
              <h3>System Health</h3>
              <p className={`metric-value ${metrics?.systemHealth === 'operational' ? 'healthy' : 'unhealthy'}`}>
                {metrics?.systemHealth || 'Unknown'}
              </p>
            </div>
          </div>
        </section>

        {/* Agent Status */}
        <section className="agents-section">
          <h2>AI Agent Status</h2>
          <div className="agents-grid">
            {metrics?.agents.map((agent) => (
              <div key={agent.id} className="agent-card">
                <div className="agent-header">
                  <h3>{agent.name}</h3>
                  <span
                    className="status-indicator"
                    style={{ backgroundColor: getStatusColor(agent.status) }}
                  >
                    {agent.status}
                  </span>
                </div>
                <div className="agent-details">
                  <div className="detail-item">
                    <span>Requests:</span>
                    <strong>{agent.requests}</strong>
                  </div>
                  <div className="detail-item">
                    <span>Success Rate:</span>
                    <strong>{agent.successRate}%</strong>
                  </div>
                  <div className="detail-item">
                    <span>Avg Response Time:</span>
                    <strong>{agent.avgResponseTime}ms</strong>
                  </div>
                  <div className="detail-item">
                    <span>Last Activity:</span>
                    <small>{new Date(agent.lastActivity).toLocaleString()}</small>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Recent Logs */}
        <section className="logs-section">
          <h2>Recent Activity Logs</h2>
          <div className="logs-container">
            {logs.slice(0, 10).map((log) => (
              <div key={log.id} className={`log-entry ${getLogLevelClass(log.level)}`}>
                <div className="log-timestamp">{new Date(log.timestamp).toLocaleTimeString()}</div>
                <div className="log-message">{log.message}</div>
                <div className="log-agent">[{log.agent}]</div>
              </div>
            ))}
          </div>
        </section>

        {/* Configuration */}
        <section className="config-section">
          <h2>Configuration</h2>
          <div className="config-container">
            <div className="config-item">
              <label>Kubectl AI Enabled:</label>
              <input
                type="checkbox"
                checked={config.kubectlAiEnabled}
                onChange={(e) => updateConfig({...config, kubectlAiEnabled: e.target.checked})}
              />
            </div>
            <div className="config-item">
              <label>Docker AI Enabled:</label>
              <input
                type="checkbox"
                checked={config.dockerAiEnabled}
                onChange={(e) => updateConfig({...config, dockerAiEnabled: e.target.checked})}
              />
            </div>
            <div className="config-item">
              <label>CI/CD AI Enabled:</label>
              <input
                type="checkbox"
                checked={config.cicdAiEnabled}
                onChange={(e) => updateConfig({...config, cicdAiEnabled: e.target.checked})}
              />
            </div>
            <div className="config-item">
              <label>AI Provider:</label>
              <select
                value={config.aiProvider || ''}
                onChange={(e) => updateConfig({...config, aiProvider: e.target.value})}
              >
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic</option>
                <option value="azure">Azure OpenAI</option>
              </select>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

async function updateConfig(newConfig) {
  try {
    await fetch('http://localhost:5001/api/config', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newConfig)
    });
  } catch (error) {
    console.error('Error updating config:', error);
  }
}

export default App;