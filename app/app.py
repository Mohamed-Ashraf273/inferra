from flask import Flask

# Create a Flask app instance
app = Flask(__name__)


# Define a route (homepage)
@app.route("/")
def home():
    return "Hello, Inferra!"


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
