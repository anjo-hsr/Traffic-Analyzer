import unittest

from main.enrichers.dns_lookup_enricher import DnsLookupEnricher


class TestDnsLookupEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dns_lookup_enricher = DnsLookupEnricher()
        cls.stream_id = 127
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

    def setUp(self):
        self.dns_lookup_enricher.dns_responses = {}

    def test_header(self):
        expected_header = "dst_query_name,dst_a_records,src_query_name,src_a_records"
        self.assertEqual(self.dns_lookup_enricher.header, expected_header)

    def test_is_response(self):
        self.assertTrue(self.dns_lookup_enricher.is_response(self.dns_packet))
        self.assertFalse(self.dns_lookup_enricher.is_response(self.normal_packet))

    def test_is_a_or_aaaa_response_type(self):
        a_response_type = "1"
        aaaa_response_type = "28"
        cname_response_type = "5"
        self.assertTrue(self.dns_lookup_enricher.is_a_or_aaaa_response_type(a_response_type))
        self.assertTrue(self.dns_lookup_enricher.is_a_or_aaaa_response_type(aaaa_response_type))
        self.assertFalse(self.dns_lookup_enricher.is_a_or_aaaa_response_type(cname_response_type))

    def test_get_empty_dict(self):
        expected_dict = {
            "query_name": "",
            "a_records": [""],
            "stream_id": self.stream_id
        }
        self.assertDictEqual(self.dns_lookup_enricher.get_empty_dict(self.stream_id), expected_dict)

    def test_generate_dns_information_without_dns_response(self):
        expected_dns_value = ","
        self.assertEqual(
            self.dns_lookup_enricher.generate_dns_information(self.normal_packet["ip.src"], self.stream_id),
            expected_dns_value)
        self.assertEqual(
            self.dns_lookup_enricher.generate_dns_information(self.normal_packet["ip.dst"], self.stream_id),
            expected_dns_value)

    def test_generate_dns_information_with_dns_reponse(self):
        expected_dns_value_src = ","
        expected_dns_value_dst = "www.hsr.ch,lb-ext-web1.hsr.ch"
        self.dns_lookup_enricher.save_dns_query(self.dns_packet)
        self.assertEqual(
            self.dns_lookup_enricher.generate_dns_information(self.normal_packet["ip.src"], self.stream_id),
            expected_dns_value_src)
        self.assertEqual(
            self.dns_lookup_enricher.generate_dns_information(self.normal_packet["ip.dst"], self.stream_id),
            expected_dns_value_dst)

    def test_safe_dns_query_with_a_record(self):
        self.dns_lookup_enricher.save_dns_query(self.dns_packet)
        dict_key = self.dns_packet["dns.a"]
        expected_dict_entry = {
            "a_records": ["lb-ext-web1.hsr.ch"],
            "query_name": "www.hsr.ch"
        }
        self.assertEqual(self.dns_lookup_enricher.dns_responses[dict_key], expected_dict_entry)

    def test_safe_dns_query_without_a_record(self):
        cname_response_type = "5"
        dns_packet = self.dns_packet.copy()
        dns_packet["dns.resp.type"] = cname_response_type

        expected_length = 0
        self.assertEqual(len(self.dns_lookup_enricher.dns_responses), expected_length)
        self.dns_lookup_enricher.save_dns_query(dns_packet)
        self.assertEqual(len(self.dns_lookup_enricher.dns_responses), expected_length)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDnsLookupEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
