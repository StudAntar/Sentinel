import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#ef4444",
  "#f59e0b",
  "#22c55e",
];

function SeverityPieChart({ alerts }) {

  const high = alerts.filter(
    a => a.severity === "high"
  ).length;

  const medium = alerts.filter(
    a => a.severity === "medium"
  ).length;

  const low = alerts.filter(
    a => a.severity === "low"
  ).length;

  const data = [
    { name: "High", value: high },
    { name: "Medium", value: medium },
    { name: "Low", value: low },
  ];

  return (
    <div style={container}>

      <h4 style={title}>
        Alert Severity
      </h4>

      <ResponsiveContainer width="100%" height={250}>

        <PieChart>

          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={90}
            dataKey="value"
          >

            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={COLORS[index]}
              />
            ))}

          </Pie>

          <Tooltip />

        </PieChart>

      </ResponsiveContainer>

    </div>
  );
}

const container = {
  background: "linear-gradient(145deg, #111827, #020617)",
  padding: "15px",
  borderRadius: "10px",
  height: "100%",
};

const title = {
  color: "#94a3b8",
  marginBottom: "10px",
};

export default SeverityPieChart;
