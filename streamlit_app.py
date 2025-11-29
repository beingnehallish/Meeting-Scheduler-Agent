import streamlit as st
from dotenv import load_dotenv
import os
from agent import MeetingAgent

load_dotenv()

lavender_css = """
<style>

/* ───────────────────────────────
   TOP LOGO  
────────────────────────────────*/
.logo-container {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.top-logo {
    width: 250px;
    height: auto;
}


/* ───────────────────────────────
   CHALLENGER BOX  
────────────────────────────────*/
.challenger-box {
    background: #ffffff;
    border-radius: 14px;
    padding: 30px 25px;
    width: 240px;
    float: right;
    margin-top: 10px;
    box-shadow: 4px 6px 0px rgba(0,0,0,0.25);
    border: 1px solid #ddd;
}

.challenger-title {
    font-size: 100px;
    color: #444;
    margin: 0;
    font-weight: 500;
}

.challenger-name {
    font-size: 100px;
    margin-top: 6px;
    color: #000;
    font-weight: 600;
}


/* Existing styling… */
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

textarea, input, select {
    background-color: #fafafa !important;
    color: #000 !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    padding: 10px !important;
}

h1, h2, h3, h4 {
    color: #222 !important;
}

.stSuccess {
    background-color: #E9FCE8 !important;
    border-radius: 8px !important;
}

</style>
"""
st.markdown(lavender_css, unsafe_allow_html=True)

# ---------- Streamlit Page ----------
st.set_page_config(page_title="AI Meeting Scheduler", layout="centered")
# ----- TOP BAR: LOGO + CHALLENGER CARD -----
col1, col2 = st.columns([3, 3.6])
with col1:
    st.image("logo.jpeg", width=180)


with col2:
    st.markdown(
        """
        <div class="challenger-box">
            <p class="challenger-title">Challenger:</p>
            <p class="challenger-name">Nehal Gupta</p>
        </div>
        """,
        unsafe_allow_html=True
    )

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
