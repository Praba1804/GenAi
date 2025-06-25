from typing import Dict, Any
from agents.realist_agent import RealistAgent
from agents.optimist_agent import OptimistAgent
from agents.expert_agent import ExpertAgent

# Initialize agents
realist_agent = RealistAgent()
optimist_agent = OptimistAgent()
expert_agent = ExpertAgent()

def user_handler(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle user input and decide next agent"""
    from utils.router import decide_next_agent
    # Add user message to history
    if "user_input" in state and state["user_input"]:
        state["history"].append({
            "speaker": "user",
            "message": state["user_input"]
        })
    
    # Decide which agent should respond next
    next_agent = decide_next_agent(state)
    state["next_agent"] = next_agent
    
    return state

def realist_handler(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Realist agent response with natural conversation flow"""
    from utils.router import decide_next_agent
    # Get the latest user message
    latest_user_message = ""
    for turn in reversed(state["history"]):
        if turn["speaker"] == "user":
            latest_user_message = turn["message"]
            break
    
    # Get realist response
    response = realist_agent.respond(latest_user_message, state["history"])
    
    # Add realist response to history
    state["history"].append({
        "speaker": "realist",
        "message": response
    })
    
    # Decide if another agent should continue the conversation
    next_agent = decide_next_agent(state)
    if next_agent != "user":
        # Let the next agent continue the conversation
        if next_agent == "optimist":
            optimist_response = optimist_agent.respond(latest_user_message, state["history"])
            state["history"].append({
                "speaker": "optimist",
                "message": optimist_response
            })
        elif next_agent == "expert":
            expert_response = expert_agent.respond(latest_user_message, state["history"])
            state["history"].append({
                "speaker": "expert",
                "message": expert_response
            })
    
    return state

def optimist_handler(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Optimist agent response with natural conversation flow"""
    from utils.router import decide_next_agent
    # Get the latest user message
    latest_user_message = ""
    for turn in reversed(state["history"]):
        if turn["speaker"] == "user":
            latest_user_message = turn["message"]
            break
    
    # Get optimist response
    response = optimist_agent.respond(latest_user_message, state["history"])
    
    # Add optimist response to history
    state["history"].append({
        "speaker": "optimist",
        "message": response
    })
    
    # Decide if another agent should continue the conversation
    next_agent = decide_next_agent(state)
    if next_agent != "user":
        # Let the next agent continue the conversation
        if next_agent == "realist":
            realist_response = realist_agent.respond(latest_user_message, state["history"])
            state["history"].append({
                "speaker": "realist",
                "message": realist_response
            })
        elif next_agent == "expert":
            expert_response = expert_agent.respond(latest_user_message, state["history"])
            state["history"].append({
                "speaker": "expert",
                "message": expert_response
            })
    
    return state

def expert_handler(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Expert agent response with natural conversation flow"""
    from utils.router import decide_next_agent
    # Get the latest user message
    latest_user_message = ""
    for turn in reversed(state["history"]):
        if turn["speaker"] == "user":
            latest_user_message = turn["message"]
            break
    
    # Get expert response
    response = expert_agent.respond(latest_user_message, state["history"])
    
    # Add expert response to history
    state["history"].append({
        "speaker": "expert",
        "message": response
    })
    
    # Decide if another agent should continue the conversation
    next_agent = decide_next_agent(state)
    if next_agent != "user":
        # Let the next agent continue the conversation
        if next_agent == "realist":
            realist_response = realist_agent.respond(latest_user_message, state["history"])
            state["history"].append({
                "speaker": "realist",
                "message": realist_response
            })
        elif next_agent == "optimist":
            optimist_response = optimist_agent.respond(latest_user_message, state["history"])
            state["history"].append({
                "speaker": "optimist",
                "message": optimist_response
            })
    
    return state

agent_map = {
    "realist": realist_agent,
    "optimist": optimist_agent,
    "expert": expert_agent,
}
