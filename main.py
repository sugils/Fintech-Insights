import os
from flask import Flask
from controller import insights_blueprint

app = Flask(__name__)
app.register_blueprint(insights_blueprint)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the dynamic port from Railway
    app.run(debug=False, host="0.0.0.0", port=port)  # Bind to all interfaces
