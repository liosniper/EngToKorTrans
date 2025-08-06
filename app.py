from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

def smart_translate(text):
    system_prompt = (
        "너는 전문 번역가다. 사용자가 영어 문장을 입력하면 자연스러운 한국어로 번역된 결과만 출력해라. "
        "만약 입력이 영어가 아니라면, 아무런 변화 없이 원문을 그대로 출력해라. 불필요한 설명은 포함하지 마라."
    )
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        max_tokens=1000,
        temperature=0
    )
    return response.choices[0].message.content.strip()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    text = data.get("text", "")
    result = smart_translate(text)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
