function AlertModal({ alert, onClose }) {

  if (!alert) return null;

  function getColor(severity) {
    if (severity === "high") return "#ef4444";
    if (severity === "medium") return "#f59e0b";
    return "#22c55e";
  }

  return (

    <div style={overlay} onClick={onClose}>

      <div
        style={modal}
        onClick={(e) => e.stopPropagation()}
      >

        {/* 🔥 Header */}
        <div style={header}>

          <h2>Alert Details</h2>

          <button
            onClick={onClose}
            style={closeBtn}
          >
            ✕
          </button>

        </div>

        {/* 🔥 Severity */}
        <div
          style={{
            ...severityBadge,
            background: getColor(alert.severity),
          }}
        >
          {(alert.severity || "unknown").toUpperCase()}
        </div>

        {/* 🔥 Details */}
        <div style={details}>

          <div style={row}>
            <span style={label}>User</span>
            <span>{alert.user_id || "Unknown"}</span>
          </div>

          <div style={row}>
            <span style={label}>IP Address</span>
            <span>{alert.ip_address || "Unknown"}</span>
          </div>

          <div style={row}>
            <span style={label}>Threat Score</span>
            <span>{alert.threat_score || 0}</span>
          </div>

          <div style={row}>
            <span style={label}>Timestamp</span>
            <span>
              {alert.timestamp
                ? new Date(alert.timestamp).toLocaleString()
                : "Unknown"}
            </span>
          </div>

        </div>

        {/* 🔥 AI Analysis */}
        <div style={analysisBox}>

          <h3 style={{ marginBottom: "10px" }}>
            AI Analysis
          </h3>

          <p style={{ color: "#cbd5e1" }}>
            Suspicious login pattern detected.
            Multiple failed authentication attempts
            indicate possible brute force activity.
          </p>

        </div>

        {/* 🔥 Actions */}
        <div style={actions}>

          <button style={safeBtn}>
            Mark Safe
          </button>

          <button style={investigateBtn}>
            Investigate
          </button>

        </div>

      </div>

    </div>
  );
}

/* 🔥 Styles */

const overlay = {
  position: "fixed",
  inset: 0,
  background: "rgba(0,0,0,0.7)",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  zIndex: 999,
};

const modal = {
  background: "linear-gradient(145deg, #111827, #020617)",
  width: "500px",
  borderRadius: "16px",
  padding: "25px",
  border: "1px solid #1f2937",
  boxShadow: "0 0 30px rgba(0,0,0,0.5)",
};

const header = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "20px",
};

const closeBtn = {
  background: "transparent",
  border: "none",
  color: "white",
  fontSize: "20px",
  cursor: "pointer",
};

const severityBadge = {
  padding: "8px 15px",
  borderRadius: "20px",
  color: "white",
  width: "fit-content",
  marginBottom: "20px",
  fontWeight: "600",
};

const details = {
  display: "flex",
  flexDirection: "column",
  gap: "12px",
  marginBottom: "25px",
};

const row = {
  display: "flex",
  justifyContent: "space-between",
  borderBottom: "1px solid #1f2937",
  paddingBottom: "8px",
};

const label = {
  color: "#94a3b8",
};

const analysisBox = {
  background: "#0f172a",
  border: "1px solid #1e293b",
  padding: "15px",
  borderRadius: "10px",
  marginBottom: "20px",
};

const actions = {
  display: "flex",
  justifyContent: "flex-end",
  gap: "10px",
};

const safeBtn = {
  background: "#22c55e",
  border: "none",
  color: "white",
  padding: "10px 15px",
  borderRadius: "8px",
  cursor: "pointer",
};

const investigateBtn = {
  background: "#38bdf8",
  border: "none",
  color: "white",
  padding: "10px 15px",
  borderRadius: "8px",
  cursor: "pointer",
};

export default AlertModal;