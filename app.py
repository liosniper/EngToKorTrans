from flask import Flask, request, jsonify
import requests
import os
import re

app = Flask(__name__)

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")

def deepl_translate(text, source_lang="EN", target_lang="KO"):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    res = requests.post(url, data=params)
    if res.status_code == 200:
        return res.json()["translations"][0]["text"]
    return ""

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    text = data.get("text", "")
    # 영어만 번역, 그 외는 그대로
    if not text:
        return jsonify({"result": ""})
    if re.match(r'^[\x00-\x7F]+$', text):  # 영어면
        result = deepl_translate(text)
    else:
        result = text
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
