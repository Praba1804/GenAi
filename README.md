# Multi-Agent Voice Conversation System

A LangGraph-powered, multi-agent conversational AI system with voice (Deepgram), real-time web search (Serper), and persistent vector memory (FAISS).

## Features

- Multiple AI agents (Realist, Optimist, Expert) with distinct personalities
- Agent-to-agent and agent-to-user handoff (no central orchestrator)
- Voice input/output (Deepgram STT/TTS)
- Real-time web search (Serper)
- Persistent vector memory (FAISS)
- Sophisticated prompt engineering for agent personas
- Beautiful Streamlit UI with chat bubbles and loading animations

## Live Demo

🚀 **Try it live:** [Your Streamlit Cloud URL will be here]

## Architecture

```
User Voice Input
   │
   ▼
Speech-to-Text (Deepgram)
   │
   ▼
LangGraph Multi-Agent System
   │      │      │
   ▼      ▼      ▼
Realist  Optimist  Expert
   │      │      │
   └──────┴──────┘
         │
         ▼
Web Search (Serper) & Vector Memory (FAISS)
         │
         ▼
Text-to-Speech (Deepgram)
         │
         ▼
   Voice Output
```

## Agent Personas

- **Realist Agent**: Practical, fact-driven, always considers risks and constraints.
- **Optimist Agent**: Positive, opportunity-focused, highlights best-case scenarios.
- **Expert Agent**: Deep subject-matter knowledge, provides technical or nuanced insights.

## Local Setup

1. `pip install -r requirements.txt`
2. Set environment variables for API keys:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export DEEPGRAM_API_KEY="your-deepgram-api-key"
   export SERPER_API_KEY="your-serper-api-key"
   ```
3. Run `streamlit run app.py` to start the system.

## Deployment

This app is deployed on Streamlit Cloud with the following configuration:

### Required API Keys (set in Streamlit Cloud secrets):

- `OPENAI_API_KEY`: For LLM and embeddings
- `DEEPGRAM_API_KEY`: For speech-to-text and text-to-speech
- `SERPER_API_KEY`: For real-time web search

### How to Deploy:

1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Set the secrets in Streamlit Cloud dashboard
4. Deploy!

## System Flow

1. User speaks (voice input) or types
2. Deepgram STT transcribes to text (if voice)
3. LangGraph routes conversation between agents and user
4. Agents use web search/memory as needed
5. Agent response is converted to speech (Deepgram TTS)
6. User hears reply and can respond

## Example Conversations

- Career decisions: "Should I do an internship or focus on my final year project?"
- Study abroad: "I'm thinking about studying abroad for my master's degree"
- Technology learning: "Should I learn React or Angular for web development?"

---

Built with ❤️ using LangGraph, Streamlit, and OpenAI
