from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StudyModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # e.g., 'Small Animal Nursing II'
    topics = db.relationship('Topic', backref='module', lazy=True)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('study_module.id'))
    title = db.Column(db.String(100), nullable=False) # e.g., 'Bandaging Technique'
    category = db.Column(db.String(50)) # e.g., 'Procedure', 'Diagnostics', 'Math'
    sub_sections = db.relationship('SubSection', backref='topic', lazy=True)

class SubSection(db.Model):
    """Breaks topics into parts like 'Primary Layer', 'Secondary Layer'"""
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    heading = db.Column(db.String(200)) # e.g., 'The 3 Layers of a Bandage'
    content = db.Column(db.Text)        # The detailed notes
    
    # New column to link your renamed images (e.g., 'eye_anatomy_internal.png')
    image_filename = db.Column(db.String(100), nullable=True)
    
    # Store things like Normal Vitals or Fluid Rates here
    structured_data = db.Column(db.JSON, nullable=True)