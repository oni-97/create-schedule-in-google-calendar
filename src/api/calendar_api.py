import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from api.event_body import EventBody

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class CalendarApi():
    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.__service = build('calendar', 'v3', credentials=creds)

    @property
    def service(self):
        return self.__service

    def get_events(self, max_results):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming' + str(max_results) + ' events')
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=max_results, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def insert_events(self, same_event_num):
        bodies = self.set_events_info(same_event_num)
        results = list()
        for body in bodies:
            result = self.service.events().insert(calendarId='primary', body=body).execute()
            results.append(result)
        return results

    def set_events_info(self, same_event_num):
        events = list()
        print('input event info')

        print('summary:', end=' ')
        summary = input()
        print('location:', end=' ')
        location = input()
        print('description:', end=' ')
        description = input()
        print('colorId:', end=' ')
        color_id = input()
        if color_id == '':
            color_id = str(0)
        for num in range(same_event_num):
            print('input ' + str(num+1) + 'th event time info')
            print('start time')
            start = self.set_event_time_info()
            print('end time')
            end = self.set_event_time_info()

            event_body = EventBody(
                summary, location, description, color_id, start, end)
            events.append(event_body.body)

        return events

    def set_event_time_info(self):
        time = {}
        print('year:', end=' ')
        time['year'] = self.convert_to_int(input())
        print('month:', end=' ')
        time['month'] = self.convert_to_int(input())
        print('day:', end=' ')
        time['day'] = self.convert_to_int(input())
        print('hour:', end=' ')
        time['hour'] = self.convert_to_int(input())
        print('minute:', end=' ')
        time['minute'] = self.convert_to_int(input())
        return time

    def convert_to_int(self, n):
        if n == '':
            return 0
        else:
            return int(n)
