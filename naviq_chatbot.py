import google.generativeai as genai
import streamlit as st
from datetime import datetime

# API Configuration
GOOGLE_API_KEY = "AIzaSyCym-9SzDNXVECOBqFy7hvCm6q4IalIZNo"
genai.configure(api_key=GOOGLE_API_KEY)

# Model Initialization
model = genai.GenerativeModel('gemini-1.5-flash')

def getResponseFromModel(user_input):
    if not isinstance(user_input, str) or not user_input.strip():
        raise ValueError("Prompt must be a non-empty string.")
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        st.error("❌ Failed to get response from Gemini API.")
        st.error(f"Details: {e}")
        return "Sorry, something went wrong. Please try again later."

# App config
st.set_page_config(page_title="NaviQ AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 NaviQ: Your Smart AI Interview Companion")
st.markdown("""
<style>
/* General layout */
body {
    background-color: #0E1117;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: #E0E0E0;
}

/* User bubble */
.user-bubble {
    background: linear-gradient(135deg, #00B4DB, #0083B0);
    color: #fff;
    padding: 14px 18px;
    border-radius: 16px 16px 4px 16px;
    margin-bottom: 10px;
    max-width: 80%;
    font-weight: 600;
    box-shadow: 0 0 10px rgba(0,180,219,0.4);
}

/* Bot bubble */
.bot-bubble {
    background: #1F2937;
    color: #D1D5DB;
    padding: 14px 18px;
    border-radius: 16px 16px 16px 4px;
    margin-bottom: 10px;
    max-width: 80%;
    margin-left: auto;
    font-weight: 500;
    box-shadow: 0 0 10px rgba(100,116,139,0.2);
}

/* Timestamp */
.timestamp {
    font-size: 12px;
    color: #94A3B8;
    text-align: right;
    margin-bottom: 12px;
    font-style: italic;
}

/* Button styling */
button {
    background-color: #2563EB;
    color: #fff;
    padding: 8px 14px;
    font-size: 13px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    margin-top: 8px;
    transition: background 0.3s ease;
}

button:hover {
    background-color: #1D4ED8;
}

/* Sidebar aesthetic (optional) */
.sidebar .css-1aumxhk {
    background-color: #1E293B;
    color: #CBD5E1;
}

/* Responsive for mobile */
@media screen and (max-width: 768px) {
    .user-bubble, .bot-bubble {
        max-width: 100%;
        font-size: 15px;
    }
}
</style>
""", unsafe_allow_html=True)



# Sidebar: Select mode
mode = st.sidebar.radio("\U0001F9E0 Choose Mode:", ["General Chat", "Coding Interview", "System Design"])
st.sidebar.info("✨ Enhance your skills with NaviQ")
st.sidebar.markdown("---")
st.sidebar.success("Built with Gemini Pro and Streamlit")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Feature Buttons for Interview Modes
if mode == "Coding Interview":
    if st.button("🎯 Generate a Coding Question"):
        question = getResponseFromModel("Give me a challenging coding interview question.")
        st.session_state["history"].append(("Coding Question", question, datetime.now()))
        st.rerun()

elif mode == "System Design":
    if st.button("🛠️ Generate a System Design Scenario"):
        prompt = getResponseFromModel("Give me a realistic system design interview question.")
        st.session_state["history"].append(("System Design Prompt", prompt, datetime.now()))
        st.rerun()

# Chat input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("\U0001F4AC Your Message / Answer:", max_chars=3000, placeholder="Type here...", height=150)
    submit_button = st.form_submit_button("Send")

    if submit_button:
        if user_input.strip():
            timestamp = datetime.now()
            if mode == "General Chat":
                response = getResponseFromModel(user_input)
            elif mode == "Coding Interview":
                prompt = f"You are a coding interviewer. Here's the candidate's answer:\n\n'{user_input}'\n\nPlease evaluate this with correctness, time/space complexity, and tips."
                response = getResponseFromModel(prompt)
            elif mode == "System Design":
                prompt = f"You are a system design interviewer. Here's the candidate's design:\n\n'{user_input}'\n\nEvaluate architecture, scalability, and trade-offs."
                response = getResponseFromModel(prompt)

            st.session_state["history"].append((user_input, response, timestamp))
            st.rerun()
        else:
            st.warning("⚠️ Please enter a valid message.")

# Clear chat
if st.session_state["history"]:
    if st.button("🧹 Clear Chat History"):
        st.session_state["history"] = []
        st.rerun()

# Display conversation
if st.session_state["history"]:
    for i, (user_msg, bot_msg, timestamp) in enumerate(st.session_state["history"]):
        st.markdown(f'<div class="user-bubble"><strong>You:</strong> {user_msg}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="timestamp">{timestamp.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="bot-bubble">
            <strong>NaviQ:</strong> {bot_msg}
        """, unsafe_allow_html=True)
