from datetime import datetime, timedelta
from icloud_sync import add_calendar_event

# Start date of the plan (Tuesday, June 24, 2025)
START_DATE = datetime(2025, 6, 24)

# Repeat length
WEEKS = 28

# === 🏋️ Workout Schedule ===
workout_schedule = {
    "Monday": ("Push + Cardio", 18),
    "Tuesday": ("Pull", 18),
    "Wednesday": ("Core + Cardio", 18),
    "Thursday": ("Legs", 18),
    "Friday": ("Chest + Cardio", 18),
    "Saturday": ("Active Rest / Stretch", 12),
    "Sunday": ("Rest", None),
}

# === 🧠 Cybersecurity Career Plan ===
cyber_plan = [
    ("Intro to Red Team Tools", 0),
    ("TryHackMe Red Team Path", 1),
    ("HTB Starting Point Boxes", 3),
    ("Buffer Overflow Practice", 5),
    ("Privilege Escalation Practice", 7),
    ("Create Custom Payloads", 9),
    ("Internal Recon Simulation", 11),
    ("Apply to Red Team Roles", 18),
    ("Red Team Final Challenge", 26),
]


def get_start_date(target_day: str, week_offset=0):
    """Get the date of a target weekday starting from the fixed START_DATE."""
    weekday_index = list(workout_schedule.keys()).index(target_day)
    start_week = START_DATE + timedelta(weeks=week_offset)
    days_ahead = (weekday_index - start_week.weekday()) % 7
    return (start_week + timedelta(days=days_ahead)).replace(hour=0, minute=0)


def sync_workouts():
    print("📅 Syncing 6-Month Workout Plan...")
    for week in range(WEEKS):
        for day, (workout, hour) in workout_schedule.items():
            if not hour:
                continue
            start_time = get_start_date(day, week_offset=week).replace(hour=hour)
            add_calendar_event(f"Workout: {workout}", start_time, duration_minutes=60)


def sync_cyber_plan():
    print("📅 Syncing Cybersecurity Career Plan...")
    for title, week_offset in cyber_plan:
        start_time = START_DATE + timedelta(weeks=week_offset)
        start_time = start_time.replace(hour=20)
        add_calendar_event(f"Cyber Task: {title}", start_time, duration_minutes=90)


if __name__ == "__main__":
    sync_workouts()
    sync_cyber_plan()
    print("✅ All plans synced to iCloud Calendar starting from Tuesday, June 24, 2025.")
