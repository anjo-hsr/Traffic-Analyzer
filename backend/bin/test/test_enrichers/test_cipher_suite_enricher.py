import unittest

from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.helpers.string_helper import enclose_with_quotes


class TestCipherSuiteEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cipher_suite_enricher = CipherSuiteEnricher()
        cls.information_dict = {}
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

    def test_header(self) -> None:
        expected_header = "cipher_suite_number"
        self.assertEqual(self.cipher_suite_enricher.header, expected_header)

    def run_test_packet(self, expected_value, packet) -> None:
        if expected_value == "":
            expected_cipher_suite = enclose_with_quotes(expected_value)
        else:
            expected_cipher_suite = "{}".format(expected_value)

        self.cipher_suite_enricher.get_information(packet, self.information_dict)
        self.assertEqual(self.information_dict["cipher_suite_number"], expected_cipher_suite)

    def test_get_cipher_suites_client_hello(self) -> None:
        expected_value = ""
        self.run_test_packet(expected_value, self.packets["client_hello"])

    def test_get_cipher_suites_server_hello(self) -> None:
        expected_value = 49200
        self.run_test_packet(expected_value, self.packets["server_hello"])

    def test_get_cipher_suites_tls_packet(self) -> None:
        expected_value = 49200
        self.run_test_packet(expected_value, self.packets["first_packet"])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCipherSuiteEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
