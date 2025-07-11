import streamlit as st
from bot_config.qa import ask
from streamlit_chat import message
from datetime import datetime
import time

st.set_page_config(
    page_title="Meoz - BI Assistant",
    layout="centered",
    page_icon="🐱"
)

# --- Custom CSS chuyên nghiệp ---
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }

    .chat-container {
        max-width: none;  
        width: 100%;   
        margin: 0;      
        padding: 0 2rem; 
    }

    .chat-bubble {
        border-radius: 15px;
        padding: 14px 18px;
        margin: 8px 0;
        font-size: 16px;
        max-width: 90%;
        line-height: 1.5;
        word-wrap: break-word;
    }

    .user-bubble {
        background: linear-gradient(to right, #d4fc79, #96e6a1);
        text-align: right;
        align-self: flex-end;
        color: #000;
    }

    .meoz-bubble {
        background: linear-gradient(to right, #a1c4fd, #c2e9fb);
        text-align: left;
        align-self: flex-start;
        color: #000;
    }

    .timestamp {
        font-size: 11px;
        color: #888;
        margin: 2px 0 4px 4px;
    }

    .avatar {
        font-size: 26px;
        margin-right: 8px;
        margin-top: -6px;
    }

    .title-header {
        font-size: 28px;
        text-align: center;
        font-weight: 600;
        margin-top: 10px;
        margin-bottom: 20px;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="title-header">🐱 Meoz - BI Assistant</div>', unsafe_allow_html=True)
st.caption("Assistant for BI Team – Borned from the love of data and cats 🐱")

# --- State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat Display ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    time_sent = msg["time"]
    avatar = "🧑‍💼" if role == "user" else "🤖"
    bubble_class = "user-bubble" if role == "user" else "meoz-bubble"
    align_style = "text-align: right;" if role == "user" else "text-align: left;"

    st.markdown(f"""
        <div style="{align_style}">
            <div class="timestamp">{avatar} {time_sent}</div>
            <div class="chat-bubble {bubble_class}">{content}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Chat Input ---
user_input = st.chat_input("Would you like to ask Meoz something ...")
if user_input:
    now = datetime.now().strftime("%H:%M")
    
    st.markdown(f"""
        <div style="text-align: right;">
            <div class="timestamp">🧑‍💼 {now}</div>
            <div class="chat-bubble user-bubble">{user_input}</div>
        </div>
    """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "user", "content": user_input, "time": now})


    with st.spinner("🤖 Meoz is thinking..."):
        full_reply = ask(user_input)
        reply_time = datetime.now().strftime("%H:%M")

        placeholder = st.empty()
        simulated = ""
        for char in full_reply:
            simulated += char
            placeholder.markdown(f"""
                <div style="text-align: left;">
                    <div class="timestamp">🤖 {reply_time}</div>
                    <div class="chat-bubble meoz-bubble">{simulated}▌</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.001)

        placeholder.markdown(f"""
            <div style="text-align: left;">
                <div class="timestamp">🤖 {reply_time}</div>
                <div class="chat-bubble meoz-bubble">{simulated}</div>
            </div>
        """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": full_reply, "time": reply_time})
