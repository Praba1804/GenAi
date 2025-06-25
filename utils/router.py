from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from typing import Dict, Any, List

class AgentRouter:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    def decide_next_agent(self, state: Dict[str, Any]) -> str:
        history = state.get("history", [])
        if not history:
            return "user"

        # --- Determine agents who have spoken since the last user message ---
        agents_in_round = set()
        for turn in reversed(history):
            if turn["speaker"] == "user":
                break
            if turn["speaker"] != "system":
                agents_in_round.add(turn["speaker"])

        all_agents = {"realist", "optimist", "expert"}
        available_agents = list(all_agents - agents_in_round)

        # If all agents have spoken, force the turn back to the user
        if not available_agents:
            print("[Router] All agents have spoken. Returning to user.")
            return "user"

        last_message = history[-1]
        return self._llm_decision(history, last_message["message"], available_agents)

    def _llm_decision(self, history: List[Dict[str, str]], latest_message: str, available_agents: List[str]) -> str:
        recent_turns = history[-6:] if len(history) > 6 else history
        formatted_history = self._format_history(recent_turns)

        prompt = f"""
You are a conversation router for a multi-agent system. Your job is to select the next speaker.

**Available Agents to Choose From:** {', '.join(available_agents)}

**Recent Conversation:**
{formatted_history}

**Instructions:**
1.  **First, analyze the last message.** Is the user asking a direct question about what a specific agent said previously (e.g., "what did the expert say?")?
    *   If YES, and the agent being asked is in the available list, your response MUST be the name of that agent.
2.  **If the user is contributing a new idea or opinion:**
    *   You must choose one agent from the "Available Agents" list to continue the discussion **only if it will add meaningful value or perspective**.
    *   Do NOT force every agent to respond to every user message. If the last agent's response is sufficient, or if it feels natural to return to the user, do so.
    *   Your choice should facilitate a natural, flowing panel discussion.
3.  **If the last speaker was an agent, and their message was a question to the user:**
    *   Return `user`.

**Your Response:**
Respond with only the single name of the next speaker from the "Available Agents" list, or `user`.
"""
        response = self.llm.invoke([
            SystemMessage(content=prompt)
        ])
        next_agent = response.content.strip().lower().replace("`", "")

        # Validate the response
        if next_agent in available_agents:
            print(f"[Router] Decided next agent: {next_agent}")
            return next_agent
        if next_agent == "user":
            print("[Router] Decided next agent: user")
            return "user"
        
        # Fallback if the LLM fails to follow instructions
        print(f"[Router] LLM failed, defaulting to first available: {available_agents[0]}")
        return available_agents[0]

    def _format_history(self, history: List[Dict[str, str]]) -> str:
        formatted = []
        for turn in history:
            speaker = turn["speaker"].capitalize()
            message = turn["message"][:100] + "..." if len(turn["message"]) > 100 else turn["message"]
            formatted.append(f"{speaker}: {message}")
        return "\n".join(formatted)

# Global router instance
router = AgentRouter()

def decide_next_agent(state: Dict[str, Any]) -> str:
    return router.decide_next_agent(state)