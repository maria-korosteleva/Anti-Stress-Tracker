import datetime as dt
from RecordClasses import Record
import fitbitWrapper


# returns the score level and a timestamp of the last avalible result
def get_last_score():
    today = dt.datetime.now().date()
    # get the info of the last sync time
    heartrate_stats = fitbitWrapper.get_heartrate_series(today, today+dt.timedelta(1), '1min')
    last_record = heartrate_stats[len(heartrate_stats)-1]
    # get precise heartrate data
    timerange = (last_record.datetime - dt.timedelta(minutes=2), last_record.datetime)
    heartrate_stats = fitbitWrapper.get_heartrate_series(today, today + dt.timedelta(1), '1sec',
                                                         start_time=timerange[0], end_time=timerange[1])

    # calculate the stress level
    # assume that we have a continuous data on the heartrate (without breaks)
    hr_values = [r.value for r in heartrate_stats]
    score = Record(__stress_score(hr_values), last_record.datetime)

    sleeps = fitbitWrapper.get_sleep_ranges(today, today+dt.timedelta(1))
    if sleeps:
        if score.datetime < sleeps[-1][1]:
            score.sleep = True

    return score


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


# returns last (interval) of timeseries
def __cut_timeseries(timeseries, interval):
    last_time = timeseries[-1].datetime
    record_id = len(timeseries) - 1
    while timeseries[record_id].datetime > last_time - interval:
        record_id -= 1
    return timeseries[record_id:]


# params: series of the heartrate records. Each record is assumed to be significant (non-zero)
# and all records are assumed to be equally and densely dustributed in time domain
# returns estimated score for a given series of heartrate records
def __stress_score(hr):
    # see http://www.cardiometry.net/issues/no10-may-2017/heart-rate-variability-analysis
    # originally from book https://www.twirpx.com/file/2327193/ (in Russian)
    # score = AMo / (2 * VR * Mo)
    # R-R interval - time delay between consecutive heart beats (assumed to be inverse value of the bpm)
    # Mo - mode - most frequent R-R interval value
    # AMo - mode amplitude - % of the intervals corresponding to Mode
    # VR - variational range - difference  between min and max R-R intervals
    r_r = [round(60./float(r), 3) for r in hr]

    # naive calculations, might be improved
    min = 200
    max = 0
    mode = 0
    mode_freq = 0
    for record in r_r:
        if record < min:
            min = record
        if record > max:
            max = record
        freq = r_r.count(record)
        if freq > mode_freq:
            mode_freq = freq
            mode = record
    # DEBUG
    print r_r
    print min, max, mode, mode_freq

    VR = max - min
    Amode = mode_freq / float(len(r_r)) * 100

    return round(Amode / (2 * VR * mode))
