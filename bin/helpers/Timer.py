import datetime


class Timer:
    @staticmethod
    def get_timestamp():
        return datetime.datetime.now().timestamp()

    def __init__(self):
        self.start_time = self.get_timestamp()
        self.end_time = self.get_timestamp()

    def set_end_time(self):
        self.end_time = self.get_timestamp()

    def print_runtime(self):
        run_time = self.end_time - self.start_time
        time_delta = datetime.timedelta(seconds=run_time)
        print("Runtime: {}".format(time_delta))