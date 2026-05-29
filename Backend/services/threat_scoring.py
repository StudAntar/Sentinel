def calculate_threat_score(anomaly_score, features):

    threat_score = 0

    # 🔴 Suspicious IP
    if features.get("suspicious_ip"):
        threat_score += 40

    # 🔴 Unknown device
    if features.get("unknown_device"):
        threat_score += 20

    # 🔴 Outside working hours
    if features.get("outside_working_hours"):
        threat_score += 15

    # 🔴 Foreign country
    if features.get("foreign_country"):
        threat_score += 15

    # 🔴 Tor browser
    if features.get("tor_browser"):
        threat_score += 20

    # 🔴 ML anomaly score
    threat_score += int(anomaly_score * 10)

    # Max 100
    if threat_score > 100:
        threat_score = 100

    return threat_score