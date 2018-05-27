import datetime as dt


# holds the data of one heart rate record
class HeartRateRecord:
    def __init__(self, heartrate, timestamp):
        self.heartrate = heartrate
        self.datetime = timestamp


# holds the data of one stress score calculation
class StressScoreRecord:
    def __init__(self, score, timestamp):
        self.score = score
        self.datetime = timestamp
        return
