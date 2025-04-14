import requests
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv
import time

# Step 0: Load environment variables
print("Loading environment variables...")
load_dotenv()

# Step 1: Configure Gemini API key
print(" Configuring Gemini API...")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Step 2: Fetch crypto data from Coingecko
def fetch_coingecko_data(coin):
    print(f"\n Fetching data for coin: {coin}...")
    time.sleep(1) 

    url = f"https://api.coingecko.com/api/v3/coins/{coin.lower()}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        market_data = data.get("market_data")
        if not market_data:
            print(f"Error: Market data not found for coin: {coin}")
            return None

        print("✅ Data fetched successfully.")
        return {
            "coin": coin,
            "date": datetime.utcnow().date().isoformat(),
            "price": market_data["current_price"]["usd"],
            "market_cap": market_data["market_cap"]["usd"],
            "volume": market_data["total_volume"]["usd"],
            "price_change_24h": market_data["price_change_percentage_24h"]
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error for {coin}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request error for {coin}: {req_err}")
    except KeyError as ke:
        print(f"❌ Missing key in response data for {coin}: {ke}")
    except Exception as e:
        print(f"❌ Unexpected error for {coin}: {e}")
    
    return None


# Step 3: Generate insights using Gemini
def generate_insight(data):
    print(f"\n Generating insights for {data['coin']} on {data['date']}...")
    
    prompt = f"""
You are a fintech analyst. Based on the following performance data for {data['date']}, provide a more detailed output that includes:

- A short summary of the coin's performance.
- 3 actionable recommendations to improve performance.
- A breakdown of key financial indicators.

Data:
- Coin: {data['coin']}
- Price (USD): ${data['price']}
- Market Cap (USD): ${data['market_cap']}
- Volume (USD): ${data['volume']}
- 24h Change: {data['price_change_24h']}%

Be specific, use a professional tone, and return the response as a paragraph with clearly numbered recommendations.
"""
    
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)

        print("✅ Insight generated successfully.")
        return response.text
    
    except Exception as e:
        print(f"❌ Error generating insight: {e}")
        return "Error generating insight."

