import requests
import sounddevice as sd
import numpy as np
import io
from config import DEEPGRAM_API_KEY, AGENT_VOICES

SAMPLE_RATE = 24000

# Synthesize speech using Deepgram TTS

def tts_to_audio(text: str, voice: str = "en-US-Wavenet-D"):
    url = "https://api.deepgram.com/v1/speak"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model": "aura-asteria-en",
        "voice": voice
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print("Deepgram TTS error:", response.text)
        return None

def play_audio(audio_bytes):
    import soundfile as sf
    audio, sr = sf.read(io.BytesIO(audio_bytes), dtype='float32')
    sd.play(audio, sr)
    sd.wait()

def speak(text: str, agent: str = "realist"):
    voice = AGENT_VOICES.get(agent, "en-US-Wavenet-D")
    audio_bytes = tts_to_audio(text, voice)
    if audio_bytes:
        play_audio(audio_bytes)
