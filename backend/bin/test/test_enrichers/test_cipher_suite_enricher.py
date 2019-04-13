import unittest

from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher


class TestCipherSuiteEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packets = {
            "client_hello": {
                "tls.handshake.type": "1",
                "tls.handshake.ciphersuite": "49200",
                "tcp.stream": 1
            }, "server_hello": {
                "tls.handshake.type": "2",
                "tls.handshake.ciphersuite": "49200",
                "tcp.stream": 1
            }, "first_packet": {
                "tls.handshake.type": "",
                "tls.handshake.ciphersuite": "",
                "tcp.stream": 1
            }}
        cls.cipher_suite_enricher = CipherSuiteEnricher()

    def run_test_packet(self, expected_value, packet):
        if expected_value == "":
            expected_cipher_suite = '"{}"'.format(expected_value)
        else:
            expected_cipher_suite = '{}'.format(expected_value)

        cipher_suite_number = self.cipher_suite_enricher.get_cipher_suite(packet)
        self.assertEqual(cipher_suite_number, expected_cipher_suite)

    def test_get_cipher_suites_client_hello(self):
        expected_value = ""
        self.run_test_packet(expected_value, self.packets["client_hello"])

    def test_get_cipher_suites_server_hello(self):
        expected_value = 49200
        self.run_test_packet(expected_value, self.packets["server_hello"])

    def test_get_cipher_suites_tls_packet(self):
        expected_value = 49200
        self.run_test_packet(expected_value, self.packets["first_packet"])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCipherSuiteEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
