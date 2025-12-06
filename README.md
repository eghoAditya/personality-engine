# Personality Engine

This project demonstrates a Memory Extraction + Personality Transformation system for a conversational AI.

## What it does

1. Takes ~30 user chat messages
2. Extracts:
   - User Preferences
   - Emotional Patterns
   - Long-term Facts
3. Generates a neutral AI reply
4. Rewrites it according to a selected personality style:
   - Calm mentor
   - Witty friend
   - Therapist-style

## Tech Used

- Python
- Streamlit
- Groq API (LLM)
- python-dotenv (environment variables)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
