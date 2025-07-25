from datetime import datetime, timedelta
from icloud_sync import add_reminder, add_calendar_event

# Test Reminder
print("⏱ Testing Reminder...")
add_reminder("Test Reminder from Python", due_days=1)

# Test Calendar Event (1 hour from now)
print("📅 Testing Calendar Event...")
event_time = datetime.now() + timedelta(hours=1)
add_calendar_event("Test Event from Python", event_time, duration_minutes=60)
