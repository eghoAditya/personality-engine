import os
import streamlit as st
from dotenv import load_dotenv

from core.llm_client import get_default_client, LLMMessage

# Load environment variables from .env
load_dotenv()

st.set_page_config(page_title="Personality Engine", page_icon="🧠")

st.title("🧠 Personality Engine")
st.caption("Founding AI Engineer Assignment - Memory + Personality Demo")

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.warning("⚠️ GROQ_API_KEY not found. Create a .env file to enable LLM features.")
else:
    st.success("🔐 GROQ_API_KEY detected! Ready to talk to Groq API.")

st.write("""
### What this app will do (soon):

1. Take ~30 user messages as input
2. Extract:
   - User Preferences
   - Emotional Patterns
   - Long-term Facts to Remember
3. Generate a neutral reply using an LLM
4. Transform the reply into different personalities:
   - Calm mentor
   - Witty friend
   - Therapist-style

We're still wiring things up step-by-step 🚀
""")

st.divider()
st.subheader("🔎 Groq LLM Test")

test_prompt = st.text_area(
    "Enter a test prompt to send to Groq:",
    value="Say hello to me in one friendly sentence.",
    height=100,
)

if st.button("Run Groq test"):
    if not groq_api_key:
        st.error("GROQ_API_KEY is missing. Please set it in a .env file and restart the app.")
    else:
        try:
            client = get_default_client()
            response_text = client.chat([
                LLMMessage(role="user", content=test_prompt)
            ])
            st.markdown("**LLM Response:**")
            st.write(response_text)
        except Exception as e:
            st.error(f"Error while calling Groq: {e}")
