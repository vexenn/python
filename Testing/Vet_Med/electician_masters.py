import webbrowser
import os
import json

# Quiz Data: 50 Questions for Master Electrician Exam
quiz_data = [
    {"question": "When calculating the service for a multifamily dwelling using the optional calculation (NEC 220.84), what demand factor is applied to the nameplate rating of 12 electrical ranges?", "options": ["40%", "41%", "45%", "50%"], "answer": "41%"},
    {"question": "In a Class I, Division 1 location, conduit seals must be installed within what distance of the enclosure for an explosion-proof apparatus?", "options": ["12 inches", "18 inches", "24 inches", "36 inches"], "answer": "18 inches"},
    {"question": "For a hospital, which branch of the Essential Electrical System supplies power to task illumination and selected receptacles in critical care areas?", "options": ["Life Safety Branch", "Critical Branch", "Equipment Branch", "Emergency System"], "answer": "Critical Branch"},
    {"question": "What is the maximum overcurrent protection for a 480V primary, 3-phase transformer with 6% impedance, where the secondary protection is not provided?", "options": ["125%", "250%", "300%", "600%"], "answer": "300%"},
    {"question": "Calculate the total load for a commercial building with 100 general purpose receptacles. (First 10 kVA at 100%, remainder at 50%).", "options": ["9,000 VA", "10,000 VA", "14,000 VA", "18,000 VA"], "answer": "14,000 VA"},
    {"question": "In an isolated power system for a hospital operating room, the line isolation monitor must alarm when the total hazard current exceeds:", "options": ["2 mA", "3.7 mA", "5 mA", "6 mA"], "answer": "5 mA"},
    {"question": "When calculating the feeder load for show windows, the load must be calculated at:", "options": ["150 VA per linear foot", "200 VA per linear foot", "180 VA per outlet", "200 watts per linear foot"], "answer": "200 VA per linear foot"},
    {"question": "The disconnecting means for a 480V motor controller must be within sight and within what distance of the motor?", "options": ["25 feet", "50 feet", "75 feet", "100 feet"], "answer": "50 feet"},
    {"question": "According to NEC 430.24, conductors supplying several motors must have an ampacity equal to the sum of the full-load current ratings of all the motors plus what percentage of the highest rated motor?", "options": ["25%", "50%", "100%", "125%"], "answer": "25%"},
    {"question": "What is the minimum size copper grounding electrode conductor for a service with 500 kcmil copper service-entrance conductors?", "options": ["4 AWG", "2 AWG", "1/0 AWG", "2/0 AWG"], "answer": "1/0 AWG"},
    {"question": "A 3-phase, 4-wire, wye-connected system usually has a voltage of:", "options": ["120/240V", "277/480V", "240/480V", "480/600V"], "answer": "277/480V"},
    {"question": "What is the demand factor for a non-dwelling unit receptacle load greater than 10 kVA?", "options": ["40%", "50%", "70%", "80%"], "answer": "50%"},
    {"question": "Which NEC table is used to determine the Full-Load Current (FLC) of a 3-phase AC motor?", "options": ["Table 430.247", "Table 430.248", "Table 430.250", "Table 430.52"], "answer": "Table 430.250"},
    {"question": "In a photovoltaic system, rapid shutdown initiation devices must be located at:", "options": ["The array only", "The inverter only", "Readily accessible locations", "The utility meter"], "answer": "Readily accessible locations"},
    {"question": "For a school building, the optional calculation method allows the lighting load to be calculated at how many VA per square foot?", "options": ["1.2 VA", "3 VA", "4.5 VA", "Based on actual connected load"], "answer": "Based on actual connected load"},
    {"question": "Mobile home service equipment must be rated not less than:", "options": ["50 Amps", "60 Amps", "100 Amps", "125 Amps"], "answer": "100 Amps"},
    {"question": "A transformer vault door must have a fire rating of at least:", "options": ["1 hour", "2 hours", "3 hours", "4 hours"], "answer": "3 hours"},
    {"question": "The ampacity of a capacitor circuit conductor must be at least what percentage of the rated current of the capacitor?", "options": ["100%", "125%", "135%", "150%"], "answer": "135%"},
    {"question": "When connecting two or more generators in parallel, which condition is NOT required?", "options": ["Same voltage", "Same frequency", "Same phase sequence", "Same amperage rating"], "answer": "Same amperage rating"},
    {"question": "According to NEC 230.95, Ground-Fault Protection of Equipment (GFPE) is required for solidly grounded wye electrical services of more than 150 volts to ground but not exceeding 600 volts phase-to-phase for each service disconnect rated at:", "options": ["400 Amps or more", "800 Amps or more", "1000 Amps or more", "1200 Amps or more"], "answer": "1000 Amps or more"},
    {"question": "What is the maximum setting for the ground-fault protection of equipment (GFPE)?", "options": ["1000 Amps", "1200 Amps", "3000 Amps", "4000 Amps"], "answer": "1200 Amps"},
    {"question": "For calculating the neutral load on a feeder supplying electric ranges, the maximum unbalanced load is considered to be what percentage of the load?", "options": ["40%", "50%", "70%", "100%"], "answer": "70%"},
    {"question": "Under the optional method for multifamily dwellings, house loads are calculated at what demand factor?", "options": ["75%", "80%", "90%", "100%"], "answer": "100%"},
    {"question": "The maximum number of disconnects for a service is:", "options": ["1", "3", "6", "10"], "answer": "6"},
    {"question": "In an agricultural building, what type of cable is specifically permitted for wet and corrosive environments?", "options": ["Type NM", "Type UF", "Type AC", "Type MC"], "answer": "Type UF"},
    {"question": "Emergency system wiring must be kept entirely independent of all other wiring and equipment unless:", "options": ["In transfer switches", "In junction boxes", "Using the same raceway", "Bundled with cable ties"], "answer": "In transfer switches"},
    {"question": "A legally required standby system must be able to supply power within:", "options": ["10 seconds", "30 seconds", "60 seconds", "90 minutes"], "answer": "60 seconds"},
    {"question": "An emergency system must be able to supply power within:", "options": ["10 seconds", "30 seconds", "60 seconds", "2 hours"], "answer": "10 seconds"},
    {"question": "What is the multiplier for the current of an arc welder with a 50% duty cycle?", "options": [".71", ".75", ".80", ".85"], "answer": ".71"},
    {"question": "When conductors are installed in parallel (electrically joined at both ends), the minimum size is:", "options": ["1/0 AWG", "2/0 AWG", "4/0 AWG", "250 kcmil"], "answer": "1/0 AWG"},
    {"question": "For a marina, the service load calculation allows a demand factor of 40% only if there are how many shore power receptacles?", "options": ["9-15", "16-50", "51-70", "71 or more"], "answer": "71 or more"},
    {"question": "Which article applies to Fire Alarm Systems?", "options": ["Article 700", "Article 725", "Article 760", "Article 770"], "answer": "Article 760"},
    {"question": "A motor controller enclosure in a Class I, Division 1 location must be:", "options": ["Dusttight", "Raintight", "Explosionproof", "General Purpose"], "answer": "Explosionproof"},
    {"question": "The phase converter disconnect must be rated at not less than what percentage of the single-phase input full-load amperage?", "options": ["115%", "125%", "150%", "200%"], "answer": "115%"},
    {"question": "In a bulk storage plant, the area within 3 feet of a fill pipe connection is classified as:", "options": ["Class I, Division 1", "Class I, Division 2", "Class II, Division 1", "Unclassified"], "answer": "Class I, Division 1"},
    {"question": "What is the maximum voltage drop allowed for a sensitive electronic equipment branch circuit?", "options": ["1.5%", "2%", "3%", "5%"], "answer": "1.5%"},
    {"question": "Which of the following determines the specific classification of a hazardous location?", "options": ["Temperature and Pressure", "Properties of the flammable materials present", "Voltage of the equipment", "Amperage of the circuit"], "answer": "Properties of the flammable materials present"},
    {"question": "High-voltage cables (over 600V) in a tunnel must be supported at intervals not exceeding:", "options": ["4 feet", "6 feet", "8 feet", "10 feet"], "answer": "8 feet"},
    {"question": "Neon tubing exceeding 1000V shall not be installed in:", "options": ["Commercial signs", "Dwelling units", "Theaters", "Parking garages"], "answer": "Dwelling units"},
    {"question": "When sizing a generator for a fire pump, the voltage drop at the motor terminals during starting must not exceed:", "options": ["5%", "10%", "15%", "20%"], "answer": "15%"},
    {"question": "Where an AC system operating at less than 1000V is grounded, the grounding electrode conductor shall be connected to the grounded service conductor at:", "options": ["The meter socket only", "The load side of the service disconnect", "Any accessible point from the load to the service point", "The transformer only"], "answer": "Any accessible point from the load to the service point"},
    {"question": "For X-ray equipment, the ampacity of supply branch-circuit conductors and the current rating of overcurrent protective devices shall not be less than ___ of the momentary rating or ___ of the long-time rating, whichever is greater.", "options": ["50%, 100%", "60%, 125%", "40%, 80%", "125%, 150%"], "answer": "50%, 100%"},
    {"question": "Cranes and hoists: The dimension of the working space in the direction of access to live parts operating at 600V or less shall be a minimum of:", "options": ["2.5 feet", "3 feet", "4 feet", "6 feet"], "answer": "2.5 feet"},
    {"question": "Calculated load for heavy-duty track lighting is:", "options": ["150 VA per foot", "180 VA per foot", "600 VA per foot", "1200 VA per foot"], "answer": "600 VA per foot"},
    {"question": "For a rectifier-type welder, the ampacity of the supply conductors shall not be less than the rated primary current multiplied by the multiplier in Table 630.11(A) based on:", "options": ["Duty cycle", "Arc voltage", "Power factor", "Temperature rise"], "answer": "Duty cycle"},
    {"question": "Which article covers Critical Operations Power Systems (COPS)?", "options": ["Article 700", "Article 701", "Article 702", "Article 708"], "answer": "Article 708"},
    {"question": "Conduit bodies are also known as:", "options": ["Junction boxes", "Condulets", "Handholes", "Pull boxes"], "answer": "Condulets"},
    {"question": "Underground conductors for a 240V landscape lighting system under a driveway (one-family dwelling) must have a minimum cover of:", "options": ["12 inches", "18 inches", "24 inches", "30 inches"], "answer": "18 inches"},
    {"question": "The operational test for a GFCI receptacle should be performed how often?", "options": ["Daily", "Weekly", "Monthly", "Annually"], "answer": "Monthly"},
    {"question": "In a recreational vehicle park, what percentage of sites must be equipped with 50-ampre, 120/240-volt receptacles?", "options": ["5%", "20%", "50%", "100%"], "answer": "20%"}
]

# Use a standard template to avoid f-string curly brace confusion
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Master Electrician Exam Prep</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #eef2f3; padding: 20px; }
        .container { max-width: 900px; margin: auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; border-bottom: 3px solid #8e44ad; padding-bottom: 10px; }
        .nav-buttons { text-align: center; margin-bottom: 30px; }
        .nav-buttons button { display: inline-block; width: auto; margin: 5px; padding: 10px 20px; font-size: 16px; background: #34495e; color: white; border: none; border-radius: 8px; cursor: pointer; }
        .q-block { border-bottom: 1px solid #eee; padding: 20px 0; }
        .q-text { font-size: 18px; font-weight: 600; margin-bottom: 15px; color: #34495e; }
        .opt { display: block; margin: 8px 0; cursor: pointer; padding: 10px; border: 1px solid #ddd; border-radius: 6px; transition: 0.2s; }
        .opt:hover { background: #f3e5f5; border-color: #8e44ad; }
        #flashcard-container { display: none; text-align: center; padding: 50px 20px; min-height: 300px; }
        .card { background: #fff; border: 2px solid #8e44ad; border-radius: 15px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .card-q { font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px; }
        .card-a { font-size: 22px; color: #27ae60; font-weight: bold; display: none; margin-top: 30px; border-top: 2px dashed #eee; padding-top: 20px; }
        button { display: block; width: 100%; padding: 15px; background: #8e44ad; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight:bold; cursor: pointer; margin-top: 20px; }
        button:hover { background: #6c3483; }
        .secondary-btn { background: #95a5a6 !important; color: white !important; width: 30% !important; display: inline-block !important; margin: 5px; }
        #score-box { text-align: center; font-size: 24px; font-weight: bold; margin-top: 30px; color: #2c3e50; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Master Electrician Exam Prep</h1>
        <div class="nav-buttons">
            <button onclick="showMode('quiz')">Quiz Mode</button>
            <button onclick="showMode('flashcards')">Flashcard Mode</button>
        </div>
        
        <div id="quiz-section">
            <div id="quiz-root"></div>
            <button id="submit-btn" onclick="checkAnswers()">Submit and Grade My Test</button>
            <button id="restart-btn" style="display:none; background:#27ae60; color:white;" onclick="startQuiz()">Reshuffle & Restart Quiz</button>
            <div id="score-box"></div>
        </div>

        <div id="flashcard-container">
            <div class="card">
                <div id="card-count" style="color: #7f8c8d; margin-bottom: 10px;"></div>
                <div class="card-q" id="display-q"></div>
                <button onclick="toggleCardAnswer()" style="background: #34495e; color:white; width: auto; margin: auto; padding: 10px 20px;">Show / Hide Answer</button>
                <div class="card-a" id="display-a"></div>
            </div>
            <div style="text-align: center;">
                <button class="secondary-btn" onclick="prevCard()">Previous</button>
                <button class="secondary-btn" onclick="markMastered()" style="background: #27ae60 !important;">Mastered!</button>
                <button class="secondary-btn" onclick="nextCard()">Next</button>
            </div>
        </div>
    </div>

    <script>
        let allData = JSON_DATA_PLACEHOLDER;
        let activeCards = [...allData];
        let currentCardIndex = 0;

        function shuffle(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        }

        function showMode(mode) {
            if (mode === 'quiz') {
                document.getElementById('quiz-section').style.display = 'block';
                document.getElementById('flashcard-container').style.display = 'none';
                startQuiz();
            } else {
                document.getElementById('quiz-section').style.display = 'none';
                document.getElementById('flashcard-container').style.display = 'block';
                activeCards = [...allData];
                shuffle(activeCards);
                currentCardIndex = 0;
                updateFlashcard();
            }
        }

        function startQuiz() {
            window.scrollTo(0,0);
            document.getElementById('score-box').innerHTML = "";
            document.getElementById('restart-btn').style.display = "none";
            document.getElementById('submit-btn').style.display = "block";
            
            shuffle(allData);
            const root = document.getElementById('quiz-root');
            root.innerHTML = "";

            allData.forEach((q, i) => {
                let opts = shuffle([...q.options]);
                let html = `<div class="q-block" id="block-${i}"><div class="q-text">${i+1}. ${q.question}</div>`;
                opts.forEach(opt => {
                    html += `<label class="opt"><input type="radio" name="q${i}" value="${opt}"> ${opt}</label>`;
                });
                html += `<div id="ans-${i}" style="display:none; margin-top:10px; font-weight:bold;"></div></div>`;
                root.innerHTML += html;
            });
        }

        function checkAnswers() {
            let score = 0;
            allData.forEach((q, i) => {
                const selected = document.querySelector(`input[name="q${i}"]:checked`);
                const feedback = document.getElementById(`ans-${i}`);
                feedback.style.display = "block";
                
                if(selected && selected.value === q.answer) {
                    score++; feedback.innerHTML = "✓ Correct"; feedback.style.color = "green";
                } else {
                    feedback.innerHTML = "✗ Incorrect. Correct: " + q.answer; feedback.style.color = "red";
                }
            });
            document.getElementById('score-box').innerHTML = "Final Score: " + score + " / " + allData.length;
            document.getElementById('submit-btn').style.display = "none";
            document.getElementById('restart-btn').style.display = "block";
            window.scrollTo(0, document.body.scrollHeight);
        }

        function updateFlashcard() {
            if (activeCards.length === 0) {
                document.getElementById('display-q').innerText = "All cards mastered!";
                document.getElementById('display-a').style.display = 'none';
                return;
            }
            document.getElementById('display-q').innerText = activeCards[currentCardIndex].question;
            document.getElementById('display-a').innerText = activeCards[currentCardIndex].answer;
            document.getElementById('display-a').style.display = 'none';
            document.getElementById('card-count').innerText = `Card ${currentCardIndex + 1} / ${activeCards.length}`;
        }

        function toggleCardAnswer() {
            const a = document.getElementById('display-a');
            a.style.display = a.style.display === 'none' ? 'block' : 'none';
        }

        function markMastered() {
            if(activeCards.length === 0) return;
            activeCards.splice(currentCardIndex, 1);
            if (currentCardIndex >= activeCards.length) currentCardIndex = 0;
            updateFlashcard();
        }

        function nextCard() { 
            if(activeCards.length === 0) return;
            currentCardIndex = (currentCardIndex + 1) % activeCards.length; 
            updateFlashcard(); 
        }

        function prevCard() { 
            if(activeCards.length === 0) return;
            currentCardIndex = (currentCardIndex - 1 + activeCards.length) % activeCards.length; 
            updateFlashcard(); 
        }

        startQuiz();
    </script>
</body>
</html>
"""

# Inject data safely
final_html = html_template.replace("JSON_DATA_PLACEHOLDER", json.dumps(quiz_data))

file_path = "master_electrician_exam.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_html)

webbrowser.open("file://" + os.path.abspath(file_path))
print(f"Success! Master Exam Suite opened from: {file_path}")