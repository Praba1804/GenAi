from agents.realist_agent import RealistAgent
from agents.optimist_agent import OptimistAgent
from agents.expert_agent import ExpertAgent
from voice.stt import stt_from_mic
from voice.tts import speak
from state.types import AgentState
from state.handlers import realist_handler, optimist_handler, expert_handler, user_handler
from utils.router import decide_next_agent

if __name__ == "__main__":
    print("Welcome to the Dynamic Multi-Agent Voice Conversation System!")
    mode = input("Choose mode: [1] Text [2] Voice\nEnter: ").strip()

    state: AgentState = {"history": [], "user_input": ""}
    
    if mode == '1':
        print("\nText mode. Type 'quit' to exit.")
        state["user_input"] = input("You: ")
    else:
        print("\nVoice mode. Say 'quit' to exit.")
        state["user_input"] = stt_from_mic()
        print(f"You: {state['user_input']}")

    # Initial user turn
    state = user_handler(state)
    
    while True:
        next_agent = decide_next_agent(state)
        print(f"[Router decided next agent is: {next_agent.upper()}]")
        
        if next_agent == "end":
            speak("Glad we could talk. Goodbye!", "realist")
            break

        if next_agent == "user":
            if mode == '1':
                state["user_input"] = input("You: ")
            else:
                state["user_input"] = stt_from_mic()
                print(f"You: {state['user_input']}")
            
            if "quit" in state["user_input"].lower():
                break
            state = user_handler(state)
            continue

        handler = {
            "realist": realist_handler,
            "optimist": optimist_handler,
            "expert": expert_handler,
        }[next_agent]
        
        # Get the latest user message for the agent
        latest_user_message = ""
        for turn in reversed(state["history"]):
            if turn["speaker"] == "user":
                latest_user_message = turn["message"]
                break
        
        print(f"[{next_agent.capitalize()} is responding...]")
        # Pass the latest user message to the handler
        agent_state = {
            "history": state["history"],
            "user_input": latest_user_message
        }
        agent_state = handler(agent_state)
        
        # Update the main state with agent response
        state["history"] = agent_state["history"]
        
        last_message = state["history"][-1]
        print(f"{last_message['speaker'].capitalize()}: {last_message['message']}")
        if mode == '2':
            speak(last_message['message'], agent=last_message['speaker'])
