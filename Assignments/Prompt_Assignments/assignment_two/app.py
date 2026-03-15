import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# File path for our "database"
DATA_FILE = 'profile.json'

def load_data():
    """Load profile data from a JSON file or return defaults."""
    default_data = {
        "name": "Justin Davis",
        "role": "Software Engineering Student",
        "about": "Currently enrolled in a software engineering bootcamp and developing 'Eternal Conflict', a Roblox MOBA.",
        "profile_img": "",  # New field for your 3D models or headshot
        "skills": ["Python", "JavaScript", "HTML/CSS", "AI Integration", "3D Modeling (Blender)"],
        "projects": [
            {"title": "Eternal Conflict", "description": "A Roblox MOBA game featuring custom 3D models developed in Blender."},
            {"title": "AI Study Guide", "description": "An interactive tool for software engineering using D.A.V.E logic and RAAS systems."}
        ],
        "email": "yourname@example.com"
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                saved_data = json.load(f)
                # Senior Tip: Merge saved data with defaults to ensure new fields (like profile_img) exist
                return {**default_data, **saved_data}
            except json.JSONDecodeError:
                return default_data
    
    return default_data

def save_data(data):
    """Save the profile dictionary to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize data
profile_data = load_data()

@app.route('/')
def home():
    return render_template('index.html', user=profile_data)

@app.route('/edit', methods=['GET', 'POST'])
def edit_profile():
    global profile_data
    if request.method == 'POST':
        # 1. Update basic profile info
        profile_data['name'] = request.form.get('name')
        profile_data['role'] = request.form.get('role')
        profile_data['about'] = request.form.get('about')
        profile_data['email'] = request.form.get('email')
        profile_data['profile_img'] = request.form.get('profile_img')
        
        # 2. Process skills (comma-separated string to list)
        skills_raw = request.form.get('skills', '')
        profile_data['skills'] = [s.strip() for s in skills_raw.split(',') if s.strip()]
        
        # 3. Process Dynamic Projects (Title/Desc lists to list of dicts)
        titles = request.form.getlist('project_title[]')
        descriptions = request.form.getlist('project_desc[]')
        
        # Combine the lists using zip
        profile_data['projects'] = [
            {"title": t, "description": d} 
            for t, d in zip(titles, descriptions) if t.strip()
        ]
        
        # 4. Save to JSON and redirect
        save_data(profile_data)
        return redirect(url_for('home'))
    
    return render_template('edit.html', user=profile_data)

if __name__ == '__main__':
    app.run(debug=True)