import datetime


class EventBody():
    def __init__(self, summary, location, description, color_id, start, end):
        self.__body = {
            'summary': summary,
            'location': location,
            'description': description,
            'colorId': color_id,
            'start': {
                'dateTime': datetime.datetime(start['year'], start['month'], start['day'], start['hour'], start['minute']).isoformat(),
                'timeZone': 'Japan',
            },
            'end': {
                'dateTime': datetime.datetime(end['year'], end['month'], end['day'], end['hour'], end['minute']).isoformat(),
                'timeZone': 'Japan',
            },
        }

    @property
    def body(self):
        return self.__body
