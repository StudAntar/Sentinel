import os
import joblib
import pandas as pd
from datetime import datetime


MODEL_VERSION = "isolation_forest_behavior_v2"
MODEL_PATH = "models/isolation_forest.pkl"


NORMAL_PROFILE = {
    "login_duration_ms": 1200,
    "mfa_duration_ms": 3200,
    "session_duration_minutes": 52,
    "failed_attempts_before_success": 0
}

def get_ml_threat_level(anomaly_score):
    if anomaly_score >= 70:
        return "HIGH"
    elif anomaly_score >= 30:
        return "MEDIUM"
    return "LOW"

def get_login_hour(log):
    timestamp = log.get("timestamp")

    if not timestamp:
        return datetime.now().hour

    try:
        return datetime.fromisoformat(timestamp).hour
    except ValueError:
        return datetime.now().hour


def prepare_single_log_features(log):
    login_hour = get_login_hour(log)

    return pd.DataFrame([{
        "login_hour": login_hour,
        "login_duration_ms": log.get("login_duration_ms", 0),
        "mfa_duration_ms": log.get("mfa_duration_ms", 0),
        "failed_attempts_before_success": log.get(
            "failed_attempts_before_success",
            0
        ),
        "session_duration_minutes": log.get(
            "session_duration_minutes",
            0
        ),
        "mfa_required": int(log.get("mfa_required", False)),
        "mfa_success": int(log.get("mfa_success", False))
    }])


def generate_ml_explanation(log, prediction):
    if prediction != "ANOMALY":
        return "Behavior appears consistent with the user's normal login pattern."

    explanations = []

    login_duration = log.get("login_duration_ms", 0)
    mfa_duration = log.get("mfa_duration_ms", 0)
    session_duration = log.get("session_duration_minutes", 0)
    failed_attempts = log.get("failed_attempts_before_success", 0)

    if login_duration > NORMAL_PROFILE["login_duration_ms"] * 3:
        explanations.append(
            f"Unusually long login duration: normal is around "
            f"{NORMAL_PROFILE['login_duration_ms']} ms, current was "
            f"{login_duration} ms."
        )

    if mfa_duration > NORMAL_PROFILE["mfa_duration_ms"] * 3:
        explanations.append(
            f"Unusually long MFA duration: normal is around "
            f"{NORMAL_PROFILE['mfa_duration_ms']} ms, current was "
            f"{mfa_duration} ms."
        )

    if session_duration > NORMAL_PROFILE["session_duration_minutes"] * 3:
        explanations.append(
            f"Unusually long session duration: normal is around "
            f"{NORMAL_PROFILE['session_duration_minutes']} minutes, current was "
            f"{session_duration} minutes."
        )

    if failed_attempts > NORMAL_PROFILE["failed_attempts_before_success"]:
        explanations.append(
            f"Failed login attempts before success: normal is around "
            f"{NORMAL_PROFILE['failed_attempts_before_success']}, current was "
            f"{failed_attempts}."
        )

    if not explanations:
        explanations.append(
            "The model detected an unusual combination of behavioral patterns "
            "compared to previous login activity."
        )

    return " ".join(explanations)


def run_ml_detection(log):
    if not os.path.exists(MODEL_PATH):
        return {
            "anomaly_score": 0,
            "prediction": "MODEL_NOT_FOUND",
            "model_version": MODEL_VERSION,
            "explanation": "ML model file was not found."
        }

    model = joblib.load(MODEL_PATH)

    features = prepare_single_log_features(log)

    prediction_raw = model.predict(features)[0]
    score_raw = model.decision_function(features)[0]

    if prediction_raw == -1:
        prediction = "ANOMALY"
    else:
        prediction = "NORMAL"

    anomaly_score = round((0.5 - score_raw) * 100, 2)

    if anomaly_score < 0:
        anomaly_score = 0

    if anomaly_score > 100:
        anomaly_score = 100

    explanation = generate_ml_explanation(log, prediction)
    print("\n========== ML RESULT ==========")
    print(f"User: {log['user_id']}")
    print(f"Prediction: {prediction}")
    print(f"Anomaly Score: {anomaly_score}")
    print(f"Threat Level: {get_ml_threat_level(anomaly_score)}")
    print(f"Explanation: {explanation}")
    print("================================\n")
    
    return {
        "anomaly_score": float(anomaly_score),
        "prediction": prediction,
        "model_version": MODEL_VERSION,
        "explanation": explanation,
        "threat_level": get_ml_threat_level(anomaly_score)
    }