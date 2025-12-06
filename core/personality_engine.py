from typing import Dict, Any
import json

from .llm_client import get_default_client, LLMMessage
from .prompts import PERSONALITY_TRANSFORM_SYSTEM_PROMPT


def json_safe_memories(memories: Dict[str, Any]) -> str:
    """
    Convert memories dict to a readable text block.
    """
    try:
        return json.dumps(memories, indent=2, ensure_ascii=False)
    except Exception:
        return str(memories)


def apply_personality_style(
    base_reply: str,
    memories: Dict[str, Any],
    personality: str,
) -> str:
    """
    Given a base (neutral) reply, extracted memories, and a personality label/description,
    ask the LLM to rewrite the reply in that style.
    """
    client = get_default_client()

    memories_text = json_safe_memories(memories)

    system_msg = LLMMessage(
        role="system",
        content=PERSONALITY_TRANSFORM_SYSTEM_PROMPT,
    )

    user_msg = LLMMessage(
        role="user",
        content=(
            f"Personality style to use:\n{personality}\n\n"
            f"User memories (for context, optional to use):\n{memories_text}\n\n"
            f"Original assistant reply:\n{base_reply}\n\n"
            "Rewrite the reply in the specified personality style while preserving "
            "all instructions and factual content."
        ),
    )

    transformed = client.chat([system_msg, user_msg])
    return transformed
