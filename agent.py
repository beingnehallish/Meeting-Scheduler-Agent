# agent.py
import os
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List
from langchain_community.llms import OpenAI
from calendar_utils import find_free_slots, create_calendar_event
from dotenv import load_dotenv

load_dotenv()

class MeetingAgent:
    def __init__(self, openai_api_key: str, service_account_json: str = None, calendar_id: str = None):
        self.openai_api_key = openai_api_key
        self.llm = OpenAI(openai_api_key=openai_api_key, temperature=0.1)
        self.service_account_json = service_account_json
        self.calendar_id = calendar_id

    def handle_request(self, text: str) -> Dict[str, Any]:
        """
        1) Use LLM to parse intent (title, duration, attendees, preferred window, mode)
        2) Check calendar availability (freebusy)
        3) Suggest slots or auto-create event
        """
        parsed = self.parse_request(text)
        response = {"parsed": parsed, "message": "", "suggestions": []}

        # check for required fields (duration & time window)
        duration_min = parsed.get("duration") or 30
        window = parsed.get("window")  # dict with start/end datetimes

        # call calendar to find free slots
        try:
            slots = find_free_slots(
                service_account_json=self.service_account_json,
                calendar_id=self.calendar_id,
                window_start=window["start"],
                window_end=window["end"],
                duration_minutes=duration_min,
                max_suggestions=3
            )
            response["suggestions"] = slots
            if slots:
                response["message"] = f"I found {len(slots)} available slot(s). Do you want me to book the first one?"
            else:
                response["message"] = "No free slots found in that window. I can suggest times outside your window if you'd like."
            return response
        except Exception as e:
            response["message"] = f"Calendar check failed: {e}"
            return response

    def create_event_from_slot(self, parsed: Dict[str,Any], slot_iso: str) -> Dict[str,Any]:
        """
        slot_iso is an ISO datetime start, we book for parsed['duration'] minutes
        """
        start_dt = datetime.fromisoformat(slot_iso)
        duration_min = parsed.get("duration", 30)
        end_dt = start_dt + timedelta(minutes=duration_min)
        title = parsed.get("title") or f"Meeting — {', '.join(parsed.get('attendees', []))}"
        created = create_calendar_event(
            service_account_json=self.service_account_json,
            calendar_id=self.calendar_id,
            start=start_dt.isoformat(),
            end=end_dt.isoformat(),
            summary=title,
            attendees=parsed.get("attendees", [])
        )
        return created

    def parse_request(self, text: str) -> Dict[str,Any]:
        """
        Basic LLM-based parsing with fallback regex parsing.
        We use the LLM to extract: title, duration (minutes), attendees (list), preferred window (start/end), mode
        """
        prompt = f"""
Extract meeting metadata from the following user request. Return a JSON only with keys:
title, duration (minutes, integer or null), attendees (list of names/emails), window (with keys start and end in ISO 8601 or null), mode (online/in-person/zoom).
User request: \"\"\"{text}\"\"\"
If a precise date wasn't mentioned, choose the next reasonable day (tomorrow) as the window.
If only time range like 'between 3-5pm tomorrow' is mentioned, set start to the start of the range and end to the end.
Return JSON.
"""
        raw = self.llm.invoke(prompt)

        # attempt to get JSON from raw - naive approach
        import json
        try:
            parsed_json = json.loads(raw.strip())
        except Exception:
            # fallback -- simple rule-based
            parsed_json = self.simple_parse(text)
        # canonicalize window datetimes
        if parsed_json.get("window") and isinstance(parsed_json["window"].get("start"), str):
            # assume ISO-like or natural -> keep as-is; calendar_utils will parse
            pass
        return parsed_json

    def simple_parse(self, text: str) -> Dict[str,Any]:
        # very naive fallback parsing
        duration = None
        m = re.search(r'(\d+)\s*(min|mins|minutes)', text.lower())
        if m:
            duration = int(m.group(1))
        # pick next day window if no explicit date
        tomorrow = datetime.utcnow().date() + timedelta(days=1)
        start = datetime.combine(tomorrow, datetime.min.time()) + timedelta(hours=9)  # 9 AM
        end = start + timedelta(hours=8)  # 9am-5pm
        return {"title": None, "duration": duration or 30, "attendees": [], "window": {"start": start.isoformat(), "end": end.isoformat()}, "mode": "online"}
