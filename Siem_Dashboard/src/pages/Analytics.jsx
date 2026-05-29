import { useEffect, useState } from "react";
import "./Analytics.css";

function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/analytics")
      .then((response) => response.json())
      .then((data) => {
        setAnalytics(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching analytics:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="analytics-loading">Loading analytics...</p>;
  }

  if (!analytics) {
    return <p className="analytics-loading">No analytics data available.</p>;
  }

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h1>Detection Analytics</h1>
        <p>Overview of detection activity, alerts, rule triggers and threat levels.</p>
      </div>

      <div className="analytics-cards">
        <div className="analytics-card">
          <span>Total Logs</span>
          <strong>{analytics.total_logs}</strong>
        </div>

        <div className="analytics-card">
          <span>Total Alerts</span>
          <strong>{analytics.total_alerts}</strong>
        </div>

        <div className="analytics-card">
          <span>High Alerts</span>
          <strong>{analytics.high_alerts}</strong>
        </div>

        <div className="analytics-card">
          <span>Avg Threat Score</span>
          <strong>{analytics.avg_threat_score}</strong>
        </div>

        <div className="analytics-card">
          <span>Successful Logins</span>
          <strong>{analytics.successful_logins}</strong>
        </div>

        <div className="analytics-card">
          <span>Failed Logins</span>
          <strong>{analytics.failed_logins}</strong>
        </div>
      </div>

      <div className="analytics-sections">
        <div className="analytics-panel">
          <h2>Rule Trigger Counts</h2>

          {analytics.rule_triggers.length === 0 ? (
            <p className="empty-text">No rule triggers yet.</p>
          ) : (
            analytics.rule_triggers.map((rule) => (
              <div className="analytics-row" key={rule.rule_name}>
                <span>{rule.rule_name}</span>
                <strong>{rule.trigger_count}</strong>
              </div>
            ))
          )}
        </div>

        <div className="analytics-panel">
          <h2>Severity Distribution</h2>

          {analytics.severity_distribution.length === 0 ? (
            <p className="empty-text">No severity data yet.</p>
          ) : (
            analytics.severity_distribution.map((item) => (
              <div className="analytics-row" key={item.severity}>
                <span>{item.severity}</span>
                <strong>{item.count}</strong>
              </div>
            ))
          )}
        </div>

        <div className="analytics-panel">
          <h2>Threat Level Distribution</h2>

          {analytics.threat_distribution.length === 0 ? (
            <p className="empty-text">No threat level data yet.</p>
          ) : (
            analytics.threat_distribution.map((item) => (
              <div className="analytics-row" key={item.threat_level}>
                <span>{item.threat_level}</span>
                <strong>{item.count}</strong>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default Analytics;