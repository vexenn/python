import webbrowser
import os

# Quiz Data based on your study guide
quiz_data = [
    {
        "question": "Which of the following animals are considered ruminants with a 4-chambered stomach?",
        "options": ["Horses and Rabbits", "Cows and Goats", "Dogs and Cats", "Pigs and Horses"],
        "answer": "Cows and Goats"
    },
    {
        "question": "What occurs at the pharynx regarding the digestive and respiratory systems?",
        "options": [
            "The digestive system stays dorsal to the respiratory system",
            "The respiratory system stays ventral to the digestive system",
            "The digestive system goes from ventral to dorsal, and the respiratory system goes from dorsal to ventral",
            "They both merge into a single tube that leads to the stomach"
        ],
        "answer": "The digestive system goes from ventral to dorsal, and the respiratory system goes from dorsal to ventral"
    },
    {
        "question": "Which accessory gland is responsible for preventing toxic substances from entering general circulation?",
        "options": ["Pancreas", "Gall Bladder", "Spleen", "Liver"],
        "answer": "Liver"
    },
    {
        "question": "If an animal has Megaesophagus, how should an owner manage their feeding?",
        "options": [
            "Feed them small meals on the floor",
            "Ensure the pet sits upright while eating and for 30 minutes after",
            "Feed only liquid diets through a tube",
            "Exercise the pet immediately after eating"
        ],
        "answer": "Ensure the pet sits upright while eating and for 30 minutes after"
    },
    {
        "question": "What is the primary difference between the omentum and the mesentery?",
        "options": [
            "The omentum contains more adipose tissue and connects the stomach to the body wall",
            "The mesentery connects the stomach to the abdominal wall",
            "The omentum is strictly for blood vessel transport",
            "The mesentery is found only in ruminants"
        ],
        "answer": "The omentum contains more adipose tissue and connects the stomach to the body wall"
    },
    {
        "question": "Which cells in the fundus are responsible for producing hydrochloric acid (HCl)?",
        "options": ["Chief cells", "Mucous neck cells", "Parietal cells", "Endocrine cells"],
        "answer": "Parietal cells"
    },
    {
        "question": "The 'Hepatic Triad' consists of which three structures?",
        "options": [
            "Liver, Pancreas, Gall Bladder",
            "Hepatic portal vein, Hepatic artery, Bile ducts",
            "Vagus nerve, Hepatic vein, Lymph nodes",
            "Stomach, Duodenum, Jejunum"
        ],
        "answer": "Hepatic portal vein, Hepatic artery, Bile ducts"
    },
    {
        "question": "In a cow, which part of the foregut is characterized by a 'honeycomb' appearance?",
        "options": ["Rumen", "Reticulum", "Omasum", "Abomasum"],
        "answer": "Reticulum"
    },
    {
        "question": "In young ruminants, what structure allows milk to bypass the reticulorumen?",
        "options": ["Pyloric sphincter", "Esophageal groove", "Pelvic flexure", "Sternal flexure"],
        "answer": "Esophageal groove"
    },
    {
        "question": "Which of the following describes 'Afferent' neurons?",
        "options": [
            "Axons that carry motor signals OUT of the spine to the muscles",
            "Cells that only exist in the brain",
            "Axons that carry sensory information from the body INTO the spine",
            "Cells that produce myelin in the CNS"
        ],
        "answer": "Axons that carry sensory information from the body INTO the spine"
    },
    {
        "question": "The Diencephalon is composed of which three structures?",
        "options": [
            "Cerebrum, Cerebellum, Brainstem",
            "Thalamus, Hypothalamus, Pituitary gland",
            "Midbrain, Pons, Medulla",
            "Dendrites, Axons, Schwann cells"
        ],
        "answer": "Thalamus, Hypothalamus, Pituitary gland"
    },
    {
        "question": "Which cells are responsible for creating the myelin sheath in the Central Nervous System (CNS)?",
        "options": ["Schwann cells", "Oligodendrocytes", "Dendrites", "Nodes of Ranvier"],
        "answer": "Oligodendrocytes"
    }
]

# HTML Content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A&P Winter 2026 Midterm Study Quiz</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; padding: 40px; line-height: 1.6; }}
        .container {{ max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .question {{ margin-bottom: 25px; padding: 15px; border-left: 5px solid #3498db; background: #fafafa; }}
        .options {{ list-style: none; padding: 0; }}
        .options li {{ margin: 10px 0; }}
        button {{ background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; transition: 0.3s; }}
        button:hover {{ background: #2980b9; }}
        .result {{ font-weight: bold; margin-top: 10px; display: none; }}
        .correct {{ color: #27ae60; }}
        .wrong {{ color: #c0392b; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Anatomy & Physiology: Midterm 1 Quiz</h1>
        <p>Topic: Digestion and Neurology (Winter Quarter 2026)</p>
        <div id="quiz"></div>
        <button onclick="calculateScore()">Submit Quiz</button>
        <div id="finalScore" style="margin-top: 20px; font-size: 20px; font-weight: bold;"></div>
    </div>

    <script>
        const quizData = {quiz_data};

        function loadQuiz() {{
            const quizContainer = document.getElementById('quiz');
            let output = '';
            quizData.forEach((item, index) => {{
                output += `
                    <div class="question">
                        <p><strong>${{index + 1}}. ${{item.question}}</strong></p>
                        <ul class="options">
                            ${{item.options.map(opt => `
                                <li>
                                    <input type="radio" name="q${{index}}" value="${{opt}}"> ${{opt}}
                                </li>
                            `).join('')}}
                        </ul>
                        <div id="res${{index}}" class="result"></div>
                    </div>
                `;
            }});
            quizContainer.innerHTML = output;
        }}

        function calculateScore() {{
            let score = 0;
            quizData.forEach((item, index) => {{
                const selected = document.querySelector(`input[name="q${{index}}"]:checked`);
                const resultDiv = document.getElementById(`res${{index}}`);
                resultDiv.style.display = 'block';
                
                if (selected && selected.value === item.answer) {{
                    score++;
                    resultDiv.innerHTML = "Correct!";
                    resultDiv.className = "result correct";
                }} else {{
                    resultDiv.innerHTML = "Incorrect. Correct answer: " + item.answer;
                    resultDiv.className = "result wrong";
                }}
            }});
            document.getElementById('finalScore').innerHTML = `Your Score: ${{score}} / ${{quizData.length}}`;
            window.scrollTo(0, document.body.scrollHeight);
        }}

        loadQuiz();
    </script>
</body>
</html>
"""

# Save and Open
file_path = "quiz.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

full_path = "file://" + os.path.abspath(file_path)
print(f"Opening quiz at: {full_path}")
webbrowser.open(full_path)