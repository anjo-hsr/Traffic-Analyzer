import unittest

from main.enrichers.tls_enricher import TlsEnricher
from main.helpers.string_helper import enclose_with_quotes


class TestTlsEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tls_enricher = TlsEnricher()
        cls.information_dict = {}
        cls.packets_tls1_2 = {
            "client_hello_tls1_2": {
                "tls.version": "0x0301",
                "tls.handshake.type": "1",
                "tls.handshake.version": "0x0303",
                "tls.handshake.extensions.supported_version": "0x0301, 0x0302, 0x0303, 0x0304",
                "tcp.stream": 1
            }, "server_hello_tls1_2": {
                "tls.version": "0x0303",
                "tls.handshake.type": "2",
                "tls.handshake.version": "0x0303",
                "tls.handshake.extensions.supported_version": "",
                "tcp.stream": 1
            }, "first_packet_tls1_2": {
                "tls.version": "0x0303",
                "tls.handshake.type": "",
                "tls.handshake.version": "",
                "tls.handshake.extensions.supported_version": "",
                "tcp.stream": 1
            }}
        cls.packets_tls1_3 = {
            "client_hello_tls1_3": {
                "tls.version": "0x0301",
                "tls.handshake.type": "1",
                "tls.handshake.version": "0x0303",
                "tls.handshake.extensions.supported_version": "0x0301, 0x0302, 0x0303, 0x0304",
                "tcp.stream": 2
            }, "server_hello_tls1_3": {
                "tls.version": "0x0303",
                "tls.handshake.type": "2",
                "tls.handshake.version": "0x0303",
                "tls.handshake.extensions.supported_version": "0x0304",
                "tcp.stream": 2
            }, "first_packet_tls1_3": {
                "tls.version": "0x0303",
                "tls.handshake.type": "",
                "tls.handshake.version": "",
                "tls.handshake.extensions.supported_version": "",
                "tcp.stream": 2
            }}

    def test_header(self) -> None:
        expected_header = "tls_ssl_version_negotiated"
        self.assertEqual(self.tls_enricher.header, expected_header)

    def run_test_packet(self, expected_value, packet) -> None:
        if expected_value == "":
            expected_tls_ssl_version = enclose_with_quotes(expected_value)
        else:
            expected_tls_ssl_version = '{}'.format(expected_value)

        self.tls_enricher.get_information(packet, self.information_dict)
        self.assertEqual(self.information_dict["tls_ssl_version_negotiated"], expected_tls_ssl_version)

    def test_get_tls_ssl_version_tls1_2(self) -> None:
        expected_value = ""
        self.run_test_packet(expected_value, self.packets_tls1_2["client_hello_tls1_2"])
        expected_value = "0x0303"
        self.run_test_packet(expected_value, self.packets_tls1_2["server_hello_tls1_2"])
        expected_value = "0x0303"
        self.run_test_packet(expected_value, self.packets_tls1_2["first_packet_tls1_2"])

    def test_get_tls_ssl_version_tls1_3(self) -> None:
        expected_value = ""
        self.run_test_packet(expected_value, self.packets_tls1_3["client_hello_tls1_3"])
        expected_value = "0x0304"
        self.run_test_packet(expected_value, self.packets_tls1_3["server_hello_tls1_3"])
        expected_value = "0x0304"
        self.run_test_packet(expected_value, self.packets_tls1_3["first_packet_tls1_3"])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTlsEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
