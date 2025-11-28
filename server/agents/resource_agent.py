import random
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Fallback strategies if Gemini fails
STRATEGIES = {
    "anxiety": [
        "**Box Breathing**: Inhale for 4s, hold for 4s, exhale for 4s, hold for 4s. Repeat 4 times.",
        "**5-4-3-2-1 Grounding**: Acknowledge 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, 1 you can taste.",
        "**Progressive Muscle Relaxation**: Tense and then relax each muscle group starting from your toes up to your head."
    ],
    "sadness": [
        "**Gentle Movement**: Go for a short walk or do some light stretching.",
        "**Comfort**: Wrap yourself in a warm blanket and drink a warm beverage.",
        "**Expression**: Write down your feelings in a journal or draw them out."
    ],
    "stress": [
        "**Time Blocking**: Focus on just one small task for 5 minutes.",
        "**Nature Break**: Step outside or look at a picture of nature.",
        "**Music**: Listen to your favorite calming playlist."
    ],
    "general": [
        "**Mindfulness**: Take a moment to just 'be' without doing anything.",
        "**Hydration**: Drink a glass of water.",
        "**Gratitude**: Think of one small thing that made you smile today."
    ]
}

SYSTEM_INSTRUCTION = """
You are a compassionate Mental Health Companion providing evidence-based coping strategies.
Generate personalized coping strategies based on the user's emotional state.
Your strategies should be:
- Evidence-based and practical
- Easy to implement immediately
- Supportive and non-judgmental
- Brief but actionable
Focus on techniques like breathing exercises, grounding, mindfulness, gentle movement, or self-compassion.
"""

def get_strategy_fallback(category):
    """Fallback function using hardcoded strategies"""
    strategy = random.choice(STRATEGIES[category])
    return f"**Coping Strategy ({category.capitalize()})**\n\n{strategy}"

def get_strategy(mood="general"):
    # Simple keyword matching for mood to category
    mood = mood.lower()
    category = "general"
    
    if any(x in mood for x in ["anxious", "worry", "panic", "scared"]):
        category = "anxiety"
    elif any(x in mood for x in ["sad", "depressed", "down", "cry"]):
        category = "sadness"
    elif any(x in mood for x in ["stress", "overwhelmed", "busy", "tired"]):
        category = "stress"
    
    # Try Gemini AI first
    try:
        if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
            print("Resource: No valid API key, using fallback")
            return get_strategy_fallback(category)
        
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        
        prompt = f"""Create a personalized coping strategy for someone experiencing {category}.
The user's mood description: "{mood}"

Provide ONE specific, actionable coping technique they can use right now.
Format your response as:
### 🌿 Coping Strategy: {category.capitalize()}

> *[A brief, calming quote or thought related to the strategy]*

**Strategy Name**

[Description of the strategy]

**Steps to Practice:**
* [Step 1]
* [Step 2]
* [Step 3]

*[Optional: Why this helps]*
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Resource Gemini Error: {e}")
        return get_strategy_fallback(category)
