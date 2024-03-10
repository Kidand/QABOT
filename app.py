from flask import Flask, request, jsonify, render_template, session
from flask_session import Session  # 新增导入
import openai
from openai import OpenAI
import os
import re

app = Flask(__name__)

# Flask Session配置
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

@app.route('/')
def index():
    # 清除旧的会话对话历史
    session.clear()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    print(user_message)

    # 从session获取当前对话历史
    if 'history' not in session:
        session['history'] = []
    history = session['history']

    history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=history  # 使用累积的对话历史
    )

    # 解析响应，获取回复内容，并更新对话历史
    bot_reply = response.choices[0].message.content if response.choices else "Sorry, I couldn't process that."
    print(bot_reply)
    # 将换行符转换为HTML的换行标签，并保留缩进
    bot_reply_html = bot_reply.replace("\n", "<br>")
    bot_reply_html = re.sub(r'(?<=<br>)(\s+)', lambda match: '&nbsp;' * len(match.group(1)), bot_reply_html)

    history.append({"role": "assistant", "content": bot_reply})

    # 保存更新后的历史到session
    session['history'] = history

    return jsonify({"reply": bot_reply_html})

if __name__ == '__main__':
    app.run(debug=True)
