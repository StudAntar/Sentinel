import random
import requests
from database.db import get_connection


API_URL = "http://127.0.0.1:5000/api/logs"


countries = [
    ("Denmark", "Copenhagen"),
    ("Sweden", "Stockholm"),
    ("Germany", "Berlin"),
    ("Netherlands", "Amsterdam"),
    ("United Kingdom", "London"),
    ("United States", "New York"),
    ("India", "Bangalore"),
    ("Brazil", "São Paulo"),
    ("Russia", "Moscow"),
    ("China", "Beijing"),
]


devices = [
    ("Dell Latitude 7440", "known_device", "Laptop", "Windows", "Chrome"),
    ("Lenovo ThinkPad X1", "known_device", "Laptop", "Windows", "Edge"),
    ("MacBook Pro", "known_device", "Laptop", "macOS", "Safari"),
    ("iPhone 15", "known_device", "Mobile", "iOS", "Safari"),
    ("Unknown Linux Device", "unknown_device", "Unknown", "Linux", "Unknown"),
]


def get_employee_emails():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM employees")
    employees = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return employees


def create_log(email):
    risk_type = random.choices(
        ["normal", "medium", "high"],
        weights=[70, 20, 10],
        k=1
    )[0]

    if risk_type == "normal":
        country, city = "Denmark", "Copenhagen"
        device, device_id, device_type, os, browser = random.choice(devices[:4])

        return {
            "user_id": email,
            "event_type": "login_success",
            "login_status": "success",
            "country": country,
            "city": city,
            "device": device,
            "device_id": device_id,
            "device_type": device_type,
            "browser": browser,
            "os": os,
            "login_duration_ms": random.randint(800, 2500),
            "mfa_required": True,
            "mfa_success": True,
            "mfa_duration_ms": random.randint(1500, 5000),
            "failed_attempts_before_success": 0,
            "session_duration_minutes": random.randint(20, 90)
        }

    if risk_type == "medium":
        country, city = random.choice(countries[1:6])
        device, device_id, device_type, os, browser = random.choice(devices)

        return {
            "user_id": email,
            "event_type": "login_success",
            "login_status": "success",
            "country": country,
            "city": city,
            "device": device,
            "device_id": device_id,
            "device_type": device_type,
            "browser": browser,
            "os": os,
            "login_duration_ms": random.randint(3000, 9000),
            "mfa_required": True,
            "mfa_success": True,
            "mfa_duration_ms": random.randint(5000, 12000),
            "failed_attempts_before_success": random.randint(1, 3),
            "session_duration_minutes": random.randint(60, 140)
        }

    country, city = random.choice(countries[6:])
    device, device_id, device_type, os, browser = random.choice(devices[-1:])

    return {
        "user_id": email,
        "event_type": random.choice(["login_success", "mfa_failure"]),
        "login_status": random.choice(["success", "failed"]),
        "country": country,
        "city": city,
        "device": device,
        "device_id": "unknown_device",
        "device_type": device_type,
        "browser": browser,
        "os": os,
        "login_duration_ms": random.randint(12000, 30000),
        "mfa_required": True,
        "mfa_success": False,
        "mfa_duration_ms": random.randint(15000, 35000),
        "failed_attempts_before_success": random.randint(4, 9),
        "session_duration_minutes": random.randint(120, 240)
    }


def seed_logs(amount=300):
    employees = get_employee_emails()

    if not employees:
        print("❌ No employees found. Seed employees first.")
        return

    print("\n==============================")
    print(" DXC AUTHENTICATION SIMULATOR ")
    print("==============================\n")

    for i in range(amount):

        email = random.choice(employees)
        log = create_log(email)

        response = requests.post(API_URL, json=log)

        if response.status_code not in [200, 201]:

            print(
                f"[FAILED] {log['event_type']} | "
                f"{email} | "
                f"{log['country']} | "
                f"{log['device_id']}"
            )

        else:

            print(
                f"[LOG GENERATED] "
                f"User: {email} | "
                f"Event: {log['event_type']} | "
                f"Country: {log['country']} | "
                f"Device: {log['device_id']} | "
                f"MFA: {log['mfa_success']}"
            )

    print("\n✅ Demo logs inserted successfully.")


if __name__ == "__main__":
    seed_logs(300)