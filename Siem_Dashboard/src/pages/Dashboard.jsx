import { useEffect, useState } from "react";
import { getAlerts, getLogs, getStats } from "../services/api";
import LoginChart from "../components/LoginChart";
import SeverityPieChart from "../components/SeverityPieChart";
import ThreatGlobe from "../components/ThreatGlobe";
import { useNavigate } from "react-router-dom";

function getColor(threatLevel) {
  const level = threatLevel?.toLowerCase();

  if (level === "critical") return "#dc2626";
  if (level === "high") return "#ef4444";
  if (level === "medium") return "#f59e0b";
  return "#22c55e";
}

function getMlColor(prediction) {
  return prediction === "ANOMALY" ? "#ef4444" : "#22c55e";
}

function Dashboard() {
  const [alerts, setAlerts] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [stats, setStats] = useState(null);
  const [mlResults, setMlResults] = useState([]);
  const [riskCorrelation, setRiskCorrelation] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchAlerts() {
      const data = await getAlerts();
      setAlerts(data.alerts || []);
    }

    async function fetchLogs() {
      const data = await getLogs();
      const logs = data.logs || [];
      const grouped = {};

      logs.forEach((log) => {
        const time = new Date(log.timestamp).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        });

        grouped[time] = (grouped[time] || 0) + 1;
      });

      const formatted = Object.keys(grouped).map((time) => ({
        time,
        logins: grouped[time],
      }));

      setChartData(formatted);
    }

    async function fetchStats() {
      const data = await getStats();
      setStats(data);
    }

    async function fetchMlResults() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/ml-results");
        const data = await response.json();
        setMlResults(data || []);
      } catch (error) {
        console.error("Error fetching ML results:", error);
      }
    }

    async function fetchRiskCorrelation() {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/risk-correlation"
        );
        const data = await response.json();
        setRiskCorrelation(data || []);
      } catch (error) {
        console.error("Error fetching risk correlation:", error);
      }
    }

    fetchAlerts();
    fetchLogs();
    fetchStats();
    fetchMlResults();
    fetchRiskCorrelation();

    const interval = setInterval(() => {
      fetchAlerts();
      fetchLogs();
      fetchStats();
      fetchMlResults();
      fetchRiskCorrelation();
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={container}>
      <div style={topSection}>
        <div style={cards}>
          <div style={{ ...card, borderLeft: "4px solid #38bdf8" }}>
            <h3>Total Alerts</h3>
            <p>{stats?.total_alerts ?? 0}</p>
          </div>

          <div style={{ ...card, borderLeft: "4px solid #ef4444" }}>
            <h3>High Severity</h3>
            <p style={{ color: "#ef4444" }}>{stats?.high_alerts ?? 0}</p>
          </div>

          <div style={{ ...card, borderLeft: "4px solid #22c55e" }}>
            <h3>Avg Score</h3>
            <p>{stats?.avg_threat_score ?? 0}</p>
          </div>

          <div style={{ ...card, borderLeft: "4px solid #a855f7" }}>
            <h3>Total Logs</h3>
            <p>{stats?.total_logs ?? 0}</p>
          </div>

          <div style={{ ...card, borderLeft: "4px solid #f59e0b" }}>
            <h3>Failed Logins</h3>
            <p>{stats?.failed_logins ?? 0}</p>
          </div>

          <div style={{ ...card, borderLeft: "4px solid #38bdf8" }}>
            <h3>Total Users</h3>
            <p>{stats?.total_users ?? 0}</p>
          </div>
        </div>

        <div style={topPanel}>
          <SeverityPieChart alerts={alerts} />
        </div>
      </div>

      <div style={middle}>
        <div style={box}>
          <h4 style={title}>Login Activity</h4>

          <div style={chartWrapper}>
            <LoginChart data={chartData} />
          </div>
        </div>

        <div style={box}>
          <h4 style={title}>Global Login Activity</h4>

          <div style={globeWrapper}>
            <ThreatGlobe />
          </div>
        </div>
      </div>

      <div style={alertsBox}>
        <h4 style={title}>Recent Alerts</h4>

        {alerts.slice(0, 5).map((a, i) => (
          <div
            key={a.id || i}
            style={{
              ...alertItem,
              borderLeft: `4px solid ${getColor(a.threat_level)}`,
              boxShadow: `0 0 10px ${getColor(a.threat_level)}33`,
              background: `linear-gradient(
                90deg,
                ${getColor(a.threat_level)}22,
                transparent
              )`,
            }}
          >
            <span>{a.user_id || "Unknown"}</span>
            <span>{(a.threat_level || "UNKNOWN").toUpperCase()}</span>
            <span>{a.threat_score ?? 0}</span>
          </div>
        ))}
      </div>

      <div style={mlBox}>
        <h4 style={title}>ML Anomaly Detection</h4>

        {mlResults.slice(0, 5).map((result, i) => (
          <div
            key={result.id || i}
            style={{
              ...mlItem,
              borderLeft: `4px solid ${getMlColor(result.prediction)}`,
              boxShadow: `0 0 10px ${getMlColor(result.prediction)}33`,
              background: `linear-gradient(
                90deg,
                ${getMlColor(result.prediction)}22,
                transparent
              )`,
            }}
          >
            <span>{result.user_id || "Unknown"}</span>

            <span
              style={{
                ...mlBadge,
                backgroundColor: getMlColor(result.prediction),
              }}
            >
              {result.prediction || "UNKNOWN"}
            </span>

            <span>{result.threat_level || "LOW"}</span>

            <span>{result.anomaly_score ?? "N/A"}</span>

            <span>{result.explanation || "No explanation available"}</span>
          </div>
        ))}
      </div>

      <div style={correlationBox}>
        <div style={correlationHeader}>
          <div>
            <h4 style={title}>Risk Correlation Analysis</h4>
            <p style={subtitle}>
              Relationship between rule-based alerts and ML behavior detection
            </p>
          </div>

          <span style={correlationTag}>RULES + BEHAVIOR</span>
        </div>

        {riskCorrelation.slice(0, 5).map((item, i) => (
          <div
            key={item.log_id || i}
            onClick={() => navigate(`/incident/${item.log_id}`)}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-2px)";
              e.currentTarget.style.filter = "brightness(1.12)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0px)";
              e.currentTarget.style.filter = "brightness(1)";
            }}
            style={{
              ...correlationItem,
              cursor: "pointer",
              borderLeft: `4px solid ${getColor(item.correlation_level)}`,
              boxShadow: `0 0 12px ${getColor(item.correlation_level)}33`,
              background: `linear-gradient(
                90deg,
                ${getColor(item.correlation_level)}1f,
                transparent
              )`,
            }}
          >
            <div>
              <p style={userText}>{item.user_id || "Unknown"}</p>
              <p style={metaText}>
                Log #{item.log_id} · {item.event_type || "unknown_event"}
              </p>
            </div>

            <div style={levelGroup}>
              <span style={smallLabel}>Rules</span>
              <span
                style={{
                  ...levelBadge,
                  backgroundColor: getColor(item.rule_threat_level),
                }}
              >
                {item.rule_threat_level || "LOW"}
              </span>
            </div>

            <div style={levelGroup}>
              <span style={smallLabel}>Behavior</span>
              <span
                style={{
                  ...levelBadge,
                  backgroundColor: getColor(item.behavior_threat_level),
                }}
              >
                {item.behavior_threat_level || "LOW"}
              </span>
            </div>

            <div style={levelGroup}>
              <span style={smallLabel}>Correlation</span>
              <span
                style={{
                  ...levelBadge,
                  backgroundColor: getColor(item.correlation_level),
                }}
              >
                {item.correlation_level || "LOW"}
              </span>
            </div>

            <p style={reasonText}>
              {item.correlation_reason || "No correlation reason available"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

const container = {
  minHeight: "100vh",
  display: "flex",
  flexDirection: "column",
  gap: "15px",
  padding: "20px",
  background: "#020617",
};

const topSection = {
  display: "grid",
  gridTemplateColumns: "2fr 1fr",
  gap: "15px",
  alignItems: "stretch",
};

const cards = {
  display: "grid",
  gridTemplateColumns: "repeat(3, 1fr)",
  gap: "15px",
};

const card = {
  background: "linear-gradient(145deg, #111827, #020617)",
  padding: "15px",
  borderRadius: "10px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
  minHeight: "110px",
};

const topPanel = {
  background: "linear-gradient(145deg, #111827, #020617)",
  borderRadius: "10px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
  overflow: "hidden",
};

const middle = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "15px",
  alignItems: "stretch",
};

const box = {
  background: "linear-gradient(145deg, #111827, #020617)",
  padding: "15px",
  borderRadius: "10px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
  height: "360px",
  overflow: "hidden",
};

const chartWrapper = {
  width: "100%",
  height: "300px",
};

const globeWrapper = {
  width: "100%",
  height: "300px",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  overflow: "hidden",
  paddingTop: "20px",
};

const alertsBox = {
  background: "linear-gradient(145deg, #111827, #020617)",
  padding: "15px",
  borderRadius: "10px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
};

const alertItem = {
  display: "grid",
  gridTemplateColumns: "2fr 1fr 80px",
  gap: "10px",
  padding: "10px",
  borderRadius: "6px",
  marginBottom: "5px",
  color: "#e5e7eb",
};

const mlBox = {
  background: "linear-gradient(145deg, #111827, #020617)",
  padding: "15px",
  borderRadius: "10px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
};

const mlItem = {
  display: "grid",
  gridTemplateColumns: "2fr 1fr 100px 100px 3fr",
  gap: "10px",
  padding: "10px",
  borderRadius: "6px",
  marginBottom: "5px",
  color: "#e5e7eb",
  alignItems: "center",
};

const mlBadge = {
  color: "#fff",
  padding: "4px 10px",
  borderRadius: "999px",
  fontSize: "12px",
  fontWeight: "bold",
  textAlign: "center",
};

const correlationBox = {
  background: "linear-gradient(145deg, #111827, #020617)",
  padding: "15px",
  borderRadius: "10px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
};

const correlationHeader = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "12px",
};

const correlationTag = {
  color: "#38bdf8",
  border: "1px solid #38bdf855",
  background: "#38bdf811",
  padding: "6px 10px",
  borderRadius: "999px",
  fontSize: "11px",
  fontWeight: "bold",
};

const correlationItem = {
  display: "grid",
  gridTemplateColumns: "2fr 1fr 1fr 1fr 3fr",
  gap: "12px",
  padding: "12px",
  borderRadius: "8px",
  marginBottom: "8px",
  color: "#e5e7eb",
  alignItems: "center",
  transition: "all 0.2s ease",
};

const levelGroup = {
  display: "flex",
  flexDirection: "column",
  gap: "4px",
};

const levelBadge = {
  color: "#fff",
  padding: "4px 10px",
  borderRadius: "999px",
  fontSize: "11px",
  fontWeight: "bold",
  textAlign: "center",
  width: "fit-content",
};

const smallLabel = {
  color: "#64748b",
  fontSize: "11px",
  textTransform: "uppercase",
};

const userText = {
  color: "#e5e7eb",
  fontWeight: "600",
  margin: 0,
};

const metaText = {
  color: "#64748b",
  fontSize: "12px",
  margin: "4px 0 0 0",
};

const reasonText = {
  color: "#cbd5e1",
  fontSize: "13px",
  lineHeight: "1.4",
  margin: 0,
};

const subtitle = {
  color: "#64748b",
  fontSize: "12px",
  margin: "-5px 0 0 0",
};

const title = {
  color: "#94a3b8",
  marginBottom: "10px",
};

export default Dashboard;