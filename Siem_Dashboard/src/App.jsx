import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import Alerts from "./pages/Alerts";
import AlertDetail from "./pages/AlertDetail";
import Employees from "./pages/Employees";
import EmployeeDetail from "./pages/EmployeeDetail";
import Logs from "./pages/Logs";
import Rules from "./pages/Rules";
import Analytics from "./pages/Analytics";
import IncidentView from "./pages/IncidentView";
function App() {
  return (
    <BrowserRouter>
      <div style={layout}>
        <Sidebar />

        <div style={content}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/alert/:id" element={<AlertDetail />} />
            <Route path="/logs" element={<Logs />} />
            <Route path="/employees" element={<Employees />} />
            <Route path="/employee/:id" element={<EmployeeDetail />} />
            <Route path="/rules" element={<Rules />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/incident/:logId" element={<IncidentView />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

const layout = {
  display: "flex",
  background: "#020617",
  color: "white",
};

const content = {
  flex: 1,
  padding: "20px",
};

export default App;