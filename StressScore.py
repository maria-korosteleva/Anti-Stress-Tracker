import datetime as dt


# holds the data of one stress score calculation
class StressScore:
    def __init__(self):
        self.score = 0
        self.datetime = dt.datetime(2018, 1, 31, 00, 00, 00)
        return
