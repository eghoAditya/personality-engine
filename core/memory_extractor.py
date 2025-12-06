from typing import List, Dict, Any
import json

from .llm_client import get_default_client, LLMMessage
from .prompts import MEMORY_EXTRACTION_SYSTEM_PROMPT


def extract_memories_from_messages(messages: List[str]) -> Dict[str, Any]:
    """
    Given a list of user messages (strings),
    call the LLM to extract:
      - user_preferences
      - emotional_patterns
      - facts
    and return a structured dict.
    (We'll implement the detailed prompt and parsing logic later.)
    """
    client = get_default_client()

    # Join messages into a single text block for now
    user_text = "\n".join(f"- {m}" for m in messages)

    system_msg = LLMMessage(role="system", content=MEMORY_EXTRACTION_SYSTEM_PROMPT)
    user_msg = LLMMessage(
        role="user",
        content=f"Here are the user's past messages:\n{user_text}\n\n"
                f"Extract memories as structured JSON.",
    )

    raw_response = client.chat([system_msg, user_msg])

    # We'll refine schema & validation later.
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError:
        # If it's not valid JSON, we just wrap raw text for now.
        data = {"raw_response": raw_response}

    return data
