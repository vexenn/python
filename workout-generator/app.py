import sys
import os
import webbrowser
from threading import Timer
from flask import Flask, render_template, request

# Import your custom utility functions
from utils.ai_agent import generate_routine
from utils.youtube import get_youtube_video_id

# 1. Initialize the app with PyInstaller pathing logic
# This ensures that when bundled as an .exe, Flask knows where to find your files
if getattr(sys, 'frozen', False):
    # When running as an .exe, look for folders in the temporary internal directory
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # When running normally in VS Code
    app = Flask(__name__)

def open_browser():
    """
    Automatically opens the default web browser to the local server address.
    """
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    condition = request.form.get('condition')
    days = request.form.get('days')
    
    # 1. Get the JSON routine from Gemini
    routine = generate_routine(condition, days)
    
    # 2. Append YouTube Video IDs to each exercise
    for day in routine:
        for exercise in day.get('exercises', []):
            video_id = get_youtube_video_id(exercise['name'])
            exercise['video_id'] = video_id

    return render_template('routine.html', routine=routine, condition=condition)

if __name__ == '__main__':
    # 2. Automation: Wait 1.5 seconds for the server to start, then open the browser
    # This makes the app feel like a real program on her Windows PC
    Timer(1.5, open_browser).start()

    # 3. CRITICAL: debug=False is required for bundled executables
    # This prevents the "reloader" crash you were seeing earlier
    app.run(debug=False)