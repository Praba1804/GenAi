import os
import streamlit as st

# Try to get API keys from Streamlit secrets first (for deployment)
# Fall back to environment variables (for local development)
def get_secret(key_name):
    try:
        # For Streamlit Cloud deployment
        return st.secrets[key_name]
    except:
        # For local development
        return os.getenv(key_name)

# API Keys and Configurations
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
DEEPGRAM_API_KEY = get_secret("DEEPGRAM_API_KEY")
SERPER_API_KEY = get_secret("SERPER_API_KEY")
# NEWS_API_KEY = os.getenv("NEWS_API_KEY")
CHROMADB_PATH = "./chroma_db/"

# Agent voice config (for TTS)
AGENT_VOICES = {
    "realist": "en-US-Wavenet-D",
    "optimist": "en-US-Wavenet-F",
    "expert": "en-US-Wavenet-B"
}