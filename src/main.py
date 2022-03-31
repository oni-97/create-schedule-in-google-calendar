from __future__ import print_function

from googleapiclient.errors import HttpError
from api.calendar_api import CalendarApi


def main():
    # print_events(10)
    insert_events(2)


def insert_events(same_event_num):
    try:
        api = CalendarApi()
        events = api.insert_events(same_event_num)

        if not events:
            print('No events inserted.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            print(start, end,  event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


def print_events(max_results):
    try:
        api = CalendarApi()
        events = api.get_events(max_results)

        if not events:
            print('No upcoming events found.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            print(start, end, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
