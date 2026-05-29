import random
import requests
from datetime import datetime, timedelta


API_URL = "http://127.0.0.1:5000/api/logs"


USERS = [
    "martin.hansen@dxc.com",
    "anna.jensen@dxc.com",
    "lasse.nielsen@dxc.com",
    "sofie.pedersen@dxc.com",
    "emil.andersen@dxc.com"
]


DEVICES = [
    ("Dell Latitude 7440", "known_device_1", "Laptop", "Windows 11", "Chrome"),
    ("Lenovo ThinkPad X1", "known_device_2", "Laptop", "Windows 11", "Edge"),
    ("MacBook Pro", "known_device_3", "Laptop", "macOS", "Safari"),
]


def generate_normal_timestamp():
    base_date = datetime.now()

    random_day = random.randint(0, 30)

    login_hour = random.randint(7, 18)

    login_minute = random.randint(0, 59)

    timestamp = base_date - timedelta(days=random_day)

    timestamp = timestamp.replace(
        hour=login_hour,
        minute=login_minute,
        second=random.randint(0, 59),
        microsecond=0
    )

    return timestamp.isoformat()


TOTAL_LOGS = 5000


print("\n===================================")
print(" GENERATING NORMAL TRAINING LOGS ")
print("===================================\n")


for i in range(TOTAL_LOGS):

    user = random.choice(USERS)

    device, device_id, device_type, os, browser = random.choice(DEVICES)

    payload = {
        "user_id": user,
        "event_type": "login_success",
        "login_status": "success",

        "timestamp": generate_normal_timestamp(),

        "ip": f"192.168.1.{random.randint(1, 255)}",
        "country": "Denmark",
        "city": "Copenhagen",

        "device": device,
        "device_id": device_id,
        "device_type": device_type,

        "browser": browser,
        "os": os,
        "user_agent": "Mozilla/5.0",

        "login_duration_ms": random.randint(800, 2500),

        "mfa_required": True,
        "mfa_success": True,
        "mfa_duration_ms": random.randint(1500, 5000),

        "failed_attempts_before_success": random.randint(0, 1),

        "session_id": f"normal_session_{i}",

        "session_duration_minutes": random.randint(20, 120)
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code in [200, 201]:

        print(
            f"[NORMAL LOG] "
            f"{i + 1}/{TOTAL_LOGS} | "
            f"{user} | "
            f"Login: {payload['login_duration_ms']} ms | "
            f"MFA: {payload['mfa_duration_ms']} ms"
        )

    else:

        print(f"[FAILED] {response.status_code}")


print("\n===================================")
print(" NORMAL TRAINING DATA COMPLETED ")
print("===================================\n")