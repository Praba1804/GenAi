from typing import List, Dict

def format_history(history: List[Dict[str, str]]) -> str:
    """Formats conversation history for prompts."""
    return "\n".join([f"{turn['speaker'].capitalize()}: {turn['message']}" for turn in history])
