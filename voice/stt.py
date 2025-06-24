import sounddevice as sd
import numpy as np
import requests
import io
from config import DEEPGRAM_API_KEY

SAMPLE_RATE = 16000
CHANNELS = 1

# Record audio from the microphone

def record_audio(duration=5):
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
    sd.wait()
    return audio

# Send audio to Deepgram for transcription

def transcribe_audio(audio) -> str:
    wav_bytes = io.BytesIO()
    import soundfile as sf
    sf.write(wav_bytes, audio, SAMPLE_RATE, format='WAV')
    wav_bytes.seek(0)
    headers = {
        'Authorization': f'Token {DEEPGRAM_API_KEY}',
        'Content-Type': 'audio/wav'
    }
    response = requests.post(
        'https://api.deepgram.com/v1/listen',
        headers=headers,
        data=wav_bytes.read()
    )
    if response.status_code == 200:
        return response.json().get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('transcript', '')
    else:
        print("Deepgram STT error:", response.text)
        return ""

def stt_from_mic(duration=5):
    audio = record_audio(duration)
    return transcribe_audio(audio)
