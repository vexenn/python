/**
 * Navigation Logic
 * Handles switching between sections and managing sidebar active states
 */
function showSection(sectionId) {
    // 1. Hide all sections
    document.querySelectorAll('section').forEach(sec => sec.classList.add('hidden'));
    
    // 2. Show the selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.remove('hidden');
    }

    // 3. Update Sidebar Active State
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('onclick')?.includes(sectionId)) {
            item.classList.add('active');
        }
    });

    // 4. Trigger specific data loading or reset timer
    if (sectionId === 'quiz') {
        loadQuiz();
    } else if (sectionId !== 'exam-sprint') {
        clearInterval(examTimer); 
    }
}

/**
 * Handle URL Parameters on Load (Deep Linking)
 */
window.onload = () => {
    const params = new URLSearchParams(window.location.search);
    const section = params.get('section');
    if (section) {
        showSection(section);
    }
};

/**
 * Filter Cheat Sheet Table
 */
function filterCheatSheet() {
    const input = document.getElementById("cheat-search").value.toLowerCase();
    const rows = document.getElementById("formula-table").getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        const text = rows[i].innerText.toLowerCase();
        rows[i].style.display = text.includes(input) ? "" : "none";
    }
}

/**
 * Step-by-Step Dose Solver
 */
async function runCalculation() {
    const weight = document.getElementById('weight').value;
    const dosage = document.getElementById('dosage').value;
    const concentration = document.getElementById('conc').value;

    if (!weight || !dosage || !concentration) {
        alert("Please fill in all fields.");
        return;
    }

    if (dosage > 100) {
        const proceed = confirm("🚨 WARNING: Dosage exceeds 100mg/kg. This is unusually high. Did you mean mcg/kg?");
        if (!proceed) return;
    }

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ weight, dosage, concentration })
        });

        const data = await response.json();
        const resultDiv = document.getElementById('solver-result');
        
        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <div class="calculation-output">
                    <h3>Final Volume: <strong>${data.result} mL</strong></h3>
                    ${data.alert ? `<p style="color: var(--warning-red); font-weight: bold;">${data.alert}</p>` : ''}
                    <hr>
                    <p><strong>Dimensional Analysis:</strong></p>
                    <ul style="list-style: none; padding: 0;">${data.steps.map(s => `<li style="margin-bottom: 5px;">✅ ${s}</li>`).join('')}</ul>
                </div>
            `;
        }
    } catch (err) {
        alert("Server error. Ensure app.py is running.");
    }
}

/**
 * Practice Quiz Module
 */
async function loadQuiz() {
    try {
        const response = await fetch('/api/questions');
        const questions = await response.json();
        const container = document.getElementById('quiz-container');
        
        container.innerHTML = questions.map(q => `
            <div class="quiz-card">
                <span class="week-tag">Week ${q.week}</span>
                <p><strong>${q.category}:</strong> ${q.question}</p>
                <div class="quiz-actions">
                    <input type="number" step="any" placeholder="Your Answer" id="ans-${q.id}">
                    <button onclick="checkQuizAnswer(${q.id}, ${q.answer}, '${q.explanation.replace(/'/g, "\\'")}')">Submit</button>
                </div>
                <div id="feedback-${q.id}" class="quiz-feedback"></div>
            </div>
        `).join('');
    } catch (err) {
        console.error("Quiz load error:", err);
    }
}

/**
 * Medical Record Simulator
 */
async function submitLog() {
    const drug = document.getElementById('log-drug').value;
    const amount_used = document.getElementById('log-amount').value;
    const initials = document.getElementById('log-initials').value;

    try {
        const response = await fetch('/api/log-entry', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ drug, amount_used, initials })
        });

        const data = await response.json();
        const feedbackDiv = document.getElementById('log-feedback');

        if (data.status === "success") {
            feedbackDiv.innerHTML = `<div class="log-entry-row">✅ ${data.entry}</div>` + feedbackDiv.innerHTML;
            document.getElementById('log-amount').value = ''; 
        } else {
            alert(data.message);
        }
    } catch (err) {
        alert("Failed to connect to the log server.");
    }
}

/**
 * Quiz Validation Logic
 */
function checkQuizAnswer(id, correct, explanation) {
    const userVal = parseFloat(document.getElementById(`ans-${id}`).value);
    const feedback = document.getElementById(`feedback-${id}`);
    
    if (Math.abs(userVal - correct) < 0.1) {
        feedback.innerHTML = `<p style="color: var(--success-green); font-weight: bold;">Correct!</p>`;
    } else {
        feedback.innerHTML = `<p style="color: var(--warning-red);">Incorrect. Answer: ${correct}. <br><strong>Logic:</strong> ${explanation}</p>`;
    }
}

/**
 * FINAL EXAM SPRINT LOGIC
 * Expanded to 15 questions with UI reset and scroll handling
 */
let examTimer;
let timeLeft = 600; 

async function startExamSprint() {
    // 1. Reset UI States
    document.getElementById('sprint-init').classList.add('hidden');
    document.getElementById('sprint-results').classList.add('hidden');
    document.getElementById('sprint-questions').classList.remove('hidden');
    
    try {
        const response = await fetch('/api/questions');
        const questions = await response.json();

        // 2. Shuffle and take exactly 15 questions
        const shuffled = questions.sort(() => 0.5 - Math.random()).slice(0, 15);

        const container = document.getElementById('sprint-container');
        container.innerHTML = shuffled.map((q, index) => `
            <div class="card" style="margin-bottom: 20px; border-left: 5px solid #cbd5e0;">
                <div style="display: flex; justify-content: space-between;">
                    <span class="week-tag" style="background: #edf2f7; color: #4a5568; font-size: 0.65rem;">${q.category}</span>
                    <span style="color: #a0aec0; font-size: 0.8rem;">Question ${index + 1} of 15</span>
                </div>
                <p style="margin-top: 10px;"><strong>${q.question}</strong></p>
                <input type="number" step="any" class="sprint-input" 
                       data-id="${q.id}" 
                       data-correct="${q.answer}" 
                       data-expl="${q.explanation.replace(/'/g, "\\'")}" 
                       placeholder="Enter answer...">
            </div>
        `).join('');

        // 3. Reset and Start Timer
        timeLeft = 600; 
        updateTimerDisplay();
        clearInterval(examTimer);
        examTimer = setInterval(updateTimer, 1000);

        // Scroll to top of questions for a fresh start
        window.scrollTo({ top: 0, behavior: 'smooth' });

    } catch (err) {
        alert("Could not load exam questions. Check if app.py is running.");
    }
}

function updateTimer() {
    timeLeft--;
    updateTimerDisplay();
    if (timeLeft <= 0) {
        clearInterval(examTimer);
        gradeExamSprint();
        alert("Time is up!");
    }
}

function updateTimerDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;
    seconds = seconds < 10 ? '0' + seconds : seconds;
    document.getElementById('exam-timer').innerText = `${minutes}:${seconds}`;
}

function gradeExamSprint() {
    clearInterval(examTimer);
    const inputs = document.querySelectorAll('.sprint-input');
    let score = 0;
    let feedbackHTML = "";

    inputs.forEach(input => {
        const userVal = parseFloat(input.value);
        const correctVal = parseFloat(input.dataset.correct);
        const expl = input.dataset.expl;
        const isCorrect = !isNaN(userVal) && Math.abs(userVal - correctVal) < 0.1;

        if (isCorrect) score++;
        
        feedbackHTML += `
            <div style="padding: 15px; border-bottom: 1px solid #eee; background: ${isCorrect ? '#f0fff4' : '#fff5f5'}">
                <p><strong>Result:</strong> ${isCorrect ? '✅ Correct' : '❌ Incorrect'}</p>
                <p style="font-size: 0.9rem; margin-top: 5px;"><strong>Answer:</strong> ${correctVal} | <strong>Logic:</strong> ${expl}</p>
            </div>
        `;
    });

    document.getElementById('sprint-questions').classList.add('hidden');
    document.getElementById('sprint-results').classList.remove('hidden');
    document.getElementById('results-data').innerHTML = `
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="font-size: 3.5rem; color: var(--primary-blue); margin: 0;">${score} / ${inputs.length}</h1>
            <p style="font-weight: bold;">${score >= (inputs.length * 0.7) ? "You're ready for Wednesday! 🩺" : "Focus on the study guides! 📖"}</p>
        </div>
        <hr>
        <div style="max-height: 400px; overflow-y: auto;">
            ${feedbackHTML}
        </div>
    `;
}