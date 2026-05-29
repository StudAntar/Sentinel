def generate_explanation(features):

    explanations = []

    if features.get("suspicious_ip"):
        explanations.append("Login from suspicious IP")

    if features.get("unknown_device"):
        explanations.append("Unknown device")

    if features.get("outside_working_hours"):
        explanations.append("Outside working hours")

    if features.get("foreign_country"):
        explanations.append("Foreign country login")

  
    if features.get("tor_browser"):
        explanations.append("Tor Browser detected")

    return explanations
