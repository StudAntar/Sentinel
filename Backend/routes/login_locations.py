from flask import Blueprint, jsonify
from database.db import get_connection

login_locations_bp = Blueprint("login_locations", __name__)

CITY_COORDINATES = {
    "Copenhagen": [55.6761, 12.5683],
    "Aarhus": [56.1629, 10.2039],
    "Berlin": [52.5200, 13.4050],
    "London": [51.5072, -0.1276],
    "Paris": [48.8566, 2.3522],
    "Madrid": [40.4168, -3.7038],
    "Rome": [41.9028, 12.4964],
    "Amsterdam": [52.3676, 4.9041],
    "Stockholm": [59.3293, 18.0686],
    "Oslo": [59.9139, 10.7522],
    "New York": [40.7128, -74.0060],
    "Dubai": [25.2048, 55.2708],
    "Tokyo": [35.6762, 139.6503],
    "Singapore": [1.3521, 103.8198],
    "Moscow": [55.7558, 37.6173]
}


@login_locations_bp.route("/api/login-locations", methods=["GET"])
def get_login_locations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT city, country, COUNT(*) as count
        FROM logs
        GROUP BY city, country
    """)

    rows = cursor.fetchall()
    results = []

    for city, country, count in rows:
        if city in CITY_COORDINATES:
            lat, lng = CITY_COORDINATES[city]

            results.append({
                "city": city,
                "country": country,
                "count": count,
                "lat": lat,
                "lng": lng
            })

    cursor.close()
    conn.close()

    return jsonify(results)