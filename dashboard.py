# dashboard.py - The office front desk
import brain
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("office.html")

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json() or {}
    text = (data.get("text") or "").lower()

    if any(w in text for w in ["price", "market", "crypto", "coin"]):
        reply = brain.market_verdict()
        details = brain.run_agent("market", "prices")
    elif any(w in text for w in ["news", "headline", "happening"]):
        reply = "Latest headlines:"
        details = brain.run_agent("news", "news")
    elif any(w in text for w in ["reddit", "buzz", "community", "hype"]):
        reply = "What the community is saying:"
        details = brain.run_agent("reddit", "buzz")
    elif any(w in text for w in ["help", "what can you do", "commands"]):
        reply = "Try: 'market update', 'latest news', 'reddit buzz', or 'are we safe'"
        details = []
    elif any(w in text for w in ["safe", "secure", "risk", "verdict"]):
        reply = brain.run_agent("security", "check")[0]
        details = []
    else:
        reply = "I heard you. Try: 'market update', 'latest news', 'reddit buzz', or 'help'"
        details = []

    return jsonify({"reply": reply, "details": details})

@app.route("/health")
def health():
    return "Office is open â"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
