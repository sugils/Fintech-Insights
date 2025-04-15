📊 Fintech AI Insight Generator

-This project is an **AI-powered insight generator** for top cryptocurrencies like Bitcoin, Ethereum, Solana, Cardano, and Ripple. 
-It fetches market data from the CoinGecko API and generates meaningful insights using **Google's Gemini LLM**. 
-All data and insights are stored in a PostgreSQL database.

🚀 **Live Demo**: [Deployed App](https://fintech-insights-production.up.railway.app/run-daily-job)

---

## 💡 Features

- ✅ Fetches daily cryptocurrency metrics from CoinGecko API
- 🧠 Uses **Gemini (Google AI)** to generate actionable financial insights
- 🗃️ Stores raw market data and AI-generated recommendations in PostgreSQL
- 🔁 Can be triggered as a daily job with a simple GET request

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask  
- **AI Model**: Gemini (Google Generative AI API)  
- **Database**: PostgreSQL  
- **Deployment**: Railway  
- **Environment Management**: `python-dotenv`

---

## 📦 Project Structure

```
├── main.py              # Flask API with /run-daily-job endpoint
├── function.py          # Logic to fetch data & generate Gemini insights
├── models.py            # PostgreSQL data storage functions
├── .env                 # API keys & DB credentials
└── requirements.txt     # Python dependencies


🔧 How It Works
Trigger the Job
Hit the /run-daily-job endpoint to start the process.

Fetch Market Data
Crypto metrics (price, market cap, volume, etc.) are pulled from the CoinGecko API.

Generate Insight
Gemini LLM analyzes the data and returns a performance summary + recommendations.

Store in DB

Raw metrics → daily_metrics table

Insights → daily_recommendations table


🖥️ Run Locally

git clone https://github.com/sugils/Fintech-Insights.git
cd Fintech-Insights
pip install -r requirements.txt
python main.py


📈 Database Tables
daily_metrics: Stores raw price, volume, and market cap info.

daily_recommendations: Stores Gemini-generated financial summaries and suggestions.


🙌 Author
Sugil S
🔗 http://sugils.github.io/Sugil-Profile/
📞 8072078586