from datetime import datetime


def safe_bool(value):
    return value is True or str(value).lower() == "true"


def extract_features(log):

    features = {}

    event_type = log.get("event_type", "unknown_event")
    country = log.get("country", "Unknown")
    device_id = log.get("device_id", "unknown_device")
    timestamp_value = log.get("timestamp")
    mfa_required = log.get("mfa_required", False)
    mfa_success = log.get("mfa_success", False)

    # Login failure
    features["login_failed"] = event_type == "login_failure"

    # MFA failure
    features["mfa_failed"] = event_type == "mfa_failure"

    # Successful login
    features["successful_login"] = event_type == "login_success"

    # Outside working hours
    try:
        timestamp = datetime.fromisoformat(str(timestamp_value))
        hour = timestamp.hour
        features["outside_working_hours"] = hour < 6 or hour > 22
    except Exception:
        features["outside_working_hours"] = False

    # Foreign country
    features["foreign_country"] = country != "Denmark"

    # Unknown device
    features["unknown_device"] = device_id == "unknown_device"

    # MFA required
    features["mfa_required"] = safe_bool(mfa_required)

    # MFA success
    features["mfa_success"] = safe_bool(mfa_success)

    # MFA failed by boolean logic
    features["mfa_failed"] = (
        features["mfa_failed"]
        or (
            features["mfa_required"] is True
            and features["mfa_success"] is False
        )
    )

    return features