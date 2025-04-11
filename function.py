import requests
import openai
import os
from datetime import datetime
from dotenv import load_dotenv
import ollama

load_dotenv()

def fetch_coingecko_data(coin="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}"
    res = requests.get(url)
    data = res.json()
    market_data = data["market_data"]
    print(market_data)
    return {
        "coin": coin,
        "date": datetime.utcnow().date().isoformat(),
        "price": market_data["current_price"]["usd"],
        "market_cap": market_data["market_cap"]["usd"],
        "volume": market_data["total_volume"]["usd"],
        "price_change_24h": market_data["price_change_percentage_24h"]
    }

def generate_insight(data):
    prompt = f"""
You are a fintech analyst. Based on the following performance data for {data['date']}, provide a short summary and 3 actionable recommendations to improve performance.

Data:
- Coin: {data['coin']}
- Price (USD): ${data['price']}
- Market Cap (USD): ${data['market_cap']}
- Volume (USD): ${data['volume']}
- 24h Change: {data['price_change_24h']}%

Summary:
"""
    desire_model = 'deepseek-r1:latest'
    response = ollama.chat(model=desire_model, messages=[{"role": "user", "content": prompt}])
    result= response['message']['content']
    return result
