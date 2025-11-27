import random

RESPONSES = [
    "I'm here for you. Tell me more about how you're feeling.",
    "It sounds like you're going through a lot. I'm listening.",
    "Take a deep breath. You are not alone in this.",
    "I understand. Sometimes things can feel overwhelming.",
    "I'm sorry I can't connect to my main brain right now, but I'm still here to listen.",
    "Sending you virtual hugs. How can I support you today?",
    "Remember to be kind to yourself. You're doing your best.",
    "That sounds tough. Do you want to talk about it?",
    "I'm listening. Please go on.",
    "Your feelings are valid. I'm here."
]

CRISIS_KEYWORDS = ["die", "kill", "suicide", "hurt myself", "end it"]
CRISIS_RESPONSE = """I'm very concerned about what you're saying. Please reach out for help immediately. 
You are not alone. 
- Suicide & Crisis Lifeline: 988 (US)
- International resources: findahelpline.com
Please talk to a professional or someone you trust right now."""

def get_fallback_response(user_input=""):
    # Simple safety check for fallback mode
    if any(keyword in user_input.lower() for keyword in CRISIS_KEYWORDS):
        return CRISIS_RESPONSE
        
    return random.choice(RESPONSES)
