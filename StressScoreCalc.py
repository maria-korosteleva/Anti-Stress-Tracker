import datetime as dt
from RecordClasses import Record
import fitbitWrapper

ss_duration = dt.timedelta(minutes=2)  # minutes


# returns the score level and a timestamp of the last avalible result
def get_last_score():
    today = dt.datetime.now().date()
    # get the info of the last sync time
    heartrate_stats = fitbitWrapper.get_heartrate_series(today, '1min')
    last_record = heartrate_stats[len(heartrate_stats) - 1]
    # get precise heartrate data
    timerange = (last_record.datetime - ss_duration, last_record.datetime)
    heartrate_stats = fitbitWrapper.get_heartrate_series(today, '1sec', start_time=timerange[0], end_time=timerange[1])

    # calculate the stress level
    # assume that we have a continuous data on the heartrate (without breaks)
    hr_values = [r.value for r in heartrate_stats]
    score = Record(int(__stress_score(hr_values)), last_record.datetime)

    sleeps = fitbitWrapper.get_sleep_ranges(today, today + dt.timedelta(1))
    if sleeps:
        if score.datetime < sleeps[-1][1]:
            score.sleep = True

    return score


# params:
# start, end - start and end of the time interval
# sr defines the distance between samples
#
# returns regularly distributed samples for a given interval, start included, end excluded
def get_stat_score(start_date, end_date, sr):
    stress_stats = []
    for day_number in range((end_date - start_date).days):
        base_date = start_date + dt.timedelta(day_number)
        heartrate_stats = fitbitWrapper.get_heartrate_series(base_date, '1sec')
        if heartrate_stats:
            if day_number == (end_date - start_date).days - 1:
                stress_stats.extend(__resample_timeseries_and_get_stress_score(heartrate_stats, sr))
            else:
                stress_stats.extend(
                    __resample_timeseries_and_get_stress_score(heartrate_stats, sr, end_of_the_day=True))

    sleeps = fitbitWrapper.get_sleep_ranges(start_date, end_date + dt.timedelta(1))
    if sleeps:
        stress_stats = __check_sleeping_records(stress_stats, sleeps)

    return stress_stats


# params: timeseries are assumed to be sorted with respect to time
# sr is assumed to be a divisor of the number of minutes in the day (24*60)
# end_of_the_day indicates if the result should be extended till the end of the day of the final recording
#
# returns regularly distributed samples of stress score for a given sample rate, \
# starting from mignight of the first day of the avalible recordings
# Values are averaged inside the sample interval, stress score is calculated on the fly
# if there are no values in the given interval, the value for the sample is set to zero
#
# Optimized to go through the timeseries only once
def __resample_timeseries_and_get_stress_score(timeseries, sr, end_of_the_day=False):
    averaged = []
    averaged_interval = []
    ss_interval = []
    # start_interval = timeseries[0].datetime
    # ss_start_interval = timeseries[0].datetime
    start_interval = dt.datetime.combine(timeseries[0].datetime.date(), dt.time(0, 0, 0))
    ss_start_interval = dt.datetime.combine(timeseries[0].datetime.date(), dt.time(0, 0, 0))
    for record in timeseries:
        while record.datetime > start_interval + sr:
            value = sum(averaged_interval) / len(averaged_interval) if len(averaged_interval) else 0
            value = int(round(value))
            averaged.append(Record(value, start_interval + sr))
            start_interval = start_interval + sr
            averaged_interval = []
            ss_start_interval = start_interval
            ss_interval = []
        else:
            while record.datetime > ss_start_interval + ss_duration:
                score = __stress_score(ss_interval)
                if score:
                    averaged_interval.append(score)
                ss_start_interval = ss_start_interval + ss_duration
                ss_interval = []
            else:
                ss_interval.append(record.value)
    last_day_ends = dt.datetime.combine(averaged[-1].datetime.date(), dt.time(23, 59, 59))
    if end_of_the_day:
        while averaged[-1].datetime < last_day_ends:
            averaged.append(Record(0, averaged[-1].datetime + sr))

    return averaged


# params: timeseries is considered to be sampled with samplerate
def __fill_the_blancs(timeseries, sr):
    return


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


# params: series of the heartrate records. Each record is assumed to be significant (non-zero)
# and all records are assumed to be equally and densely dustributed in time domain
# returns estimated score for a given series of heartrate records or 0 if it cannot be estimated
def __stress_score(hr):
    # see http://www.cardiometry.net/issues/no10-may-2017/heart-rate-variability-analysis
    # originally from book https://www.twirpx.com/file/2327193/ (in Russian)
    # score = AMo / (2 * VR * Mo)
    # R-R interval - time delay between consecutive heart beats (assumed to be inverse value of the bpm)
    # Mo - mode - most frequent R-R interval value
    # AMo - mode amplitude - % of the intervals corresponding to Mode
    # VR - variational range - difference  between min and max R-R intervals

    r_r = [round(60. / float(r), 3) for r in hr]

    if len(r_r) == 0:
        return 0  # give up to calculate the score to prevent division by zero

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
    # print r_r
    # print min, max, mode, mode_freq

    VR = max - min
    Amode = mode_freq / float(len(r_r)) * 100

    if abs(VR) < 0.0001:
        return 0  # give up to calculate the score to prevent division by zero

    return round(Amode / (2 * VR * mode))
