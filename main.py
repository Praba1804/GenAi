from agents.realist_agent import RealistAgent
from agents.optimist_agent import OptimistAgent
from agents.expert_agent import ExpertAgent
from voice.stt import stt_from_mic
from voice.tts import speak
from utils.router import decide_next_agent
from utils.avatars import avatars

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

if __name__ == "__main__":
    print("Welcome to the Dynamic Multi-Agent Voice Conversation System!")
    print("🤖 Hi! I'm here with my colleagues to discuss any topic you'd like. What would you like us to explore together?")
    
    mode = input("Choose mode: [1] Text [2] Voice\nEnter: ").strip()

    # Initialize agents
    realist_agent = RealistAgent()
    optimist_agent = OptimistAgent()
    expert_agent = ExpertAgent()
    
    # Initialize conversation state
    history = []
    
    while True:
        # Get user input
        if mode == '1':
            user_input = input("You: ")
        else:
            user_input = stt_from_mic()
            print(f"You: {user_input}")
        
        if "quit" in user_input.lower():
            print("Goodbye! 👋")
            break
        
        # Add user input to history
        history.append({"speaker": "user", "message": user_input})

        # Agent response loop
        while True:
            state = {"history": history}
            next_agent = decide_next_agent(state)
            print(f"[Router] Next agent: {next_agent}")

            if next_agent == "user":
                break  # Wait for next user input

            agent = {
                "realist": realist_agent,
                "optimist": optimist_agent,
                "expert": expert_agent
            }.get(next_agent)

            if agent:
                response = agent.respond(state)
                history.append({"speaker": agent.name.lower(), "message": response})
                print(f"{avatars.get(agent.name.lower())} {agent.name}: {response}")
                if mode == '2':
                    speak(response, agent=agent.name.lower())

                # Handoff detection
                if should_handoff_to_user(response):
                    break
            else:
                print(f"[Router] Error: Unknown agent '{next_agent}'")
                break
        print()
