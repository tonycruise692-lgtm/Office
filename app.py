@app.route("/command", methods=["POST"])
def command():
    try:
        text = request.json.get("text", "").strip()
        reply, details = brain.handle(text)
        return jsonify({"reply": reply, "details": details})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"reply": f"⚠️ ERROR: {repr(e)}"})
