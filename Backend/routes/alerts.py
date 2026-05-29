from flask import Blueprint, jsonify

from database.queries import (
    get_alerts,
    get_alerts_by_user,
    get_alert_by_id,
    delete_alert
)


alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/alerts", methods=["GET"])
def fetch_alerts():

    alerts = get_alerts()

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

    return jsonify({
        "alerts": formatted_alerts
    })


@alerts_bp.route("/alerts/user/<user_id>", methods=["GET"])
def fetch_user_alerts(user_id):

    alerts = get_alerts_by_user(user_id)

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

    return jsonify({
        "alerts": formatted_alerts
    })


@alerts_bp.route("/alerts/<int:alert_id>", methods=["GET"])
def fetch_alert_by_id(alert_id):

    result = get_alert_by_id(alert_id)

    if result is None:
        return jsonify({
            "error": "Alert not found"
        }), 404

    return jsonify({
        "alert": {
            "id": result[0],
            "user_id": result[1],
            "threat_score": result[2],
            "explanation": result[3],
            "created_at": str(result[4]),
            "threat_level": result[5],
            "country": result[6],
            "log_id": result[7]
        },
        "log": {
            "id": result[8],
            "timestamp": str(result[9]),
            "ip": result[10],
            "device": result[11],
            "event_type": result[12],
            "login_status": result[13],
            "city": result[14],
            "device_id": result[15],
            "device_type": result[16],
            "browser": result[17],
            "os": result[18],
            "user_agent": result[19],
            "login_duration_ms": result[20],
            "mfa_required": result[21],
            "mfa_success": result[22],
            "mfa_duration_ms": result[23],
            "failed_attempts_before_success": result[24],
            "session_id": result[25],
            "session_duration_minutes": result[26]
        }
    })


@alerts_bp.route("/alerts/<int:alert_id>", methods=["DELETE"])
def remove_alert(alert_id):

    delete_alert(alert_id)

    return jsonify({
        "message": "Alert deleted successfully"
    })