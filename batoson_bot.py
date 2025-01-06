import streamlit as st
import openai
from datetime import datetime

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# 初期設定
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": """あなたはグレゴリー・ベイトソンの教育モデルに基づいた教育コーチです。
            以下を行います：
            1. 感情状態を分析。
            2. 学習段階に応じた対話を提供。
            3. 内省を促進。"""
        }
    ]

# チャットボットの関数
def chat_with_bot(user_input):
    # ユーザーのメッセージを追加
    user_message = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state["messages"].append(user_message)

    # OpenAI API呼び出し
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=st.session_state["messages"]
        )
        bot_message = response["choices"][0]["message"]
        st.session_state["messages"].append(bot_message)
        return bot_message["content"]
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return "エラーが発生しました。"

# Streamlit UI
st.title("ベイトソン教育モデルコーチ - チャットボット")
st.write("あなたの感情や学習目標について話し合い、内省を促進します。")

# ユーザー入力
user_input = st.text_input("あなたのメッセージを入力してください:")

# チャットを進行
if st.button("送信") and user_input:
    bot_response = chat_with_bot(user_input)
    st.write("**コーチ:** " + bot_response)

# 会話履歴を表示
st.write("### 会話履歴")
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.write(f"**あなた:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.write(f"**コーチ:** {msg['content']}")
