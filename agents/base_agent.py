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
        pass

    def needs_search(self, message: str, context: Dict[str, Any]) -> bool:
        """Decide if a web search is needed. Default: False."""
        return False

    def process_search_results(self, results: list, context: Dict[str, Any]) -> str:
        """Format search results for agent response. Default: return summary."""
        if not results:
            return "No relevant results found."
        return "\n".join([str(r) for r in results])
