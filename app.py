from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"result": ""})

    # 영어면 한국어로 번역, 아니면 원문 그대로
    src_lang = translator.detect(text).lang
    if src_lang == "en":
        result = translator.translate(text, src='en', dest='ko').text
    else:
        result = text

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
