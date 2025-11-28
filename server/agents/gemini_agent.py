import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Safety settings to ensure safe interactions
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

SYSTEM_INSTRUCTION = """
You are a compassionate, empathetic, and supportive Mental Health Companion. 
Your goal is to listen to the user, validate their feelings, and provide gentle advice, daily plans, or tips to improve their well-being.
You are NOT a doctor. If the user expresses self-harm or severe crisis, gently encourage them to seek professional help immediately.
Your tone should be warm, friendly, and non-judgmental.
"""

def generate_response(history, user_input):
    try:
        if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
            return None # Trigger fallback

        model = genai.GenerativeModel(model_name="gemini-2.0-flash", system_instruction=SYSTEM_INSTRUCTION)
        
        # Convert history to Gemini format
        chat_history = []
        for msg in history:
            role = "user" if msg['role'] == "user" else "model"
            chat_history.append({"role": role, "parts": [msg['content']]})

        chat = model.start_chat(history=chat_history)
        response = chat.send_message(user_input, safety_settings=SAFETY_SETTINGS)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None
