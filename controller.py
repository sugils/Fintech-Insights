from flask import Blueprint, jsonify
from function import fetch_coingecko_data, generate_insight
from models import store_data, store_recommendation, get_latest_data

insights_blueprint = Blueprint("insights", __name__)

@insights_blueprint.route("/run-daily-job", methods=["GET"])
def run_daily_job():
    # Step 1: Fetch
    data = fetch_coingecko_data("bitcoin")

    # Step 2: Store raw data
    store_data(data)

    # Step 3: Get latest from DB
    latest_data = get_latest_data()

    # Step 4: Send to LLM
    summary = generate_insight(latest_data)

    # Step 5: Store LLM output
    store_recommendation(summary)

    return jsonify({"status": "success", "summary": summary})
