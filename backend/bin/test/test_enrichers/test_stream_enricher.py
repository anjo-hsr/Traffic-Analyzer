import unittest

from main.enrichers.stream_enricher import StreamEnricher


class TestStreamEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stream_enricher = StreamEnricher()
        cls.source_ip_address = "10.0.0.1"
        cls.destination_ip_address = "8.8.8.8"

        cls.public_packet = {
            "ip.dst": "152.96.36.100",
            "ip.src": "10.0.0.1",
            "tcp.dstport": "443",
            "tcp.srcport": "52012",
            "udp.dstport": "",
            "udp.srcport": "",
            "_ws.col.Protocol": "TLS"
        }
        cls.private_packet = {
            "ip.dst": "224.0.0.5",
            "ip.src": "10.0.0.1",
            "tcp.dstport": "",
            "tcp.srcport": "",
            "udp.dstport": "",
            "udp.srcport": "",
            "_ws.col.Protocol": "OSPF"
        }

    def test_header(self) -> None:
        expected_header = "traffic_analyzer_tcp_stream"
        self.assertEqual(self.stream_enricher.header, expected_header)

    def test_generate_stream_id_public(self) -> None:
        tcp_packet_string = ",".join(self.public_packet[information] for information in self.public_packet)
        expected_stream_id = 75033177
        stream_id = StreamEnricher.generate_stream_id(tcp_packet_string)["stream_id"]
        self.assertEqual(stream_id, expected_stream_id)

    def test_get_combined_strings_public_packet(self) -> None:
        expected_string = "10.0.0.1,152.96.36.100,52012,443,,,TLS;152.96.36.100,10.0.0.1,443,52012,,,TLS"
        self.assertEqual(StreamEnricher.get_combined_strings(self.public_packet), expected_string)

    def test_get_combined_strings_private_packet(self) -> None:
        expected_string = ""
        self.assertEqual(StreamEnricher.get_combined_strings(self.private_packet), expected_string)

    def test_get_stream_id_public_packet(self) -> None:
        expected_size = 1
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)
        self.stream_enricher.get_stream_id(self.public_packet)
        expected_size += 1
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)

    def test_get_stream_id_private_packet(self) -> None:
        expected_size = 1
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)
        self.stream_enricher.get_stream_id(self.private_packet)
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
