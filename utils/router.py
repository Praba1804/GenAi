from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import List, Dict, Any
from config import OPENAI_API_KEY
from utils.helpers import format_history


ROUTER_PROMPT = """You are an expert router in a multi-agent conversation. Your job is to decide who should speak next.

The participants are:
- "realist": A practical, fact-driven agent. Good for analysis, risks, and concrete steps.
- "optimist": A positive, opportunity-focused agent. Good for brainstorming, encouragement, and possibilities.
- "expert": A knowledgeable agent with deep expertise. Good for technical details, data, and research-backed insights.
- "user": The human participant. Choose this when their input, opinion, or a direct question is needed.
- "end": Choose this if the user wants to end the conversation (e.g., says "goodbye", "thanks, I'm done").

IMPORTANT: When the user asks about what someone said earlier (like "What did the Realist say earlier?"), choose the appropriate agent to respond, NOT the user.

Here is the conversation history (last message is the most recent):
{history}

Based on the last message and the conversation, who should speak next?
Respond with ONLY a single word from this list: realist, optimist, expert, user, end
Do not use quotes or punctuation.
"""

def decide_next_agent(state: Dict[str, Any]) -> str:
    """Uses an LLM to decide the next agent."""
    history = state.get("history", [])
    if not history:
        return "user"  # Start with the user if history is empty

    formatted_history = format_history(history)
    prompt = ROUTER_PROMPT.format(history=formatted_history)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.6)  
    try:
        response = llm.invoke([
            SystemMessage(content=prompt)
        ])
        next_agent = response.content.strip().lower().strip('"').strip("'")
        print(f"[Router] LLM response: {response.content.strip()}")
        
        valid_agents = ["realist", "optimist", "expert", "user", "end"]
        if next_agent in valid_agents:
            print(f"[Router decided next agent is: {next_agent.upper()}]")
            return next_agent
        else:
            print(f"[Router] Invalid agent response: {next_agent}")
    except Exception as e:
        print(f"Error in routing: {e}")

    return "user" # Default to user on error or invalid response 