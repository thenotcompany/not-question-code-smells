from __future__ import annotations

import os
import requests


class EventTracker:

    def __init__(self):
        self.base_url = "https://api.eventtracker.com/v1"
        self.api_key = os.getenv("EVENT_TRACKER_API_KEY")

    def track_event(self, event_name: str, data: dict):
        url = f"{self.base_url}/events"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json={"event": event_name, "data": data})
        return response.json()
