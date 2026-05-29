import { Link } from "react-router-dom";
import { useState } from "react";
import logo from "../assets/logo.png";

function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div
      style={{
        ...sidebar,
        width: collapsed ? "80px" : "220px",
      }}
    >
      <div style={top}>
        {!collapsed && (
          <div style={logoContainer}>
            <img src={logo} alt="logo" style={logoStyle} />
            <span style={logoText}>Sentinel</span>
          </div>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          style={toggleBtn}
        >
          ☰
        </button>
      </div>

      <nav style={nav}>
        <Link to="/" style={link}>Dashboard</Link>
        <Link to="/alerts" style={link}>Alerts</Link>
        <Link to="/logs" style={link}>Logs</Link>
        <Link to="/employees" style={link}>Employees</Link>
        <Link to="/rules" style={link}>Rules</Link>
        <Link to="/analytics" style={link}>Analytics</Link>
      </nav>
    </div>
  );
}

const sidebar = {
  height: "100vh",
  background: "#020617",
  borderRight: "1px solid #1f2937",
  padding: "20px",
  display: "flex",
  flexDirection: "column",
  transition: "0.3s",
};

const top = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "30px",
};

const logoContainer = {
  display: "flex",
  alignItems: "center",
  gap: "10px",
};

const logoStyle = {
  width: "35px",
  height: "35px",
};

const logoText = {
  fontSize: "18px",
  fontWeight: "600",
  color: "#38bdf8",
};

const toggleBtn = {
  background: "transparent",
  border: "none",
  color: "white",
  fontSize: "20px",
  cursor: "pointer",
};

const nav = {
  display: "flex",
  flexDirection: "column",
  gap: "15px",
};

const link = {
  color: "#94a3b8",
  textDecoration: "none",
  fontSize: "14px",
};

export default Sidebar;