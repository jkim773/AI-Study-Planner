
from datetime import datetime, timezone, timedelta
import GoogleCalendarExtract
import GoogleCalendarInsert
import ChatGPT


"""
For example,
    schedule a group study in july 30th is valid given these constraints
    event1
	    2025-06-30T00:00:00+09:00
	    2025-06-30T13:00:00+09:00
    event2
	    2025-06-30T14:00:00+09:00
	    2025-07-01T00:00:00+09:00
    because there is still a 1 hour gap between 13:00:00 to 14:00:00
"""



def main():

    
    avoidTheseEvents = GoogleCalendarExtract.getAllEventsNext6Months(calendarID)


    # Define current date in KST
    # Set timezone to Korea Standard Time (UTC+9)
    KST = timezone(timedelta(hours=9))
    now = datetime.now(KST)
    now_iso = now.replace(microsecond=0).isoformat()

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
    {avoidTheseEvents}


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



    print(now_iso)
    print(avoidTheseEvents)
    # prompt_text = "schedule an hour meeting on july 5 after 14:00"
    # prompt_text = "schedule a meeting on 2025-07-05,16:00,17:00"
    # prompt_text = "schedule an hour meeting on july 4"
    prompt_text = "schedule an hour meeting on july 7, 8, 9"



    ChatGPTOutput = ChatGPT.ask_chatgpt(output_requirement, prompt_text)
    print(ChatGPTOutput)
    # Examples of ChatGPT output
    # 2025-07-04,14:00,15:00,Schedule Meeting
    # 2025-06-30,13:00,14:00,Study Math test
    # 2025-07-01,13:00,14:00,Study Math test
    # 2025-07-02,13:00,14:00,Study Math test
    # 2025-07-03,13:00,14:00,Study Math test
    # 2025-07-05,13:00,14:00,Study Math test
    # 2025-07-06,13:00,14:00,Study Math test
    # 2025-07-07,13:00,14:00,Study Math test
    GoogleCalendarInsert.create_events_from_ChatGPT_output(calendarID, ChatGPTOutput)

# Error creating event for line: 2025-06-30,13:00,14:00,Study Math Test
# <HttpError 403 when requesting
# GPT-4.1
# GPT-4o
# ChatGPT-4o
# GPT-4.1 mini
# GPT-4.1 nano
# GPT-4o mini












if __name__ == "__main__":
    main()
