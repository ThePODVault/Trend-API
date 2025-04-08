from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import os

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

@app.route("/trend", methods=["GET"])
def get_trend():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Missing 'keyword' parameter"}), 400

    try:
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m')
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({"error": "No trend data found"}), 404

        trend_data = [
            {"date": date.strftime('%Y-%m-%d'), "interest": int(row[keyword])}
            for date, row in data.iterrows()
        ]

        return jsonify({"keyword": keyword, "trend": trend_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Railway-compatible dynamic port setup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Railway's assigned port
    print(f"🚀 Flask is running on port {port}")
    app.run(host="0.0.0.0", port=port)        # Make app accessible externally
