# holds the data of one record of something
class Record:
    def __init__(self, value, timestamp, sleep=False):
        self.value = value
        self.datetime = timestamp
        self.sleep = sleep  # true if current record correspond to sleep

    def __repr__(self):
        return "value : {}, datetime : {}, sleep : {}\n".format(self.value, self.datetime, self.sleep)