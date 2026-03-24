from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

# Load the secret variables from your .env file into the environment
load_dotenv()

app = Flask(__name__)

# Configure your AI API key securely
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# --- NEW: The Homepage Route ---
@app.route('/')
def home():
    # This tells Flask to look in the templates folder and serve this HTML file
    return render_template('index.html')

# --- Your Existing AI Route ---
@app.route('/generate-alt-text', methods=['POST'])
def generate_alt():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
        
    image_file = request.files['image']
    img = Image.open(image_file)
    user_context = request.form.get('context', 'No context provided.')
    
    prompt = f"""
    You are an expert web accessibility (a11y) specialist. 
    Generate a highly descriptive, concise alt text (under 125 characters) for this image.
    Tailor the description specifically to this context: "{user_context}"
    Output ONLY the alt text string, nothing else.
    """
    
    # Using the free and fast Flash model
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([prompt, img])
    
    return jsonify({"alt_text": response.text.strip()})

if __name__ == '__main__':
    app.run(debug=True)