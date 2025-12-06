from typing import Dict, Any
import json

from .llm_client import get_default_client, LLMMessage
from .prompts import NEUTRAL_ASSISTANT_SYSTEM_PROMPT


def generate_neutral_reply(user_query: str, memories: Dict[str, Any]) -> str:
    """
    Generate a neutral, helpful reply to the user's current query,
    optionally using extracted memories for personalization.
    """
    client = get_default_client()

    if memories:
        try:
            memories_text = json.dumps(memories, ensure_ascii=False, indent=2)
        except Exception:
            memories_text = str(memories)
    else:
        memories_text = "No long-term memories are available."

    system_msg = LLMMessage(
        role="system",
        content=NEUTRAL_ASSISTANT_SYSTEM_PROMPT,
    )

    user_msg = LLMMessage(
        role="user",
        content=(
            "Here is the user's long-term memory context (preferences, emotional patterns, facts):\n"
            f"{memories_text}\n\n"
            "Now the user is asking the following question or request:\n"
            f"{user_query}\n\n"
            "Respond in a neutral, clear, and practical way. "
            "You may lightly use the memory context to make the answer more tailored, "
            "but do not overdo the personalization."
        ),
    )

    reply = client.chat([system_msg, user_msg])
    return reply
