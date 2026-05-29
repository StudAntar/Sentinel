import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { getEmployeeById } from "../services/api";

function getRiskColor(score) {
  if (score >= 60) return "#ef4444";
  if (score >= 25) return "#f59e0b";
  return "#22c55e";
}

function EmployeeDetail() {
  const { id } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    async function fetchEmployee() {
      const response = await getEmployeeById(id);
      setData(response);
    }

    fetchEmployee();

    const interval = setInterval(fetchEmployee, 3000);

    return () => clearInterval(interval);
  }, [id]);

  if (!data) {
    return <div style={loading}>Loading...</div>;
  }

  const employee = data.employee;
  const logs = data.logs || [];
  const alerts = data.alerts || [];

  return (
    <div style={container}>
      <div style={header}>
        <div style={avatar}>
          {employee.user_id.charAt(0).toUpperCase()}
        </div>

        <div>
          <h1>{employee.user_id}</h1>
          <p style={subtitle}>User investigation panel</p>
        </div>
      </div>

      <div style={grid}>
        <Card title="Risk Score" value={employee.risk_score} color={getRiskColor(employee.risk_score)} />
        <Card title="Total Alerts" value={employee.total_alerts} color="#f59e0b" />
        <Card title="Total Logs" value={employee.total_logs} color="#38bdf8" />
        <Card title="Last Login" value={employee.last_login || "N/A"} color="#22c55e" />
      </div>

      <div style={section}>
        <h2>Recent Alerts</h2>

        {alerts.length === 0 ? (
          <p style={muted}>No alerts found for this user.</p>
        ) : (
          alerts.map((alert) => (
            <div key={alert.id} style={item}>
              <strong>{alert.threat_level}</strong> — Score {alert.threat_score}
              <br />
              <span style={muted}>{alert.explanation}</span>
              <br />
              <span style={muted}>{alert.created_at}</span>
            </div>
          ))
        )}
      </div>

      <div style={section}>
        <h2>Recent Logs</h2>

        {logs.length === 0 ? (
          <p style={muted}>No logs found for this user.</p>
        ) : (
          logs.slice(0, 10).map((log) => (
            <div key={log.id} style={item}>
              <strong>{log.event_type}</strong> — {log.login_status}
              <br />
              <span style={muted}>
                {log.ip} | {log.country} | {log.device} | {log.browser} | {log.os}
              </span>
              <br />
              <span style={muted}>{log.timestamp}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

function Card({ title, value, color }) {
  return (
    <div style={{ ...card, borderLeft: `4px solid ${color}` }}>
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
}

const container = {
  padding: "20px",
  minHeight: "100vh",
  background: "#020617",
  color: "white",
};

const header = {
  display: "flex",
  gap: "20px",
  alignItems: "center",
  marginBottom: "25px",
};

const avatar = {
  width: "80px",
  height: "80px",
  background: "#38bdf8",
  borderRadius: "50%",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  fontSize: "30px",
  fontWeight: "700",
};

const subtitle = {
  color: "#94a3b8",
};

const grid = {
  display: "grid",
  gridTemplateColumns: "repeat(4, 1fr)",
  gap: "15px",
  marginBottom: "25px",
};

const card = {
  background: "linear-gradient(145deg,#111827,#020617)",
  padding: "20px",
  borderRadius: "12px",
};

const section = {
  background: "#111827",
  padding: "20px",
  borderRadius: "12px",
  marginBottom: "20px",
};

const item = {
  background: "#020617",
  padding: "12px",
  borderRadius: "8px",
  marginTop: "10px",
};

const muted = {
  color: "#94a3b8",
};

const loading = {
  padding: "50px",
  color: "white",
};

export default EmployeeDetail;