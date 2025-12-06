# Personality Engine 

Founding AI Engineer assignment implementation: a **Memory Extraction + Personality Transformation** system for a conversational AI.

##  What this project does

Given a set of past user chat messages (e.g., ~30 messages), this app:

1. **Extracts long-term memories** from the messages:
   -  **User Preferences** (e.g., likes step-by-step instructions, hates skipped steps)
   -  **Emotional Patterns** (e.g., gets anxious before interviews, feels better with a clear plan)
   -  **Facts Worth Remembering** (e.g., lives in India, preparing for software engineering roles)

2. **Generates a neutral/base reply** to a new user query:
   - Uses a neutral, professional tone
   - Can lightly use the extracted memories to personalize the answer

3. **Transforms the neutral reply into different personalities**:
   -  **Calm mentor** – structured, reassuring, practical
   -  **Witty friend** – playful, lightly sarcastic but kind
   -  **Therapist-style** – empathetic, reflective, emotionally safe

4. **Shows Before/After responses**:
   - **Before:** Neutral reply
   - **After:** Same content, different tone (selected personality)

This demonstrates:
- Reasoning + prompt design
- Structured output parsing (JSON schema for memories)
- Working with user memory
- Modular system design

---

## Tech Stack

- **Python**
- **Streamlit** – UI + app runner
- **Groq API** – LLM backend (e.g., `llama-3.1-8b-instant`)
- **python-dotenv** – environment variable loading

---

## Local Setup

### 1. Clone / open the repo

Using GitHub Desktop or git:

```bash
git clone <your-repo-url>
cd personality-engine
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4.Configure environment variables

Copy the example file:
```bash
cp .env.example .env
```
Edit .env and set your real Groq API key.
```bash
GROQ_API_KEY=your_real_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### 5. Run the app
```bash
streamlit run app.py
```
Open the URL shown in terminal (usually http://localhost:8501)

## 🧪 How to Use the App

1️⃣ **Groq LLM Test**
- Use the top section to send a simple test prompt to Groq and confirm the LLM is working.

2️⃣ **Memory Extraction**
- Scroll to **“🧠 Memory Extraction from User Messages”**
- Paste ~30 of the user’s past messages (one per line is fine)
- Click **“Extract Memories”**
- The app will extract and display:
  - 🎯 User Preferences
  - 💭 Emotional Patterns
  - 🧾 Facts Worth Remembering
- Expand **Raw memory JSON** for the complete structured output.

3️⃣ **Neutral Assistant Reply**
- Scroll to **“💬 Neutral Assistant Reply”**
- Enter the user's new question
- Click **“Generate Neutral Reply”**
- The system uses the extracted memories (if available)
- Result: a clear, neutral, helpful answer

4️⃣ **Personality Engine – Before/After**
- Scroll to **“🎭 Personality Engine - Before / After”**
- Choose a personality:
  - Calm mentor 👨‍🏫
  - Witty friend 😄
  - Therapist-style 🧑‍⚕️
- Click **“Transform Neutral Reply”**
- The UI shows:
  - 📤 Before: Neutral Reply
  - 🎨 After: Personality-styled reply

> Same core meaning, different tone 🌀

---

## 🧩 Code Structure

personality engine/
├── app.py # Streamlit UI + orchestration
├── core/
│ ├── init.py
│ ├── llm_client.py # Groq API wrapper
│ ├── prompts.py # LLM prompt templates
│ ├── memory_extractor.py # Memory extraction + JSON parsing
│ ├── assistant.py # Neutral reply generation using memory
│ └── personality_engine.py # Personality transformation logic
├── .env.example
├── requirements.txt
└── README.md


- **llm_client.py**
  - Wrapper for Groq chat completion
  - Defaults to model: `llama-3.1-8b-instant`

- **memory_extractor.py**
  - Extracts:
    - `user_preferences`
    - `emotional_patterns`
    - `facts`
  - Ensures valid structured JSON

- **assistant.py**
  - Neutral, helpful replies using memory context

- **personality_engine.py**
  - Tone transformation → Calm mentor, Witty friend, Therapist-style

---

## 🌐 Deployment

You can deploy easily using **Streamlit Cloud**:

1. Push the repo to GitHub  
2. Go to: https://streamlit.io/cloud  
3. Click **New App** → select your repo  
4. Set:
   - Main file: `app.py`
5. Add **Secrets** (environment variables):
   - `GROQ_API_KEY=your_key_here`
   - (optional) `GROQ_MODEL=llama-3.1-8b-instant`
6. Deploy → copy the public URL for assignment submission 🚀