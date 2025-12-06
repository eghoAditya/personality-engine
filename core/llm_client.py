import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv
from groq import Groq

# Load environment variables (including GROQ_API_KEY)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@dataclass
class LLMMessage:
    role: str  # "system", "user", "assistant"
    content: str


class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key or GROQ_API_KEY
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in environment.")
        self.model = model
        self.client = Groq(api_key=self.api_key)

    def chat(self, messages: List[LLMMessage]) -> str:
        """
        Basic wrapper for Groq chat completion.
        For now, returns the assistant message content as plain text.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            temperature=0.3,
        )
        return response.choices[0].message.content


# We'll create a singleton-style helper later if needed
def get_default_client() -> LLMClient:
    return LLMClient()
