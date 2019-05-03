import unittest
from datetime import datetime

from main.helpers.traffic_limit_helper import TrafficLimitHelper


class TestTrafficLimitHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.request_per_period = 2
        cls.period_time = 1
        cls.traffic_limit_helper = TrafficLimitHelper(cls.request_per_period, cls.period_time)

    def setUp(self):
        self.traffic_limit_helper.reset_period_timestamp()

    def test_get_timestamp(self):
        timestamp = datetime.now().timestamp()
        self.assertAlmostEqual(TrafficLimitHelper.get_timestamp(), timestamp, 1)

    def test_reset_period_timestamp(self):
        expected_counter = 0
        self.traffic_limit_helper.counter = expected_counter + 1
        self.traffic_limit_helper.reset_period_timestamp()
        self.assertEqual(self.traffic_limit_helper.counter, expected_counter)

    def test_increase_counter(self):
        expected_counter = 0
        self.assertEqual(self.traffic_limit_helper.counter, expected_counter)
        self.traffic_limit_helper.check_request_load()
        expected_counter += 1
        self.assertEqual(self.traffic_limit_helper.counter, expected_counter)

    def test_check_request_load_ok(self):
        timestamp_before = datetime.now().timestamp()
        self.traffic_limit_helper.check_request_load()
        timestamp_after = datetime.now().timestamp()
        self.assertAlmostEqual(timestamp_after - timestamp_before, 0, 1)

    def test_check_request_load_waiting(self):
        counter = 0
        while counter != self.request_per_period:
            self.traffic_limit_helper.check_request_load()
            counter += 1

        timestamp_before = datetime.now().timestamp()
        self.traffic_limit_helper.check_request_load()
        timestamp_after = datetime.now().timestamp()
        self.assertAlmostEqual(timestamp_after - timestamp_before, 1, 1)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTrafficLimitHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
