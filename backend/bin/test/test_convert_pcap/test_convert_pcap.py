import unittest


class TestConvertPcapMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConvertPcapMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
