from flask import Blueprint, jsonify
from database.db import get_connection


api_risk_correlation = Blueprint("api_risk_correlation", __name__)


def correlate_risk(rule_level, behavior_level):
    rule_level = (rule_level or "LOW").upper()
    behavior_level = (behavior_level or "LOW").upper()

    if rule_level == "HIGH" and behavior_level == "HIGH":
        return "CRITICAL", "Rules and ML both detected high-risk behavior."

    if rule_level == "HIGH" and behavior_level == "MEDIUM":
        return "HIGH", "Rules detected high-risk indicators while ML detected medium-risk abnormal behavior."

    if rule_level == "HIGH":
        return "HIGH", "Rules detected high-risk indicators, while ML did not detect strong abnormal behavior."

    if behavior_level == "HIGH":
        return "HIGH", "ML detected high-risk abnormal behavior."

    if rule_level == "MEDIUM" and behavior_level == "MEDIUM":
        return "HIGH", "Rules and ML both detected medium-risk signals."

    if rule_level == "MEDIUM" or behavior_level == "MEDIUM":
        return "MEDIUM", "Either rules or ML detected medium-risk activity."

    return "LOW", "No strong correlation between rules and ML behavior analysis."


@api_risk_correlation.route("/api/risk-correlation", methods=["GET"])
def get_risk_correlation():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            logs.id,
            logs.user_id,
            logs.event_type,
            logs.timestamp,

            CASE
                WHEN COUNT(CASE WHEN alerts.threat_level = 'HIGH' THEN 1 END) > 0 THEN 'HIGH'
                WHEN COUNT(CASE WHEN alerts.threat_level = 'MEDIUM' THEN 1 END) > 0 THEN 'MEDIUM'
                WHEN COUNT(CASE WHEN alerts.threat_level = 'LOW' THEN 1 END) > 0 THEN 'LOW'
                ELSE 'LOW'
            END AS rule_threat_level,

            COALESCE(ml_results.threat_level, 'LOW') AS behavior_threat_level,
            ml_results.prediction,
            ml_results.anomaly_score,
            ml_results.explanation

        FROM logs
        LEFT JOIN alerts ON alerts.log_id = logs.id
        LEFT JOIN ml_results ON ml_results.log_id = logs.id

        GROUP BY
            logs.id,
            logs.user_id,
            logs.event_type,
            logs.timestamp,
            ml_results.threat_level,
            ml_results.prediction,
            ml_results.anomaly_score,
            ml_results.explanation

        ORDER BY logs.timestamp DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    results = []

    for row in rows:
        correlation_level, correlation_reason = correlate_risk(
            row[4],
            row[5]
        )

        results.append({
            "log_id": row[0],
            "user_id": row[1],
            "event_type": row[2],
            "timestamp": row[3],
            "rule_threat_level": row[4],
            "behavior_threat_level": row[5],
            "ml_prediction": row[6],
            "anomaly_score": row[7],
            "ml_explanation": row[8],
            "correlation_level": correlation_level,
            "correlation_reason": correlation_reason
        })

    return jsonify(results), 200