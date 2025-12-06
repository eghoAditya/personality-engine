from typing import List, Dict, Any
import json

from .llm_client import get_default_client, LLMMessage
from .prompts import MEMORY_EXTRACTION_SYSTEM_PROMPT


def extract_memories_from_messages(messages: List[str]) -> Dict[str, Any]:
    """
    Given a list of user messages (strings), call the LLM to extract:
      - user_preferences
      - emotional_patterns
      - facts

    Returns a structured dict matching the schema described in MEMORY_EXTRACTION_SYSTEM_PROMPT.
    If the model output is not valid JSON, a fallback dict with raw text is returned.
    """
    client = get_default_client()

    if not messages:
        return {
            "user_preferences": [],
            "emotional_patterns": [],
            "facts": [],
            "warning": "No messages provided.",
        }

    numbered_messages_lines = []
    for idx, msg in enumerate(messages, start=1):
        numbered_messages_lines.append(f"{idx}. {msg}")
    messages_block = "\n".join(numbered_messages_lines)

    system_msg = LLMMessage(role="system", content=MEMORY_EXTRACTION_SYSTEM_PROMPT)
    user_msg = LLMMessage(
        role="user",
        content=(
            "You will receive a list of the user's past chat messages, in chronological order.\n"
            "Each message is numbered. Use the numbering when filling evidence_messages.\n\n"
            "USER MESSAGES:\n"
            f"{messages_block}\n\n"
            "Now extract memories according to the JSON schema. "
            "Respond with JSON only."
        ),
    )

    raw_response = client.chat([system_msg, user_msg])

    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError:
        try:
            first_brace = raw_response.index("{")
            last_brace = raw_response.rindex("}")
            json_str = raw_response[first_brace : last_brace + 1]
            parsed = json.loads(json_str)
        except Exception:
            parsed = {
                "user_preferences": [],
                "emotional_patterns": [],
                "facts": [],
                "raw_response": raw_response,
                "error": "Model did not return valid JSON.",
            }

    for key in ["user_preferences", "emotional_patterns", "facts"]:
        if key not in parsed or not isinstance(parsed[key], list):
            parsed[key] = []

    return parsed
