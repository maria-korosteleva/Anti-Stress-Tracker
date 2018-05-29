import datetime as dt
from RecordClasses import Record
import fitbitWrapper


# returns the score level and a timestamp of the last avalible result
def get_last_score():
    today = dt.datetime.now().date()
    heartrate_stats = fitbitWrapper.get_heartrate_series(today, today+dt.timedelta(1), '1min')
    last_record = heartrate_stats[len(heartrate_stats)-1]
    sleeps = fitbitWrapper.get_sleep_ranges(today, today+dt.timedelta(1))
    if sleeps:
        if last_record.datetime < sleeps[-1][1]:
            last_record.sleep = True

    return last_record


# params:
# start, end - start and end of the time interval
# sr defines the distance between samples
#
# returns regularly distributed samples for a given interval, start included, end excluded
def get_stat_score(start, end, sr):
    heartrate_stats = fitbitWrapper.get_heartrate_series(start, end, '1min')
    sleeps = fitbitWrapper.get_sleep_ranges(start, end + dt.timedelta(1))
    heartrate_stats = __resample_and_average_timeseries(heartrate_stats, sr)
    if sleeps:
        heartrate_stats = __check_sleeping_records(heartrate_stats, sleeps)

    return heartrate_stats


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


# for every intro in timeseries check if the person was sleeping at the moment
def __check_sleeping_records(timeseries, sleep_ranges):
    record_id = 0
    for sleep_record in sleep_ranges:
        while timeseries[record_id].datetime < sleep_record[0]:
            record_id += 1
            if record_id >= len(timeseries):
                return timeseries
        while sleep_record[0] <= timeseries[record_id].datetime <= sleep_record[1]:
            timeseries[record_id].sleep = True
            record_id += 1
            if record_id >= len(timeseries):
                return timeseries
    return timeseries
