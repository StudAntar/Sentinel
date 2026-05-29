from flask import Blueprint, request, jsonify

from services.log_pipeline import process_log

api_logs_bp = Blueprint("api_logs", __name__)


@api_logs_bp.route("/api/logs", methods=["POST"])
def receive_log():

    log_data = request.json

    # Backend-controlled IP address
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    if client_ip and "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()

    log_data["ip"] = client_ip

    result = process_log(log_data)

    return jsonify(result)