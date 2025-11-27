import streamlit as st
from dotenv import load_dotenv
import os
from agent import MeetingAgent

load_dotenv()

lavender_css = """
<style>
.stApp {
    background-color: #ffffff !important;
}
p{
    color:black;
}
button, .stButton>button, .stForm button, button[kind="primary"], button[type="submit"], div.stButton > button  {
    background-color: #4A7BFF !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}
button * {
    color: white !important;
}

/* INPUT FIELDS */
textarea, input, select {
    background-color: #fafafa !important;
    color: #000 !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    padding: 10px !important;
}

/* HEADERS */
h1, h2, h3, h4 {
    color: #222 !important;
}

/* SUCCESS BOX */
.stSuccess {
    background-color: #E9FCE8 !important;
    border-radius: 8px !important;
}

</style>
"""
st.markdown(lavender_css, unsafe_allow_html=True)

# ---------- Streamlit Page ----------
st.set_page_config(page_title="AI Meeting Scheduler", layout="centered")

st.title("Meeting Scheduler Agent — Internship Challenge")
st.markdown("Enter a natural language request (Example: 'Schedule 30-min sync with Rahul tomorrow between 3–5 PM')")

agent = MeetingAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    service_account_json=os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"),
    calendar_id=os.getenv("GOOGLE_SERVICE_ACCOUNT_CALENDAR_ID")
)

with st.form("main_form"):
    user_text = st.text_area("Your Request", height=140)
    submit = st.form_submit_button("Process")

if submit and user_text.strip():
    with st.spinner("Thinking... Checking calendar..."):
        result = agent.handle_request(user_text)

    st.subheader("AI Response")
    st.write(result["message"])

    if result.get("suggestions"):
        st.markdown("### Suggested Slots")
        for slot in result["suggestions"]:
            st.write(f"- {slot}")

    if result.get("event_created"):
        st.success("Event created successfully!")
        st.json(result["event_created"])

    # Let the user confirm a slot
    if result.get("suggestions"):
        idx = st.selectbox("Choose a slot to create the event:",
                           range(len(result["suggestions"])),
                           format_func=lambda i: result["suggestions"][i])

        if st.button("Create Event"):
            slot = result["suggestions"][idx]
            with st.spinner("Creating event..."):
                created = agent.create_event_from_slot(result["parsed"], slot)
            st.success("Event created!")
            st.json(created)
