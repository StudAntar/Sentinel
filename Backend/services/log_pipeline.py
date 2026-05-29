from datetime import datetime
from services.feature_engineering import extract_features
from services.rule_engine import run_rules
from database.queries import insert_log, insert_alert, insert_ml_result
from services.ml_engine import run_ml_detection


def normalize_log(log_data):
    normalized_log = dict(log_data)

    normalized_log["timestamp"] = datetime.now().isoformat()

    normalized_log["user_id"] = normalized_log.get("user_id", "unknown_user")
    normalized_log["event_type"] = normalized_log.get("event_type", "unknown_event")
    normalized_log["login_status"] = normalized_log.get("login_status", "unknown")

    normalized_log["ip"] = normalized_log.get("ip", "unknown_ip")
    normalized_log["country"] = normalized_log.get("country", "Unknown")
    normalized_log["city"] = normalized_log.get("city", "Unknown")

    normalized_log["device"] = normalized_log.get("device", "Unknown")
    normalized_log["device_id"] = normalized_log.get("device_id", "unknown_device")
    normalized_log["device_type"] = normalized_log.get("device_type", "Unknown")

    normalized_log["browser"] = normalized_log.get("browser", "Unknown")
    normalized_log["os"] = normalized_log.get("os", "Unknown")
    normalized_log["user_agent"] = normalized_log.get("user_agent", "Unknown")

    normalized_log["login_duration_ms"] = normalized_log.get("login_duration_ms", 0)
    normalized_log["mfa_required"] = normalized_log.get("mfa_required", False)
    normalized_log["mfa_success"] = normalized_log.get("mfa_success", False)
    normalized_log["mfa_duration_ms"] = normalized_log.get("mfa_duration_ms", 0)
    normalized_log["failed_attempts_before_success"] = normalized_log.get(
        "failed_attempts_before_success",
        0
    )

    normalized_log["session_id"] = normalized_log.get("session_id", "no_session")
    normalized_log["session_duration_minutes"] = normalized_log.get(
        "session_duration_minutes",
        0
    )

    return normalized_log


def correlate_risk(rule_level, behavior_level):
    rule_level = (rule_level or "LOW").upper()
    behavior_level = (behavior_level or "LOW").upper()

    if rule_level == "HIGH" and behavior_level == "HIGH":
        correlation_level = "CRITICAL"
        correlation_reason = (
            "Rules detected concrete high-risk security indicators, "
            "and the ML behavior model also detected high-risk abnormal behavior."
        )

    elif rule_level == "HIGH" and behavior_level == "MEDIUM":
        correlation_level = "HIGH"
        correlation_reason = (
            "Rules detected concrete high-risk security indicators, "
            "while the ML behavior model detected medium-risk abnormal behavior."
        )

    elif rule_level == "HIGH" and behavior_level == "LOW":
        correlation_level = "HIGH"
        correlation_reason = (
            "Rules detected concrete high-risk security indicators, "
            "but the ML behavior model did not detect strong behavioral deviation."
        )

    elif rule_level == "MEDIUM" and behavior_level == "HIGH":
        correlation_level = "HIGH"
        correlation_reason = (
            "Rules detected medium-risk indicators, while the ML behavior model "
            "detected high-risk abnormal behavior."
        )

    elif rule_level == "LOW" and behavior_level == "HIGH":
        correlation_level = "HIGH"
        correlation_reason = (
            "Rules did not detect strong concrete indicators, but the ML behavior "
            "model detected high-risk abnormal behavior."
        )

    elif rule_level == "MEDIUM" and behavior_level == "MEDIUM":
        correlation_level = "HIGH"
        correlation_reason = (
            "Both rules and the ML behavior model detected medium-risk signals, "
            "which strengthens the overall risk correlation."
        )

    elif rule_level == "MEDIUM" or behavior_level == "MEDIUM":
        correlation_level = "MEDIUM"
        correlation_reason = (
            "Either the rules engine or the ML behavior model detected "
            "medium-risk activity."
        )

    else:
        correlation_level = "LOW"
        correlation_reason = (
            "No strong correlation was found between rule-based indicators "
            "and behavioral anomaly detection."
        )

    return {
        "correlation_level": correlation_level,
        "correlation_reason": correlation_reason,
        "rule_threat_level": rule_level,
        "behavior_threat_level": behavior_level
    }


def process_log(log_data):
    normalized_log = normalize_log(log_data)

    log_id = insert_log(normalized_log)

    features = extract_features(normalized_log)

    rule_results = run_rules(normalized_log, features)

    ml_result = run_ml_detection(normalized_log)

    risk_correlation = correlate_risk(
        rule_level=rule_results["threat_level"],
        behavior_level=ml_result["threat_level"]
    )

    insert_ml_result(
        log_id=log_id,
        user_id=normalized_log["user_id"],
        anomaly_score=ml_result["anomaly_score"],
        prediction=ml_result["prediction"],
        model_version=ml_result["model_version"],
        explanation=ml_result["explanation"],
        threat_level=ml_result["threat_level"]
    )

    if rule_results["findings"]:
        for finding in rule_results["findings"]:
            insert_alert(
                log_id=log_id,
                user_id=normalized_log["user_id"],
                threat_score=finding["score"],
                explanation=finding["description"],
                threat_level=finding["severity"],
                country=normalized_log["country"],
                rule_name=finding["rule_name"],
                severity=finding["severity"]
            )

    return {
        "message": "Log processed successfully",
        "log_id": log_id,
        "event_type": normalized_log["event_type"],
        "user_id": normalized_log["user_id"],
        "features": features,
        "rule_results": rule_results,
        "ml_result": ml_result,
        "risk_correlation": risk_correlation
    }