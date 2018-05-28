import datetime as dt
from RecordClasses import Record
import fitbitWrapper


# returns the score level and a timestamp of the last avalible result
def get_last_score():
    today = dt.datetime.now().date()
    heartrate_stats = fitbitWrapper.get_heartrate_series(today, today+dt.timedelta(1), '1min')
    last_record = heartrate_stats[len(heartrate_stats)-1]
    return last_record


# params:
# start, end - start and end of the time interval
# sr defines the distance between samples
#
# returns regularly distributed samples for a given interval, start included, end excluded
def get_stat_score(start, end, sr):
    heartrate_stats = fitbitWrapper.get_heartrate_series(start, end, '1min')

    return __resample_and_average_timeseries(heartrate_stats, sr)


# returns regularly distributed samples for a given samplerate.
# Values are averaged inside the sample interval
# if there are no values in the given interval, the value for the sample is set to zero
def __resample_and_average_timeseries(timeseries, sr):
    averaged = [timeseries[0]]
    interval = []
    start_interval = timeseries[0].datetime
    for record in timeseries:
        while record.datetime > start_interval + sr:
            value = sum(interval) / len(interval) if len(interval) else 0
            averaged.append(Record(value, start_interval+sr))
            start_interval = start_interval + sr
            interval = []
        else:
            interval.append(record.value)

    return averaged
