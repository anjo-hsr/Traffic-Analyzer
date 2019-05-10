import unittest

from main.enrichers.threat_info_enricher import ThreatInfoEnricher


class TestThreatInfoEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threat_info_enricher = ThreatInfoEnricher
        cls.urls = ["www.hsr.ch", "www.google.ch"]

    def test_generate_request_data(self):
        url_entries = self.threat_info_enricher.get_url_entries(self.urls)
        expected_dict = {
            "threatInfo": {
                "threatTypes": ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                                "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": url_entries
            }
        }
        actual_dict = self.threat_info_enricher.generate_request_data(self.urls)
        self.assertDictEqual(actual_dict, expected_dict)

    def test_remove_quotations(self):
        string_with_quotations = '"hsr","rapperswil","st. gallen","switzerland"'
        expected_string = "hsr,rapperswil,st. gallen,switzerland"
        self.assertEqual(self.threat_info_enricher.remove_quotations(string_with_quotations), expected_string)

    def test_get_url_entries(self):
        expected_list = [{"url": "www.hsr.ch"}, {"url": "www.google.ch"}]
        self.assertListEqual(self.threat_info_enricher.get_url_entries(self.urls), expected_list)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestThreatInfoEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
