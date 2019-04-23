import time

from datetime import datetime


class TrafficLimitHelper:
    def __init__(self, requests_per_period, period_time):
        self.requests_per_period = requests_per_period
        self.period_time = period_time
        self.period_start_timestamp = self.timestamp()
        self.counter = 0

    @property
    def waiting_time(self):
        return self.period_time - (self.timestamp() - self.period_start_timestamp)

    @staticmethod
    def timestamp():
        return datetime.now().timestamp()

    def get_requests_per_period(self):
        return self.requests_per_period

    def reset_period_timestamp(self):
        self.period_start_timestamp = self.timestamp
        self.counter = 0

    def increase_counter(self):
        self.counter += 1

    def check_request_load(self):
        self.increase_counter()

        if (self.counter == self.requests_per_period) and self.waiting_time > 0:
            time.sleep(self.waiting_time)
            self.reset_period_timestamp()

        if self.waiting_time < 0:
            self.reset_period_timestamp()
