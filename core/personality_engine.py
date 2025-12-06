from typing import Dict, Any

from .llm_client import get_default_client, LLMMessage
from .prompts import PERSONALITY_TRANSFORM_SYSTEM_PROMPT


def apply_personality_style(
    base_reply: str,
    memories: Dict[str, Any],
    personality: str,
) -> str:
    """
    Given a base (neutral) reply, extracted memories, and a personality label,
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
            f"Personality style to use: {personality}\n\n"
            f"User memories (for context, optional to use):\n{memories_text}\n\n"
            f"Original assistant reply:\n{base_reply}\n\n"
            f"Rewrite the reply in the specified personality style while preserving "
            f"all instructions and factual content."
        ),
    )

    transformed = client.chat([system_msg, user_msg])
    return transformed


def json_safe_memories(memories: Dict[str, Any]) -> str:
    """
    Convert memories dict to a readable text block.
    We keep this simple for now.
    """
    try:
        import json
        return json.dumps(memories, indent=2, ensure_ascii=False)
    except Exception:
        return str(memories)
