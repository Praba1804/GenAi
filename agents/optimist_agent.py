from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent
from typing import Any, Dict
from utils.helpers import format_history
from search.serper_client import serper_search

class OptimistAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Optimist", persona="Positive, opportunity-focused, highlights best-case scenarios.")
        with open("prompts/optimist_prompt.txt", "r") as f:
            self.persona_prompt = f.read()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.8)

    def respond(self, state: Dict[str, Any]) -> str:
        history = format_history(state.get("history", []))
        user_input = state.get("user_input", "")
        
        # Check if web search is needed
        if self.needs_search(user_input, state):
            search_results = serper_search(user_input)
            
            # Format search results
            if search_results:
                search_summary = "\n".join([
                    f"- {r.get('title', 'No title')}: {r.get('snippet', 'No snippet')[:100]}..."
                    for r in search_results[:3]
                ])
                prompt = f"{self.persona_prompt}\n\nRecent Web Search Results:\n{search_summary}\n\nConversation History:\n{history}\n\nYour Response (incorporate the search results if relevant):"
            else:
                prompt = f"{self.persona_prompt}\n\nConversation History:\n{history}\n\nYour Response:"
        else:
            prompt = f"{self.persona_prompt}\n\nConversation History:\n{history}\n\nYour Response:"

        response = self.llm.invoke([
            SystemMessage(content=prompt)
        ])
        return response.content

    def handoff(self, context: Dict[str, Any]) -> str:
        # Placeholder: Decide next agent or user
        return "user"

    def needs_search(self, message: str, context: Dict[str, Any]) -> bool:
        keywords = ["benefit", "opportunity", "growth", "success", "positive", "increase", "improve", "2024"]
        return any(k in message.lower() for k in keywords)
