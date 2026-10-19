from flask import Flask, request, jsonify, send_file
import brain

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("office.html")

@app.route("/command", methods=["POST"])
def command():
    text = request.json.get("text", "").strip()
    reply, details = brain.handle(text)
    return jsonify({"reply": reply, "details": details})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
