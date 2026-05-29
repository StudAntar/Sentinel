import { useEffect, useState } from "react";
import { getAlerts } from "../services/api";
import { useNavigate } from "react-router-dom";

function getColor(threatLevel) {
  const level = threatLevel?.toLowerCase();

  if (level === "high") return "#ef4444";
  if (level === "medium") return "#f59e0b";
  return "#22c55e";
}

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    async function fetchAlerts() {
      const data = await getAlerts();

      if (Array.isArray(data)) {
        setAlerts(data);
      } else {
        setAlerts(data.alerts || []);
      }
    }

    fetchAlerts();

    const interval = setInterval(fetchAlerts, 3000);

    return () => clearInterval(interval);
  }, []);

  const filteredAlerts = alerts.filter((alert) => {
    const threatLevel = alert.threat_level?.toLowerCase() || "unknown";

    const matchesFilter =
      filter === "all" ? true : threatLevel === filter;

    const matchesSearch =
      (alert.user_id || "")
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      (alert.country || "")
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      String(alert.log_id || "")
        .toLowerCase()
        .includes(search.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  return (
    <div style={container}>
      <div style={header}>
        <div>
          <h1 style={title}>Alerts Center</h1>
          <p style={subtitle}>Real-time threat monitoring</p>
        </div>

        <input
          type="text"
          placeholder="Search user, country or log ID..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={searchInput}
        />
      </div>

      <div style={filters}>
        {["all", "high", "medium", "low"].map((level) => (
          <button
            key={level}
            style={{
              ...filterBtn,
              background:
                filter === level
                  ? getColor(level)
                  : "#111827",
            }}
            onClick={() => setFilter(level)}
          >
            {level.toUpperCase()}
          </button>
        ))}
      </div>

      <div style={alertsContainer}>
        {filteredAlerts.map((alert, index) => (
          <div
            key={alert.id || index}
            onClick={() => navigate(`/alert/${alert.id}`)}
            style={{
              ...alertCard,
              borderLeft: `5px solid ${getColor(alert.threat_level)}`,
              boxShadow: `0 0 12px ${getColor(alert.threat_level)}33`,
            }}
          >
            <div style={topRow}>
              <div>
                <div style={userText}>
                  {alert.user_id || "Unknown User"}
                </div>

                <div style={ipText}>
                  Country: {alert.country || "Unknown"} | Log ID:{" "}
                  {alert.log_id || "N/A"}
                </div>
              </div>

              <div
                style={{
                  ...severityBadge,
                  background: getColor(alert.threat_level),
                }}
              >
                {(alert.threat_level || "UNKNOWN").toUpperCase()}
              </div>
            </div>

            <div style={explanationText}>
              {alert.explanation || "No explanation"}
            </div>

            <div style={bottomRow}>
              <div>
                Threat Score:
                <span style={score}> {alert.threat_score || 0}</span>
              </div>

              <div style={timestamp}>
                {alert.created_at
                  ? new Date(alert.created_at).toLocaleString()
                  : "No timestamp"}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

const container = {
  padding: "20px",
  display: "flex",
  flexDirection: "column",
  gap: "20px",
  background: "#020617",
  minHeight: "100vh",
};

const header = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
};

const title = {
  fontSize: "32px",
  marginBottom: "5px",
};

const subtitle = {
  color: "#64748b",
};

const searchInput = {
  background: "#111827",
  border: "1px solid #1f2937",
  color: "white",
  padding: "10px 15px",
  borderRadius: "8px",
  width: "280px",
  outline: "none",
};

const filters = {
  display: "flex",
  gap: "10px",
};

const filterBtn = {
  border: "none",
  color: "white",
  padding: "8px 15px",
  borderRadius: "8px",
  cursor: "pointer",
  transition: "0.2s",
};

const alertsContainer = {
  display: "flex",
  flexDirection: "column",
  gap: "15px",
  overflowY: "auto",
};

const alertCard = {
  background: "linear-gradient(145deg, #111827, #020617)",
  padding: "15px",
  borderRadius: "12px",
  transition: "0.2s",
  cursor: "pointer",
};

const topRow = {
  display: "flex",
  justifyContent: "space-between",
  marginBottom: "12px",
};

const userText = {
  fontSize: "18px",
  fontWeight: "600",
};

const ipText = {
  color: "#64748b",
  fontSize: "14px",
  marginTop: "4px",
};

const severityBadge = {
  padding: "6px 12px",
  borderRadius: "20px",
  color: "white",
  fontSize: "12px",
  fontWeight: "600",
};

const explanationText = {
  color: "#cbd5e1",
  fontSize: "14px",
  marginBottom: "12px",
};

const bottomRow = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  color: "#94a3b8",
};

const score = {
  color: "white",
  fontWeight: "600",
};

const timestamp = {
  fontSize: "13px",
};

export default Alerts;