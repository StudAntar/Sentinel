import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

function getColor(level) {
  const value = level?.toLowerCase();

  if (value === "critical") return "#dc2626";
  if (value === "high") return "#ef4444";
  if (value === "medium") return "#f59e0b";
  return "#22c55e";
}

function IncidentView() {
  const { logId } = useParams();
  const navigate = useNavigate();
  const [incident, setIncident] = useState(null);

  useEffect(() => {
    async function fetchIncident() {
      const response = await fetch(
        `http://127.0.0.1:5000/api/incidents/${logId}`
      );

      const data = await response.json();
      setIncident(data);
    }

    fetchIncident();
  }, [logId]);

  if (!incident) {
    return (
      <div style={loadingContainer}>
        <div style={loader}></div>
        <p>Loading Incident...</p>
      </div>
    );
  }

  const { log, alerts, ml_result, risk_correlation } = incident;

  return (
    <div style={container}>
      <div style={header}>
        <div>
          <button onClick={() => navigate("/")} style={backButton}>
            ← Back to Dashboard
          </button>

          <h2 style={heading}>Incident View</h2>
          <p style={muted}>
            Log #{log.id} · {log.user_id || "Unknown user"}
          </p>
        </div>

        <span
          style={{
            ...badge,
            backgroundColor: getColor(risk_correlation.correlation_level),
          }}
        >
          {risk_correlation.correlation_level || "LOW"}
        </span>
      </div>

      <div style={grid}>
        <div style={card}>
          <h3>Risk Correlation</h3>
          <p style={bodyText}>
            {risk_correlation.correlation_reason ||
              "No correlation reason available."}
          </p>

          <div style={levels}>
            <span>Rules: {risk_correlation.rule_threat_level || "LOW"}</span>
            <span>
              Behavior: {risk_correlation.behavior_threat_level || "LOW"}
            </span>
          </div>
        </div>

        <div style={card}>
          <h3>ML Behavior Detection</h3>
          <p>
            <b>Prediction:</b> {ml_result?.prediction || "N/A"}
          </p>
          <p>
            <b>Score:</b> {ml_result?.anomaly_score ?? "N/A"}
          </p>
          <p>
            <b>Threat:</b> {ml_result?.threat_level || "LOW"}
          </p>
          <p style={muted}>
            {ml_result?.explanation || "No ML explanation available."}
          </p>
        </div>
      </div>

      <div style={card}>
        <h3>Triggered Rules</h3>

        {alerts.length > 0 ? (
          alerts.map((alert) => (
            <div
              key={alert.id}
              style={{
                ...alertRow,
                borderLeft: `4px solid ${getColor(alert.threat_level)}`,
              }}
            >
              <span>{alert.rule_name || "N/A"}</span>
              <span>{alert.threat_level || "LOW"}</span>
              <span>{alert.threat_score ?? "N/A"}</span>
              <span>{alert.explanation || "No explanation available"}</span>
            </div>
          ))
        ) : (
          <p style={muted}>No rules were triggered for this incident.</p>
        )}
      </div>

      <div style={card}>
        <h3>Raw Log Details</h3>

        <div style={rawGrid}>
          <p><b>Event:</b> {log.event_type || "N/A"}</p>
          <p><b>Status:</b> {log.login_status || "N/A"}</p>
          <p><b>IP:</b> {log.ip || "N/A"}</p>
          <p><b>Country:</b> {log.country || "N/A"}</p>
          <p><b>City:</b> {log.city || "N/A"}</p>
          <p><b>Device:</b> {log.device || "N/A"}</p>
          <p><b>Device ID:</b> {log.device_id || "N/A"}</p>
          <p><b>OS:</b> {log.os || "N/A"}</p>
          <p><b>Browser:</b> {log.browser || "N/A"}</p>
          <p><b>MFA Required:</b> {String(log.mfa_required)}</p>
          <p><b>MFA Success:</b> {String(log.mfa_success)}</p>
          <p>
            <b>Failed Attempts:</b>{" "}
            {log.failed_attempts_before_success ?? "N/A"}
          </p>
          <p><b>Login Duration:</b> {log.login_duration_ms ?? "N/A"} ms</p>
          <p><b>MFA Duration:</b> {log.mfa_duration_ms ?? "N/A"} ms</p>
          <p>
            <b>Session Duration:</b>{" "}
            {log.session_duration_minutes ?? "N/A"} min
          </p>
          <p>
            <b>Timestamp:</b>{" "}
            {log.timestamp ? new Date(log.timestamp).toLocaleString() : "N/A"}
          </p>
        </div>
      </div>
    </div>
  );
}

const container = {
  minHeight: "100vh",
  background: "#020617",
  color: "#e5e7eb",
  padding: "20px",
};

const loadingContainer = {
  minHeight: "100vh",
  background: "#020617",
  color: "#94a3b8",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
};

const loader = {
  width: "38px",
  height: "38px",
  border: "4px solid #1e293b",
  borderTop: "4px solid #38bdf8",
  borderRadius: "50%",
  marginBottom: "15px",
};

const header = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "20px",
};

const heading = {
  marginTop: "14px",
  marginBottom: "5px",
};

const backButton = {
  background: "#0f172a",
  color: "#e5e7eb",
  border: "1px solid #334155",
  padding: "8px 14px",
  borderRadius: "8px",
  cursor: "pointer",
};

const grid = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "15px",
  marginBottom: "15px",
};

const card = {
  background: "linear-gradient(145deg, #111827, #020617)",
  padding: "18px",
  borderRadius: "12px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
  marginBottom: "15px",
};

const badge = {
  color: "#fff",
  padding: "8px 16px",
  borderRadius: "999px",
  fontWeight: "bold",
};

const muted = {
  color: "#94a3b8",
};

const bodyText = {
  color: "#cbd5e1",
  lineHeight: "1.5",
};

const levels = {
  display: "flex",
  gap: "15px",
  marginTop: "12px",
  color: "#cbd5e1",
};

const alertRow = {
  display: "grid",
  gridTemplateColumns: "1.5fr 1fr 80px 3fr",
  gap: "10px",
  padding: "10px",
  borderRadius: "6px",
  marginBottom: "8px",
  background: "#020617",
};

const rawGrid = {
  display: "grid",
  gridTemplateColumns: "repeat(3, 1fr)",
  gap: "10px",
};

export default IncidentView;