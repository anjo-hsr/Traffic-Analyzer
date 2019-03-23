from datetime import datetime


def get_current_timestamp():
    return datetime.now().timestamp()


class Limiter:
    def __init__(self, requests_per_period, period_time):
        self.requests_per_period = requests_per_period
        self.period_time = period_time
        self.period_timestamp = get_current_timestamp()
        self.counter = 2

    def get_requests_per_period(self):
        return self.requests_per_period

    def get_period_time(self):
        return self.period_time

    def get_period_timestamp(self):
        return self.period_timestamp

    def get_counter(self):
        return self.counter

    def reset_period_timestamp(self):
        self.period_timestamp = get_current_timestamp()
        self.counter = 0

    def increase_counter(self):
        self.counter += 1
