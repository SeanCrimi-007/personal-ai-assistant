import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from caldav import DAVClient
from icalendar import Calendar, Event

# Load iCloud credentials from .env
load_dotenv()
ICLOUD_EMAIL = os.getenv("ICLOUD_EMAIL")
ICLOUD_APP_PASSWORD = os.getenv("ICLOUD_APP_PASSWORD")

# CalDAV server
CALDAV_URL = "https://caldav.icloud.com/"


def connect_to_icloud():
    """Establishes a CalDAV client connection to iCloud."""
    if not ICLOUD_EMAIL or not ICLOUD_APP_PASSWORD:
        raise ValueError("❌ Missing iCloud credentials in .env file.")

    client = DAVClient(CALDAV_URL, username=ICLOUD_EMAIL, password=ICLOUD_APP_PASSWORD)
    principal = client.principal()
    calendars = principal.calendars()
    return calendars


def add_reminder(summary: str, due_days: int = 1) -> bool:
    """Adds a reminder to the iCloud Reminders calendar."""
    try:
        calendars = connect_to_icloud()
        reminders_calendar = next((cal for cal in calendars if "Reminders" in cal.name), None)

        if not reminders_calendar:
            print("❌ Reminders calendar not found.")
            return False

        reminder_due = datetime.now() + timedelta(days=due_days)
        reminders_calendar.save_todo(summary=summary, due=reminder_due)
        print(f"✅ Reminder added: {summary} (Due in {due_days} day(s))")
        return True

    except Exception as e:
        print(f"❌ Error adding reminder: {e}")
        return False


def add_calendar_event(summary: str, start_time: datetime, duration_minutes: int = 60) -> bool:
    """Adds a calendar event to your iCloud calendar."""
    try:
        calendars = connect_to_icloud()
        # Prefer calendar named "Workouts", otherwise fallback to first calendar
        target_calendar = next(
            (cal for cal in calendars if "Workouts" in cal.name or "Calendar" in cal.name),
            calendars[0] if calendars else None
        )

        if not target_calendar:
            print("❌ No suitable calendar found.")
            return False

        end_time = start_time + timedelta(minutes=duration_minutes)

        event = Event()
        event.add("summary", summary)
        event.add("dtstart", start_time)
        event.add("dtend", end_time)
        event.add("dtstamp", datetime.now())

        cal = Calendar()
        cal.add_component(event)
        target_calendar.add_event(cal.to_ical())

        print(f"📆 Event added: {summary} from {start_time} to {end_time}")
        return True

    except Exception as e:
        print(f"❌ Error adding event: {e}")
        return False
