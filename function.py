import requests
import openai
import os
from datetime import datetime
from dotenv import load_dotenv
import ollama

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    # response =  client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.7
    # )
    result= response['message']['content']
    return result
    # return response.choices[0].message.content.strip()

# import openai
# import os
# from datetime import datetime
# from dotenv import load_dotenv
# import ollama
# from openbb import obb

# load_dotenv()

# # OpenAI setup
# openai.api_key = os.getenv("OPENAI_API_KEY")
# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # -------------------- OpenBB Crypto Data -------------------- #
# def fetch_crypto_data(symbol="BTC", currency="USD"):
#     try:
#         # Fetch historical price data
#         crypto_data = obb.crypto.price.historical(
#             symbol=f"{symbol}{currency}",
#             provider="yfinance",
#             start_date=datetime.utcnow().date(),
#             end_date=datetime.utcnow().date(),
#             interval="1d"
#         ).to_df()

#         latest = crypto_data.iloc[-1]

#         return {
#             "coin": symbol,
#             "date": latest.name.date().isoformat(),
#             "price": latest["close"],
#             "market_cap": None,  # OpenBB may not provide this directly
#             "volume": latest["volume"],
#             "price_change_24h": ((latest["close"] - latest["open"]) / latest["open"]) * 100
#         }
#     except Exception as e:
#         print(f"[OpenBB Crypto Error] {e}")
#         return {
#             "coin": symbol,
#             "date": datetime.utcnow().date().isoformat(),
#             "price": None,
#             "market_cap": None,
#             "volume": None,
#             "price_change_24h": None
#         }

# # -------------------- OpenBB Financial Data -------------------- #
# def fetch_financial_data(ticker="AAPL"):
#     try:
#         # Fetch income statement data
#         fin_data = obb.equity.fundamental.income(ticker).to_df()
#         latest = fin_data.iloc[0]

#         return {
#             "revenue_usd": latest.get("TotalRevenue", 0),
#             "transactions": int(latest.get("NetIncome", 0) // 100),  # Simulated transactions
#             "spend_usd": latest.get("OperatingExpense", 0),
#             "conversion_rate": round((latest.get("NetIncome", 1) / latest.get("TotalRevenue", 1)) * 100, 2)
#         }
#     except Exception as e:
#         print(f"[OpenBB Financial Error] {e}")
#         return {
#             "revenue_usd": 0,
#             "transactions": 0,
#             "spend_usd": 0,
#             "conversion_rate": 0
#         }

# # -------------------- Simulated Engagement Data -------------------- #
# def fetch_engagement_data():
#     return {
#         "bounce_rate": 52.3,                     # %
#         "avg_session_duration": "00:03:45",      # HH:MM:SS
#         "new_users": 1300,
#         "returning_users": 850
#     }

# # -------------------- Insight Generator -------------------- #
# def generate_insight(data):
#     prompt = f"""
# You are a fintech analyst. Based on the following performance data for {data['date']}, provide a short summary and 3 actionable recommendations to improve performance.

# 📈 Crypto Data:
# - Coin: {data['coin']}
# - Price (USD): ${data['price']}
# - Volume: ${data['volume']}
# - 24h Change: {data['price_change_24h']}%

# 💰 Financials:
# - Revenue: ${data['revenue_usd']}
# - Transactions: {data['transactions']}
# - Spend: ${data['spend_usd']}
# - Conversion Rate: {data['conversion_rate']}%

# 📊 Engagement:
# - Bounce Rate: {data['bounce_rate']}%
# - Avg. Session Duration: {data['avg_session_duration']}
# - New Users: {data['new_users']}
# - Returning Users: {data['returning_users']}

# Summary:
# """
#     desire_model = 'deepseek-r1:latest'
#     response = ollama.chat(model=desire_model, messages=[{"role": "user", "content": prompt}])
#     return response['message']['content']

# # -------------------- Main Runner -------------------- #
# if __name__ == "__main__":
#     crypto_data = fetch_crypto_data("BTC", "USD")
#     financial_data = fetch_financial_data("AAPL")
#     engagement_data = fetch_engagement_data()

#     all_data = {
#         **crypto_data,
#         **financial_data,
#         **engagement_data
#     }

#     insights = generate_insight(all_data)
#     print("\n🧠 AI-Powered Insight:\n")
#     print(insights)
