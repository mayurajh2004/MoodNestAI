import random
import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Fallback routines if Gemini fails
MORNING_ROUTINES = [
    "1. Drink a glass of water.\n2. 5-minute stretching.\n3. Write down 3 things you are grateful for.",
    "1. Make your bed.\n2. 10-minute meditation.\n3. Healthy breakfast.",
    "1. Short walk outside.\n2. Review your goals for the day.\n3. Listen to uplifting music."
]

EVENING_ROUTINES = [
    "1. Digital detox (no screens) for 1 hour before bed.\n2. Read a book.\n3. Reflect on what went well today.",
    "1. Warm bath or shower.\n2. Journaling your thoughts.\n3. Prepare clothes for tomorrow.",
    "1. Relaxation exercises.\n2. Listen to calming sounds.\n3. Sleep at a consistent time."
]

SYSTEM_INSTRUCTION = """
You are a compassionate Mental Health Companion creating personalized daily plans.
Generate a brief, actionable plan (3-4 steps) based on the time of day and user's mood.
Your plans should be:
- Practical and easy to follow
- Supportive and encouraging
- Focused on mental well-being and self-care
- Formatted as a numbered list
Keep the tone warm and non-judgmental.
"""

def generate_plan_fallback(time_of_day, routine):
    """Fallback function using hardcoded templates"""
    plan = f"**{time_of_day} Plan for You**\n\nBased on the time of day, here is a gentle plan:\n\n{routine}\n\n*Remember: Small steps make a big difference.*"
    return plan

def generate_plan(user_mood="neutral", recent_context=""):
    hour = datetime.datetime.now().hour
    
    # Determine time of day
    if 5 <= hour < 12:
        time_of_day = "Morning"
        fallback_routine = random.choice(MORNING_ROUTINES)
    elif 12 <= hour < 18:
        time_of_day = "Afternoon"
        fallback_routine = "1. Take a short break.\n2. Hydrate.\n3. Do a quick breathing exercise."
    else:
        time_of_day = "Evening"
        fallback_routine = random.choice(EVENING_ROUTINES)
    
    # Try Gemini AI first
    try:
        if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
            print("Planner: No valid API key, using fallback")
            return generate_plan_fallback(time_of_day, fallback_routine)
        
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        
        prompt = f"""Create a personalized {time_of_day.lower()} plan for someone who is feeling {user_mood}.
The current time is {hour}:00.

Recent Chat Context:
{recent_context}

Provide 3-4 actionable steps that will help them feel better and take care of their mental health.
Format your response as a Markdown table:
**{time_of_day} Plan for You**

| Time | Activity | Details |
| :--- | :--- | :--- |
| [Time] | [Activity Name] | [Brief Description] |
...

*[Add an encouraging closing message]*
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Planner Gemini Error: {e}")
        return generate_plan_fallback(time_of_day, fallback_routine)
