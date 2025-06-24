from agents.realist_agent import RealistAgent
from agents.optimist_agent import OptimistAgent
from agents.expert_agent import ExpertAgent
from state.types import AgentState
from memory.faiss_memory_client import FaissMemoryClient
from search.serper_client import serper_search

# Agent and memory instances
realist = RealistAgent()
optimist = OptimistAgent()
expert = ExpertAgent()
memory_client = FaissMemoryClient()

# Generic agent handler
def agent_handler(state: AgentState, agent) -> AgentState:
    response = agent.respond(state)
    state["history"].append({"speaker": agent.name.lower(), "message": response})
    memory_client.add_turn(agent.name.lower(), response)
    return state

# Specific handlers
def realist_handler(state: AgentState) -> AgentState:
    return agent_handler(state, realist)

def optimist_handler(state: AgentState) -> AgentState:
    return agent_handler(state, optimist)

def expert_handler(state: AgentState) -> AgentState:
    return agent_handler(state, expert)

# User handler now just stores the turn
def user_handler(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "")
    if user_input:
        state["history"].append({"speaker": "user", "message": user_input})
        memory_client.add_turn("user", user_input)
        state["user_input"] = "" # Clear after processing
    return state
