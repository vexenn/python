import os
import sys
from flask import Flask, render_template, jsonify, request

# This logic tells Flask where to find your files when running as a .exe
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

# COMPREHENSIVE QUIZ DATABASE: 50 Questions mapped to Syllabus SLOs
quiz_data = [
    # WEEKS 1-2: DOSAGE & METRIC (Questions 1-10)
    {
        "id": 1, "week": "1-2", "category": "Dosage (Unit Mismatch)", 
        "question": "DVM orders 0.5mg/kg of a drug for a 10lb dog. Conc is 500mcg/mL. How many mL?",
        "answer": 4.5,
        "explanation": "1. 10lb / 2.2 = 4.54kg\n2. 4.54kg * 0.5mg/kg = 2.27mg\n3. 500mcg = 0.5mg\n4. 2.27mg / 0.5mg/mL = 4.54mL."
    },
    {
        "id": 2, "week": "1-2", "category": "Apothecary Conversion", 
        "question": "A patient needs 1/2 grain of Aspirin. 1 grain = 64.8mg. How many mg is this?",
        "answer": 32.4,
        "explanation": "64.8mg / 2 = 32.4mg."
    },
    {
        "id": 3, "week": "1-2", "category": "Dosage", 
        "question": "A 55lb dog needs 5mg/kg of a drug. Available as 25mg tablets. How many tablets?",
        "answer": 5,
        "explanation": "1. 55lb / 2.2 = 25kg\n2. 25kg * 5mg/kg = 125mg\n3. 125mg / 25mg = 5 tablets."
    },
    {
        "id": 4, "week": "1-2", "category": "Unit Conversion", 
        "question": "Convert 0.04 grams to micrograms (mcg).",
        "answer": 40000,
        "explanation": "1. 0.04g * 1000 = 40mg\n2. 40mg * 1000 = 40,000mcg."
    },
    {
        "id": 5, "week": "1-2", "category": "Dosage", 
        "question": "A 4kg cat needs 22mg/kg of an antibiotic (100mg/mL). Volume?",
        "answer": 0.88,
        "explanation": "4kg * 22mg/kg = 88mg. 88mg / 100mg/mL = 0.88mL."
    },
    {
        "id": 6, "week": "1-2", "category": "Dosage", 
        "question": "Order: 15mg/kg for a 3kg kitten. Conc: 50mg/mL. Volume?",
        "answer": 0.9,
        "explanation": "3kg * 15mg/kg = 45mg. 45mg / 50mg/mL = 0.9mL."
    },
    {
        "id": 7, "week": "1-2", "category": "Dosage", 
        "question": "A 12lb cat needs 10mg/kg of a suspension (100mg/5mL). Volume?",
        "answer": 2.7,
        "explanation": "1. 12lb / 2.2 = 5.45kg\n2. 5.45kg * 10mg/kg = 54.5mg\n3. (54.5mg / 100mg) * 5mL = 2.72mL."
    },
    {
        "id": 8, "week": "1-2", "category": "Dosage", 
        "question": "A 110lb dog needs 0.5mg/kg of a 25mg/mL drug. Volume?",
        "answer": 1,
        "explanation": "1. 110lb / 2.2 = 50kg\n2. 50kg * 0.5mg/kg = 25mg\n3. 25mg / 25mg/mL = 1mL."
    },
    {
        "id": 9, "week": "1-2", "category": "Dosage", 
        "question": "A 15kg dog needs 20mg/kg of a drug available in 100mg scored tablets. How many tablets?",
        "answer": 3,
        "explanation": "15kg * 20mg/kg = 300mg. 300mg / 100mg = 3 tablets."
    },
    {
        "id": 10, "week": "1-2", "category": "Dosage", 
        "question": "Order: 0.2mg/kg for a 5kg cat. Conc: 0.5mg/mL. Volume?",
        "answer": 2,
        "explanation": "5kg * 0.2mg/kg = 1mg. 1mg / 0.5mg/mL = 2mL."
    },

    # WEEK 3: DILUTIONS & PERCENTAGES (Questions 11-20)
    {
        "id": 11, "week": 3, "category": "Dilutions", 
        "question": "A 2.5% solution contains how many mg per mL?",
        "answer": 25,
        "explanation": "Shortcut: Multiply percentage by 10. 2.5% * 10 = 25mg/mL."
    },
    {
        "id": 12, "week": 3, "category": "Dilutions", 
        "question": "Make 250mL of a 2% solution from a 20% stock. mL of stock needed?",
        "answer": 25,
        "explanation": "C1V1 = C2V2. (20)(V1) = (2)(250). V1 = 500 / 20 = 25mL."
    },
    {
        "id": 13, "week": 3, "category": "Dilutions", 
        "question": "How much 50% Dextrose is needed to make 500mL of a 5% Dextrose solution?",
        "answer": 50,
        "explanation": "(50)(V1) = (5)(500). V1 = 2500 / 50 = 50mL."
    },
    {
        "id": 14, "week": 3, "category": "Dilutions", 
        "question": "You have 100mg/mL stock. You need 50mL of a 10mg/mL dilution. mL of stock?",
        "answer": 5,
        "explanation": "(100)(V1) = (10)(50). V1 = 500 / 100 = 5mL."
    },
    {
        "id": 15, "week": 3, "category": "Dilutions", 
        "question": "How many grams are in 1 liter of a 0.9% NaCl solution?",
        "answer": 9,
        "explanation": "0.9% = 0.9g / 100mL. (0.9 / 100) * 1000mL = 9g."
    },
    {
        "id": 16, "week": 3, "category": "Dilutions", 
        "question": "Dilute 10mL of a 10% drug to a 2% solution. What is the final total volume?",
        "answer": 50,
        "explanation": "(10)(10) = (2)(V2). 100 = 2 * V2. V2 = 50mL."
    },
    {
        "id": 17, "week": 3, "category": "Dilutions", 
        "question": "A 1:1000 solution contains how many mg per mL?",
        "answer": 1,
        "explanation": "1:1000 = 1g/1000mL = 1000mg/1000mL = 1mg/mL."
    },
    {
        "id": 18, "week": 3, "category": "Dilutions", 
        "question": "Make 60mL of 3% hydrogen peroxide from 12% stock. mL of diluent (water) needed?",
        "answer": 45,
        "explanation": "1. (12)(V1) = (3)(60). V1 = 15mL stock. 2. 60mL total - 15mL stock = 45mL diluent."
    },
    {
        "id": 19, "week": 3, "category": "Dilutions", 
        "question": "How many mg/mL in a 0.5% solution?",
        "answer": 5,
        "explanation": "0.5% * 10 = 5mg/mL."
    },
    {
        "id": 20, "week": 3, "category": "Dilutions", 
        "question": "Make 100mL of a 1:1000 solution from 1:100 stock. mL of stock?",
        "answer": 10,
        "explanation": "1:100 = 10mg/mL. 1:1000 = 1mg/mL. (10)(V1) = (1)(100). V1 = 10mL."
    },

    # WEEK 6: FLUID RATES & DEFICITS (Questions 21-30)
    {
        "id": 21, "week": 6, "category": "Fluid Rate", 
        "question": "A 10kg dog is 8% dehydrated. Calculate ONLY the replacement deficit (mL).",
        "answer": 800,
        "explanation": "% Dehydrated (0.08) * Weight (10kg) * 1000 = 800mL."
    },
    {
        "id": 22, "week": 6, "category": "Fluid Rate", 
        "question": "20kg dog, maint rate 50mL/kg/day. gtt/min using a 15gtt/mL set?",
        "answer": 10,
        "explanation": "1. 20*50 = 1000mL/day. 2. 1000 / 1440 min = 0.69 mL/min. 3. 0.69 * 15 = 10.4 gtt/min."
    },
    {
        "id": 23, "week": 6, "category": "Fluid Rate", 
        "question": "5kg cat, 10% dehydrated. Calculate replacement deficit (mL) to be given over 24 hours.",
        "answer": 500,
        "explanation": "0.10 * 5kg * 1000 = 500mL."
    },
    {
        "id": 24, "week": 6, "category": "Fluid Rate", 
        "question": "TotalDaily: Maint (600mL) + Deficit (400mL). mL/hr over 24 hours?",
        "answer": 42,
        "explanation": "(600+400) / 24 = 41.66 mL/hr."
    },
    {
        "id": 25, "week": 6, "category": "Fluid Rate", 
        "question": "Drip rate for 1000mL over 8 hours using a 20gtt/mL set?",
        "answer": 42,
        "explanation": "1. 1000 / 480 min = 2.08 mL/min. 2. 2.08 * 20 = 41.6 gtt/min."
    },
    {
        "id": 26, "week": 6, "category": "Fluid Rate", 
        "question": "2kg puppy, 4mL/kg/hr rate. Drip rate in gtt/min using microdrip (60gtt/mL)?",
        "answer": 8,
        "explanation": "1. 2kg * 4mL = 8mL/hr. 2. 8mL / 60 min = 0.133 mL/min. 3. 0.133 * 60 = 8 gtt/min."
    },
    {
        "id": 27, "week": 6, "category": "Fluid Rate", 
        "question": "30kg dog, 7% dehydrated. Replace deficit over 12 hours. mL/hr?",
        "answer": 175,
        "explanation": "1. 0.07 * 30 * 1000 = 2100mL. 2. 2100 / 12 = 175 mL/hr."
    },
    {
        "id": 28, "week": 6, "category": "Fluid Rate", 
        "question": "12lb cat, maint fluids 50mL/kg/day. Total daily mL?",
        "answer": 273,
        "explanation": "1. 12 / 2.2 = 5.45kg. 2. 5.45 * 50 = 272.5mL."
    },
    {
        "id": 29, "week": 6, "category": "Fluid Rate", 
        "question": "Maint (500) + Deficit (300) + OngoingLoss (100). Total mL over 24h?",
        "answer": 900,
        "explanation": "500 + 300 + 100 = 900mL."
    },
    {
        "id": 30, "week": 6, "category": "Fluid Rate", 
        "question": "Drip rate (gtt/min) for 250mL over 2 hours using 10gtt/mL set?",
        "answer": 21,
        "explanation": "1. 250 / 120 min = 2.08 mL/min. 2. 2.08 * 10 = 20.8 gtt/min."
    },

    # WEEK 8: CRI LOGIC (Questions 31-40)
    {
        "id": 31, "week": 8, "category": "CRI", 
        "question": "15mL drug added to 500mL bag. How much fluid do you remove first?",
        "answer": 15,
        "explanation": "Displacement rule: Remove same volume as drug being added."
    },
    {
        "id": 32, "week": 8, "category": "CRI", 
        "question": "10kg dog, 2mcg/kg/min dose, 100mL/hr fluid rate. 1L bag. mg to add?",
        "answer": 12,
        "explanation": "1. 1000/100 = 10hrs. 2. 2mcg*10kg*60min*10hr = 12000mcg (12mg)."
    },
    {
        "id": 33, "week": 8, "category": "CRI", 
        "question": "5kg cat, 0.1mg/kg/hr dose, 10mL/hr rate. mg in 250mL bag?",
        "answer": 12.5,
        "explanation": "1. 250/10 = 25hrs. 2. 0.1mg*5kg*25hrs = 12.5mg."
    },
    {
        "id": 34, "week": 8, "category": "CRI", 
        "question": "15kg dog, 5mcg/kg/min. 500mL bag lasts 5 hours. mg to add?",
        "answer": 22.5,
        "explanation": "5mcg * 15kg * 60min * 5hr = 22,500mcg (22.5mg)."
    },
    {
        "id": 35, "week": 8, "category": "CRI", 
        "question": "mg needed for 24h CRI: Dose 2mg/kg/day, Weight 20kg.",
        "answer": 40,
        "explanation": "2mg * 20kg = 40mg (already per day)."
    },
    {
        "id": 36, "week": 8, "category": "CRI", 
        "question": "30kg dog, Dopamine 5mcg/kg/min, Fluid 120mL/hr. 500mL bag. mg to add?",
        "answer": 37.5,
        "explanation": "1. 500/120 = 4.16hr. 2. 5mcg*30kg*60min*4.16hr = 37,440mcg (37.5mg)."
    },
    {
        "id": 37, "week": 8, "category": "CRI", 
        "question": "20kg dog, 0.5mg/kg/hr Morphine. 1L bag lasts 10 hours. mg to add?",
        "answer": 100,
        "explanation": "0.5mg * 20kg * 10hrs = 100mg."
    },
    {
        "id": 38, "week": 8, "category": "CRI", 
        "question": "8kg cat, 1mcg/kg/min. 250mL bag lasts 10 hours. mg to add?",
        "answer": 4.8,
        "explanation": "1mcg * 8kg * 60min * 10hrs = 4,800mcg (4.8mg)."
    },
    {
        "id": 39, "week": 8, "category": "CRI", 
        "question": "50kg dog, 10mcg/kg/min, 200mL/hr rate, 1L bag. mg to add?",
        "answer": 150,
        "explanation": "1. 1000/200 = 5hrs. 2. 10mcg * 50kg * 60min * 5hrs = 150,000mcg (150mg)."
    },
    {
        "id": 40, "week": 8, "category": "CRI", 
        "question": "12kg dog, 0.2mg/kg/hr Metoclopramide. 500mL bag lasts 8 hours. mg to add?",
        "answer": 19.2,
        "explanation": "0.2mg * 12kg * 8hrs = 19.2mg."
    },

    # WEEK 9: mEq & COMBINED (Questions 41-50)
    {
        "id": 41, "week": 9, "category": "mEq", 
        "question": "Add 20mEq KCl to 500mL bag. Stock is 2mEq/mL. Volume?",
        "answer": 10,
        "explanation": "20mEq / 2mEq/mL = 10mL."
    },
    {
        "id": 42, "week": 9, "category": "mEq", 
        "question": "10kg dog, 0.5mEq/kg/hr max KCl rate. Max mEq allowed per hour?",
        "answer": 5,
        "explanation": "0.5mEq * 10kg = 5mEq/hr."
    },
    {
        "id": 43, "week": 9, "category": "mEq", 
        "question": "Add 40mEq KCl to 1L bag. Stock is 2mEq/mL. Volume?",
        "answer": 20,
        "explanation": "40mEq / 2mEq/mL = 20mL."
    },
    {
        "id": 44, "week": 9, "category": "mEq", 
        "question": "5kg cat, fluids 15mL/hr. Bag has 20mEq/L KCl. mEq/hr delivered?",
        "answer": 0.3,
        "explanation": "(20mEq / 1000mL) * 15mL/hr = 0.3mEq/hr."
    },
    {
        "id": 45, "week": 9, "category": "mEq", 
        "question": "25kg dog, 30mEq/L KCl at 100mL/hr rate. mEq/kg/hr?",
        "answer": 0.12,
        "explanation": "1. (30/1000)*100 = 3mEq/hr. 2. 3 / 25kg = 0.12mEq/kg/hr. (Safe)."
    },
    {
        "id": 46, "week": 9, "category": "mEq", 
        "question": "mL of 2mEq/mL KCl to get 15mEq?",
        "answer": 7.5,
        "explanation": "15 / 2 = 7.5mL."
    },
    {
        "id": 47, "week": 9, "category": "mEq", 
        "question": "40kg dog, 40mEq/L KCl at 150mL/hr. mEq/kg/hr?",
        "answer": 0.15,
        "explanation": "1. (40/1000)*150 = 6mEq/hr. 2. 6 / 40kg = 0.15mEq/kg/hr. (Safe)."
    },
    {
        "id": 48, "week": 9, "category": "mEq", 
        "question": "Max safe mEq/hr for 12kg dog?",
        "answer": 6,
        "explanation": "0.5mEq * 12kg = 6mEq/hr."
    },
    {
        "id": 49, "week": 9, "category": "mEq", 
        "question": "Add 10mEq KCl to 250mL bag. Stock 2mEq/mL. Volume?",
        "answer": 5,
        "explanation": "10 / 2 = 5mL."
    },
    {
        "id": 50, "week": 9, "category": "mEq", 
        "question": "8kg cat, 20mEq/L KCl at 20mL/hr. mEq/kg/hr?",
        "answer": 0.05,
        "explanation": "1. (20/1000)*20 = 0.4mEq/hr. 2. 0.4 / 8kg = 0.05mEq/kg/hr."
    }
]

# COMPREHENSIVE STUDY GUIDES: The "Final Exam Cheat-Sheet" versions
study_guides = {
    "1-2": {
        "title": "Dosage & Metric Mastery",
        "content": "Precision is life in pharmacology. Instructors love to mix systems (Apothecary vs. Metric). \n\nGOTCHA: Watch for the 'lb' trap. In Vet Med, we always calculate in kg unless the dose is specifically written in mg/lb. \n\nCLINICAL PEARL: 1 grain (gr) is approx 64.8mg. If the test says 65mg or 60mg, use the specific conversion your instructor provided, but 64.8 is the VTNE standard.",
        "breakdown": "1. Convert lbs to kg (Divide by 2.2)\n2. Multiply kg by Dose (mg/kg) = Total mg needed\n3. Divide Total mg by Concentration (mg/mL) = mL to draw up",
        "example_problem": "A 44lb dog needs a sedative dosed at 0.2mg/kg. The concentration is 5mg/mL. How many mL will you draw up?",
        "example_solution": "1. 44lb / 2.2 = 20kg\n2. 20kg * 0.2mg/kg = 4mg needed\n3. 4mg / 5mg/mL = 0.8mL"
    },
    "3": {
        "title": "Dilutions & Solution Logic",
        "content": "Dilutions are about moving from a 'Stock' (concentrated) to a 'Working' (diluted) solution. \n\nGOTCHA: If the question asks for how much 'diluent' to add, subtract the stock volume from the total volume. \n\nCLINICAL PEARL: The 10x Shortcut. To convert % to mg/mL, just move the decimal one place to the right (e.g., 2% = 20mg/mL).",
        "breakdown": "C1V1 = C2V2\nC1: Concentration of Stock\nV1: Volume of Stock needed\nC2: Desired Concentration\nV2: Desired Final Volume",
        "example_problem": "You need 250mL of a 2% Chlorhexidine solution for a wound flush. You have 10% stock. How much stock and how much water do you mix?",
        "example_solution": "1. (10%)(V1) = (2%)(250mL)\n2. 10 * V1 = 500\n3. V1 = 50mL (Stock Volume)\n4. Diluent: 250mL total - 50mL stock = 200mL water"
    },
    "6": {
        "title": "Fluid Therapy: The Triple Total",
        "content": "On a final, they rarely ask for just one number. You must calculate the 'Total 24-Hour Requirement'. \n\nGOTCHA: Drip sets! Macro (10, 15, 20 gtt/mL) for large dogs; Micro (60 gtt/mL) for cats and small dogs (<7kg). \n\nCLINICAL PEARL: Skin tenting, tacky mucous membranes, and sunken eyes are your cues for % dehydration.",
        "breakdown": "Total Daily Volume = [Maintenance (60mL/kg/day)] + [Deficit (% dehyd * kg * 1000)] + [Ongoing Losses (Estimated)]",
        "example_problem": "A 20kg dog is 5% dehydrated. Maintenance is 60mL/kg/day. Calculate the mL/hr needed to cover Maint + Deficit over 24 hours.",
        "example_solution": "1. Maintenance: 20kg * 60mL = 1200mL\n2. Deficit: 0.05 * 20kg * 1000 = 1000mL\n3. Total: 1200 + 1000 = 2200mL\n4. Rate: 2200mL / 24hrs = 91.6 -> 92mL/hr"
    },
    "8": {
        "title": "Week 8: CRI Logic (The 4-Step Method)",
        "content": "Constant Rate Infusions (CRI) keep a drug at a 'steady state'. \n\nGOTCHA: The 'Time' Trap. If the fluid rate changes, the CRI concentration in the bag is no longer accurate. \n\nCLINICAL PEARL: Use the 'M-W-T' shortcut: (mg/kg/min * kg * min bag lasts) / Conc = mL to add.",
        "breakdown": "1. Time: Bag Vol / Fluid Rate = Hours bag lasts\n2. mg: Dose * Weight * 60 * Hours\n3. mL: Total mg / Concentration\n4. Safety: Subtract drug volume from bag before adding",
        "example_problem": "20kg dog, 2mcg/kg/min Fentanyl, Rate 50mL/hr, Bag 500mL. Fentanyl is 50mg/mL. How much do you add?",
        "example_solution": "1. Time: 500mL / 50mL/hr = 10 hrs\n2. mg: (2mcg * 20kg * 60min * 10hr) / 1000 = 24mg\n3. mL: 24mg / 50mg/mL = 0.48mL\n4. Displacement: Withdraw 0.48mL from bag first!"
    },
    "9": {
        "title": "mEq & Electrolyte Safety",
        "content": "Potassium (KCl) is the most common additive, but it is lethal if given too fast. \n\nGOTCHA: The 'K-Max'. Never exceed 0.5 mEq/kg/hr. If your math result is 0.6, you must slow the fluid rate or reduce the KCl. \n\nCLINICAL PEARL: Electrolytes are measured in Milliequivalents (mEq), which represent the number of available ionic charges.",
        "breakdown": "1. Calculate mEq delivered per hour: (mEq in bag / Bag Vol) * Fluid Rate\n2. Calculate mEq/kg/hr: Hourly mEq / Weight\n3. Compare to 0.5 limit",
        "example_problem": "You add 40 mEq of KCl to a 1L bag. Patient (20kg) is at 150mL/hr. Is this safe?",
        "example_solution": "1. Conc in bag: 40mEq / 1000mL = 0.04 mEq/mL\n2. Delivered/hr: 0.04 mEq/mL * 150mL/hr = 6 mEq/hr\n3. Weight check: 6 mEq / 20kg = 0.3 mEq/kg/hr\n4. Status: SAFE (0.3 < 0.5)"
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/study-guide/<week_id>')
def study_guide(week_id):
    guide = study_guides.get(week_id)
    return render_template('guide.html', guide=guide) if guide else ("Guide Not Found", 404)

@app.route('/api/questions')
def get_questions():
    return jsonify(quiz_data)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    try:
        # Sanitization: Ensure numbers are positive and non-zero
        w = max(0.001, float(data['weight']))
        d = max(0.001, float(data['dosage']))
        c = max(0.001, float(data['concentration']))
        
        res = (w * d) / c
        
        # Clinical Safety Warning
        alert = ""
        if d > 50:
            alert = "⚠️ SAFETY ALERT: This dosage is significantly high. Please verify mg vs. mcg!"
        
        return jsonify({
            "result": round(res, 2),
            "alert": alert,
            "steps": [
                f"Weight ({w}kg) × Dosage ({d}mg/kg) = {round(w*d, 2)}mg total",
                f"Total mg ({round(w*d, 2)}) ÷ Concentration ({c}mg/mL) = {round(res, 2)}mL"
            ]
        })
    except (ValueError, TypeError, ZeroDivisionError):
        return jsonify({"error": "Invalid input. Please enter numbers greater than zero."}), 400

@app.route('/api/log-entry', methods=['POST'])
def log_entry():
    data = request.json
    initials = data.get('initials', '').upper()
    if not initials:
        return jsonify({"status": "error", "message": "Legal requirement: Initials must be provided for log entries."}), 400
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    return jsonify({
        "status": "success", 
        "entry": f"[{timestamp}] {data['amount_used']}mL of {data['drug']} recorded by RVT-{initials}"
    })

if __name__ == '__main__':
    app.run(debug=True)