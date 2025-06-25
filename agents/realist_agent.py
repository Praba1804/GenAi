from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent
from typing import Any, Dict, List
from utils.helpers import format_history
from search.serper_client import serper_search
from memory.faiss_memory_client import FaissMemoryClient
import re

class RealistAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Realist", persona="Practical, fact-driven, considers risks and constraints.")
        with open("prompts/realist_prompt.txt", "r") as f:
            self.persona_prompt = f.read()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.memory_client = FaissMemoryClient()

    def _decide_search(self, last_message: str) -> str:
        """Use LLM to decide if a search is needed and what the query should be."""
        # Expanded fallback keyword/pattern check
        search_triggers = [
            "do research", "find out", "look up", "search for", "can you research", "could you research", "can you find", "could you find", "can you look", "could you look",
            "how many", "how much", "what percentage", "number of", "statistics", "data", "report", "survey", "study", "recent", "current", "latest", "trend", "ratio", "proportion"
        ]
        lowered = last_message.lower()
        # Regex for years (e.g., 2024, 2023, 2022)
        year_pattern = re.compile(r"\b(20[2-3][0-9])\b")
        # Regex for numeric/statistical queries
        numeric_patterns = [
            r"how many", r"how much", r"what percentage", r"number of", r"percent", r"ratio", r"proportion"
        ]
        if any(phrase in lowered for phrase in search_triggers):
            return last_message
        if year_pattern.search(lowered):
            return last_message
        if any(re.search(pat, lowered) for pat in numeric_patterns):
            return last_message
        if lowered.endswith("?") and any(word in lowered for word in ["how", "what", "when", "where", "which", "who", "is", "are", "do", "does", "did"]):
            return last_message

        prompt = f"""Given the last message in a conversation, decide if you need to search the web for more information.
The user is talking to a panel of AI agents (Realist, Optimist, Expert).
Only search for specific, factual, or up-to-date information that you wouldn't already know.
Do not search for general opinions or to answer conversational pleasantries.

If the user's message contains phrases like 'do research', 'find out', 'look up', 'search for', 'how many', 'how much', 'what percentage', 'number of', 'statistics', 'data', 'report', 'survey', 'study', 'recent', 'current', 'latest', 'trend', 'in 2024', 'in 2023', 'in 2022', or any year, you MUST trigger a web search using the user's message as the search query.
If the user's message is a question about numbers, statistics, data, recent events, or anything time-specific, you MUST trigger a web search.

Examples that MUST trigger a search:
- "How many people did both in 2024?"
- "What percentage of students interned last year?"
- "Find out the latest trends in AI."
- "Do some research on white elephants."
- "What is the current unemployment rate?"

Last Message: "{last_message}"

If a search is needed, respond with the search query.
If no search is needed, respond with "NO_SEARCH".
Your response must be either the search query or the exact phrase "NO_SEARCH".
"""
        response = self.llm.invoke([SystemMessage(content=prompt)])
        decision = response.content.strip()
        if decision == "NO_SEARCH":
            return None
        return decision

    def respond(self, state: Dict[str, Any]) -> str:
        """Respond to user input with memory and selective search capabilities"""
        history = state.get("history", [])
        last_turn = history[-1]
        last_message = last_turn["message"]
        last_speaker = last_turn["speaker"]

        print(f"[{self.name}] Processing last message from {last_speaker}: '{last_message[:50]}...'")

        # Add the last turn to memory
        self.memory_client.add_turn(last_speaker, last_message)

        # Decide if web search is needed
        search_query = self._decide_search(last_message)
        search_context = ""
        if search_query:
            print(f"[{self.name}] Web search triggered for: {search_query}")
            search_results = serper_search(search_query)
            print(f"[{self.name}] Found {len(search_results)} search results")
            
            if search_results:
                # Show only the top 2 results, clearly labeled
                search_context = "\nRecent Web Search Results (summarize or cite these in your answer):\n" + "\n".join([
                    f"{i+1}. {r.get('title', 'No title')}: {r.get('snippet', 'No snippet')[:200]}..." for i, r in enumerate(search_results[:2])
                ])

        # Retrieve relevant memory
        memory_results = self.memory_client.query(last_message, n_results=3)
        memory_context = ""
        if memory_results:
            memory_context = f"\nRelevant Context from Memory:\n" + "\n".join([f"- {result['speaker']}: {result['message']}" for result in memory_results])
            print(f"[{self.name}] Retrieved {len(memory_results)} memory items")

        # Format conversation history
        formatted_history = format_history(history)
        
        # Check if the user is asking a direct question to this agent
        is_direct_question = f"what did {self.name.lower()}" in last_message.lower() or f"what was {self.name.lower()}" in last_message.lower()

        if is_direct_question:
            # Simplified prompt for answering a direct question
            prompt = f"""The user is asking what you, the {self.name} agent, said earlier.
Search the conversation history and summarize your previous points concisely.

Conversation History:
{formatted_history}

User Question: "{last_message}"

Your Answer (summarize your previous points directly and concisely). After you answer, the conversation will return to the user.
"""
        else:
            # Build the prompt for a research-focused discussion contribution
            prompt = f"""{self.persona_prompt}

You are the {self.name} agent in a panel discussion.
Your goal is to be conversational and build on the discussion naturally.
- If search results are provided, your answer MUST be based on them. Summarize or cite the most relevant findings to directly answer the user's question.
- Only use your own knowledge if no search results are available.
- Acknowledge and reference what the last speaker ({last_speaker}) said.
- Use the provided memory context to enrich your response.
- Keep your response concise, conversational, and to a maximum of 3 sentences.

{memory_context}
{search_context}

Conversation History:
{formatted_history}

Last message from {last_speaker}: "{last_message}"

Your Response (be conversational, reference the last speaker, and add your unique perspective):"""

        response = self.llm.invoke([
            SystemMessage(content=prompt)
        ])
        
        # Store your own response in memory
        self.memory_client.add_turn(self.name.lower(), response.content)
        
        return response.content

    def needs_search(self, message: str, context: List[Dict[str, str]]) -> bool:
        """Decide if web search is needed"""
        search_keywords = [
            "current", "latest", "2024", "news", "market", "demand", 
            "salary", "trend", "job", "cost", "tuition", "internship",
            "career", "opportunities", "companies", "industry"
        ]
        return any(k in message.lower() for k in search_keywords)
