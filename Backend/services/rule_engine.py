def calculate_threat_level(score):
    if score >= 70:
        return "HIGH"

    if score >= 30:
        return "MEDIUM"

    return "LOW"


def run_rules(log, features):
    findings = []
    rule_score = 0

    if features.get("login_failed"):
        findings.append({
            "rule_name": "LOGIN_FAILURE",
            "severity": "LOW",
            "score": 10,
            "description": "Login attempt failed."
        })
        rule_score += 10

    if features.get("mfa_failed"):
        findings.append({
            "rule_name": "MFA_FAILURE",
            "severity": "MEDIUM",
            "score": 25,
            "description": "Multi-factor authentication failed."
        })
        rule_score += 25

    if features.get("outside_working_hours"):
        findings.append({
            "rule_name": "OUTSIDE_WORKING_HOURS",
            "severity": "LOW",
            "score": 20,
            "description": "Login attempt occurred outside normal working hours."
        })
        rule_score += 20

    if features.get("foreign_country"):
        findings.append({
            "rule_name": "FOREIGN_COUNTRY",
            "severity": "HIGH",
            "score": 40,
            "description": "Login attempt came from a foreign country."
        })
        rule_score += 40

    if features.get("unknown_device"):
        findings.append({
            "rule_name": "UNKNOWN_DEVICE",
            "severity": "MEDIUM",
            "score": 25,
            "description": "Login attempt came from an unknown device."
        })
        rule_score += 25

    failed_attempts = log.get("failed_attempts_before_success", 0)

    if failed_attempts >= 5:
        findings.append({
            "rule_name": "MULTIPLE_FAILED_ATTEMPTS",
            "severity": "MEDIUM",
            "score": 35,
            "description": "Multiple failed login attempts detected."
        })
        rule_score += 35

    suspicious_agents = [
        "curl",
        "python",
        "bot",
        "scanner"
    ]

    user_agent = str(log.get("user_agent", "")).lower()

    if any(agent in user_agent for agent in suspicious_agents):
        findings.append({
            "rule_name": "SUSPICIOUS_USER_AGENT",
            "severity": "MEDIUM",
            "score": 30,
            "description": "Suspicious user agent detected."
        })
        rule_score += 30

    if features.get("impossible_travel"):
        findings.append({
            "rule_name": "IMPOSSIBLE_TRAVEL",
            "severity": "HIGH",
            "score": 60,
            "description": "Impossible travel behavior detected."
        })
        rule_score += 60

    rule_score = min(rule_score, 100)

    threat_level = calculate_threat_level(rule_score)

    return {
        "rule_score": rule_score,
        "threat_level": threat_level,
        "findings": findings
    }