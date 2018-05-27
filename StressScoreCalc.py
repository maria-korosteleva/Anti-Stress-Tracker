import datetime as dt
from StressScore import StressScore


class StressScoreCalc:
    def __init__(self):
        return

    # returns the score level and a timestamp of the last avalible result
    @staticmethod
    def get_last_score():
        score = StressScore()
        score.score = 50
        score.datetime = dt.datetime(2018, 1, 31, 14, 00, 00)
        return score

    # params:
    # start, end - start and end of the time interval
    # sr defines the distance between samples
    #
    # returns regularly distributed samples for a given interval
    @staticmethod
    def get_stat_score(start, end, sr):
        score_1 = StressScore()
        score_1.score = 50
        score_1.datetime = dt.datetime(2018, 1, 31, 14, 00, 00)

        score_2 = StressScore()
        score_2.score = 60
        score_2.datetime = dt.datetime(2018, 1, 31, 15, 00, 00)

        return score_1, score_2
