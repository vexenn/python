import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_routine(condition, days):
    
    # Using 2.5 Flash because your dashboard shows an active 5 RPM free tier!
    model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})
    
    prompt = f"""
    Act as an expert physical therapist and personal trainer. 
    Create a {days}-day workout routine tailored for someone dealing with {condition}.
    Focus on rehabilitation, safety, and general health. 
    
    Output strictly as a JSON array of objects. Do not include markdown formatting or extra text.
    Format:
    [
      {{
        "day": "Day 1",
        "focus": "Mobility and Stretching",
        "exercises": [
          {{"name": "Seated Calf Stretch", "sets": "3", "reps": "30 seconds"}},
          {{"name": "Towel Scrunches", "sets": "3", "reps": "15"}}
        ]
      }}
    ]
    """
    
    response = model.generate_content(prompt)
    try:
        routine_data = json.loads(response.text)
        return routine_data
    except json.JSONDecodeError:
        print("Failed to parse JSON from AI response.")
        return []