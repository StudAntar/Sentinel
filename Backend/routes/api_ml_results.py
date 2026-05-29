from flask import Blueprint, jsonify
from database.queries import get_ml_results


api_ml_results = Blueprint("api_ml_results", __name__)


@api_ml_results.route("/api/ml-results", methods=["GET"])
def ml_results():
    results = get_ml_results()

    formatted_results = []

    for row in results:
        formatted_results.append({
            "id": row[0],
            "log_id": row[1],
            "user_id": row[2],
            "anomaly_score": row[3],
            "prediction": row[4],
            "model_version": row[5],
            "explanation": row[6],
            "threat_level": row[7],
            "created_at": row[8]
})
    return jsonify(formatted_results), 200