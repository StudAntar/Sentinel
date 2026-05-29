from flask import Blueprint, jsonify
from database.db import get_connection


api_incidents = Blueprint("api_incidents", __name__)


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


@api_incidents.route("/api/incidents/<int:log_id>", methods=["GET"])
def get_incident(log_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            timestamp,
            ip,
            country,
            city,
            device,
            device_id,
            device_type,
            browser,
            os,
            user_agent,
            event_type,
            login_status,
            login_duration_ms,
            mfa_required,
            mfa_success,
            mfa_duration_ms,
            failed_attempts_before_success,
            session_id,
            session_duration_minutes
        FROM logs
        WHERE id = %s
    """, (log_id,))

    log = cursor.fetchone()

    if not log:
        cursor.close()
        conn.close()
        return jsonify({"error": "Incident not found"}), 404

    cursor.execute("""
        SELECT
            id,
            threat_score,
            explanation,
            threat_level,
            rule_name,
            severity,
            created_at
        FROM alerts
        WHERE log_id = %s
        ORDER BY created_at DESC
    """, (log_id,))

    alerts = cursor.fetchall()

    cursor.execute("""
        SELECT
            id,
            anomaly_score,
            prediction,
            model_version,
            explanation,
            threat_level,
            created_at
        FROM ml_results
        WHERE log_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (log_id,))

    ml = cursor.fetchone()

    cursor.close()
    conn.close()

    rule_level = "LOW"

    alert_levels = [a[3] for a in alerts]

    if "HIGH" in alert_levels:
        rule_level = "HIGH"
    elif "MEDIUM" in alert_levels:
        rule_level = "MEDIUM"
    elif "LOW" in alert_levels:
        rule_level = "LOW"

    behavior_level = ml[5] if ml else "LOW"

    correlation_level, correlation_reason = correlate_risk(
        rule_level,
        behavior_level
    )

    incident = {
        "log": {
            "id": log[0],
            "user_id": log[1],
            "timestamp": log[2],
            "ip": log[3],
            "country": log[4],
            "city": log[5],
            "device": log[6],
            "device_id": log[7],
            "device_type": log[8],
            "browser": log[9],
            "os": log[10],
            "user_agent": log[11],
            "event_type": log[12],
            "login_status": log[13],
            "login_duration_ms": log[14],
            "mfa_required": log[15],
            "mfa_success": log[16],
            "mfa_duration_ms": log[17],
            "failed_attempts_before_success": log[18],
            "session_id": log[19],
            "session_duration_minutes": log[20]
        },
        "alerts": [
            {
                "id": a[0],
                "threat_score": a[1],
                "explanation": a[2],
                "threat_level": a[3],
                "rule_name": a[4],
                "severity": a[5],
                "created_at": a[6]
            }
            for a in alerts
        ],
        "ml_result": {
            "id": ml[0],
            "anomaly_score": ml[1],
            "prediction": ml[2],
            "model_version": ml[3],
            "explanation": ml[4],
            "threat_level": ml[5],
            "created_at": ml[6]
        } if ml else None,
        "risk_correlation": {
            "rule_threat_level": rule_level,
            "behavior_threat_level": behavior_level,
            "correlation_level": correlation_level,
            "correlation_reason": correlation_reason
        }
    }

    return jsonify(incident), 200