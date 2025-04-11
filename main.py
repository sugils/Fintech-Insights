from flask import Flask, jsonify
from function import fetch_coingecko_data,generate_insight
from models import store_data

app = Flask(__name__)

@app.route("/run-daily-job", methods=["GET"])
def run_daily_job():
    try:
        coin_list = ["bitcoin", "ethereum", "solana", "cardano", "ripple"]
        failed_coins = []

        for coin in coin_list:
            data = fetch_coingecko_data(coin)
            if data:
                store_data(data)
            else:
                failed_coins.append(coin)
                print(f"Skipping {coin}: Data fetch failed.")


        # Step 1: Fetch data from CoinGecko
        data = fetch_coingecko_data("bitcoin")

        # Step 2: Store raw data in DB
        store_data(data)

        # Step 3: Process all records and generate AI insights
        insights= generate_insight(data)

        return jsonify({
            "status": "success",
            "message": "Job completed and insights generated.",
            "insights_generated":insights,
            "failed_coins": failed_coins
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
