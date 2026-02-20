from datetime import datetime
import os
import threading
import time
import webbrowser

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder=".", static_url_path="")
# Database migration to VUTS schema
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vuts_system.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
db = SQLAlchemy(app)

# --- RELATIONAL MODELS ---

class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    requestor = db.Column(db.String(100), nullable=False)
    assignee = db.Column(db.String(100), default="Unassigned")
    priority = db.Column(db.Enum("Low", "Medium", "High", name="task_priority", native_enum=False), default="Medium")
    is_resolved = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True) # Calendar logic support
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Linked comments system for the resolution workflow
    comments = db.relationship('Comment', backref='ticket', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "requestor": self.requestor,
            "assignee": self.assignee,
            "priority": self.priority,
            "is_resolved": self.is_resolved,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() + "Z"
        }

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- MASTER ALIGNED API CONTROLLERS ---

@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

# MASTER ALIGNMENT: Handles both GET (fetch) and POST (create) at /api/tasks
@app.route("/api/tasks", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        date_str = request.args.get('date')
        query = Ticket.query
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                query = query.filter(Ticket.due_date == target_date)
            except ValueError:
                return jsonify({"error": "Invalid date"}), 400
        tickets = query.order_by(Ticket.created_at.desc()).all()
        return jsonify([t.to_dict() for t in tickets]), 200

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        # Validation for required VUTS fields
        if not data.get("title") or not data.get("requestor"):
            return jsonify({"error": "Title and Requestor are required"}), 400

        ticket = Ticket(
            title=data.get("title"),
            requestor=data.get("requestor"),
            assignee=data.get("assignee", "Unassigned"),
            priority=data.get("priority", "Medium"),
            due_date=datetime.strptime(data["due_date"], '%Y-%m-%d').date() if data.get("due_date") else None
        )
        db.session.add(ticket)
        db.session.commit()
        return jsonify(ticket.to_dict()), 201

# RESOLVE ENDPOINT: Specialized atomic operation
@app.post("/api/tickets/<int:ticket_id>/resolve")
def resolve_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    data = request.get_json(silent=True) or {}
    
    # 1. Post final comment if provided
    if data.get("comment"):
        new_comment = Comment(content=data["comment"], ticket_id=ticket.id)
        db.session.add(new_comment)
    
    # 2. Mark as Resolved
    ticket.is_resolved = True
    db.session.commit()
    return jsonify({"message": "Resolved"}), 200

# DELETE ENDPOINT: Aligned to /api/tasks to match deletion logic
@app.delete("/api/tasks/<int:ticket_id>")
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200

# --- STARTUP & DX ---

@app.errorhandler(500)
def handle_500(error):
    db.session.rollback()
    return jsonify({"error": "Internal Server Error"}), 500

def _open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=_open_browser, daemon=True).start()
    app.run(debug=True, port=5000)