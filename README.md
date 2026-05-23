# Team Availability Tracker (Flask + SQLite)

A simple full-stack app that shows team members and lets you toggle **Available / Busy**. Updates are stored in **SQLite** instantly via a Flask API—no page reload.

## Folder Structure

```
team-availability-tracker/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── database.db
```

## Features
- Dashboard lists team members with **role**
- Availability badge: **Green = Available**, **Red = Busy**
- Toggle switch updates status instantly
- Backend APIs:
  - `GET /members`
  - `POST /toggle/<id>`

## Setup Instructions

### 1) Create and activate a virtual environment
**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

### 3) Run the app
```powershell
python app.py
```

Open your browser at:
- http://127.0.0.1:5000

On first run, the app will create `database.db` and insert sample team members.

## API Docs

### `GET /members`
Returns JSON:
```json
{
  "members": [
    {"id": 1, "name": "Akshay", "role": "Frontend", "available": true}
  ]
}
```

### `POST /toggle/<id>`
Toggles a member’s availability and returns:
```json
{"id": 1, "available": true}
```

## Notes
- Availability is stored as a boolean-like integer in SQLite (`available` is `0` or `1`).

