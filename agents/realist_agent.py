from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent
from typing import Any, Dict
from utils.helpers import format_history
from search.serper_client import serper_search

class RealistAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Realist", persona="Practical, fact-driven, considers risks and constraints.")
        with open("prompts/realist_prompt.txt", "r") as f:
            self.persona_prompt = f.read()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    def respond(self, state: Dict[str, Any]) -> str:
        history = format_history(state.get("history", []))
        user_input = state.get("user_input", "")
        print(f"[Realist] User input: {user_input}")
        
        # Check if web search is needed
        if self.needs_search(user_input, state):
            print(f"[Realist] Web search triggered for: {user_input}")
            search_results = serper_search(user_input)
            print(f"[Realist] Found {len(search_results)} search results")
            
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
            print(f"[Realist] No web search needed")
            prompt = f"{self.persona_prompt}\n\nConversation History:\n{history}\n\nYour Response:"

        response = self.llm.invoke([
            SystemMessage(content=prompt)
        ])
        return response.content

    def handoff(self, context: Dict[str, Any]) -> str:
        # Placeholder: Decide next agent or user
        return "optimist"

    def needs_search(self, message: str, context: Dict[str, Any]) -> bool:
        keywords = ["current", "latest", "2024", "news", "market", "demand", "salary", "trend", "job", "cost", "tuition"]
        return any(k in message.lower() for k in keywords)
