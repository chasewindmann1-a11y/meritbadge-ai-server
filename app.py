from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

AI_KEY = os.getenv("AI_KEY")


@app.route("/requirements")
def get_requirements():
    badge = request.args.get("badge", "").strip()

    if not badge:
        return jsonify({"error": "No badge provided"}), 400

    # Use USScouts mirror (much more reliable)
    url = f"https://usscouts.org/mb/mb-{badge.replace(' ', '').lower()}.asp"

    try:
        page = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
    except Exception as e:
        return jsonify({"requirements": [f"Error fetching page: {str(e)}"]})

    if page.status_code != 200:
        return jsonify({"requirements": ["Could not load official requirements."]})

    # AI extraction
    try:
        ai_response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {AI_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "Extract the merit badge requirements as a clean numbered list."
                    },
                    {
                        "role": "user",
                        "content": page.text
                    }
                ]
            }
        )

        data = ai_response.json()
        text = data["choices"][0]["message"]["content"]
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        return jsonify({"requirements": lines})

    except Exception as e:
        return jsonify({"requirements": [f"AI error: {str(e)}"]})


@app.route("/")
def home():
    return "Merit Badge AI Server is running."
