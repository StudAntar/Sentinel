def generate_explanation(features):

    explanations = []

    # 🔴 Suspicious IP
    if features.get("suspicious_ip"):
        explanations.append("Login from suspicious IP")

    # 🔴 Unknown device
    if features.get("unknown_device"):
        explanations.append("Unknown device")

    # 🔴 Outside working hours
    if features.get("outside_working_hours"):
        explanations.append("Outside working hours")

    # 🔴 Foreign country
    if features.get("foreign_country"):
        explanations.append("Foreign country login")

    # 🔴 Tor browser
    if features.get("tor_browser"):
        explanations.append("Tor Browser detected")

    return explanations