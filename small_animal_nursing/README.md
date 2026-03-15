# 🐾 Vet Tech Study & Clinical Companion

A full-stack web application designed to help Veterinary Technician students study for lab practicals and perform critical clinical calculations in high-stress environments. 

Inspired by a love for animals (and a desire to keep my own dog and three cats safe!), this tool bridges the gap between software engineering and veterinary medicine by replacing static notes with an interactive, database-driven platform.

## ✨ Key Features

* **Interactive Study Modules:** Database-driven study guides covering topics like Vital Signs, ECG Interpretation, and Ophthalmic Procedures.
* **Lab Practical Exam Engine:** A 50-question multiple-choice testing system with randomized options, immediate grading feedback, and score tracking.
* **Clinical Calculators:**
    * **Fluid Therapy:** Calculates 24-hour replacement requirements and hourly IV rates based on maintenance, deficit, and ongoing losses.
    * **Nutritional Support (RER):** Calculates base Resting Energy Requirements and applies illness factors for recovery.
    * **🚨 Emergency Drug Doser:** A built-in formulary that instantly converts patient weight and $mg/kg$ dosages into precise $mL$ volumes for crash-cart scenarios. Frontend validation prevents impossible inputs (e.g., negative weights).
* **Document Library:** A scrollable, embedded PDF library for quick access to cheat sheets and clinical guidelines.
* **Modern UI/UX:** Fully responsive design with a custom-built CSS variable system featuring a seamless Light/Dark Mode toggle for late-night studying or night-shift clinic use.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite, Flask-SQLAlchemy (ORM)
* **Frontend:** HTML5, Vanilla CSS (CSS Variables for theme switching), Vanilla JavaScript, Jinja2 Templating
* **Architecture:** MVC (Model-View-Controller) pattern

## 🚀 Installation & Setup

To run this application locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/vet-tech-companion.git](https://github.com/YourUsername/vet-tech-companion.git)
   cd vet-tech-companion