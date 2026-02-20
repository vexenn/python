from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "agents.db"

app = Flask(__name__, static_folder="static")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS agent_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        existing = conn.execute("SELECT COUNT(1) AS count FROM agent_patterns").fetchone()["count"]
        if existing == 0:
            conn.executemany(
                """
                INSERT INTO agent_patterns (level, title, description)
                VALUES (?, ?, ?)
                """,
                [
                    (
                        "basic",
                        "Single Agent Prompting",
                        "Use one coding agent for focused tasks with explicit constraints.",
                    ),
                    (
                        "intermediate",
                        "Prompt + Test Loop",
                        "Chain drafting and testing to reduce regressions and improve quality.",
                    ),
                    (
                        "advanced",
                        "Multi-Agent Orchestration",
                        "Coordinate planner, implementer, and reviewer agents under policy guardrails.",
                    ),
                ],
            )
        conn.commit()


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/api/levels")
def levels():
    descriptions = {
        "basic": "Foundational workflows for prompt clarity, constraints, and fast iteration.",
        "intermediate": "Structured workflows with tests, checks, and iterative quality loops.",
        "advanced": "Production-grade orchestration, governance, and scalable team operations.",
    }

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT level, COUNT(*) AS count
            FROM agent_patterns
            GROUP BY level
            ORDER BY CASE level
                WHEN 'basic' THEN 1
                WHEN 'intermediate' THEN 2
                WHEN 'advanced' THEN 3
                ELSE 4
            END
            """
        ).fetchall()

    return jsonify(
        {
            "levels": [
                {
                    "level": row["level"],
                    "count": row["count"],
                    "description": descriptions.get(row["level"], "Agent module"),
                }
                for row in rows
            ]
        }
    )


@app.get("/api/patterns")
def patterns():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, level, title, description, created_at FROM agent_patterns ORDER BY id"
        ).fetchall()

    return jsonify({"patterns": [dict(row) for row in rows]})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


init_db()

if __name__ == "__main__":
    app.run(debug=True)
