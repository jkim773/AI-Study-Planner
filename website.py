import streamlit as st
from datetime import datetime, timezone, timedelta
import GoogleCalendarExtract
import GoogleCalendarInsert
import ChatGPT

def main():
    st.markdown(
        """
        <style>
        /* Ensure full-screen layout */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            height: 100%;
            margin: 0;
            padding: 0;
        }

        /* Background image and dimming overlay */
        [data-testid="stApp"] {
            background: linear-gradient(
                rgba(0, 0, 0, 0.5), 
                rgba(0, 0, 0, 0.5)
            ),
            url("https://cdn.pixabay.com/photo/2017/05/08/19/04/agenda-2296195_1280.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        """,

    # User input
    user_input = st.text_input("What do you want to schedule? (e.g., 'schedule meeting on 7/5'):")
    calendar_id = st.text_input("Enter your Google Calendar ID:")



    if "chatgpt_output" not in st.session_state:
        st.session_state.chatgpt_output = ""

    if st.button("Generate Schedule"):
        if not user_input or not calendar_id:
            st.error("Please provide both the request and the calendar ID.")
            return

        # Current time in KST
        KST = timezone(timedelta(hours=9))
        now = datetime.now(KST)
        now_iso = now.replace(microsecond=0).isoformat()

        # Fetch events to avoid
        avoid_events = GoogleCalendarExtract.getAllEventsNext6Months(calendar_id)

        # Prompt
        output_requirement = f"""
        Current datetime is {now_iso}
        Make it parsing friendly.
        Respond only with CSV-like output
        Don't say anything extra like "Sure, I can help you create a study plan. Here's a suggested schedule:"
        Turn the dates into number
        Don’t assume what the user has to study unless specified
        Always have starting time and ending time
        If the user provides the date of scheduling as July 4th. Assume current year

        The constraint of scheduling:
        1 Do not schedule anything before current time.
        2 If scheduling is invalid. Literally output "Invalid" and provide a reason why.
        For example, if the user tries to schedule on june 5 when todays date is june 8.


        if current date is 
        2025-06-29T15:41:22.875616+09:00

        event1
            2025-06-30T00:00:00+09:00
            2025-06-30T13:00:00+09:00
        event2
            2025-06-30T14:00:00+09:00
            2025-07-01T00:00:00+09:00

        Bad Output:
        2025-06-30,N/A,N/A,Scheduling is invalid (No available time slots due to existing events)
        There is a 1 hour gap 13:00:00 and 14:00:00

        Good Output:
        2025-06-30,13:00,14:00,Schedule Meeting

        Always avoid these events but use any 1 hour or more time gap available unless specified:
        {avoid_events}


        Example input:
        physics test, difficulty level 4, study all material by march 13th (test day), not available on march 8th due to family dinner

        Example output:
        2025-03-07,17:00,19:00,Review notes and identify weak topics
        2025-03-08,N/A,N/A,Unavailable (Family Dinner)
        2025-03-09,15:00,17:00, Study Physics test
        2025-03-10,19:00,21:00, Study Physics test
        2025-03-11,19:00,21:00, Study Physics test
        2025-03-12,20:00,22:00, Study Physics test
        """


        # Ask ChatGPT
        chatgpt_output = ChatGPT.ask_chatgpt(output_requirement, user_input)
        st.session_state.chatgpt_output = chatgpt_output


    # Show output if available
    if st.session_state.chatgpt_output:
        st.text_area("ChatGPT Generated Schedule (CSV):", st.session_state.chatgpt_output, height=200)

        if st.button("Add to Google Calendar"):
            try:
                GoogleCalendarInsert.create_events_from_ChatGPT_output(calendar_id, st.session_state.chatgpt_output)
                st.success("Events added to Google Calendar.")
            except Exception as e:
                st.error(f"Error adding events: {e}")

if __name__ == "__main__":
    main()
