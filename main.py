from flask import Flask
from controller import insights_blueprint

app = Flask(__name__)
app.register_blueprint(insights_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
