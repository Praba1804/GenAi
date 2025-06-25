import streamlit as st
import time
from utils.router import decide_next_agent
from utils.avatars import avatars
from agents.realist_agent import RealistAgent
from agents.optimist_agent import OptimistAgent
from agents.expert_agent import ExpertAgent

# --- Session State Initialization ---
if "history" not in st.session_state:
    st.session_state.history = []
if "turn" not in st.session_state:
    st.session_state.turn = "user" # Start with the user
if "agents" not in st.session_state:
    st.session_state.agents = {
        "realist": RealistAgent(),
        "optimist": OptimistAgent(),
        "expert": ExpertAgent()
    }

# Handoff phrases to detect when to return to user
HANDOFF_PHRASES = [
    "let me know", "can you tell me", "what do you think", "could you share", "please provide", "would you like", "do you have", "are you considering", "what's your", "what is your", "how about you", "tell me more", "could you clarify", "may I ask", "would you mind"
]

def should_handoff_to_user(response: str) -> bool:
    resp = response.strip().lower()
    if resp.endswith("?"):
        return True
    for phrase in HANDOFF_PHRASES:
        if phrase in resp:
            return True
    return False

st.title("🤖 Multi-Agent Discussion Panel")

# --- System Greeting (only once) ---
if not st.session_state.history:
    st.session_state.history.append({
        "speaker": "system", 
        "message": "Hi! I'm here with my colleagues to discuss any topic you'd like. What would you like us to explore together?"
    })

# --- Chat History Display ---
for turn in st.session_state.history:
    speaker = turn['speaker']
    message = turn['message']
    avatar = avatars.get(speaker, '🤖')
    with st.chat_message(name=speaker, avatar=avatar):
        st.write(message)

# --- Agent Turn Logic ---
if st.session_state.turn != "user":
    agent_name = st.session_state.turn
    agent = st.session_state.agents.get(agent_name)
    if agent:
        with st.spinner(f"{agent.name} is thinking..."):
            time.sleep(1) # UX delay
            response = agent.respond({"history": st.session_state.history})
            
            # STATE UPDATE ONLY: Add agent response to history
            st.session_state.history.append({"speaker": agent_name, "message": response})
            
            # --- Turn-taking logic ---
            # First, check if this was a direct Q&A response
            last_user_message = ""
            for turn in reversed(st.session_state.history):
                if turn["speaker"] == "user":
                    last_user_message = turn["message"].lower()
                    break
            
            is_direct_qa = f"what did {agent_name}" in last_user_message or f"what was {agent_name}" in last_user_message

            # Decide the next turn, with multiple override levels
            if is_direct_qa:
                st.session_state.turn = "user"
            elif should_handoff_to_user(response):
                st.session_state.turn = "user"
            else:
                st.session_state.turn = decide_next_agent({"history": st.session_state.history})

            st.rerun() # Rerun to render the new message & process next turn
    else:
        st.error(f"Error: Unknown agent '{agent_name}'")
        st.session_state.turn = "user"
        st.rerun()

# --- User Input Logic ---
def on_user_input():
    if st.session_state.user_input:
        # Add user message to history and decide next turn
        st.session_state.history.append({"speaker": "user", "message": st.session_state.user_input})
        st.session_state.turn = decide_next_agent({"history": st.session_state.history})
        st.session_state.user_input = ""

# Display the input box, which will trigger the agent logic on the next rerun
st.text_input("Your message:", key="user_input", on_change=on_user_input, disabled=(st.session_state.turn != "user"))
