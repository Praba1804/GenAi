from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent
from typing import Any, Dict, List
from utils.helpers import format_history
from search.serper_client import serper_search
from memory.faiss_memory_client import FaissMemoryClient

class ExpertAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Expert", persona="Knowledgeable, analytical, provides detailed insights and expert advice.")
        with open("prompts/expert_prompt.txt", "r") as f:
            self.persona_prompt = f.read()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.6)
        self.memory_client = FaissMemoryClient()

    def respond(self, user_input: str, history: List[Dict[str, str]]) -> str:
        """Respond to user input with memory and search capabilities"""
        print(f"[Expert] Processing: {user_input}")
        
        # Store user input in memory
        self.memory_client.add_turn("user", user_input)
        
        # Retrieve relevant memory
        memory_results = self.memory_client.query(user_input, n_results=3)
        memory_context = ""
        if memory_results:
            memory_context = f"\nRelevant Context from Memory:\n" + "\n".join([f"- {result['speaker']}: {result['message']}" for result in memory_results])
            print(f"[Expert] Retrieved {len(memory_results)} memory items")
        
        # Check if web search is needed
        search_context = ""
        if self.needs_search(user_input, history):
            print(f"[Expert] Web search triggered for: {user_input}")
            search_results = serper_search(user_input)
            print(f"[Expert] Found {len(search_results)} search results")
            
            if search_results:
                search_context = f"\nRecent Web Search Results:\n" + "\n".join([
                    f"- {r.get('title', 'No title')}: {r.get('snippet', 'No snippet')[:150]}..."
                    for r in search_results[:3]
                ])
        
        # Format conversation history
        formatted_history = format_history(history)
        
        # Build the prompt
        prompt = f"""{self.persona_prompt}

You are the Expert agent. You should:
1. Provide detailed, knowledgeable insights
2. Use data and research to support your points
3. Use search results and memory context when relevant
4. Build on what other agents have said
5. Keep responses conversational and natural
6. Offer expert analysis and recommendations

{memory_context}
{search_context}

Conversation History:
{formatted_history}

Current User Input: {user_input}

Your Response (be knowledgeable and conversational):"""

        response = self.llm.invoke([
            SystemMessage(content=prompt)
        ])
        
        # Store response in memory
        self.memory_client.add_turn("expert", response.content)
        
        return response.content

    def needs_search(self, message: str, context: List[Dict[str, str]]) -> bool:
        """Decide if web search is needed"""
        search_keywords = [
            "research", "data", "statistics", "analysis", "study", 
            "report", "findings", "evidence", "trends", "industry",
            "market", "technology", "innovation", "best practices"
        ]
        return any(k in message.lower() for k in search_keywords)
