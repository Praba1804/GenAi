import streamlit as st
import time
from state.handlers import realist_handler, optimist_handler, expert_handler, user_handler
from utils.router import decide_next_agent

# Session state for chat history and turn
if "history" not in st.session_state:
    st.session_state["history"] = []
if "turn" not in st.session_state:
    st.session_state["turn"] = "system"
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
if "conversation_started" not in st.session_state:
    st.session_state["conversation_started"] = False

# Avatars for each participant
avatars = {
    "user": "👤",
    "realist": "🧑‍💼",
    "optimist": "😃",
    "expert": "🧑‍🔬",
    "system": "🤖"
}

# Agent names for display
agent_names = {
    "user": "You",
    "realist": "Realist",
    "optimist": "Optimist", 
    "expert": "Expert",
    "system": "System"
}

st.title("🤖 Multi-Agent Voice Conversation Demo")

# Display chat history with better formatting
for turn in st.session_state["history"]:
    speaker = turn['speaker']
    message = turn['message']
    
    # Create a chat bubble effect
    if speaker == "user":
        st.markdown(f"""
        <div style="text-align: right; margin: 10px 0;">
            <div style="background-color: #007bff; color: white; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;">
                <strong>{message}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: left; margin: 10px 0;">
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;">
                <strong>{avatars.get(speaker, '🤖')} {agent_names.get(speaker, speaker.capitalize())}:</strong><br>
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

def send_message():
    if st.session_state.user_input:
        st.session_state.history.append({"speaker": "user", "message": st.session_state.user_input})
        st.session_state.turn = decide_next_agent({"history": st.session_state["history"]})
        st.session_state.user_input = ""  # This is safe inside the callback
        st.rerun()

# System greeting
if not st.session_state["conversation_started"]:
    st.session_state["history"].append({
        "speaker": "system", 
        "message": "Hi! I'm here with my colleagues to discuss any topic you'd like. What would you like us to explore together?"
    })
    st.session_state["conversation_started"] = True
    st.session_state["turn"] = "user"
    st.rerun()

# User input
if st.session_state["turn"] == "user":
    st.text_input("You:", key="user_input", on_change=send_message)
else:
    # Agent turn with loading spinner
    agent_name = agent_names.get(st.session_state["turn"], st.session_state["turn"].capitalize())
    agent_avatar = avatars.get(st.session_state["turn"], "🤖")
    
    with st.spinner(f"{agent_avatar} {agent_name} is thinking..."):
        # Add a small delay for better UX
        time.sleep(0.5)
        
        handler = {
            "realist": realist_handler,
            "optimist": optimist_handler,
            "expert": expert_handler,
        }[st.session_state["turn"]]
        
        # Get the latest user message for the agent
        latest_user_message = ""
        for turn in reversed(st.session_state["history"]):
            if turn["speaker"] == "user":
                latest_user_message = turn["message"]
                break
        
        # Pass the latest user message to the handler
        agent_state = {
            "history": st.session_state["history"],
            "user_input": latest_user_message
        }
        agent_state = handler(agent_state)
        
        # Update the main state with agent response
        st.session_state["history"] = agent_state["history"]
        st.session_state["turn"] = decide_next_agent({"history": st.session_state["history"]})
        st.rerun()
