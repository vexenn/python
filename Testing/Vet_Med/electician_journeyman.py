import webbrowser
import os
import json

# Quiz Data: 50 Questions for Journeyman Electrician Exam
quiz_data = [
    {"question": "What is the maximum recommended voltage drop for a combined feeder and branch circuit?", "options": ["2%", "3%", "5%", "10%"], "answer": "5%"},
    {"question": "Which NEC Article covers the requirements for Grounding and Bonding?", "options": ["Article 210", "Article 240", "Article 250", "Article 310"], "answer": "Article 250"},
    {"question": "What is the maximum number of 12 AWG conductors allowed in a 4 x 4 x 1-1/2 inch square metal box?", "options": ["9", "10", "13", "15"], "answer": "9"},
    {"question": "According to NEC 210.52, receptacle outlets in a dwelling unit wall space must be spaced so that no point along the floor line is more than how far from an outlet?", "options": ["4 feet", "6 feet", "10 feet", "12 feet"], "answer": "6 feet"},
    {"question": "When sizing motor overload protection for a motor with a service factor of 1.15, the device should be selected to trip at no more than what percentage of the nameplate full-load current?", "options": ["100%", "115%", "125%", "140%"], "answer": "125%"},
    {"question": "What is the minimum working space clearance depth for equipment operating at 480V with exposed live parts on one side and grounded parts on the other (Condition 2)?", "options": ["3 feet", "3.5 feet", "4 feet", "5 feet"], "answer": "3.5 feet"},
    {"question": "Conductors for a continuous load must be sized at what percentage of the continuous load current?", "options": ["80%", "100%", "125%", "150%"], "answer": "125%"},
    {"question": "Which table is used to determine the ampacity of insulated conductors rated 0-2000 volts?", "options": ["Table 250.66", "Table 310.15(B)(16) (formerly 310.16)", "Table 430.248", "Chapter 9 Table 1"], "answer": "Table 310.15(B)(16) (formerly 310.16)"},
    {"question": "How many degrees of bends are allowed in a single run of conduit between pull points?", "options": ["180 degrees", "270 degrees", "360 degrees", "450 degrees"], "answer": "360 degrees"},
    {"question": "What is the minimum size copper grounding electrode conductor required for a 200A service fed by 3/0 AWG copper conductors?", "options": ["8 AWG", "6 AWG", "4 AWG", "2 AWG"], "answer": "4 AWG"},
    {"question": "A 10 HP, 3-phase, 230V motor has a Full Load Amperage (FLA) of 28A. What is the minimum ampacity for the branch circuit conductors?", "options": ["28 A", "35 A", "40 A", "50 A"], "answer": "35 A"},
    {"question": "In a residential garage, at least one 120-volt, 20-ampere branch circuit must be installed to supply receptacle outlets. This circuit generally cannot supply outlets:", "options": ["Inside the house", "Outside the garage", "In the attic", "In the basement"], "answer": "Outside the garage"},
    {"question": "For a single-family dwelling, the service disconnecting means must have a rating of not less than:", "options": ["60 Amps", "100 Amps", "150 Amps", "200 Amps"], "answer": "100 Amps"},
    {"question": "What is the volume allowance required per 14 AWG conductor in a box fill calculation?", "options": ["1.5 cubic inches", "2.0 cubic inches", "2.25 cubic inches", "2.5 cubic inches"], "answer": "2.0 cubic inches"},
    {"question": "What is the volume allowance required per 12 AWG conductor in a box fill calculation?", "options": ["2.0 cubic inches", "2.25 cubic inches", "2.5 cubic inches", "3.0 cubic inches"], "answer": "2.25 cubic inches"},
    {"question": "When applying the general lighting load for a dwelling unit, what is the unit load per square foot?", "options": ["1.5 VA", "2.0 VA", "3.0 VA", "4.5 VA"], "answer": "3.0 VA"},
    {"question": "Which NEC article covers Solar Photovoltaic (PV) Systems?", "options": ["Article 680", "Article 690", "Article 700", "Article 702"], "answer": "Article 690"},
    {"question": "What is the standard frequency of AC power in the US?", "options": ["50 Hz", "60 Hz", "120 Hz", "400 Hz"], "answer": "60 Hz"},
    {"question": "If you have three 10-ohm resistors in parallel, what is the total resistance?", "options": ["3.33 Ohms", "10 Ohms", "30 Ohms", "33 Ohms"], "answer": "3.33 Ohms"},
    {"question": "According to NEC 300.4(A)(1), holes bored in wood framing members must be at least how far from the nearest edge?", "options": ["1 inch", "1-1/4 inches", "1-1/2 inches", "2 inches"], "answer": "1-1/4 inches"},
    {"question": "If a hole in a framing member is closer than 1-1/4 inches to the edge, what must be installed?", "options": ["A conduit sleeve", "A steel plate (nail plate)", "A warning label", "A GFCI"], "answer": "A steel plate (nail plate)"},
    {"question": "Which type of conduit is known as 'Rigid Metal Conduit'?", "options": ["EMT", "RMC", "PVC", "FMC"], "answer": "RMC"},
    {"question": "What is the maximum distance from a box that EMT must be supported?", "options": ["1 foot", "3 feet", "5 feet", "6 feet"], "answer": "3 feet"},
    {"question": "The 'high leg' of a 120/240V, 3-phase, 4-wire delta system must be marked with which color?", "options": ["Black", "Red", "Blue", "Orange"], "answer": "Orange"},
    {"question": "The high leg in a delta system is typically measuring what voltage to ground?", "options": ["120V", "208V", "240V", "277V"], "answer": "208V"},
    {"question": "A general-purpose receptacle in a commercial building is calculated at how many VA per outlet?", "options": ["150 VA", "180 VA", "200 VA", "360 VA"], "answer": "180 VA"},
    {"question": "Which Article governs Temporary Installations?", "options": ["Article 525", "Article 590", "Article 600", "Article 620"], "answer": "Article 590"},
    {"question": "What is the maximum overcurrent protection allowed for 14 AWG copper wire (unless specific motor/hvac exceptions apply)?", "options": ["10 Amps", "15 Amps", "20 Amps", "25 Amps"], "answer": "15 Amps"},
    {"question": "What is the maximum overcurrent protection for 12 AWG copper wire?", "options": ["15 Amps", "20 Amps", "25 Amps", "30 Amps"], "answer": "20 Amps"},
    {"question": "What is the maximum overcurrent protection for 10 AWG copper wire?", "options": ["20 Amps", "25 Amps", "30 Amps", "40 Amps"], "answer": "30 Amps"},
    {"question": "Under the optional method for a single-family dwelling, the first 10 kVA of load is calculated at what percentage?", "options": ["40%", "50%", "80%", "100%"], "answer": "100%"},
    {"question": "In a Class I, Division 1 location, which wiring method is typically required?", "options": ["EMT with set screw connectors", "Threaded Rigid Metal Conduit", "PVC Schedule 40", "NM Cable"], "answer": "Threaded Rigid Metal Conduit"},
    {"question": "When calculating the service load for a dryer, what is the minimum VA rating you must use?", "options": ["3000 VA", "4000 VA", "5000 VA", "6000 VA"], "answer": "5000 VA"},
    {"question": "What is the smallest size wire allowed for a service-entrance conductor?", "options": ["10 AWG", "8 AWG", "6 AWG", "4 AWG"], "answer": "8 AWG"},
    {"question": "Which NEC Article covers Swimming Pools, Fountains, and Similar Installations?", "options": ["Article 680", "Article 682", "Article 700", "Article 725"], "answer": "Article 680"},
    {"question": "AC Cable (Armored Cable) must be supported within what distance of a box?", "options": ["6 inches", "12 inches", "18 inches", "24 inches"], "answer": "12 inches"},
    {"question": "Liquidtight Flexible Metal Conduit (LFMC) is limited to what length when used for flexibility at equipment connections?", "options": ["3 feet", "4 feet", "6 feet", "10 feet"], "answer": "6 feet"},
    {"question": "Which color is strictly reserved for the Equipment Grounding Conductor?", "options": ["White", "Gray", "Green (or bare)", "Black"], "answer": "Green (or bare)"},
    {"question": "In a 3-wire, single-phase 120/240V system, how many ungrounded conductors are there?", "options": ["One", "Two", "Three", "Four"], "answer": "Two"},
    {"question": "What is the multiplier for current when calculating the power in a 3-phase circuit (P = E x I x ...)?", "options": ["1.414", "1.732", "2.0", "3.14"], "answer": "1.732"},
    {"question": "Auxiliary gutters must not extend greater than how many feet beyond the equipment they supplement?", "options": ["10 feet", "20 feet", "30 feet", "50 feet"], "answer": "30 feet"},
    {"question": "A switch controlling a lighting load must be grounded. If a snap switch is replaced where no grounding means exists, it must be replaced with:", "options": ["A non-metallic faceplate and non-grounding switch", "A metal faceplate", "A GFCI breaker", "An AFCI breaker"], "answer": "A non-metallic faceplate and non-grounding switch"},
    {"question": "Small appliance branch circuits in a dwelling unit must be rated at:", "options": ["15 Amps", "20 Amps", "30 Amps", "50 Amps"], "answer": "20 Amps"},
    {"question": "How many small appliance branch circuits are required minimum in a dwelling kitchen area?", "options": ["One", "Two", "Three", "Four"], "answer": "Two"},
    {"question": "Track lighting load is calculated at 150 VA for every ___ feet of track.", "options": ["1 foot", "2 feet", "4 feet", "5 feet"], "answer": "2 feet"},
    {"question": "Which hazardous location classification involves combustible dust?", "options": ["Class I", "Class II", "Class III", "Class IV"], "answer": "Class II"},
    {"question": "Underground service conductors installed in RMC must have a minimum cover depth of:", "options": ["6 inches", "12 inches", "18 inches", "24 inches"], "answer": "6 inches"},
    {"question": "Direct buried UF cable generally requires a minimum cover depth of:", "options": ["12 inches", "18 inches", "24 inches", "30 inches"], "answer": "24 inches"},
    {"question": "What is the minimum size required for the main bonding jumper in a service?", "options": ["Based on service entrance conductor size (Table 250.102(C)(1))", "Always 4 AWG", "Always 1/0 AWG", "Same size as grounding electrode conductor"], "answer": "Based on service entrance conductor size (Table 250.102(C)(1))"},
    {"question": "A bathroom receptacle outlet must be on a separate 20A circuit unless:", "options": ["It also supplies the hallway", "The circuit supplies only that bathroom's outlets and lights", "The house is less than 1000 sq ft", "The receptacle is GFCI type"], "answer": "The circuit supplies only that bathroom's outlets and lights"}
]

# Use a standard template to avoid f-string curly brace confusion
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Journeyman Electrician Exam Prep</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #eef2f3; padding: 20px; }
        .container { max-width: 900px; margin: auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; border-bottom: 3px solid #e67e22; padding-bottom: 10px; }
        .nav-buttons { text-align: center; margin-bottom: 30px; }
        .nav-buttons button { display: inline-block; width: auto; margin: 5px; padding: 10px 20px; font-size: 16px; background: #34495e; color: white; border: none; border-radius: 8px; cursor: pointer; }
        .q-block { border-bottom: 1px solid #eee; padding: 20px 0; }
        .q-text { font-size: 18px; font-weight: 600; margin-bottom: 15px; color: #34495e; }
        .opt { display: block; margin: 8px 0; cursor: pointer; padding: 10px; border: 1px solid #ddd; border-radius: 6px; transition: 0.2s; }
        .opt:hover { background: #fff3e0; border-color: #e67e22; }
        #flashcard-container { display: none; text-align: center; padding: 50px 20px; min-height: 300px; }
        .card { background: #fff; border: 2px solid #e67e22; border-radius: 15px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .card-q { font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px; }
        .card-a { font-size: 22px; color: #27ae60; font-weight: bold; display: none; margin-top: 30px; border-top: 2px dashed #eee; padding-top: 20px; }
        button { display: block; width: 100%; padding: 15px; background: #e67e22; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight:bold; cursor: pointer; margin-top: 20px; }
        button:hover { background: #d35400; }
        .secondary-btn { background: #95a5a6 !important; color: white !important; width: 30% !important; display: inline-block !important; margin: 5px; }
        #score-box { text-align: center; font-size: 24px; font-weight: bold; margin-top: 30px; color: #2c3e50; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Journeyman Electrician Exam Prep</h1>
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

file_path = "journeyman_exam_tool.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_html)

webbrowser.open("file://" + os.path.abspath(file_path))
print(f"Success! Journeyman Exam Suite opened from: {file_path}")