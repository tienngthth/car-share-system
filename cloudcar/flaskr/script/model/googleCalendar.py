# pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client httplib2
# python3 add_event.py --noauth_local_webserver

# Reference: https://developers.google.com/calendar/quickstart/python
# Documentation: https://developers.google.com/calendar/overview

# Be sure to enable the Google Calendar API on your Google account by following the reference link above and
# download the credentials.json file and place it in the same directory as this file.
import pathlib
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class GoogleCalendar():
    service = None

    def  __init__(self, user_name):
        SCOPES = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("flaskr/script/model/" "{}-token.json".format(user_name))
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets(
                "flaskr/script/model/credentials.json", 
                SCOPES
            )
            creds = tools.run_flow(flow, store)
        self.service = build("calendar", "v3", http=creds.authorize(Http()))

    def insert_event(self, rent_date, rent_time):
        event = {
            "summary": "Your car is ready - Car Share",
            "location": "Car Share Office",
            "description": "Please visit Car Share Office to pick up your car",
            "start": {
                "dateTime": "{}T{}:00:00+07:00".format(rent_date, rent_time),
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "end": {
                "dateTime": "{}T{}:30:00+07:00".format(rent_date, rent_time),
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    { "method": "email", "minutes": 5 },
                    { "method": "popup", "minutes": 10 },
                ],
            }
        }
        event = self.service.events().insert(calendarId = "primary", body = event).execute()
        print("Event created: {}".format(event.get("htmlLink")))