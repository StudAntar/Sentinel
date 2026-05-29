from flask import Flask
from flask_cors import CORS

from routes.upload import upload_bp
from routes.alerts import alerts_bp
from routes.logs import logs_bp
from routes.login import login_bp
from routes.otp import otp_bp
from routes.stats import stats_bp
from routes.health import health_bp
from routes.api_logs import api_logs_bp
from routes.employees import employees_bp
from routes.rules import rules_bp
from routes.analytics import analytics_bp
from routes.login_locations import login_locations_bp
from routes.api_ml_results import api_ml_results
from routes.api_risk_correlation import api_risk_correlation
from routes.api_incidents import api_incidents

app = Flask(__name__)
CORS(app)

app.register_blueprint(upload_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(login_bp)
app.register_blueprint(otp_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(health_bp)
app.register_blueprint(api_logs_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(rules_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(login_locations_bp)
app.register_blueprint(api_ml_results)
app.register_blueprint(api_risk_correlation)
app.register_blueprint(api_incidents)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)