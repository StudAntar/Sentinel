from database.db import get_connection


# 🔹 GEM LOGS
def insert_log(log):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (
            user_id,
            timestamp,
            ip,
            country,
            city,
            device,
            device_id,
            device_type,
            browser,
            os,
            user_agent,
            event_type,
            login_status,
            login_duration_ms,
            mfa_required,
            mfa_success,
            mfa_duration_ms,
            failed_attempts_before_success,
            session_id,
            session_duration_minutes
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        RETURNING id
    """, (
        log["user_id"],
        log["timestamp"],
        log["ip"],
        log["country"],
        log["city"],
        log["device"],
        log["device_id"],
        log["device_type"],
        log["browser"],
        log["os"],
        log["user_agent"],
        log["event_type"],
        log["login_status"],
        log["login_duration_ms"],
        log["mfa_required"],
        log["mfa_success"],
        log["mfa_duration_ms"],
        log["failed_attempts_before_success"],
        log["session_id"],
        log["session_duration_minutes"]
    ))

    log_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return log_id


# 🔹 GEM ALERTS
def insert_alert(
    log_id,
    user_id,
    threat_score,
    explanation,
    threat_level,
    country,
    rule_name,
    severity
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (
            log_id,
            user_id,
            threat_score,
            explanation,
            threat_level,
            country,
            rule_name,
            severity
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        log_id,
        user_id,
        threat_score,
        explanation,
        threat_level,
        country,
        rule_name,
        severity
    ))

    conn.commit()
    cursor.close()
    conn.close()


# 🔹 HENT ALLE ALERTS
def get_alerts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM alerts
        ORDER BY created_at DESC
    """)

    alerts = cursor.fetchall()

    cursor.close()
    conn.close()

    return alerts


# 🔹 HENT ALLE LOGS
def get_logs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM logs
        ORDER BY timestamp DESC
    """)

    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return logs


# 🔹 STATS
def get_stats():

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
        SELECT COUNT(DISTINCT user_id)
        FROM logs
    """)
    total_users = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM alerts
    """)
    suspicious_users = cursor.fetchone()[0]

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

    stats = {
        "total_logs": total_logs,
        "total_alerts": total_alerts,
        "high_alerts": high_alerts,
        "avg_threat_score": avg_threat_score,
        "total_users": total_users,
        "suspicious_users": suspicious_users,
        "successful_logins": successful_logins,
        "failed_logins": failed_logins
    }

    cursor.close()
    conn.close()

    return stats


# 🔹 HENT LOGS FOR BRUGER
def get_logs_by_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM logs
        WHERE user_id = %s
        ORDER BY timestamp DESC
    """, (user_id,))

    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return logs


# 🔹 HENT ALERTS FOR BRUGER
def get_alerts_by_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM alerts
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    alerts = cursor.fetchall()

    cursor.close()
    conn.close()

    return alerts


# 🔹 HENT ÉN ALERT MED TILHØRENDE LOG
def get_alert_by_id(alert_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            alerts.id,
            alerts.user_id,
            alerts.threat_score,
            alerts.explanation,
            alerts.created_at,
            alerts.threat_level,
            alerts.country,
            alerts.log_id,
            alerts.rule_name,
            alerts.severity,

            logs.id,
            logs.timestamp,
            logs.ip,
            logs.device,
            logs.event_type,
            logs.login_status,
            logs.city,
            logs.device_id,
            logs.device_type,
            logs.browser,
            logs.os,
            logs.user_agent,
            logs.login_duration_ms,
            logs.mfa_required,
            logs.mfa_success,
            logs.mfa_duration_ms,
            logs.failed_attempts_before_success,
            logs.session_id,
            logs.session_duration_minutes

        FROM alerts
        LEFT JOIN logs ON alerts.log_id = logs.id
        WHERE alerts.id = %s
    """, (alert_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# 🔹 DELETE ALERT
def delete_alert(alert_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM alerts
        WHERE id = %s
    """, (alert_id,))

    conn.commit()

    cursor.close()
    conn.close()


# 🔹 DELETE LOG
def delete_log(log_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM logs
        WHERE id = %s
    """, (log_id,))

    conn.commit()

    cursor.close()
    conn.close()

    # 🔹 GEM ML RESULTAT
# 🔹 GEM ML RESULTAT
def insert_ml_result(
    log_id,
    user_id,
    anomaly_score,
    prediction,
    model_version,
    explanation,
    threat_level
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ml_results (
            log_id,
            user_id,
            anomaly_score,
            prediction,
            model_version,
            explanation,
            threat_level
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        log_id,
        user_id,
        float(anomaly_score),
        prediction,
        model_version,
        explanation,
        threat_level
    ))

    conn.commit()
    cursor.close()
    conn.close()

# 🔹 HENT ALLE ML RESULTATER
def get_ml_results():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            log_id,
            user_id,
            anomaly_score,
            prediction,
            model_version,
            explanation,
            threat_level,
            created_at
        FROM ml_results
        ORDER BY created_at DESC
    """)

    ml_results = cursor.fetchall()

    cursor.close()
    conn.close()

    return ml_results