from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model (using gemini-1.5-flash for speed and cost-effectiveness)
# New code
model = genai.GenerativeModel('gemini-2.5-flash', 
                              generation_config={"response_mime_type": "application/json"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    data = request.json
    destination = data.get('destination')
    duration = data.get('duration', '3 days')
    preferences = data.get('preferences', 'No specific preferences')

    prompt = f"""
    You are an expert, highly organized travel concierge. Your goal is to create detailed, highly rated, and practical travel itineraries based on user preferences. 
    
    User Destination: {destination}
    Duration: {duration}
    Preferences: {preferences}

    You MUST respond ONLY with a valid, well-structured JSON object. Do not include any markdown formatting like ```json or trailing text. The JSON must strictly follow this structure:

    {{
      "destination": "Name of the city/country",
      "emergency_info": {{
        "police": "local number",
        "ambulance": "local number",
        "fire": "local number",
        "embassy_tip": "Brief advice on locating their embassy"
      }},
      "suggested_areas_to_stay": [
        {{
          "neighborhood": "Name of area",
          "vibe": "Brief description",
          "price_tier": "Low/Medium/High"
        }}
      ],
      "itinerary": [
        {{
          "day": 1,
          "theme": "Brief theme for the day",
          "activities": [
            {{
              "time_of_day": "Morning",
              "type": "Scenery / Museum / Activity",
              "name": "Name of the place",
              "description": "Why they should visit",
              "estimated_cost": "Free / Low / Medium / High"
            }}
          ],
          "dining_suggestions": [
            {{
              "meal": "Lunch",
              "name": "Name of restaurant or food market",
              "type": "Highly Rated / Low Cost",
              "cuisine": "Type of food",
              "description": "Why it is recommended"
            }}
          ]
        }}
      ]
    }}

    Guidelines:
    1. Ensure a logical geographic flow for each day.
    2. Prioritize highly rated local food spots.
    3. Include at least one museum or cultural site and one scenic/nature spot per day if possible.
    4. Provide verified local emergency contacts.
    """

    try:
        response = model.generate_content(prompt)
        # Parse the JSON string from Gemini into a Python dictionary
        itinerary_data = json.loads(response.text) 
        return jsonify(itinerary_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to generate itinerary. Please try again."}), 500

if __name__ == '__main__':
    app.run(debug=True)