from app import app
from models import db, StudyModule, Topic, SubSection

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        nursing_module = StudyModule(name="Small Animal Nursing II")
        db.session.add(nursing_module)
        db.session.commit()

        # --- TOPIC 1: BANDAGING & SLINGS ---
        bandaging = Topic(module_id=nursing_module.id, title="Bandaging & Slings", category="Procedure")
        db.session.add(bandaging)
        db.session.commit()
        db.session.add_all([
            SubSection(topic_id=bandaging.id, heading="Ehmer Sling", content="Pelvic limb stabilization. Maintains hip in flexion/abduction.", image_filename="ehmer_sling.png"),
            SubSection(topic_id=bandaging.id, heading="Velpeau Sling", content="Forelimb non-weight bearing stabilization.", image_filename="velpeau_sling.png")
        ])

        # --- TOPIC 2: VITAL SIGNS & MONITORING ---
        vitals = Topic(module_id=nursing_module.id, title="Vital Signs & Monitoring", category="Diagnostics")
        db.session.add(vitals)
        db.session.commit()
        db.session.add_all([
            SubSection(topic_id=vitals.id, heading="Normal TPR Ranges", content="Standard reference ranges for canine and feline assessment.", image_filename="dog_cat_vitals_table.png",
                       structured_data={"Dog": {"Temp": "100.0-102.5°F", "HR": "60-160 bpm", "RR": "16-32 brpm"}, "Cat": {"Temp": "100.0-102.5°F", "HR": "140-220 bpm", "RR": "20-42 brpm"}}),
            SubSection(topic_id=vitals.id, heading="Blood Pressure Cuff Placement", content="Cuff width should be 40% of limb circumference.", image_filename="placement_of_bp_cuff.png"),
            SubSection(topic_id=vitals.id, heading="Doppler Probe Placement", content="Placement on the digital or metacarpal artery.", image_filename="placement_of_doppler_probe.png")
        ])

        # --- TOPIC 3: ECG INTERPRETATION ---
        ecg = Topic(module_id=nursing_module.id, title="ECG Interpretation", category="Diagnostics")
        db.session.add(ecg)
        db.session.commit()
        db.session.add_all([
            SubSection(topic_id=ecg.id, heading="First-Degree AV Block", content="Prolonged PR interval.", image_filename="first_degree_av_block.png"),
            SubSection(topic_id=ecg.id, heading="Second-Degree AV Block", content="Some P waves not followed by QRS.", image_filename="second_degree_av_block.png"),
            SubSection(topic_id=ecg.id, heading="Third-Degree AV Block", content="Complete dissociation.", image_filename="third_degree_av_block.png"),
            SubSection(topic_id=ecg.id, heading="V-Tach", content="Life-threatening ventricular arrhythmia.", image_filename="ventricular_tachycardia.png"),
            SubSection(topic_id=ecg.id, heading="V-Fib", content="Requires immediate defibrillation.", image_filename="vetricular_fibrillation.png"),
            SubSection(topic_id=ecg.id, heading="Atrial Fibrillation", content="Irregularly irregular rhythm (shoes in a dryer).", image_filename="atrial_fibrillation.png"),
            SubSection(topic_id=ecg.id, heading="Asystole", content="No electrical activity (Flatline).", image_filename="asystole.png")
        ])

        # --- TOPIC 4: NURSING SKILLS ---
        skills = Topic(module_id=nursing_module.id, title="Clinical Nursing Skills", category="Procedure")
        db.session.add(skills)
        db.session.commit()
        db.session.add_all([
            SubSection(topic_id=skills.id, heading="Catheter Anatomy", content="Hub, stylet, and flashback chamber.", image_filename="catheter_anatomy.png"),
            SubSection(topic_id=skills.id, heading="Taping Technique", content="Correct Chevron taping for IV stability.", image_filename="taping_technique_step_1_2.png"),
            SubSection(topic_id=skills.id, heading="Phlebitis", content="Inflammation of the vein wall. Watch for redness and heat.", image_filename="phlebitis.png"),
            SubSection(topic_id=skills.id, heading="Extravasation", content="Fluid leaking into tissue (Vesicant risk). Stop infusion immediately.", image_filename="extravasation.png")
        ])

        # --- TOPIC 5: OPHTHALMIC NURSING ---
        sensory = Topic(module_id=nursing_module.id, title="Ophthalmic Procedures", category="Procedure")
        db.session.add(sensory)
        db.session.commit()
        db.session.add_all([
            SubSection(topic_id=sensory.id, heading="Eye Anatomy", content="Internal structures of the globe.", image_filename="eye_anatomy.png"),
            SubSection(topic_id=sensory.id, heading="Schirmer Tear Test", content="Measures tear production. Normal: 15-25 mm/min.", image_filename="stt_strips_in_eye.png"),
            SubSection(topic_id=sensory.id, heading="Tonopen Tonometry", content="Measures IOP. Normal: 15-25 mmHg.", image_filename="tonopen_on_eye.png"),
            SubSection(topic_id=sensory.id, heading="Fluorescein Stain", content="Visualizes corneal epithelial defects (ulcers).", image_filename="fluorescein_stain_in_eye.png")
        ])

        # --- TOPIC 6: LAB PRACTICAL PREP (50 Questions MCQ) ---
        quiz = Topic(module_id=nursing_module.id, title="Lab Practical Prep", category="Study Tool")
        db.session.add(quiz)
        db.session.commit()

        db.session.add_all([
            # cardiology
            SubSection(topic_id=quiz.id, heading="Q: Emergency Rhythms", content="Which ECG rhythm is characterized by a 'shoes in a dryer' sound on auscultation?", structured_data={"correct": "Atrial Fibrillation", "options": ["Atrial Fibrillation", "V-Tach", "Sinus Arrhythmia", "First-Degree AV Block"]}),
            SubSection(topic_id=quiz.id, heading="Q: Waveform ID", content="What does the P-wave on an ECG represent?", structured_data={"correct": "Atrial Depolarization", "options": ["Atrial Depolarization", "Ventricular Depolarization", "Atrial Repolarization", "Ventricular Repolarization"]}),
            SubSection(topic_id=quiz.id, heading="Q: Lead Placement", content="Where is the 'White' lead placed in standard 3-lead ECG positioning?", structured_data={"correct": "Right Forelimb (RF)", "options": ["Right Forelimb (RF)", "Left Forelimb (LF)", "Left Hindlimb (LH)", "Right Hindlimb (RH)"]}),
            # fluids
            SubSection(topic_id=quiz.id, heading="Q: Fluid Deficit", content="10kg dog, 5% dehydrated. Calculate the deficit in mL.", structured_data={"correct": "500 mL", "options": ["500 mL", "50 mL", "1000 mL", "250 mL"]}),
            SubSection(topic_id=quiz.id, heading="Q: Drip Rates", content="Calculate the gtt/sec for 100mL/hr using a 60gtt/mL set.", structured_data={"correct": "1.6 gtt/sec", "options": ["1.6 gtt/sec", "2.5 gtt/sec", "0.5 gtt/sec", "10 gtt/sec"]}),
            SubSection(topic_id=quiz.id, heading="Q: Constant Rate Infusion", content="What does CRI stand for in fluid therapy?", structured_data={"correct": "Constant Rate Infusion", "options": ["Constant Rate Infusion", "Critical Rate Intake", "Calculated Rate Injection", "Continuous Renal Index"]}),
            # anatomy
            SubSection(topic_id=quiz.id, heading="Q: Ophthalmic Anatomy", content="Which structure produces aqueous humor?", structured_data={"correct": "Ciliary Body", "options": ["Ciliary Body", "Iris", "Retina", "Optic Nerve"]}),
            SubSection(topic_id=quiz.id, heading="Q: Gastric Location", content="Which side of the patient should you clip for a percutaneous endoscopic gastrostomy (PEG) tube?", structured_data={"correct": "Left Side", "options": ["Left Side", "Right Side", "Ventral Midline", "Dorsal Midline"]}),
            SubSection(topic_id=quiz.id, heading="Q: Dental Formula", content="How many teeth does an adult dog have?", structured_data={"correct": "42", "options": ["42", "30", "32", "44"]}),
            SubSection(topic_id=quiz.id, heading="Q: Feline Dental", content="How many teeth does an adult cat have?", structured_data={"correct": "30", "options": ["30", "42", "28", "32"]}),
            # pharmacology
            SubSection(topic_id=quiz.id, heading="Q: Antidotes", content="What is the reversal agent for Dexmedetomidine?", structured_data={"correct": "Atipamezole", "options": ["Atipamezole", "Naloxone", "Flumazenil", "Yohimbine"]}),
            SubSection(topic_id=quiz.id, heading="Q: Opioids", content="Which opioid is a partial mu-agonist often used for mild to moderate pain?", structured_data={"correct": "Buprenorphine", "options": ["Buprenorphine", "Morphine", "Hydromorphone", "Butorphanol"]}),
            SubSection(topic_id=quiz.id, heading="Q: NSAIDs", content="Name a common side effect of NSAIDs in canine patients.", structured_data={"correct": "GI Ulceration", "options": ["GI Ulceration", "Sedation", "Seizures", "Tachycardia"]}),
            SubSection(topic_id=quiz.id, heading="Q: Calculations", content="A 20lb dog needs 2mg/kg of a 5% solution. How many mLs?", structured_data={"correct": "0.36 mL", "options": ["0.36 mL", "1.2 mL", "0.15 mL", "0.8 mL"]}),
            # anesthesia
            SubSection(topic_id=quiz.id, heading="Q: Machine Parts", content="What is the function of the pop-off valve?", structured_data={"correct": "Exhausts waste gas", "options": ["Exhausts waste gas", "Delivers oxygen", "Vaporizes anesthetic", "Measures heart rate"]}),
            SubSection(topic_id=quiz.id, heading="Q: Refilling", content="When should soda lime granules be changed?", structured_data={"correct": "After 6-8 hours of use", "options": ["After 6-8 hours of use", "Every month", "When they turn green", "Once a year"]}),
            SubSection(topic_id=quiz.id, heading="Q: Intubation", content="How do you measure the length of an endotracheal tube?", structured_data={"correct": "Nose to thoracic inlet", "options": ["Nose to thoracic inlet", "Nose to last rib", "Canine tooth to ear", "Mouth to xiphoid"]}),
            SubSection(topic_id=quiz.id, heading="Q: Monitoring", content="What does a capnograph measure?", structured_data={"correct": "End-tidal CO2", "options": ["End-tidal CO2", "Blood pressure", "Oxygen saturation", "Temperature"]}),
            # radiology
            SubSection(topic_id=quiz.id, heading="Q: Positioning", content="For a lateral abdominal radiograph, where should the beam be centered?", structured_data={"correct": "Caudal aspect of 13th rib", "options": ["Caudal aspect of 13th rib", "Umbilicus", "Xiphoid process", "Greater trochanter"]}),
            SubSection(topic_id=quiz.id, heading="Q: Safety", content="What is the 'ALARA' principle in radiology?", structured_data={"correct": "As Low As Reasonably Achievable", "options": ["As Low As Reasonably Achievable", "Always Look At Radiant Areas", "All Lead Aprons Required Always", "Avoid Low Alpha Radiation Areas"]}),
            SubSection(topic_id=quiz.id, heading="Q: Contrast", content="Which contrast agent is contraindicated if a GI perforation is suspected?", structured_data={"correct": "Barium Sulfate", "options": ["Barium Sulfate", "Iohexol", "Air", "Water"]}),
            # lab
            SubSection(topic_id=quiz.id, heading="Q: Hematology", content="Which white blood cell is most commonly associated with allergic reactions?", structured_data={"correct": "Eosinophil", "options": ["Eosinophil", "Neutrophil", "Lymphocyte", "Monocyte"]}),
            SubSection(topic_id=quiz.id, heading="Q: Urine S.G.", content="What is the 'Isosthenuric' range for urine specific gravity?", structured_data={"correct": "1.008 to 1.012", "options": ["1.008 to 1.012", "1.035 to 1.045", "1.001 to 1.005", "1.015 to 1.025"]}),
            SubSection(topic_id=quiz.id, heading="Q: Skin Scrape", content="Which parasite requires a deep skin scrape?", structured_data={"correct": "Demodex mites", "options": ["Demodex mites", "Sarcoptes mites", "Cheyletiella", "Otodectes"]}),
            SubSection(topic_id=quiz.id, heading="Q: Blood Tubes", content="Which anticoagulant is found in a Lavender Top Tube (LTT)?", structured_data={"correct": "EDTA", "options": ["EDTA", "Heparin", "Sodium Citrate", "Lithium"]}),
            # skills
            SubSection(topic_id=quiz.id, heading="Q: Catheter Care", content="How often should an IV catheter be flushed if not on continuous fluids?", structured_data={"correct": "Every 4 hours", "options": ["Every 4 hours", "Once a day", "Every 12 hours", "Only when used"]}),
            SubSection(topic_id=quiz.id, heading="Q: Wound Healing", content="What is 'Debridement'?", structured_data={"correct": "Removal of necrotic tissue", "options": ["Removal of necrotic tissue", "Suturing a wound", "Applying a bandage", "Irrigating with saline"]}),
            SubSection(topic_id=quiz.id, heading="Q: Triage", content="What are the 'Big 4' blood parameters checked in emergency triage?", structured_data={"correct": "PCV, TS, BG, Lactate", "options": ["PCV, TS, BG, Lactate", "ALT, ALP, BUN, CREA", "WBC, RBC, HGB, PLT", "Na, K, Cl, Ca"]}),
            SubSection(topic_id=quiz.id, heading="Q: Thermoregulation", content="At what temperature is a patient considered 'Hypothermic'?", structured_data={"correct": "Below 99°F", "options": ["Below 99°F", "Below 101°F", "Below 97°F", "Below 100°F"]}),
            SubSection(topic_id=quiz.id, heading="Q: Recumbency", content="How often should a recumbent patient be turned to prevent ulcers?", structured_data={"correct": "Every 2-4 hours", "options": ["Every 2-4 hours", "Once a day", "Every 8 hours", "Every 30 minutes"]}),
            # surgery
            SubSection(topic_id=quiz.id, heading="Q: Hemostats", content="Which instrument has longitudinal serrations for its entire length?", structured_data={"correct": "Rochester-Carmalt", "options": ["Rochester-Carmalt", "Kelly", "Crile", "Mosquito"]}),
            SubSection(topic_id=quiz.id, heading="Q: Suture ID", content="Is PDS an absorbable or non-absorbable suture?", structured_data={"correct": "Absorbable", "options": ["Absorbable", "Non-absorbable", "Metallic", "Silk"]}),
            SubSection(topic_id=quiz.id, heading="Q: Scalpels", content="Which scalpel blade size fits a #3 handle?", structured_data={"correct": "10, 11, 12, or 15", "options": ["10, 11, 12, or 15", "20, 21, or 22", "8, 9, or 13", "18 or 24"]}),
            # respiratory
            SubSection(topic_id=quiz.id, heading="Q: SpO2 Values", content="What is the target SpO2 percentage for a patient on 100% oxygen?", structured_data={"correct": "98-100%", "options": ["98-100%", "90-95%", "100-110%", "85-90%"]}),
            SubSection(topic_id=quiz.id, heading="Q: Cyanosis", content="At what SpO2 level does a patient typically show blue mucous membranes?", structured_data={"correct": "Less than 75%", "options": ["Less than 75%", "Less than 90%", "Less than 95%", "Less than 85%"]}),
            # parasites
            SubSection(topic_id=quiz.id, heading="Q: Zoonosis", content="Which intestinal parasite causes Visceral Larva Migrans in humans?", structured_data={"correct": "Roundworm", "options": ["Roundworm", "Hookworm", "Tapeworm", "Whipworm"]}),
            SubSection(topic_id=quiz.id, heading="Q: Vectors", content="What is the intermediate host for the tapeworm Dipylidium caninum?", structured_data={"correct": "The Flea", "options": ["The Flea", "The Tick", "The Mosquito", "The Snail"]}),
            # prep
            SubSection(topic_id=quiz.id, heading="Q: Fasting", content="How long should a healthy adult dog be fasted before elective surgery?", structured_data={"correct": "8-12 hours", "options": ["8-12 hours", "2-4 hours", "24 hours", "No fasting required"]}),
            SubSection(topic_id=quiz.id, heading="Q: Scrub Technique", content="When performing a surgical scrub, should you scrub 'clean to dirty'?", structured_data={"correct": "Clean to dirty", "options": ["Clean to dirty", "Dirty to clean", "Side to side", "Periphery to center"]}),
            # behavior
            SubSection(topic_id=quiz.id, heading="Q: Restraint", content="Which vein is most commonly used for blood collection in a fractious cat?", structured_data={"correct": "Medial Saphenous", "options": ["Medial Saphenous", "Jugular", "Cephalic", "Lateral Saphenous"]}),
            SubSection(topic_id=quiz.id, heading="Q: Body Language", content="Name one sign of fear in a canine patient.", structured_data={"correct": "Tucked tail", "options": ["Tucked tail", "Wagging tail", "Direct eye contact", "Ears forward"]}),
            # micro
            SubSection(topic_id=quiz.id, heading="Q: Gram Staining", content="What color do Gram-Positive bacteria appear under the microscope?", structured_data={"correct": "Purple/Blue", "options": ["Purple/Blue", "Red/Pink", "Green", "Colorless"]}),
            SubSection(topic_id=quiz.id, heading="Q: Fungi", content="What is the common name for Microsporum canis?", structured_data={"correct": "Ringworm", "options": ["Ringworm", "Yeast", "Thrush", "Athlete's foot"]}),
            # cpr
            SubSection(topic_id=quiz.id, heading="Q: Compression Rate", content="What is the recommended compression rate for CPR in dogs?", structured_data={"correct": "100-120 bpm", "options": ["100-120 bpm", "60-80 bpm", "140-160 bpm", "200 bpm"]}),
            SubSection(topic_id=quiz.id, heading="Q: Drug Admin", content="If an IV is not available during CPR, which other route is commonly used?", structured_data={"correct": "Intratracheal", "options": ["Intratracheal", "Subcutaneous", "Oral", "Intramuscular"]}),
            # equipment
            SubSection(topic_id=quiz.id, heading="Q: Centrifuge", content="What is the term for the liquid portion on top of a centrifuged sample?", structured_data={"correct": "Supernatant", "options": ["Supernatant", "Sediment", "Buffy Coat", "Precipitate"]}),
            SubSection(topic_id=quiz.id, heading="Q: Refractometer", content="What must you use to calibrate a refractometer?", structured_data={"correct": "Distilled water", "options": ["Distilled water", "Tap water", "Alcohol", "Saline"]}),
            # client
            SubSection(topic_id=quiz.id, heading="Q: Toxicities", content="Which common human sweetener is highly toxic to dogs?", structured_data={"correct": "Xylitol", "options": ["Xylitol", "Stevia", "Aspartame", "Saccharine"]}),
            SubSection(topic_id=quiz.id, heading="Q: Medication Labeling", content="What does 'q.i.d.' stand for on a prescription?", structured_data={"correct": "Four times a day", "options": ["Four times a day", "Every hour", "Once a day", "Twice a day"]}),
            SubSection(topic_id=quiz.id, heading="Q: Post-Op", content="Why is an E-collar used post-operatively?", structured_data={"correct": "Prevent self-trauma", "options": ["Prevent self-trauma", "Improve hearing", "Keep neck warm", "Prevent barking"]})
        ])

        db.session.commit()
        print("Master Database restored successfully!")

if __name__ == '__main__':
    seed_data()