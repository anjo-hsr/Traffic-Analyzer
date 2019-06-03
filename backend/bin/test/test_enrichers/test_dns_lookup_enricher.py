import unittest

from main.enrichers.dns_lookup_enricher import DnsLookupEnricher


class TestDnsLookupEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dns_lookup_enricher = DnsLookupEnricher()
        cls.stream_id = 127
        cls.information_dict = {}
        cls.dns_packet = {
            "ip.src": "10.0.0.2",
            "ip.dst": "8.8.8.8",
            "_ws.col.Protocol": "DNS",
            "dns.flags.response": "1",
            "dns.resp.type": "5,1",
            "dns.qry.name": "www.hsr.ch",
            "dns.resp.name": "www.hsr.ch,lb-ext-web1.hsr.ch",
            "dns.a": "152.96.36.100",
            "dns.aaaa": ""
        }
        cls.normal_packet = {
            "ip.src": "10.0.0.2",
            "ip.dst": "152.96.36.100",
            "_ws.col.Protocol": "HTTP",
            "dns.flags.response": "",
            "dns.resp.type": "",
            "dns.qry.name": "",
            "dns.resp.name": "",
            "dns.a": "",
            "dns.aaaa": ""
        }

    def setUp(self) -> None:
        self.dns_lookup_enricher.dns_responses = {}

    def set_information_dict(self, packet):
        self.information_dict["ip_src_combined"] = packet["ip.src"]
        self.information_dict["ip_dst_combined"] = packet["ip.dst"]

    def test_header(self) -> None:
        expected_header = "dst_query_name,dst_hostnames,src_query_name,src_hostnames"
        self.assertEqual(self.dns_lookup_enricher.header, expected_header)

    def test_get_empty_dict(self) -> None:
        expected_dict = {
            "query_name": "",
            "hostnames": {""},
        }
        self.assertDictEqual(self.dns_lookup_enricher.get_empty_dict(), expected_dict)

    def test_generate_dns_information_without_dns_response(self) -> None:
        empty_string = '""'
        self.set_information_dict(self.dns_packet)

        self.dns_lookup_enricher.save_dns_query(self.dns_packet)
        self.dns_lookup_enricher.get_information(self.dns_packet, self.information_dict)

        self.assertEqual(self.information_dict["dst_query_name"], empty_string)
        self.assertEqual(self.information_dict["dst_hostnames"], empty_string)
        self.assertEqual(self.information_dict["src_query_name"], empty_string)
        self.assertEqual(self.information_dict["src_hostnames"], empty_string)

    def test_generate_dns_information_with_dns_reponse_dst(self) -> None:
        dst_query_name = '"www.hsr.ch"'
        dst_hostnames = '"www.hsr.ch,lb-ext-web1.hsr.ch"'
        src_query_name = '""'
        src_hostnames = '""'

        self.set_information_dict(self.dns_packet)
        self.dns_lookup_enricher.save_dns_query(self.dns_packet)

        self.set_information_dict(self.normal_packet)
        self.dns_lookup_enricher.get_information(self.normal_packet, self.information_dict)

        self.assertEqual(self.information_dict["dst_query_name"], dst_query_name)
        self.assertEqual(self.information_dict["dst_hostnames"], dst_hostnames)
        self.assertEqual(self.information_dict["src_query_name"], src_query_name)
        self.assertEqual(self.information_dict["src_hostnames"], src_hostnames)

    def test_safe_dns_query_with_a_record(self) -> None:
        self.dns_lookup_enricher.save_dns_query(self.dns_packet)
        dict_key = self.dns_packet["dns.a"]
        expected_dict_entry = {
            "query_name": "www.hsr.ch",
            "hostnames": {"www.hsr.ch", "lb-ext-web1.hsr.ch"}
        }
        self.assertEqual(self.dns_lookup_enricher.dns_responses[dict_key].keys(), expected_dict_entry.keys())
        self.assertCountEqual(self.dns_lookup_enricher.dns_responses[dict_key]["hostnames"],
                              expected_dict_entry["hostnames"])

    def test_safe_dns_query_without_a_record(self) -> None:
        expected_length = 0
        self.assertEqual(len(self.dns_lookup_enricher.dns_responses), expected_length)
        self.dns_lookup_enricher.save_dns_query(self.normal_packet)
        self.assertEqual(len(self.dns_lookup_enricher.dns_responses), expected_length)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDnsLookupEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
