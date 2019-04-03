from datetime import datetime, timedelta


class Timer:
    @staticmethod
    def get_timestamp():
        return datetime.now().timestamp()

    def __init__(self):
        self.start_time = self.get_timestamp()
        self.end_time = self.get_timestamp()
        self.time_sum = 0.0
        self.lap_start = self.get_timestamp()

    @property
    def run_time(self):
        return self.end_time - self.start_time

    def set_end_time(self):
        self.end_time = self.get_timestamp()

    def print_runtime(self):
        time_delta = timedelta(seconds=self.run_time)
        print("Runtime: {}".format(time_delta))

    def start_lap(self):
        self.lap_start = self.get_timestamp()

    def end_lap(self):
        self.time_sum += self.get_timestamp() - self.lap_start

    def print_time_sum(self):
        time_delta = timedelta(seconds=self.time_sum)
        print("Runtime: {}".format(time_delta))
