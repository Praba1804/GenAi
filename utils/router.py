from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from typing import Dict, Any, List
from state.handlers import agent_map

class AgentRouter:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    def decide_next_agent(self, state: Dict[str, Any]) -> str:
        history = state.get("history", [])
        if not history:
            return "user"

        last_message = history[-1]
        last_speaker = last_message["speaker"]

        if last_speaker == "user":
            return self._llm_decision(history, last_message["message"])

        # Check agent's own handoff logic if available
        if last_speaker in agent_map:
            agent = agent_map[last_speaker]
            handoff_decision = agent.handoff({"history": history})
            if handoff_decision in ["user", "realist", "optimist", "expert"]:
                print(f"[Router] Handoff suggested: {handoff_decision}")
                return handoff_decision

        return self._llm_decision(history, last_message["message"])

    def _llm_decision(self, history: List[Dict[str, str]], latest_user_message: str) -> str:
        recent_turns = history[-6:] if len(history) > 6 else history
        formatted_history = self._format_history(recent_turns)

        prompt = f"""
You are a conversation router for a multi-agent system with three agents:

1. Realist Agent: Practical, considers risks and constraints, asks clarifying questions
2. Optimist Agent: Enthusiastic, focuses on opportunities and positive aspects
3. Expert Agent: Knowledgeable, provides detailed insights and expert analysis

Recent Conversation:
{formatted_history}

Latest User Message: "{latest_user_message}"

Instructions:
- After a user message, always let an agent respond first.
- If the last agent's message is a direct question to the user, or if more information is needed from the user, choose "user".
- Otherwise, let another agent respond to build on the previous agent's points, provide a different perspective, or add more information.
- Encourage agents to reference each other's points and continue the discussion until a user response is necessary.
- Only return to "user" if the conversation cannot proceed without their input.

Respond with only the agent name: realist, optimist, expert, or user.
"""
        response = self.llm.invoke([
            SystemMessage(content=prompt)
        ])
        next_agent = response.content.strip().lower()
        valid_agents = ["realist", "optimist", "expert", "user"]
        if next_agent not in valid_agents:
            return "realist"  # Default to Realist if LLM fails
        print(f"[Router] Decided next agent: {next_agent}")
        return next_agent

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