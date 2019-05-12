import unittest


class TestEnrichCsv(unittest.TestCase):
    def test(self) -> None:
        pass


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichCsv)
    unittest.TextTestRunner(verbosity=2).run(suite)
