import datetime as dt
from RecordClasses import StressScoreRecord
from fitbitWrapper import FitbitWrapper


class StressScoreCalc:
    def __init__(self):
        return

    # returns the score level and a timestamp of the last avalible result
    @staticmethod
    def get_last_score():
        score = StressScoreRecord(50, dt.datetime(2018, 1, 31, 14, 00, 00))
        return score

    # params:
    # start, end - start and end of the time interval
    # sr defines the distance between samples
    #
    # returns regularly distributed samples for a given interval
    @staticmethod
    def get_stat_score(start, end, sr):
        fitbit = FitbitWrapper()
        fitbit.get_heartrate_series(start, end, '1min')

        score_1 = StressScoreRecord(50, dt.datetime(2018, 1, 31, 14, 00, 00))
        score_2 = StressScoreRecord(60, dt.datetime(2018, 1, 31, 15, 00, 00))

        return score_1, score_2