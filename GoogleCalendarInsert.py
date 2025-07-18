import GoogleCalendarExtract
from googleapiclient.discovery import build





def create_events_from_ChatGPT_output(inputCalendarID, chatgpt_output):
    creds = GoogleCalendarExtract.getCredFromToken()
 


    service = build('calendar', 'v3', credentials=creds)
    calendar_id = inputCalendarID  # or your specific calendar ID

    lines = chatgpt_output.strip().split("\n")

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) < 4:
            continue

        date_str, start_time, end_time, summary = parts

        if start_time == "N/A" or end_time == "N/A":
            continue  # skip unavailable days

        try:
            # Format: 2025-06-29,09:00,10:00,...
            start_datetime = f"{date_str}T{start_time}:00+09:00"
            end_datetime = f"{date_str}T{end_time}:00+09:00"

            event = {
                'summary': summary.strip(),
                'start': {'dateTime': start_datetime, 'timeZone': 'Asia/Seoul'},
                'end': {'dateTime': end_datetime, 'timeZone': 'Asia/Seoul'},
            }

            created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f"✅ Event created: {created_event['summary']} ({start_datetime} - {end_datetime})")

        except Exception as e:
            print(f"❌ Error creating event for line: {line}")
            print(str(e))

