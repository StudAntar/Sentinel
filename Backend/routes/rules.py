from flask import Blueprint, jsonify

rules_bp = Blueprint("rules", __name__)


@rules_bp.route("/api/rules", methods=["GET"])
def get_rules():

    rules = [
        {
            "rule_name": "LOGIN_FAILURE",
            "severity": "LOW",
            "score": 10,
            "description": "Login attempt failed."
        },
        {
            "rule_name": "MFA_FAILURE",
            "severity": "MEDIUM",
            "score": 25,
            "description": "Multi-factor authentication failed."
        },
        {
            "rule_name": "OUTSIDE_WORKING_HOURS",
            "severity": "LOW",
            "score": 20,
            "description": "Login attempt occurred outside normal working hours."
        },
        {
            "rule_name": "FOREIGN_COUNTRY",
            "severity": "HIGH",
            "score": 40,
            "description": "Login attempt came from a foreign country."
        },
        {
            "rule_name": "UNKNOWN_DEVICE",
            "severity": "MEDIUM",
            "score": 25,
            "description": "Login attempt came from an unknown device."
        },
        {
            "rule_name": "MULTIPLE_FAILED_ATTEMPTS",
            "severity": "MEDIUM",
            "score": 35,
            "description": "Multiple failed login attempts detected."
        },
        {
            "rule_name": "SUSPICIOUS_USER_AGENT",
            "severity": "MEDIUM",
            "score": 30,
            "description": "Suspicious user agent detected."
        },
        {
            "rule_name": "IMPOSSIBLE_TRAVEL",
            "severity": "HIGH",
            "score": 60,
            "description": "Impossible travel behavior detected."
        }
    ]

    return jsonify(rules)