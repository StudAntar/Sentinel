import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from database.db import get_connection


MODEL_PATH = "models/isolation_forest.pkl"


def fetch_training_logs():
    conn = get_connection()

    query = """
        SELECT
            timestamp,
            login_duration_ms,
            mfa_duration_ms,
            failed_attempts_before_success,
            session_duration_minutes,
            mfa_required,
            mfa_success
        FROM logs
        WHERE
            event_type = 'login_success'
            AND login_status = 'success'
            AND mfa_success = true
            AND failed_attempts_before_success <= 2
            AND login_duration_ms BETWEEN 500 AND 10000
            AND mfa_duration_ms BETWEEN 500 AND 15000
            AND session_duration_minutes BETWEEN 5 AND 180
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df


def prepare_features(df):
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["login_hour"] = df["timestamp"].dt.hour

    df["mfa_required"] = df["mfa_required"].astype(int)
    df["mfa_success"] = df["mfa_success"].astype(int)

    return df[
        [
            "login_hour",
            "login_duration_ms",
            "mfa_duration_ms",
            "failed_attempts_before_success",
            "session_duration_minutes",
            "mfa_required",
            "mfa_success"
        ]
    ]


def train_model():
    df = fetch_training_logs()

    if len(df) < 500:
        print("Not enough normal logs to train model.")
        print(f"Current normal training logs: {len(df)}")
        print("Recommended minimum: 500")
        print("Run: python -m services.generate_normal_logs")
        return

    features = prepare_features(df)

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("isolation_forest", IsolationForest(
            n_estimators=500,
            contamination=0.03,
            random_state=42
        ))
    ])

    model.fit(features)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("\n========== ML TRAINING COMPLETED ==========")
    print(f"Training rows used: {len(features)}")
    print(f"Model saved to: {MODEL_PATH}")
    print("Model type: Isolation Forest")
    print("Contamination: 0.03")
    print("Features used:")
    for column in features.columns:
        print(f"- {column}")

    print("\nTraining data summary:")
    print(features.describe())
    print("===========================================\n")


if __name__ == "__main__":
    train_model()