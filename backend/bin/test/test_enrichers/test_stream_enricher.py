import unittest

from main.enrichers.stream_enricher import StreamEnricher


class TestStreamEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stream_enricher = StreamEnricher()
        cls.source_ip_address = "10.0.0.1"
        cls.destination_ip_address = "8.8.8.8"

        cls.public_packet = {
            "ip.dst": "152.96.36.100",
            "ip.src": "10.0.0.1",
            "tcp.dstport": "443",
            "tcp.srcport": "52012",
            "udp.dstport": "",
            "udp.srcport": ""
        }
        cls.private_packet = {
            "ip.dst": "224.0.0.1",
            "ip.src": "10.0.0.1",
            "tcp.dstport": "",
            "tcp.srcport": "",
            "udp.dstport": "",
            "udp.srcport": ""
        }

    def test_generate_stream_id_public(self):
        tcp_packet_string = ",".join(self.public_packet[information] for information in self.public_packet)
        expected_stream_id = 27795967
        self.assertEqual(StreamEnricher.generate_stream_id(tcp_packet_string).stream_id, expected_stream_id)

    def test_get_combined_strings_public_packet(self):
        expected_string = "10.0.0.1,152.96.36.100,52012,443,,;152.96.36.100,10.0.0.1,443,52012,,"
        self.assertEqual(StreamEnricher.get_combined_strings(self.public_packet), expected_string)

    def test_get_combined_strings_private_packet(self):
        expected_string = ""
        self.assertEqual(StreamEnricher.get_combined_strings(self.private_packet), expected_string)

    def test_get_stream_id_public_packet(self):
        expected_size = 1
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)
        self.stream_enricher.get_stream_id(self.public_packet)
        expected_size += 1
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)

    def test_get_stream_id_private_packet(self):
        expected_size = 1
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)
        self.stream_enricher.get_stream_id(self.private_packet)
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
