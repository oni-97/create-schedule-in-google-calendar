from __future__ import print_function

from googleapiclient.errors import HttpError
from api.calendar_api import CalendarApi


def main():
    while True:
        print('input menu number')
        print('1: get  2: insert')
        try:
            menu =  input()
            if(menu == '1'):
                print('input maximum number of events')
                max_results =  input()
                insert_events(max_results)
            elif(menu == '2'):
                print('input insert number of same events')
                same_event_num =  input()
                insert_events(same_event_num)
        except EOFError:
            break
        
        



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
