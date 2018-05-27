import ConfigParser
import fitbit
from RecordClasses import HeartRateRecord
import datetime as dt


class FitbitWrapper:
    def __init__(self):
        parser = ConfigParser.SafeConfigParser()
        parser.read('config.ini')
        CLIENT_ID = parser.get('Login Parameters', 'C_ID')
        CLIENT_SECRET = parser.get('Login Parameters', 'C_SECRET')
        ACCESS_TOKEN = parser.get('Login Parameters', 'ACCESS_TOKEN')
        REFRESH_TOKEN = parser.get('Login Parameters', 'REFRESH_TOKEN')

        self.client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                                    refresh_token=REFRESH_TOKEN)
        return

    def get_heartrate_series(self, start_date, end_date, detail_level):
        # start_date
        stats = self.client.time_series('activities/heart', base_date='2018-05-26', end_date='2018-05-27')
        beauty_stats = []
        for elem in stats['activities-heart-intraday']['dataset']:
            
            beauty_stats.append(HeartRateRecord(elem['value'], elem['time']))
        # print stats
        return beauty_stats
        # self.client.intraday_time_series('activities/heart', base_date='2018-05-27', detail_level=detail_level)
