from flask import Flask, jsonify
from function import fetch_coingecko_data,generate_insight
from models import store_data,store_recommendation

app = Flask(__name__)

@app.route("/run-daily-job", methods=["GET"])
def run_daily_job():
    try:
         # Step 1: Fetch data from CoinGecko
        coin_list = ["bitcoin", "ethereum", "solana", "cardano", "ripple"]
        for coin in coin_list:
            data = fetch_coingecko_data(coin)
            if data:
                # Step 2: Store raw data in DB
                store_data(data)
            else:
                print(f"Skipping {coin}: Data fetch failed.")

        # Step 3: Process all records and generate AI insights
        insights= generate_insight(data)
        store_insights  = store_recommendation(insights)

        return jsonify({
            "status": "success",
            "message": "Job completed and insights generated.",
            "insights_generated":insights,
            "insertion_status":store_insights
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
