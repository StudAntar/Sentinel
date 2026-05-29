def parse_logs(raw_logs):

    parsed_logs = []

    for entry in raw_logs:

        parsed_log = {
            "user_id": entry.get("user_id"),
            "timestamp": entry.get("timestamp"),
            "ip": entry.get("ip"),
            "country": entry.get("country"),
            "device": entry.get("device"),
            "browser": entry.get("browser"),
            "os": entry.get("os"),
            "event_type": entry.get("event_type"),
            "login_status": entry.get("login_status")
        }

        parsed_logs.append(parsed_log)

    return parsed_logs