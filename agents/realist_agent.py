from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent
from typing import Any, Dict, List
from utils.helpers import format_history
from search.serper_client import serper_search
from memory.faiss_memory_client import FaissMemoryClient

class RealistAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Realist", persona="Practical, fact-driven, considers risks and constraints.")
        with open("prompts/realist_prompt.txt", "r") as f:
            self.persona_prompt = f.read()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.memory_client = FaissMemoryClient()

    def respond(self, user_input: str, history: List[Dict[str, str]]) -> str:
        """Respond to user input with memory and search capabilities"""
        print(f"[Realist] Processing: {user_input}")
        
        # Store user input in memory
        self.memory_client.add_turn("user", user_input)
        
        # Retrieve relevant memory
        memory_results = self.memory_client.query(user_input, n_results=3)
        memory_context = ""
        if memory_results:
            memory_context = f"\nRelevant Context from Memory:\n" + "\n".join([f"- {result['speaker']}: {result['message']}" for result in memory_results])
            print(f"[Realist] Retrieved {len(memory_results)} memory items")
        
        # Check if web search is needed
        search_context = ""
        if self.needs_search(user_input, history):
            print(f"[Realist] Web search triggered for: {user_input}")
            search_results = serper_search(user_input)
            print(f"[Realist] Found {len(search_results)} search results")
            
            if search_results:
                search_context = f"\nRecent Web Search Results:\n" + "\n".join([
                    f"- {r.get('title', 'No title')}: {r.get('snippet', 'No snippet')[:150]}..."
                    for r in search_results[:3]
                ])
        
        # Format conversation history
        formatted_history = format_history(history)
        
        # Build the prompt
        prompt = f"""{self.persona_prompt}

You are the Realist agent. You should:
1. Be practical and consider real-world constraints
2. Ask clarifying questions when needed
3. Use search results and memory context when relevant
4. Build on what other agents have said
5. Keep responses conversational and natural

{memory_context}
{search_context}

Conversation History:
{formatted_history}

Current User Input: {user_input}

Your Response (be conversational and natural):"""

        response = self.llm.invoke([
            SystemMessage(content=prompt)
        ])
        
        # Store response in memory
        self.memory_client.add_turn("realist", response.content)
        
        return response.content

    def needs_search(self, message: str, context: List[Dict[str, str]]) -> bool:
        """Decide if web search is needed"""
        search_keywords = [
            "current", "latest", "2024", "news", "market", "demand", 
            "salary", "trend", "job", "cost", "tuition", "internship",
            "career", "opportunities", "companies", "industry"
        ]
        return any(k in message.lower() for k in search_keywords)
