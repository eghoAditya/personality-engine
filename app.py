import os
import json

import streamlit as st
from dotenv import load_dotenv

from core.llm_client import get_default_client, LLMMessage
from core.memory_extractor import extract_memories_from_messages
from core.assistant import generate_neutral_reply
from core.personality_engine import apply_personality_style

# Load environment variables from .env
load_dotenv()

st.set_page_config(page_title="Personality Engine")

# Lightweight styling for reply cards and main container
st.markdown(
    """
    <style>
        .reply-card {
            background-color: #2b2b2b;
            border-radius: 6px;
            border: 1px solid #444444;
            padding: 12px 14px;
            max-height: 260px;
            overflow-y: auto;
            font-size: 0.95rem;
            line-height: 1.4;
        }
        .reply-card.before {
            border-left: 4px solid #888888;
        }
        .reply-card.after {
            border-left: 4px solid #4B8BFF;
        }
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Personality presets used by the Personality Engine
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

st.title("Personality Engine")

groq_api_key = os.getenv("GROQ_API_KEY")

# if not groq_api_key:
#     st.warning("GROQ_API_KEY not found. Create a .env file and set GROQ_API_KEY to enable LLM features.")
# else:
#     st.success("GROQ_API_KEY detected. The app is ready to call the Groq API.")

st.write(
    """
This application demonstrates:

1. Extraction of long-term user memories from past messages:
   - User preferences
   - Emotional patterns
   - Facts worth remembering
2. Generation of a neutral, helpful reply to a new user query.
3. Transformation of that neutral reply into different personality styles:
   - Calm mentor
   - Witty friend
   - Therapist-style
"""
)

# Global Reset Button
if st.button("Reset All"):
    st.session_state.clear()
    st.rerun()

# Groq LLM Test
# st.divider()
# st.subheader("Groq LLM Test")

# test_prompt = st.text_area(
#     "Enter a test prompt to send to Groq:",
#     value="Say hello in one friendly sentence.",
#     height=80,
#     key="groq_test_prompt",
# )

# if st.button("Run Groq Test"):
#     if not groq_api_key:
#         st.error("GROQ_API_KEY is missing. Please set it in a .env file and restart the app.")
#     else:
#         try:
#             client = get_default_client()
#             response_text = client.chat(
#                 [LLMMessage(role="user", content=test_prompt)]
#             )
#             st.markdown("**LLM Response:**")
#             st.write(response_text)
#         except Exception as e:
#             st.error(f"Error while calling Groq: {e}")



# Memory Extraction Section
st.divider()
st.subheader("Memory Extraction from User Messages")

st.write(
    """
Paste the user's past chat messages below (ideally around 30 messages).
One message per line is sufficient. The system will extract:

- User preferences
- Emotional patterns
- Long-term facts worth remembering
"""
)

messages_input = st.text_area(
    "Paste past user messages here:",
    value=(
        "I get really anxious before interviews.\n"
        "Please explain things step-by-step, I hate when instructions skip steps.\n"
        "I'm preparing for a software engineering role.\n"
        "I live in India.\n"
        "I feel more confident when I have a clear plan."
    ),
    height=200,
    key="messages_input",
)

if "memories" not in st.session_state:
    st.session_state["memories"] = None

if st.button("Extract Memories"):
    if not groq_api_key:
        st.error("GROQ_API_KEY is missing. Please set it in a .env file and restart the app.")
    else:
        raw_lines = [
            line.strip() for line in messages_input.splitlines() if line.strip()
        ]
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

memories = st.session_state.get("memories")
if memories:
    st.subheader("Extracted Memories")

    user_preferences = memories.get("user_preferences", [])
    emotional_patterns = memories.get("emotional_patterns", [])
    facts = memories.get("facts", [])

    st.markdown("**User Preferences**")
    if user_preferences:
        for pref in user_preferences:
            importance = pref.get("importance", "").lower()
            highlight_importance = (
                "<span style='color: green; font-weight: 600;'>high</span>"
                if importance == "high"
                else importance
            )
            st.markdown(
                f"- **{pref.get('category', 'unknown').title()}**: "
                f"{pref.get('description', '')} "
                f"(importance: {highlight_importance})",
                unsafe_allow_html=True,
            )
    else:
        st.write("No user preferences extracted.")

    st.markdown("**Emotional Patterns**")
    if emotional_patterns:
        for emo in emotional_patterns:
            st.markdown(
                f"- Pattern: {emo.get('pattern', '')}\n"
                f"  - Triggers: {emo.get('typical_triggers', 'N/A')}\n"
                f"  - Reactions: {emo.get('typical_reactions', 'N/A')}"
            )
    else:
        st.write("No emotional patterns extracted.")

    st.markdown("**Facts Worth Remembering**")
    if facts:
        for fact in facts:
            stability = fact.get("stability", "").lower()
            highlight_stability = (
                "<span style='color: green; font-weight: 600;'>high</span>"
                if stability == "high"
                else stability
            )
            st.markdown(
                f"- **{fact.get('category', 'other').title()}**: "
                f"{fact.get('fact', '')} "
                f"(stability: {highlight_stability})",
                unsafe_allow_html=True,
            )
    else:
        st.write("No long-term facts extracted.")

    with st.expander("Raw memory JSON (for debugging)", expanded=False):
        st.json(memories)

    st.download_button(
        label="Download Memories JSON",
        data=json.dumps(memories, indent=2, ensure_ascii=False),
        file_name="extracted_memories.json",
        mime="application/json",
    )
else:
    st.info(
        "No memories extracted yet. Paste messages and click 'Extract Memories' to see results."
    )


# Neutral Assistant Reply (Base Response)
st.divider()
st.subheader("Neutral Assistant Reply")

st.write(
    """
Use this section to ask a new question or request.
The assistant will respond in a neutral and helpful tone,
optionally using the extracted memories for light personalization.
"""
)

if "neutral_reply" not in st.session_state:
    st.session_state["neutral_reply"] = ""

user_query = st.text_area(
    "Your new question or request:",
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
    st.markdown("**Neutral Reply**")
    st.write(st.session_state["neutral_reply"])
else:
    st.info(
        "No neutral reply generated yet. Enter a question and click 'Generate Neutral Reply'."
    )

# Personality Engine - Transform Neutral Reply
st.divider()
st.subheader("Personality Transformation")

st.write(
    """
This section rewrites the neutral reply into different personality styles
while keeping the core content and instructions the same.
"""
)

if "personality_reply" not in st.session_state:
    st.session_state["personality_reply"] = ""

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
                current_memories = st.session_state.get("memories") or {}
                base_reply = st.session_state.get("neutral_reply", "")
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

# Show Before / After side by side with divider and cards
if st.session_state.get("neutral_reply") and st.session_state.get("personality_reply"):

    col1, col_div, col2 = st.columns([1.3, 0.1, 1.3])

    with col1:
        st.markdown(
            "<h4 style='margin-bottom: 10px;'>Before: Neutral Reply</h4>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='reply-card before'>", unsafe_allow_html=True)
        st.markdown(st.session_state["neutral_reply"])
        st.markdown("</div>", unsafe_allow_html=True)

    with col_div:
        st.markdown(
            """
            <div style='
                width: 2px;
                background-color: #d0d0d0;
                height: 100%;
                margin: 0 auto;
            '></div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"<h4 style='margin-bottom: 10px;'>After: {personality_label} Style</h4>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='reply-card after'>", unsafe_allow_html=True)
        st.markdown(st.session_state["personality_reply"])
        st.markdown("</div>", unsafe_allow_html=True)

    # Horizontal separator under the comparison
    st.markdown(
        "<hr style='margin-top: 25px; margin-bottom: 15px;'>",
        unsafe_allow_html=True,
    )

    # Memory context / explainability below the comparison
    current_memories = st.session_state.get("memories") or {}
    if any(current_memories.values()):
        st.markdown("**Memory context considered:**")
        for category, items in current_memories.items():
            if isinstance(items, list):
                for item in items[:3]:
                    desc = (
                        item.get("description")
                        or item.get("fact")
                        or item.get("pattern")
                    )
                    if desc:
                        st.markdown(f"- {category}: {desc}")
    else:
        st.caption("No memory context was used.")
elif st.session_state.get("neutral_reply"):
    st.info(
        "Neutral reply is ready. Choose a personality and click "
        "'Transform Neutral Reply' to see the styled version."
    )
else:
    st.info("No neutral reply yet. Generate a neutral reply first above.")
