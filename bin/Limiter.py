from datetime import datetime
import time


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

    def check_request_load(self, limiter):
        current_time = get_current_timestamp()
        limiter.increase_counter()
        waiting_time = limiter.get_period_time() - (current_time - limiter.get_period_timestamp())

        if (limiter.counter == limiter.requests_per_period) and waiting_time > 0:
            time.sleep(waiting_time)
            limiter.reset_period_timestamp()

        if waiting_time < 0:
            limiter.reset_period_timestamp()
