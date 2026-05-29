from flask import Blueprint, jsonify

from database.queries import (
    get_logs,
    get_logs_by_user,
    delete_log
)
logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/logs", methods=["GET"])
def fetch_logs():

    logs = get_logs()

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

    return jsonify({
        "logs": formatted_logs
    })
@logs_bp.route("/logs/<user_id>", methods=["GET"])
def fetch_user_logs(user_id):

    logs = get_logs_by_user(user_id)

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

    return jsonify({
        "logs": formatted_logs
    })
@logs_bp.route("/logs/<int:log_id>", methods=["DELETE"])
def remove_log(log_id):

    delete_log(log_id)

    return jsonify({
        "message": "Log deleted successfully"
    })