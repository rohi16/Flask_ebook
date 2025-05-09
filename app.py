from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Securely get your OpenAI key from Render environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Welcome to the eBook Generator. Use /generate?topic=your_topic"

@app.route('/generate')
def generate_ebook():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({"error": "Missing 'topic' parameter in the URL"}), 400

    try:
        prompt = f"Write an engaging introduction for an eBook about {topic}. Keep it informative and useful."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        ebook_text = response.choices[0].message.content

        return jsonify({
            "topic": topic,
            "ebook_intro": ebook_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
