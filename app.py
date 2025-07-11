import streamlit as st
from bot_config.qa import ask
from streamlit_chat import message
from datetime import datetime
import time

st.set_page_config(
    page_title="Puppy - Professional Assistant for FBA Team",
    layout="centered",
    page_icon="🐶"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f7f9fc;
    }

    .chat-container {
        width: 100%;
        max-width: 800px;
        margin: auto;
        padding: 1rem;
    }

    .chat-bubble {
        border-radius: 18px;
        padding: 14px 20px;
        margin: 10px 0;
        font-size: 16px;
        max-width: 85%;
        line-height: 1.6;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    .user-bubble {
        background: linear-gradient(to right, #9be15d, #00e3ae);
        color: #000;
        align-self: flex-end;
        text-align: right;
        margin-left: auto;
    }

    .puppy-bubble {
        background: linear-gradient(to right, #a1c4fd, #c2e9fb);
        color: #000;
        align-self: flex-start;
        text-align: left;
        margin-right: auto;
    }

    .timestamp {
        font-size: 11px;
        color: #888;
        margin-bottom: 4px;
    }

    .avatar {
        font-size: 22px;
        vertical-align: middle;
        margin-right: 5px;
    }

    .title-header {
        font-size: 30px;
        text-align: center;
        font-weight: bold;
        color: #1e3d59;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        font-size: 14px;
        color: #666;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="title-header">Puppy - Your FBA Assistant 🐶</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Trained with data. Driven by curiosity. Here to help your FBA journey.</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Made by quocla from BI team.</div>', unsafe_allow_html=True)

# --- State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat Display ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    time_sent = msg["time"]
    avatar = "👤" if role == "user" else "🐶"
    bubble_class = "user-bubble" if role == "user" else "puppy-bubble"
    align_style = "text-align: right;" if role == "user" else "text-align: left;"

    st.markdown(f"""
        <div style="{align_style}">
            <div class="timestamp">{avatar} {time_sent}</div>
            <div class="chat-bubble {bubble_class}">{content}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Chat Input ---
user_input = st.chat_input("What would you like to ask Puppy?")
if user_input:
    now = datetime.now().strftime("%H:%M")

    # Add user message to state
    st.session_state.messages.append({
        "role": "user", "content": user_input, "time": now
    })

    # Display user message immediately
    st.markdown(f"""
        <div style="text-align: right;">
            <div class="timestamp">👤 {now}</div>
            <div class="chat-bubble user-bubble">{user_input}</div>
        </div>
    """, unsafe_allow_html=True)

    # Bot thinking
    with st.spinner("🐶 Puppy is thinking..."):
        full_reply = ask(user_input)
        reply_time = datetime.now().strftime("%H:%M")

        placeholder = st.empty()
        simulated = ""
        for char in full_reply:
            simulated += char
            placeholder.markdown(f"""
                <div style="text-align: left;">
                    <div class="timestamp">🐶 {reply_time}</div>
                    <div class="chat-bubble puppy-bubble">{simulated}▌</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.001)

        placeholder.markdown(f"""
            <div style="text-align: left;">
                <div class="timestamp">🐶 {reply_time}</div>
                <div class="chat-bubble puppy-bubble">{simulated}</div>
            </div>
        """, unsafe_allow_html=True)

    # Add assistant message to state
    st.session_state.messages.append({
        "role": "assistant", "content": full_reply, "time": reply_time
    })
