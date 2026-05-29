from flask import Blueprint, jsonify

from database.queries import (
    get_logs_by_user,
    get_alerts_by_user
)


employees_bp = Blueprint("employees", __name__)


@employees_bp.route("/employees/<user_id>", methods=["GET"])
def fetch_employee_detail(user_id):

    logs = get_logs_by_user(user_id)
    alerts = get_alerts_by_user(user_id)

    formatted_logs = []

    for log in logs:
        formatted_logs.append({
            "id": log[0],
            "user_id": log[1],
            "timestamp": str(log[2]),
            "ip": log[3],
            "device": log[4],
            "event_type": log[5],
            "country": log[6],
            "browser": log[7],
            "os": log[8],
            "login_status": log[9]
        })

    formatted_alerts = []

    for alert in alerts:
        formatted_alerts.append({
            "id": alert[0],
            "user_id": alert[1],
            "threat_score": alert[2],
            "explanation": alert[3],
            "created_at": str(alert[4]),
            "threat_level": alert[5],
            "country": alert[6],
            "log_id": alert[7]
        })

    max_risk_score = 0

    if formatted_alerts:
        max_risk_score = max(
            alert["threat_score"] for alert in formatted_alerts
        )

    last_login = None

    if formatted_logs:
        last_login = formatted_logs[0]["timestamp"]

    return jsonify({
        "employee": {
            "user_id": user_id,
            "total_logs": len(formatted_logs),
            "total_alerts": len(formatted_alerts),
            "risk_score": max_risk_score,
            "last_login": last_login
        },
        "logs": formatted_logs,
        "alerts": formatted_alerts
    })