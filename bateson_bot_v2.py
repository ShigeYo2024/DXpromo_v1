import streamlit as st
import openai
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt
import random

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# 初期設定
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """あなたはグレゴリー・ベイトソンの教育モデルに基づいた教育コーチです。以下を行います：\n1. 感情状態を分析。\n2. 学習段階に応じた対話を提供。\n3. 内省を促進。"""}
    ]
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# 感情分析関数（省略可）
def analyze_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.5:
        return "ポジティブ"
    elif polarity < -0.5:
        return "ネガティブ"
    else:
        return "ニュートラル"

# 学習進捗の更新関数（省略可）
def update_progress(stage):
    if "progress" not in st.session_state:
        st.session_state["progress"] = {"zero_learning": 0, "first_learning": 0, "second_learning": 0, "third_learning": 0}
    st.session_state["progress"][stage] += 1

# チャットボットとのやり取り
def communicate():
    messages = st.session_state["messages"]

    # ユーザーのメッセージを追加
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    # 感情分析結果を追加（オプション）
    emotion = analyze_emotion(st.session_state["user_input"])
    messages.append({"role": "assistant", "content": f"感情分析結果: {emotion}"})

    # OpenAI API呼び出し
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )
        bot_message = response["choices"][0]["message"]
        messages.append(bot_message)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

    # 入力欄をリセット
    st.session_state["user_input"] = ""

# Streamlit UI
st.title("AI Coach べいとそん: チャットボット")
st.write("あなたの感情や学習目標について話し合い、内省を促進します。")

# 入力欄（高さを3行に設定）
user_input = st.text_area("今の気持ちと学びたいことを教えてください:", 
                          key="user_input", 
                          height=100, 
                          on_change=communicate)

# チャット履歴の表示
if st.session_state["messages"]:
    messages = st.session_state["messages"]
    for message in reversed(messages[1:]):  # 最初のシステムメッセージはスキップ
        speaker = "🙂" if message["role"] == "user" else "🤖"
        st.write(f"{speaker}: {message['content']}")
