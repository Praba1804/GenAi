# Multi-Agent Voice Conversation System

A LangGraph-powered, multi-agent conversational AI system with voice (Deepgram), real-time web search (Serper, NewsAPI), and persistent vector memory (ChromaDB).

## Features

- Multiple AI agents (Realist, Optimist, Expert) with distinct personalities
- Agent-to-agent and agent-to-user handoff (no central orchestrator)
- Voice input/output (Deepgram STT/TTS)
- Real-time web search (Serper, NewsAPI)
- Persistent vector memory (ChromaDB)
- Sophisticated prompt engineering for agent personas

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
Web Search (Serper/NewsAPI) & Vector Memory (ChromaDB)
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

## Setup

1. `pip install -r requirements.txt` (or use Pipfile)
2. Set API keys in `config.py` for Deepgram, Serper, NewsAPI, and ChromaDB.
3. Run `python main.py` to start the system.

## System Flow

1. User speaks (voice input)
2. Deepgram STT transcribes to text
3. LangGraph routes conversation between agents and user
4. Agents use web search/memory as needed
5. Agent response is converted to speech (Deepgram TTS)
6. User hears reply and can respond

---

See `prompts/` for agent prompt engineering and `README.md` for full documentation.
