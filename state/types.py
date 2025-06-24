from typing import TypedDict, List, Dict, Any, Optional

class ConversationTurn(TypedDict):
    speaker: str  # 'user', 'realist', 'optimist', 'expert'
    message: str

class AgentState(TypedDict, total=False):
    history: List[ConversationTurn]
    current_agent: str  # 'realist', 'optimist', 'expert', or 'user'
    user_input: Optional[str]
    memory_context: Optional[List[str]]  # Retrieved memory chunks
