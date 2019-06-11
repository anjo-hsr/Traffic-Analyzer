import unittest

from main.enrichers.stream_enricher import StreamEnricher


class TestStreamEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.stream_enricher = StreamEnricher()
        cls.source_ip_address = "10.0.0.1"
        cls.destination_ip_address = "8.8.8.8"
        cls.information_dict = {
            "ip_dst_combined": "152.96.36.100",
            "ip_src_combined": "10.0.0.1"
        }

        cls.public_packet = {
            "ip.dst": "152.96.36.100",
            "ip.src": "10.0.0.1",
            "tcp.dstport": "443",
            "tcp.srcport": "52012",
            "udp.dstport": "",
            "udp.srcport": "",
            "ip.proto": "6"
        }
        cls.private_packet = {
            "ip.dst": "10.0.0.2",
            "ip.src": "10.0.0.1",
            "tcp.dstport": "",
            "tcp.srcport": "",
            "udp.dstport": "",
            "udp.srcport": "",
            "ip.proto": "1"
        }

    def test_header(self) -> None:
        expected_header = "traffic_analyzer_stream"
        self.assertEqual(self.stream_enricher.header, expected_header)

    def test_generate_stream_id_public(self) -> None:
        tcp_packet_string = ",".join(self.public_packet[information] for information in self.public_packet)
        expected_stream_id = 48357853
        stream_id = StreamEnricher.generate_stream_id(tcp_packet_string)["stream_id"]
        self.assertEqual(stream_id, expected_stream_id)

    def test_get_combined_strings_public_packet(self) -> None:
        expected_string = "10.0.0.1,152.96.36.100,52012,443,,,6;152.96.36.100,10.0.0.1,443,52012,,,6"
        self.assertEqual(
            StreamEnricher.get_combined_strings(self.public_packet, self.information_dict),
            expected_string
        )

    def test_get_combined_strings_private_packet(self) -> None:
        expected_string = ""
        self.assertEqual(
            StreamEnricher.get_combined_strings(self.private_packet, self.information_dict),
            expected_string
        )

    def test_get_stream_id_public_packet(self) -> None:
        expected_size = 1
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)
        self.stream_enricher.get_information(self.public_packet, self.information_dict)
        expected_size += 1
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)

    def test_get_stream_id_private_packet(self) -> None:
        expected_size = 1
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)
        self.stream_enricher.get_information(self.private_packet, self.information_dict)
        self.assertEqual(len(self.stream_enricher.stream_ids), expected_size)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
