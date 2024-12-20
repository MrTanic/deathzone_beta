import requests
import json
from pytz import timezone
from datetime import datetime

# Globale Zeitzone festlegen
GERMAN_TIMEZONE = timezone('Europe/Berlin')

def send_webhook_notification(webhook_url, title, description, success=True, next_run_time=None, color=None):
    if color is None:
        color = 0x00FF00 if success else 0xFF0000
    elif success is None:
        color = 0xFFA500  # Orange für kein aktiver Krieg
    elif success == "preparation":
        color = 0xFFFF00  # Gelb für Vorbereitungstag

    current_time = datetime.now(GERMAN_TIMEZONE).strftime("%d-%m-%Y %H:%M:%S")
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "footer": {"text": f"Next: {next_run_time or 'Not scheduled'}"},
        "author": {
            "name": f"Sent {current_time}"
        }
    }

    data = {"embeds": [embed]}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification: {response.status_code}, {response.text}")