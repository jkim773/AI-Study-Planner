from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta

# If modifying these SCOPES, delete token.json
SCOPES = ['https://www.googleapis.com/auth/calendar']




def getCredFromToken():
    creds = None
    # Load credentials from token.json if available
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)

    # If no valid credentials, login
    # if you don't have cred or even if you have one it's not valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Starts a browser window to authenticate
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    return creds




def getAllTheEventsAfterNow(inputCalendarID):
    """Shows the upcoming 10 events on the user's primary calendar."""
    creds = getCredFromToken()

    # Connect to the Google Calendar API
    service = build('calendar', 'v3', credentials=creds)

    # Get current time in UTC format
    # DEPRECATED
    # now = datetime.datetime.utcnow().isoformat() + 'Z'
    now = datetime.now(timezone.utc).isoformat()

    # print('Getting the upcoming 10 events')

    # Call the Calendar API
    # get a dictionary of metadata of the calendar and its events
    events_result = service.events().list(calendarId=inputCalendarID, timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return


    allTheEvents = ""
    # Print events
    for event in events:
        summary = event.get('summary', 'No Title')
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        thisEvent = summary + "\n\t" + start + "\n\t" +  end + "\n"


        allTheEvents = allTheEvents + thisEvent
        # print(f"{summary}")
        # print(f"   Start: {start}")
        # print(f"   End:   {end}\n")
    # print(allTheEvents)
    return allTheEvents







def getAllEventsNext6Months(inputCalendarID):
    creds = getCredFromToken()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.now(timezone.utc)
    time_min = now.isoformat()
    time_max = (now + timedelta(days=30*6)).isoformat()  # approx 6 months

    events_result = service.events().list(
        calendarId=inputCalendarID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
        return

    allTheEvents = ""
    for event in events:
        summary = event.get('summary', 'No Title')
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        allTheEvents += f"{summary}\n\t{start}\n\t{end}\n"

    return allTheEvents



if __name__ == '__main__':
    getAllTheEventsAfterNow()
