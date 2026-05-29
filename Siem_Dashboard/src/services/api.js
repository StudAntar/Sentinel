const API_URL = "http://127.0.0.1:5000";

// 🔹 Alerts
export async function getAlerts() {
  const res = await fetch(`${API_URL}/alerts`);
  return res.json();
}

export async function getAlertById(id) {
  const res = await fetch(`${API_URL}/alerts/${id}`);
  return res.json();
}

// 🔹 Logs
export async function getLogs() {
  const res = await fetch(`${API_URL}/logs`);
  return res.json();
}

// 🔹 Employee Detail
export async function getEmployeeById(userId) {
  const res = await fetch(
    `${API_URL}/employees/${encodeURIComponent(userId)}`
  );

  return res.json();
} 

// 🔹 Stats
export async function getStats() {
  const res = await fetch(`${API_URL}/stats`);
  return res.json();
}