from flask import Blueprint, request, jsonify

from services.parser import parse_logs
from services.feature_engineering import extract_features
from services.threat_scoring import calculate_threat_score
from services.explanation import generate_explanation

from database.queries import insert_log, insert_alert

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload_logs", methods=["POST"])
def upload_logs():

    data = request.json

    parsed_logs = parse_logs(data)

    alerts = []

    for log in parsed_logs:

        insert_log(log)

        features = extract_features(log)

        anomaly_score = predict_anomaly(features)

        threat_score = calculate_threat_score(
            anomaly_score,
            features
        )

        explanation = generate_explanation(features)

        if threat_score >= 80:

            threat_level = "HIGH"

            insert_alert(
                log["user_id"],
                threat_score,
                ", ".join(explanation),
                threat_level,
                log["country"]
            )

            alerts.append({
                "user_id": log["user_id"],
                "threat_score": threat_score,
                "threat_level": threat_level,
                "country": log["country"],
                "explanation": explanation
            })

    return jsonify({
        "alerts": alerts
    })
