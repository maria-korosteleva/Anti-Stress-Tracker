import ConfigParser
import fitbit
from RecordClasses import HeartRateRecord
import datetime as dt

config_filename = 'config.ini'


def __store_token(token_dict):
    # Function for refreshing access_token, refresh_token, and expires_at.
    file_config = open(config_filename, 'w')
    config = ConfigParser.SafeConfigParser()
    config.read(config_filename)

    config.set('Login Parameters', 'ACCESS_TOKEN', token_dict['access_token'])
    config.set('Login Parameters', 'REFRESH_TOKEN', token_dict['refresh_token'])
    config.set('Login Parameters', 'EXPIRES_AT', str(int(token_dict['expires_at'])))

    config.write(file_config)
    file_config.close()
    return


def __read_config():
    parser = ConfigParser.SafeConfigParser()
    parser.read(config_filename)
    CLIENT_ID = parser.get('Login Parameters', 'C_ID')
    CLIENT_SECRET = parser.get('Login Parameters', 'C_SECRET')
    ACCESS_TOKEN = parser.get('Login Parameters', 'ACCESS_TOKEN')
    REFRESH_TOKEN = parser.get('Login Parameters', 'REFRESH_TOKEN')
    EXPIRES_AT = parser.get('Login Parameters', 'EXPIRES_AT')

    return CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRES_AT


def __get_client():
    CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN, EXPIRES_AT = __read_config()

    client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True,
                           access_token=ACCESS_TOKEN,
                           refresh_token=REFRESH_TOKEN,
                           expires_at=EXPIRES_AT,
                           refresh_cb=__store_token)
    return client


def get_heartrate_series(start_date, end_date, detail_level):
    client = __get_client()
    # start_date
    stats = client.intraday_time_series('activities/heart', base_date='2018-05-26', detail_level=detail_level)
    beauty_stats = []
    for elem in stats['activities-heart-intraday']['dataset']:
        # get the time in datetime format
        timestamp = dt.datetime.strptime('2018-05-26'+elem['time'], '%Y-%m-%d%H:%M:%S')
        beauty_stats.append(HeartRateRecord(elem['value'], timestamp))
    # print stats
    return beauty_stats
    # self.client.intraday_time_series('activities/heart', base_date='2018-05-27', detail_level=detail_level)
