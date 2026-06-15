from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

AI_KEY = os.getenv("AI_KEY")  # Parent adds this in Render

@app.route("/requirements")
def get_requirements():
    badge = request.args.get("badge", "").strip()

    if not badge:
        return jsonify({"error": "No badge provided"}), 400

    # 1. Fetch official BSA merit badge page
    url = f"https://www.scouting.org/merit-badges/{badge.replace(' ', '-').lower()}/"
    page = requests.get(url)

    if page.status_code != 200:
        return jsonify({"requirements": ["Could not load official requirements."]})

    # 2. Send page text to AI to extract requirements
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
                    "content": "Extract the official merit badge requirements as a clean numbered list."
                },
                {
                    "role": "user",
                    "content": page.text
                }
            ]
        }
    )

    data = ai_response.json()

    # 3. Parse AI output into a list
    text = data["choices"][0]["message"]["content"]
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    return jsonify({"requirements": lines})
