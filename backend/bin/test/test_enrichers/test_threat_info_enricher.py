import unittest

from main.enrichers.threat_info_enricher import ThreatInfoEnricher


class TestThreatInfoEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threat_dict = {
            "": "",
            "url-threatUnspecified": "THREAT_TYPE_UNSPECIFIED",
            "url-threatMalware": "MALWARE",
            "url-threatSocialEngineering": "SOCIAL_ENGINEERING",
            "url-threatSoftware": "UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION",
            "url-threatMalwareAndSoftware": "MALWARE,UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION"
        }
        cls.threat_info_enricher = ThreatInfoEnricher()
        cls.normal_urls = ["www.hsr.ch", "www.google.ch"]
        cls.threat_urls = ["url-threatSocialEngineering", "url-threatSoftware", "url-threatMalwareAndSoftware"]

    def test_generate_request_data(self):
        url_entries = self.threat_info_enricher.get_url_entries(self.normal_urls)
        expected_dict = {
            "threatInfo": {
                "threatTypes": ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                                "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": url_entries
            }
        }
        actual_dict = self.threat_info_enricher.generate_request_data(self.normal_urls)
        self.assertDictEqual(actual_dict, expected_dict)

    def setUp(self):
        self.threat_info_enricher = ThreatInfoEnricher()

    def test_get_url_entries(self):
        expected_list = [{"url": "www.hsr.ch"}, {"url": "www.google.ch"}]
        self.assertListEqual(self.threat_info_enricher.get_url_entries(self.normal_urls), expected_list)

    def test_update_threat_dict_empty(self):
        expected_dict = {"": ""}
        self.assertEqual(self.threat_info_enricher.threat_dict, expected_dict)
        response_dict = {}
        self.threat_info_enricher.update_threat_dict(response_dict)
        self.assertEqual(self.threat_info_enricher.threat_dict, expected_dict)

    def test_update_threat_dict_full(self):
        expected_dict = {"": ""}
        self.assertDictEqual(self.threat_info_enricher.threat_dict, expected_dict)
        response_dict = {
            "matches": [
                {
                    "threat": {"url": "url-threatUnspecified"},
                    "threatType": "THREAT_TYPE_UNSPECIFIED"
                },
                {
                    "threat": {"url": "url-threatMalware"},
                    "threatType": "MALWARE"
                },
                {
                    "threat": {"url": "url-threatSocialEngineering"},
                    "threatType": "SOCIAL_ENGINEERING"},
                {
                    "threat": {"url": "url-threatSoftware"},
                    "threatType": "UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION"},
                {
                    "threat": {"url": "url-threatMalwareAndSoftware"},
                    "threatType": "MALWARE,UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION"},
            ]}
        self.threat_info_enricher.update_threat_dict(response_dict)
        self.assertDictEqual(self.threat_info_enricher.threat_dict, self.threat_dict)

    def test_reduce_threat_information(self):
        self.threat_info_enricher.threat_dict = self.threat_dict
        expected_set = {"SOCIAL_ENGINEERING", "MALWARE", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"}
        self.assertSetEqual(self.threat_info_enricher.reduce_threat_information(self.threat_urls), expected_set)

    def test_get_threat_number(self):
        threat_types = ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                        "POTENTIALLY_HARMFUL_APPLICATION"]
        threat_number = 2
        for threat_type in threat_types:
            self.assertEqual(self.threat_info_enricher.get_threat_number(threat_type), str(threat_number))
            threat_number += 1

    def test_remove_quotations(self):
        string_with_quotations = '"hsr","rapperswil","st. gallen","switzerland"'
        expected_string = "hsr,rapperswil,st. gallen,switzerland"
        self.assertEqual(self.threat_info_enricher.remove_quotations(string_with_quotations), expected_string)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestThreatInfoEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
