import unittest

from main.enrichers.protocol_enricher import ProtocolEnricher


class TestTlsEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocols = {
            "http": {"frame.protocols": ":http"},
            "https": {"frame.protocols": ":https"},
            "quic": {"frame.protocols": ":quic"},
            "stp": {"frame.protocols": ":stp"}
        }

    def test_protocols(self):
        protocol_enricher = ProtocolEnricher()
        for protocol in self.protocols:
            self.assertEqual(protocol_enricher.get_protocol(self.protocols[protocol]), protocol)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTlsEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
