from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent
from typing import Any, Dict
from utils.helpers import format_history
from search.serper_client import serper_search

class ExpertAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Expert", persona="Deep subject-matter knowledge, provides technical or nuanced insights.")
        with open("prompts/expert_prompt.txt", "r") as f:
            self.persona_prompt = f.read()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.6)

    def respond(self, state: Dict[str, Any]) -> str:
        history = format_history(state.get("history", []))
        user_input = state.get("user_input", "")
        print(f"[Expert] User input: {user_input}")
        # Add instruction for a single, concise paragraph
        prompt = f"{self.persona_prompt}\n\nPlease respond in a single, concise paragraph.\n"
        # Check if web search is needed
        if self.needs_search(user_input, state):
            print(f"[Expert] Web search triggered for: {user_input}")
            search_results = serper_search(user_input)
            print(f"[Expert] Found {len(search_results)} search results")
            if search_results:
                search_summary = "\n".join([
                    f"- {r.get('title', 'No title')}: {r.get('snippet', 'No snippet')[:100]}..."
                    for r in search_results[:3]
                ])
                prompt += f"\nRecent Web Search Results:\n{search_summary}"
        else:
            print(f"[Expert] No web search needed")
        prompt += f"\nConversation History:\n{history}\n\nYour Response (incorporate the search results if relevant):"
        response = self.llm.invoke([
            SystemMessage(content=prompt)
        ])
        # Restrict to first paragraph
        return response.content.split('\n\n')[0]

    def handoff(self, context: Dict[str, Any]) -> str:
        # Placeholder: Decide next agent or user
        return "realist"

    def needs_search(self, message: str, context: Dict[str, Any]) -> bool:
        keywords = ["study", "research", "report", "data", "statistics", "analysis", "2024", "findings"]
        return any(k in message.lower() for k in keywords)
