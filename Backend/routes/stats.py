from flask import Blueprint, jsonify

from database.queries import get_stats

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/stats", methods=["GET"])
def fetch_stats():

    stats = get_stats()

    return jsonify(stats)