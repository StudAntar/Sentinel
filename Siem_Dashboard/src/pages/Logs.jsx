import { useEffect, useState } from "react";
import { getLogs } from "../services/api";

function Logs() {
  const [logs, setLogs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function fetchLogs() {
      const data = await getLogs();
      setLogs(data.logs || []);
    }

    fetchLogs();

    const interval = setInterval(fetchLogs, 3000);

    return () => clearInterval(interval);
  }, []);

  const filteredLogs = logs.filter((log) => {
    const searchValue = search.toLowerCase();

    return (
      (log.user_id || "").toLowerCase().includes(searchValue) ||
      (log.event_type || "").toLowerCase().includes(searchValue) ||
      (log.ip || "").toLowerCase().includes(searchValue) ||
      (log.country || "").toLowerCase().includes(searchValue) ||
      (log.device || "").toLowerCase().includes(searchValue)
    );
  });

  return (
    <div style={container}>
      <div style={header}>
        <div>
          <h1 style={title}>Logs</h1>
          <p style={subtitle}>Raw authentication events</p>
        </div>

        <input
          type="text"
          placeholder="Search user, IP, country, event..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={searchInput}
        />
      </div>

      <div style={tableWrapper}>
        <table style={table}>
          <thead>
            <tr>
              <th style={th}>Time</th>
              <th style={th}>User</th>
              <th style={th}>Event</th>
              <th style={th}>Status</th>
              <th style={th}>IP</th>
              <th style={th}>Country</th>
              <th style={th}>Device</th>
              <th style={th}>Browser</th>
              <th style={th}>OS</th>
            </tr>
          </thead>

          <tbody>
            {filteredLogs.map((log) => (
              <tr key={log.id} style={tr}>
                <td style={td}>
                  {log.timestamp
                    ? new Date(log.timestamp).toLocaleString()
                    : "N/A"}
                </td>
                <td style={td}>{log.user_id}</td>
                <td style={td}>{log.event_type}</td>
                <td style={td}>{log.login_status}</td>
                <td style={td}>{log.ip}</td>
                <td style={td}>{log.country}</td>
                <td style={td}>{log.device}</td>
                <td style={td}>{log.browser}</td>
                <td style={td}>{log.os}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const container = {
  padding: "20px",
  background: "#020617",
  minHeight: "100vh",
  color: "white",
};

const header = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "20px",
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
  width: "320px",
  outline: "none",
};

const tableWrapper = {
  background: "linear-gradient(145deg, #111827, #020617)",
  borderRadius: "12px",
  padding: "15px",
  overflowX: "auto",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
};

const table = {
  width: "100%",
  borderCollapse: "collapse",
};

const th = {
  textAlign: "left",
  padding: "12px",
  color: "#94a3b8",
  borderBottom: "1px solid #1f2937",
  fontSize: "13px",
};

const td = {
  padding: "12px",
  borderBottom: "1px solid #1f2937",
  fontSize: "13px",
  color: "#e5e7eb",
};

const tr = {
  transition: "0.2s",
};

export default Logs;