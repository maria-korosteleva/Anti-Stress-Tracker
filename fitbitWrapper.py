import ConfigParser
import fitbit
from RecordClasses import Record
import datetime as dt
import time

config_filename = 'config.ini'


# returns heartrate stats for a dayrange with start_date included, end_date excluded
def get_heartrate_series(start_date, end_date, detail_level):
    if not detail_level in ['1sec', '1min', '15min']:
        raise ValueError("Period must be either '1sec', '1min', or '15min'")

    client = __get_client()
    beauty_stats = []
    for day_number in range((end_date - start_date).days):
        base_date = start_date+dt.timedelta(day_number)
        stats = client.intraday_time_series('activities/heart',
                                            base_date=base_date,
                                            detail_level=detail_level)

        for elem in stats['activities-heart-intraday']['dataset']:
            # get the time in datetime format
            timestamp = dt.datetime.strptime(elem['time'], '%H:%M:%S')
            beauty_stats.append(Record(elem['value'], dt.datetime.combine(base_date, timestamp.time())))
    return beauty_stats


# returns sleeping ranges (start-end time of the sleep) for given dates, end date excluded
# includes both night sleep and naps
def get_sleep_ranges(start_date, end_date):
    client = __get_client()
    beauty_stats = []
    for day_number in range((end_date - start_date).days):
        base_date = start_date+dt.timedelta(day_number)
        stats = client.sleep(date=base_date)['sleep']
        for elem in stats:
            start = dt.datetime.strptime(elem['startTime'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            duration = dt.timedelta(minutes=elem['timeInBed'])
            end = start + duration
            beauty_stats.append((start, end))
    return beauty_stats


# Private methods #
def __store_token(token_dict):
    # Function for refreshing access_token, refresh_token, and expires_at.
    config = ConfigParser.SafeConfigParser()
    config.read(config_filename)

    file_config = open(config_filename, 'w')
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
