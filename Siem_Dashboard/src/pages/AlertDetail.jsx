import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { getAlertById } from "../services/api";

function getColor(threatLevel) {
  const level = threatLevel?.toLowerCase();

  if (level === "high") return "#ef4444";
  if (level === "medium") return "#f59e0b";
  return "#22c55e";
}

function AlertDetail() {
  const { id } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    getAlertById(id).then((response) => setData(response));
  }, [id]);

  if (!data) return <p>Loading...</p>;

  const alert = data.alert;
  const log = data.log;

  return (
    <div style={container}>
      <h1>Alert Detail</h1>

      <div style={card}>
        <h2>Alert Information</h2>

        <p><strong>Alert ID:</strong> {alert.id}</p>
        <p><strong>Log ID:</strong> {alert.log_id}</p>
        <p><strong>User:</strong> {alert.user_id}</p>
        <p><strong>Threat Score:</strong> {alert.threat_score}</p>

        <p style={{ color: getColor(alert.threat_level) }}>
          <strong>Threat Level:</strong> {alert.threat_level}
        </p>

        <p><strong>Country:</strong> {alert.country}</p>
        <p><strong>Created At:</strong> {alert.created_at}</p>
        <p><strong>Explanation:</strong> {alert.explanation}</p>
      </div>

      <div style={card}>
        <h2>Related Log</h2>

        <p><strong>Log ID:</strong> {log.id}</p>
        <p><strong>Timestamp:</strong> {log.timestamp}</p>
        <p><strong>Event Type:</strong> {log.event_type}</p>
        <p><strong>Login Status:</strong> {log.login_status}</p>
        <p><strong>IP:</strong> {log.ip}</p>
        <p><strong>City:</strong> {log.city}</p>
        <p><strong>Device:</strong> {log.device}</p>
        <p><strong>Device ID:</strong> {log.device_id}</p>
        <p><strong>Device Type:</strong> {log.device_type}</p>
        <p><strong>Browser:</strong> {log.browser}</p>
        <p><strong>OS:</strong> {log.os}</p>
        <p><strong>MFA Required:</strong> {String(log.mfa_required)}</p>
        <p><strong>MFA Success:</strong> {String(log.mfa_success)}</p>
        <p><strong>User Agent:</strong> {log.user_agent}</p>
      </div>
    </div>
  );
}

const container = {
  padding: "25px",
  color: "white",
  background: "#020617",
  minHeight: "100vh",
};

const card = {
  background: "linear-gradient(145deg, #111827, #020617)",
  padding: "20px",
  borderRadius: "10px",
  marginBottom: "20px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
};

export default AlertDetail;