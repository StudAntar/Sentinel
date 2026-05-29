import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getAlerts, getLogs } from "../services/api";

function Employees() {
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function fetchData() {
      const logsData = await getLogs();
      const alertsData = await getAlerts();

      const logs = logsData.logs || [];
      const alerts = alertsData.alerts || [];

      const users = {};

      logs.forEach((log) => {
        if (!users[log.user_id]) {
          users[log.user_id] = {
            user_id: log.user_id,
            name: log.user_id,
            department: "Unknown department",
            logs: 0,
            alerts: 0,
            lastLogin: log.timestamp,
            risk: 0,
            status: "active",
          };
        }

        users[log.user_id].logs += 1;

        if (new Date(log.timestamp) > new Date(users[log.user_id].lastLogin)) {
          users[log.user_id].lastLogin = log.timestamp;
        }
      });

      alerts.forEach((alert) => {
        if (users[alert.user_id]) {
          users[alert.user_id].alerts += 1;
          users[alert.user_id].risk = Math.max(
            users[alert.user_id].risk,
            alert.threat_score || 0
          );
        }
      });

      setEmployees(Object.values(users));
    }

    fetchData();

    const interval = setInterval(fetchData, 3000);

    return () => clearInterval(interval);
  }, []);

  const filteredEmployees = employees.filter((emp) =>
    emp.user_id.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={container}>
      <div style={header}>
        <div>
          <h1 style={title}>Employees</h1>
          <p style={subtitle}>Users detected from authentication logs</p>
        </div>

        <input
          type="text"
          placeholder="Search employee..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={searchInput}
        />
      </div>

      <div style={grid}>
        {filteredEmployees.map((emp) => (
          <Link
            key={emp.user_id}
            to={`/employee/${encodeURIComponent(emp.user_id)}`}
            style={{ textDecoration: "none", color: "inherit" }}
          >
            <div
              style={{
                ...card,
                borderLeft:
                  emp.risk >= 60
                    ? "4px solid #ef4444"
                    : emp.risk >= 25
                    ? "4px solid #f59e0b"
                    : "4px solid #22c55e",
              }}
            >
              <div style={avatar}>{emp.user_id.charAt(0).toUpperCase()}</div>

              <div>
                <div style={name}>{emp.user_id}</div>
                <div style={department}>
                  Logs: {emp.logs} | Alerts: {emp.alerts}
                </div>
                <div style={department}>Risk score: {emp.risk}</div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

const container = {
  padding: "20px",
  background: "#020617",
  minHeight: "100vh",
};

const header = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "25px",
};

const title = {
  fontSize: "32px",
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
  width: "250px",
  outline: "none",
};

const grid = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fill,minmax(280px,1fr))",
  gap: "20px",
};

const card = {
  background: "linear-gradient(145deg,#111827,#020617)",
  borderRadius: "14px",
  padding: "20px",
  display: "flex",
  alignItems: "center",
  gap: "15px",
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
  cursor: "pointer",
};

const avatar = {
  width: "50px",
  height: "50px",
  borderRadius: "50%",
  background: "#38bdf8",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  fontWeight: "bold",
  fontSize: "20px",
};

const name = {
  fontWeight: "600",
  fontSize: "15px",
};

const department = {
  color: "#64748b",
  marginTop: "4px",
  fontSize: "13px",
};

export default Employees;