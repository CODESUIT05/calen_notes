import json
import calendar
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

# Global variables
selected_date = None
notes = {}
month = datetime.now().month
year = datetime.now().year

# Initialize Flask app
app = Flask(__name__)

# Load notes from a file
def load_notes():
    try:
        with open("notes.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save notes to a file
def save_notes():
    with open("notes.json", "w") as f:
        json.dump(notes, f)

# Show the calendar for a given month and year
def generate_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    calendar_data = []

    for row in cal:
        week = []
        for day in row:
            if day != 0:
                day_str = f"{day:02d}-{month:02d}-{year}"
                note = notes.get(day_str, "")
                week.append({"day": day, "note": note, "date": day_str})
            else:
                week.append(None)
        calendar_data.append(week)

    return calendar_data

# Routes
@app.route("/")
def index():
    global month, year
    calendar_data = generate_calendar(year, month)
    return render_template("index.html", calendar_data=calendar_data, year=year, month=month)

@app.route("/save_note", methods=["POST"])
def save_note():
    global selected_date, month, year
    note = request.form.get("note")
    day = request.form.get("day")

    if day and note:
        date_str = f"{int(day):02d}-{month:02d}-{year}"
        notes[date_str] = note
        save_notes()

    return redirect(url_for("index"))

@app.route("/delete_note", methods=["POST"])
def delete_note():
    global selected_date, month, year
    day = request.form.get("day")

    if day:
        date_str = f"{int(day):02d}-{month:02d}-{year}"
        if date_str in notes:
            del notes[date_str]
            save_notes()

    return redirect(url_for("index"))

@app.route("/prev_month")
def prev_month():
    global month, year
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    return redirect(url_for("index"))

@app.route("/next_month")
def next_month():
    global month, year
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    return redirect(url_for("index"))

if __name__ == "__main__":
    notes = load_notes()
    app.run(debug=True)
