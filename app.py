from flask import Flask, jsonify
from real_time_data_fetcher import fetch_real_time_data

app = Flask(__name__)

@app.route('/api/treasury-data')
def get_treasury_data():
    data = fetch_real_time_data()
    if data:
        return jsonify(data)
    return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == "__main__":
    app.run(debug=True)