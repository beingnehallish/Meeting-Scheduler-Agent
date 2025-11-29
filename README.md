

# **⏲️ MEETING SCHEDULER AGENT ⏲️** 

### *Built for the AI Agent Development Challenge — Rooman Technologies*

---

<p align="center">
  <img src="https://github.com/user-attachments/assets/97345af1-0b1f-4d27-bb3d-e7b3e575deb9" width="650">
</p>

---

## 🌟 **Overview**

The **AI Meeting Scheduler Agent** is an intelligent assistant that transforms natural-language meeting requests into **real, scheduled Google Calendar events**.

Using a powerful LLM, the agent can:

✔ Understand user intent from free-form text
✔ Extract meeting details (date, duration, attendees, constraints)
✔ Check real-time Google Calendar availability
✔ Suggest optimal meeting slots
✔ Create the event automatically



https://github.com/user-attachments/assets/ea577731-e4cd-4b62-8b44-a63e53c1b8ea



This project showcases **practical AI engineering**, **API integration**, and **autonomous agent design**, created as part of the **AI Agent Development Challenge**.

---

## ✨ **Features**

### 🔍 1. Natural Language Understanding

Type requests like:

> *"Schedule a 30-min sync with Rahul tomorrow between 3–5 PM."*

The agent extracts:

* Meeting purpose
* Duration
* Date & time window
* Mode
* Attendees

---

### 📅 2. Automatic Google Calendar Availability Check

Uses **Google Calendar FreeBusy API** to analyze availability in real-time.

---

### 💡 3. Smart Slot Suggestions

Suggests clean, conflict-free time slots based on user availability.

---

### ⚡ 4. One-Click Event Creation

Choose a slot → Agent immediately creates the event on Google Calendar.

---

### 🎨 5. Sleek Streamlit UI

A minimal, lavender-themed interface built for simplicity and speed.

---

## ⚠️ **Limitations**

* LLM accuracy depends on clarity of user input
* Timezone defaults to UTC (basic handling)
* No automated attendee email lookup
* Works with a single configured calendar
* No multi-calendar conflict resolution yet

---

## 🧠 **Tech Stack & APIs**

### 🧩 AI / LLM

* **OpenAI GPT** (via LangChain)

### 🏗 Framework

* **LangChain** → LLM orchestration & reasoning pipeline

### 🎛 Frontend UI

* **Streamlit**

### ☁️ APIs

* **Google Calendar API**
  (FreeBusy + Event Creation)

### 🔐 Authentication

* **Google Service Account**

### 📦 Dependencies

* python-dotenv
* dateutil
* pytz
* requests

---

## 🛠 **Setup & Run Instructions**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/beingnehallish/Meeting-Scheduler-Agent
cd meeting-scheduler-agent
```

### 2️⃣ Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 4. Configure Google Calendar API

1. Create a Google Cloud project
2. Enable **Google Calendar API**
3. Create a **Service Account**
4. Download the **JSON key**
5. Create a calendar and **share it** with the service account

   * Permission: *Make changes to events*
6. Save JSON key inside the repository

---

## 🔧 5. Create `.env`

Example:

```
OPENAI_API_KEY=sk-xxxx
GOOGLE_SERVICE_ACCOUNT_JSON=D:\projects\Calender-Agent\service_account.json
GOOGLE_SERVICE_ACCOUNT_CALENDAR_ID=your_calendar_id@group.calendar.google.com
```

---

## ▶️ 6. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

App opens at:
📍 [http://localhost:8501](http://localhost:8501)

---

## 🚀 **Potential Improvements**

### 🕒 1. Automatic Timezone Detection

Convert UTC → user local timezone.

### 🗂 2. Multi-Calendar Support

Schedule across multiple calendars seamlessly.

### 👥 3. Attendee Email Resolution

Integrate Google People API to auto-map names → emails.

### 🧠 4. Intelligent Slot Ranking

Avoid lunch hours, prioritize mornings, use ML ranking.

### ✏️ 5. Modify or Delete Events

Add update/cancel event actions.

### 🔐 6. OAuth-Based Login

Each user connects their own calendar securely.

### 💬 7. Multi-Turn Conversation

Bot asks clarifying questions when needed.

---

## 🏁 **Final Notes**

This project demonstrates the **full lifecycle** of an AI-powered meeting scheduler:

✨ LLM Reasoning
✨ Natural Language Parsing
✨ Real-world Calendar API Execution
✨ Clean Frontend
✨ Autonomous Agent Workflow

