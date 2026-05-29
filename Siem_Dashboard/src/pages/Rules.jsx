import { useEffect, useState } from "react";
import "./Rules.css";

function Rules() {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/rules")
      .then((response) => response.json())
      .then((data) => {
        setRules(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching rules:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="rules-loading">Loading rules...</p>;
  }

  return (
    <div className="rules-page">
      <div className="rules-header">
        <h1>Detection Rules</h1>
        <p>Overview of active rule-based detections used by the SIEM engine.</p>
      </div>

      <div className="rules-grid">
        {rules.map((rule) => (
          <div className="rule-card" key={rule.rule_name}>
            <div className="rule-card-header">
              <h3>{rule.rule_name}</h3>
              <span className={`severity ${rule.severity.toLowerCase()}`}>
                {rule.severity}
              </span>
            </div>

            <p>{rule.description}</p>

            <div className="rule-footer">
              <span>Score</span>
              <strong>{rule.score}</strong>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Rules;