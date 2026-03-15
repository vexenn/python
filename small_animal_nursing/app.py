import os
import sys
import random
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, url_for
from models import db, StudyModule, Topic, SubSection

# --- PyInstaller Path Handling ---
if getattr(sys, 'frozen', False):
    # If the app is running as a bundled .exe
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    
    # Put the database right next to the .exe so her data is saved permanently
    exe_dir = os.path.dirname(sys.executable)
    db_path = os.path.join(exe_dir, 'instance', 'study_guide.db')
    instance_path = os.path.join(exe_dir, 'instance')
else:
    # If running normally via VS Code
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'study_guide.db')
    instance_path = os.path.join(basedir, 'instance')

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Automatically create the database file if it doesn't exist
with app.app_context():
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    db.create_all()

# --- Auto-Open Browser Function ---
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

@app.route('/')
def index():
    """Main dashboard with search functionality and module list."""
    query = request.args.get('q', '').strip()
    
    if query:
        search_results = Topic.query.join(SubSection).filter(
            (Topic.title.ilike(f'%{query}%')) | 
            (SubSection.heading.ilike(f'%{query}%')) | 
            (SubSection.content.ilike(f'%{query}%'))
        ).distinct().all()
        
        return render_template('index.html', 
                               modules=[], 
                               search_results=search_results, 
                               query=query)
    
    modules = StudyModule.query.all()
    return render_template('index.html', modules=modules, search_results=None)

@app.route('/topic/<int:topic_id>')
def topic_detail(topic_id):
    """Displays specific notes for a topic with randomization for study tools."""
    topic = Topic.query.get_or_404(topic_id)
    
    sub_sections = list(topic.sub_sections)
    if topic.category == "Study Tool":
        random.shuffle(sub_sections)
        for sub in sub_sections:
            if sub.structured_data and 'options' in sub.structured_data:
                random.shuffle(sub.structured_data['options'])
    
    if "ECG" in topic.title:
        return render_template('nursing/rhythm_library.html', topic=topic, sub_sections=sub_sections)
    
    return render_template('nursing/procedures.html', topic=topic, sub_sections=sub_sections)

@app.route('/quiz/<int:topic_id>/submit', methods=['POST'])
def submit_quiz(topic_id):
    """Grades the multiple-choice quiz and returns the results page."""
    topic = Topic.query.get_or_404(topic_id)
    score = 0
    results = []
    sub_sections = topic.sub_sections
    total = len(sub_sections)

    for sub in sub_sections:
        user_answer = request.form.get(f"question_{sub.id}")
        correct_answer = sub.structured_data.get('correct')
        
        is_correct = (user_answer == correct_answer)
        if is_correct:
            score += 1
            
        results.append({
            "heading": sub.heading,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    return render_template('nursing/quiz_results.html', 
                           topic=topic, 
                           score=score, 
                           total=total, 
                           results=results)

@app.route('/calculator', methods=['GET', 'POST'])
def fluid_calculator():
    """Handles Fluid Therapy, Nutritional (RER), and Emergency Drug calculations."""
    result = None
    rer_result = None
    drug_result = None
    active_tab = request.form.get('calc_type', 'fluids')

    # Emergency Drug Formulary (Concentrations & Dosages)
    formulary = {
        "Atropine": {"conc": 0.5, "dose": 0.04, "unit": "mg/kg"},
        "Epinephrine": {"conc": 1.0, "dose": 0.01, "unit": "mg/kg"},
        "Lidocaine": {"conc": 20.0, "dose": 2.0, "unit": "mg/kg"},
        "Naloxone": {"conc": 0.4, "dose": 0.04, "unit": "mg/kg"}
    }

    if request.method == 'POST':
        try:
            weight_lb = float(request.form.get('weight', 0))
            weight_kg = weight_lb / 2.2
            
            if active_tab == 'fluids':
                dehydration_pct = float(request.form.get('dehydration', 0)) / 100
                losses_ml = float(request.form.get('losses', 0))
                
                maintenance = weight_kg * 55 
                deficit = weight_kg * dehydration_pct * 1000
                total_24h = maintenance + deficit + losses_ml
                
                result = {
                    "weight_kg": round(weight_kg, 2),
                    "maintenance": round(maintenance, 2),
                    "deficit": round(deficit, 2),
                    "total": round(total_24h, 2),
                    "hourly": round(total_24h / 24, 2)
                }
            
            elif active_tab == 'rer':
                rer_kcal = 70 * (weight_kg ** 0.75)
                rer_result = {
                    "weight_kg": round(weight_kg, 2),
                    "rer_kcal": round(rer_kcal, 2),
                    "illness_factor_1_25": round(rer_kcal * 1.25, 2),
                    "illness_factor_1_5": round(rer_kcal * 1.5, 2)
                }

            elif active_tab == 'drugs':
                drug_name = request.form.get('drug_name')
                drug_info = formulary.get(drug_name)
                
                # Formula: (Weight kg * Dose mg/kg) / Concentration mg/mL = Volume mL
                total_mg = weight_kg * drug_info['dose']
                total_ml = total_mg / drug_info['conc']

                drug_result = {
                    "name": drug_name,
                    "weight_kg": round(weight_kg, 2),
                    "total_mg": round(total_mg, 3),
                    "total_ml": round(total_ml, 2),
                    "conc": drug_info['conc'],
                    "dose_rate": drug_info['dose']
                }

        except (ValueError, ZeroDivisionError):
            result = {"error": "Please enter valid numerical values."}
        
    return render_template('nursing/fluid_calc.html', 
                           result=result, 
                           rer_result=rer_result, 
                           drug_result=drug_result,
                           active_tab=active_tab,
                           formulary=formulary)

if __name__ == '__main__':
    # Wait 1 second for the server to start, then open the browser
    Timer(1, open_browser).start()
    # Run the Flask server without debug mode to prevent dual-booting in PyInstaller
    app.run(port=5000)