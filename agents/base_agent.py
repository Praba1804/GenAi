from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """Abstract base class for all agents."""
    name: str
    persona: str

    def __init__(self, name: str, persona: str):
        self.name = name
        self.persona = persona

    @abstractmethod
    def respond(self, state: Dict[str, Any]) -> str:
        """
        Respond to the current conversation state.
        The state includes the full history. The agent should decide
        what to respond to based on the last turn.
        """
        pass

    def handoff(self, state):
        # Default: always return None (let router decide)
        return None
