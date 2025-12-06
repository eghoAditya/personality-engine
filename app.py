import os
import streamlit as st
from dotenv import load_dotenv

# Load .env environment variables if available
load_dotenv()

st.set_page_config(page_title="Personality Engine", page_icon="🧠")

st.title("🧠 Personality Engine")
st.caption("Founding AI Engineer Assignment - Memory + Personality Demo")

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.warning("⚠️ GROQ_API_KEY not found. Create a .env file to enable LLM features.")
else:
    st.success("🔐 GROQ_API_KEY detected! Ready to integrate with Groq API.")

st.write("""
### What this app will do:

1. Take ~30 user messages as input
2. Extract:
   - User Preferences
   - Emotional Patterns
   - Long-term Facts to Remember
3. Generate a neutral reply using LLM
4. Transform reply into different personalities:
   - Calm mentor
   - Witty friend
   - Therapist-style

We'll build these features step-by-step 🚀
""")
