import os
import streamlit as st
from dotenv import load_dotenv

from core.llm_client import get_default_client, LLMMessage
from core.memory_extractor import extract_memories_from_messages
from core.assistant import generate_neutral_reply
from core.personality_engine import apply_personality_style

load_dotenv()

PERSONALITY_PRESETS = {
    "Calm mentor": (
        "calm_mentor: You speak like a calm, experienced mentor. "
        "You are patient, structured, and encouraging. You avoid slang, "
        "and you gently reassure the user while giving practical advice."
    ),
    "Witty friend": (
        "witty_friend: You speak like a playful, witty friend. "
        "You can use light humor and mild sarcasm, but you are always kind "
        "and supportive. You keep things casual and fun, but still helpful."
    ),
    "Therapist-style": (
        "therapist_style: You speak like an empathetic therapist or counselor. "
        "You validate the user's emotions, reflect their feelings, and ask gentle, "
        "open-ended questions when appropriate. Your tone is soft, non-judgmental, "
        "and focused on emotional safety."
    ),
}


st.set_page_config(page_title="Personality Engine", page_icon="🧠")

st.title("🧠 Personality Engine")


groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.warning(" GROQ_API_KEY not found. Create a .env file to enable LLM features.")
else:
    st.success(" GROQ_API_KEY detected! Ready to talk to Groq API.")

st.write("""
### What this app will do:

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
""")

st.divider()
st.subheader(" Groq LLM Test")

test_prompt = st.text_area(
    "Enter a test prompt to send to Groq:",
    value="Say hello to me in one friendly sentence.",
    height=80,
    key="groq_test_prompt",
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


# Memory Extraction Section

st.divider()
st.subheader("🧠 Memory Extraction from User Messages")

st.write("""
Paste the user's past chat messages below (ideally around 30 messages).
One message per line is fine.
We'll extract:
- User preferences
- Emotional patterns
- Long-term facts
""")

messages_input = st.text_area(
    "Paste past user messages here:",
    value="I get really anxious before interviews.\n"
          "Please explain things step-by-step, I hate when instructions skip steps.\n"
          "I'm preparing for a software engineering role.\n"
          "I live in India.\n"
          "I feel more confident when I have a clear plan.",
    height=200,
    key="messages_input",
)

if "memories" not in st.session_state:
    st.session_state["memories"] = None

if st.button("Extract Memories"):
    if not groq_api_key:
        st.error("GROQ_API_KEY is missing. Please set it in a .env file and restart the app.")
    else:
       
        raw_lines = [line.strip() for line in messages_input.splitlines() if line.strip()]
        if not raw_lines:
            st.warning("Please paste at least one message before extracting memories.")
        else:
            with st.spinner("Analyzing messages and extracting memories..."):
                try:
                    memories = extract_memories_from_messages(raw_lines)
                    st.session_state["memories"] = memories
                except Exception as e:
                    st.error(f"Error while extracting memories: {e}")
                    st.session_state["memories"] = None

# Display extracted memories (if available)
memories = st.session_state.get("memories")
if memories:
    st.subheader(" Extracted Memories")

    user_preferences = memories.get("user_preferences", [])
    emotional_patterns = memories.get("emotional_patterns", [])
    facts = memories.get("facts", [])

    st.markdown("#### User Preferences")
    if user_preferences:
        for pref in user_preferences:
            st.markdown(f"- **{pref.get('category', 'unknown').title()}**: {pref.get('description', '')} "
                        f"(importance: `{pref.get('importance', 'unknown')}`)")
    else:
        st.write("_No user preferences extracted._")

    st.markdown("#### Emotional Patterns")
    if emotional_patterns:
        for emo in emotional_patterns:
            st.markdown(
                f"- **Pattern**: {emo.get('pattern', '')}\n"
                f"  - Triggers: {emo.get('typical_triggers', 'N/A')}\n"
                f"  - Reactions: {emo.get('typical_reactions', 'N/A')}"
            )
    else:
        st.write("_No emotional patterns extracted._")

    st.markdown("#### Facts Worth Remembering")
    if facts:
        for fact in facts:
            st.markdown(
                f"- **{fact.get('category', 'other').title()}**: {fact.get('fact', '')} "
                f"(stability: `{fact.get('stability', 'unknown')}`)"
            )
    else:
        st.write("_No long-term facts extracted._")

    with st.expander("🔍 Raw memory JSON (for debugging)", expanded=False):
        st.json(memories)
else:
    st.info("No memories extracted yet. Paste messages and click 'Extract Memories' to see results.")
    
# Neutral Assistant Reply (Base Response)

st.divider()
st.subheader(" Neutral Assistant Reply")

st.write("""
Use this section to ask a new question or request.
The assistant will:
- Use a neutral, helpful tone
- Optionally use the extracted memories (if available) for light personalization
""")

if "neutral_reply" not in st.session_state:
    st.session_state["neutral_reply"] = ""

user_query = st.text_area(
    "Your new question / request:",
    value="Can you help me plan how to prepare for my next interview?",
    height=100,
    key="user_query_input",
)

if st.button("Generate Neutral Reply"):
    if not groq_api_key:
        st.error("GROQ_API_KEY is missing. Please set it in a .env file and restart the app.")
    elif not user_query.strip():
        st.warning("Please enter a question or request.")
    else:
        with st.spinner("Generating neutral reply..."):
            try:
                current_memories = st.session_state.get("memories") or {}
                reply = generate_neutral_reply(user_query.strip(), current_memories)
                st.session_state["neutral_reply"] = reply
            except Exception as e:
                st.error(f"Error while generating neutral reply: {e}")
                st.session_state["neutral_reply"] = ""

if st.session_state.get("neutral_reply"):
    st.markdown("#### Neutral Reply")
    st.write(st.session_state["neutral_reply"])
else:
    st.info("No neutral reply generated yet. Enter a question and click 'Generate Neutral Reply'.")

# Personality Engine - Transform Neutral Reply
st.divider()
st.subheader("🎭 Personality Engine - Before / After")

st.write("""
Here we take the **neutral reply** and rewrite it in different personality styles
while keeping the core content and instructions the same.
""")

if "personality_reply" not in st.session_state:
    st.session_state["personality_reply"] = ""

# Let the user pick a personality
personality_label = st.selectbox(
    "Choose a personality style:",
    options=list(PERSONALITY_PRESETS.keys()),
    index=0,
)

if st.button("Transform Neutral Reply"):
    if not groq_api_key:
        st.error("GROQ_API_KEY is missing. Please set it in a .env file and restart the app.")
    elif not st.session_state.get("neutral_reply"):
        st.warning("Please generate a neutral reply first.")
    else:
        with st.spinner("Transforming reply into selected personality..."):
            try:
                # Get current memories and neutral reply
                current_memories = st.session_state.get("memories") or {}
                base_reply = st.session_state.get("neutral_reply", "")

                # Combine personality label and description into one string
                personality_instruction = PERSONALITY_PRESETS[personality_label]

                transformed = apply_personality_style(
                    base_reply=base_reply,
                    memories=current_memories,
                    personality=personality_instruction,
                )
                st.session_state["personality_reply"] = transformed
            except Exception as e:
                st.error(f"Error while transforming reply: {e}")
                st.session_state["personality_reply"] = ""

# Show Before / After
if st.session_state.get("neutral_reply") and st.session_state.get("personality_reply"):
    st.markdown("#### 📤 Before: Neutral Reply")
    st.write(st.session_state["neutral_reply"])

    st.markdown(f"#### 🎨 After: {personality_label} Style")
    st.write(st.session_state["personality_reply"])
elif st.session_state.get("neutral_reply"):
    st.info("Neutral reply is ready. Choose a personality and click 'Transform Neutral Reply' to see the styled version.")
else:
    st.info("No neutral reply yet. Generate a neutral reply first above.")


