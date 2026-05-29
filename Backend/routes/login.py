from flask import Blueprint, request, jsonify
import re

from database.queries import insert_log, insert_alert

login_bp = Blueprint("login", __name__)

USERS = {
    "martin.hansen@dxc.com": "K9!vR2pQx7Lz",
    "anna.jensen@dxc.com": "T4#nW8sLp2Qa",
    "lasse.nielsen@dxc.com": "M7@qZ3rTx9Vb",
    "sofie.pedersen@dxc.com": "R2%kL8mNp5Yc",
    "emil.andersen@dxc.com": "P6&xD1vHs8Qr"
}


@login_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    user_id = data.get("user_id", "")
    password = data.get("password", "")

    user_id_regex = r"^[a-zA-Z0-9._%+-]+@dxc\.com$"
    password_regex = r"^(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z0-9!@#$%^&*]{8,}$"

    if not re.match(user_id_regex, user_id):
        return jsonify({
            "message": "Invalid user_id format. User ID must be a valid DXC email."
        }), 400

    if not re.match(password_regex, password):
        return jsonify({
            "message": "Password must contain at least 8 characters, one number and one special character."
        }), 400

    if user_id in USERS and password == USERS[user_id]:

        log = {
            "user_id": user_id,
            "timestamp": "2026-05-12 13:00:00",
            "ip": "192.168.1.50",
            "country": "Denmark",
            "device": "known_device",
            "browser": "Chrome",
            "os": "Windows",
            "event_type": "login_success",
            "login_status": "success"
        }

        insert_log(log)

        return jsonify({
            "message": "Login successful",
            "user_id": user_id
        })

    explanation = [
        "Wrong password detected",
        "User credentials did not match stored credentials",
        "Possible unauthorized login attempt"
    ]

    insert_alert(
        user_id,
        100,
        ", ".join(explanation),
        "HIGH",
        "Unknown"
    )

    return jsonify({
        "message": "Invalid credentials"
    }), 401