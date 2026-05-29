def calculate_threat_score(anomaly_score, features):

    threat_score = 0

    if features.get("suspicious_ip"):
        threat_score += 40

    if features.get("unknown_device"):
        threat_score += 20

    if features.get("outside_working_hours"):
        threat_score += 15

    if features.get("foreign_country"):
        threat_score += 15

    if features.get("tor_browser"):
        threat_score += 20

    threat_score += int(anomaly_score * 10)

    if threat_score > 100:
        threat_score = 100

    return threat_score
