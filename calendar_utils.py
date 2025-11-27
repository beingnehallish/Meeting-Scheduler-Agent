# calendar_utils.py
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar']

def build_service_from_service_account(sa_json_path: str):
    creds = service_account.Credentials.from_service_account_file(sa_json_path, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
    return service

def find_free_slots(service_account_json: str, calendar_id: str, window_start: str, window_end: str, duration_minutes: int = 30, max_suggestions: int = 3):
    """
    Returns a list of suggested start times in ISO format (UTC).
    window_start and window_end can be ISO strings or datetime objects.
    """
    if isinstance(window_start, str):
        window_start_dt = date_parser.parse(window_start)
    else:
        window_start_dt = window_start
    if isinstance(window_end, str):
        window_end_dt = date_parser.parse(window_end)
    else:
        window_end_dt = window_end

    service = build_service_from_service_account(service_account_json)

    body = {
        "timeMin": window_start_dt.isoformat(),
        "timeMax": window_end_dt.isoformat(),
        "items": [{"id": calendar_id}],
    }
    fb = service.freebusy().query(body=body).execute()
    busy_periods = fb['calendars'][calendar_id]['busy']

    # construct available slots
    candidate_start = window_start_dt
    suggestions = []
    while candidate_start + timedelta(minutes=duration_minutes) <= window_end_dt and len(suggestions) < max_suggestions:
        candidate_end = candidate_start + timedelta(minutes=duration_minutes)
        overlap = False
        for b in busy_periods:
            bstart = date_parser.parse(b['start'])
            bend = date_parser.parse(b['end'])
            if not (candidate_end <= bstart or candidate_start >= bend):
                overlap = True
                candidate_start = bend  # skip to end of busy
                break
        if not overlap:
            suggestions.append(candidate_start.astimezone(pytz.UTC).isoformat())
            candidate_start = candidate_start + timedelta(minutes=duration_minutes + 5)
    return suggestions

def create_calendar_event(service_account_json: str, calendar_id: str, start: str, end: str, summary: str, attendees: list = None, description: str = ""):
    service = build_service_from_service_account(service_account_json)
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start, 'timeZone': 'UTC'},
        'end': {'dateTime': end, 'timeZone': 'UTC'},
    }
    if attendees:
        event['attendees'] = [{'email': a} if '@' in a else {'displayName': a} for a in attendees]

    created = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created
