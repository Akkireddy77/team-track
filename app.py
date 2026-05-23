from flask import Flask, jsonify, request, g, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"


def get_db():
    # Create a single connection per request
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            available INTEGER NOT NULL CHECK (available IN (0,1))
        )
        """
    )

    cur.execute("SELECT COUNT(*) FROM members")
    count = cur.fetchone()[0]

    if count == 0:
        sample = [
            ("Akshay", "Frontend" , 1),
            ("Priya", "Backend" , 1),
            ("Rahul", "DevOps" , 0),
            ("Nisha", "QA" , 1),
            ("Vikram", "Design" , 0),
        ]
        cur.executemany(
            "INSERT INTO members (name, role, available) VALUES (?, ?, ?)",
            sample,
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/members", methods=["GET"])
def members():
    db = get_db()
    rows = db.execute(
        "SELECT id, name, role, available FROM members ORDER BY name"
    ).fetchall()

    data = [
        {
            "id": row["id"],
            "name": row["name"],
            "role": row["role"],
            "available": bool(row["available"]),
        }
        for row in rows
    ]
    return jsonify({"members": data})


@app.route("/toggle/<int:member_id>", methods=["POST"])
def toggle(member_id: int):
    db = get_db()
    row = db.execute(
        "SELECT id, available FROM members WHERE id = ?", (member_id,)
    ).fetchone()

    if row is None:
        return jsonify({"error": "Member not found"}), 404

    new_value = 0 if row["available"] == 1 else 1

    db.execute(
        "UPDATE members SET available = ? WHERE id = ?",
        (new_value, member_id),
    )
    db.commit()

    return jsonify({"id": member_id, "available": bool(new_value)})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
