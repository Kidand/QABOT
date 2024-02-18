from flask import Flask, request, jsonify, render_template
import openai
import os

def chat_gpt_response(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # 选择模型
        # model="gpt-4", # GPT-4
        messages=[
            {"role": "system", "content": "你是Joseph Yan开发的人工智能助手."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        n=1,
        temperature=0.5,
    )

    return response.choices[0].message['content'].strip()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['input']
    response = chat_gpt_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
