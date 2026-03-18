from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from PIL import Image

app = Flask(__name__)

# Configure your AI API key (always store this in environment variables, never in plain text!)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/generate-alt-text', methods=['POST'])
def generate_alt():
    # 1. Grab the uploaded image from the request
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
        
    image_file = request.files['image']
    img = Image.open(image_file)
    
    # 2. Grab the context provided by the user
    user_context = request.form.get('context', 'No context provided.')
    
    # 3. Create the prompt combining your instructions and the user's context
    prompt = f"""
    You are an expert web accessibility (a11y) specialist. 
    Generate a highly descriptive, concise alt text (under 125 characters) for this image.
    Tailor the description specifically to this context: "{user_context}"
    Output ONLY the alt text string, nothing else.
    """
    
    # 4. Send the prompt and the image to the multimodal AI
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([prompt, img])
    
    # 5. Send the generated text back to your website
    return jsonify({"alt_text": response.text.strip()})

if __name__ == '__main__':
    app.run(debug=True)