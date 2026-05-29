from flask import Blueprint, request, jsonify

otp_bp = Blueprint("otp", __name__)


@otp_bp.route("/verify_otp", methods=["POST"])
def verify_otp():

    data = request.json

    user_id = data.get("user_id")
    otp = data.get("otp")

    if otp == "123456":

        return jsonify({
            "message": "OTP verified",
            "user_id": user_id
        })

    else:

        return jsonify({
            "message": "Invalid OTP"
        }), 401
