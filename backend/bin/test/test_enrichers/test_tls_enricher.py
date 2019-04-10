import unittest

from io import StringIO
from unittest.mock import patch

from main.enrichers.tls_enricher import TlsEnricher


class TestTlsEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        cls.tls_enricher = TlsEnricher()

    def run_test_packet(self, expected_value, packet):
        if expected_value == "":
            expected_tls_ssl_version = '"{}"'.format(expected_value)
        else:
            expected_tls_ssl_version = '{}'.format(expected_value)

        tls_ssl_version = self.tls_enricher.get_tls_ssl_version(packet)
        self.assertEqual(tls_ssl_version, expected_tls_ssl_version)

    def test_get_tls_ssl_version_tls1_2(self):
        expected_value = ""
        self.run_test_packet(expected_value, self.packets_tls1_2["client_hello_tls1_2"])
        expected_value = "0x0303"
        self.run_test_packet(expected_value, self.packets_tls1_2["server_hello_tls1_2"])
        expected_value = "0x0303"
        self.run_test_packet(expected_value, self.packets_tls1_2["first_packet_tls1_2"])

    def test_get_tls_ssl_version_tls1_3(self):
        expected_value = ""
        self.run_test_packet(expected_value, self.packets_tls1_3["client_hello_tls1_3"])
        expected_value = "0x0304"
        self.run_test_packet(expected_value, self.packets_tls1_3["server_hello_tls1_3"])
        expected_value = "0x0304"
        self.run_test_packet(expected_value, self.packets_tls1_3["first_packet_tls1_3"])

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_full_locations(self, mock_stdout):
        print_text = "Print out for all 2 stream to tls version entries\n1 --> 0x0303\n2 --> 0x0304\n\n\n\n"
        self.tls_enricher.print()
        self.assertEqual(mock_stdout.getvalue(), print_text)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTlsEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
