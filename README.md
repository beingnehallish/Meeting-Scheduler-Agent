AI MEETING SCHEDULER - README (TEXT VERSION)

---

## Overview

The AI Meeting Scheduler Agent is an automated scheduler that converts natural-language meeting requests into actual Google Calendar events.
It uses a language model to parse user instructions, determine the meeting timing, check availability using the Google Calendar FreeBusy API, suggest free time slots, and create events when confirmed by the user.

This project is built for the AI Agent Development Challenge and demonstrates practical AI engineering ability, API integration, and an autonomous agent workflow.

---

## Features

1. Natural Language Understanding
   Users can type free-form requests such as:
   "Schedule a 30-min sync with Rahul tomorrow between 3–5 PM."
   The agent extracts duration, attendees, meeting purpose, date/time window, and meeting mode.

2. Automatic Calendar Availability Check
   Uses Google Calendar freebusy() API to find available slots.

3. Smart Slot Suggestions
   Suggests free time slots based on the user's availability.

4. One-Click Event Creation
   User selects a slot and the agent creates a meeting in Google Calendar.

5. Streamlit UI
   Clean, interactive, lightweight UI with lavender-themed styling.

---

## Limitations

* LLM parsing depends on input clarity; ambiguous requests may need correction.
* Timezone awareness is basic (defaults to UTC).
* Attendee email resolution is not automated.
* Only one calendar is supported (defined in .env).
* No advanced conflict resolution across multiple calendars.

---

## Tech Stack and APIs Used

AI / LLM:

* OpenAI GPT (via LangChain)

Framework:

* LangChain for LLM orchestration

Frontend:

* Streamlit

APIs:

* Google Calendar FreeBusy API
* Google Calendar Events API

Authentication:

* Google Service Account

Environment:

* python-dotenv
* .env variables

Other Libraries:

* dateutil
* pytz
* requests

---

## Setup and Run Instructions

1. Clone the project
   git clone <your-repo-url>
   cd meeting-scheduler-agent

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate   (Windows)

3. Install dependencies
   pip install -r requirements.txt

4. Set up Google Calendar API

* Create a Google Cloud project
* Enable Google Calendar API
* Create a Service Account
* Download the JSON key
* Create a new calendar and share it with the service account email
  Permission: Make changes to events
* Place the JSON file in your project directory

5. Create .env file
   Example:
   OPENAI_API_KEY=sk-xxxx
   GOOGLE_SERVICE_ACCOUNT_JSON=D:\projects\Calender-Agent\service_account.json
   GOOGLE_SERVICE_ACCOUNT_CALENDAR_ID=[your_calendar_id@group.calendar.google.com](mailto:your_calendar_id@group.calendar.google.com)

6. Run Streamlit app
   streamlit run streamlit_app.py

App URL:
[http://localhost:8501](http://localhost:8501)

---

## Potential Improvements

1. Timezone Awareness
   Automatically detect local timezone and convert UTC times.

2. Multi-Calendar Support
   Let users switch between multiple calendars.

3. Email Resolution for Attendees
   Use Google People API to map names to emails.

4. Smart Slot Ranking
   Avoid lunch hours, prioritize efficient times, or use ML ranking.

5. Editing and Deleting Events
   Add UI options to modify or cancel events.

6. OAuth Login
   Let each user schedule on their own calendar instead of a shared service account calendar.

7. Multi-turn Conversations
   Agent can ask clarifying questions like:
   "Do you want this meeting online or in person?"

---

## Final Notes

This project demonstrates the complete lifecycle of an AI-powered meeting scheduling agent: LLM reasoning, parsing, API integration, and real-world calendar automation.
It meets the AI Agent Development Challenge requirements such as real use-case creation, API usage, UI demonstration, and clear system architecture.
