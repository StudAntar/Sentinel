from flask import Blueprint, jsonify
from database.db import get_connection

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/api/analytics", methods=["GET"])
def get_analytics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total_logs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts")
    total_alerts = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM alerts
        WHERE threat_level = 'HIGH'
    """)
    high_alerts = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(AVG(threat_score), 0)
        FROM alerts
    """)
    avg_threat_score = round(cursor.fetchone()[0])

    cursor.execute("""
        SELECT COUNT(*) FROM logs
        WHERE login_status = 'success'
    """)
    successful_logins = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM logs
        WHERE login_status = 'failed'
    """)
    failed_logins = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            rule_name,
            COUNT(*) as trigger_count
        FROM alerts
        GROUP BY rule_name
        ORDER BY trigger_count DESC
    """)

    rule_triggers = [
        {
            "rule_name": row[0],
            "trigger_count": row[1]
        }
        for row in cursor.fetchall()
    ]

    cursor.execute("""
        SELECT
            severity,
            COUNT(*) as count
        FROM alerts
        GROUP BY severity
    """)

    severity_distribution = [
        {
            "severity": row[0],
            "count": row[1]
        }
        for row in cursor.fetchall()
    ]

    cursor.execute("""
        SELECT
            threat_level,
            COUNT(*) as count
        FROM alerts
        GROUP BY threat_level
    """)

    threat_distribution = [
        {
            "threat_level": row[0],
            "count": row[1]
        }
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return jsonify({
        "total_logs": total_logs,
        "total_alerts": total_alerts,
        "high_alerts": high_alerts,
        "avg_threat_score": avg_threat_score,
        "successful_logins": successful_logins,
        "failed_logins": failed_logins,
        "rule_triggers": rule_triggers,
        "severity_distribution": severity_distribution,
        "threat_distribution": threat_distribution
    })
