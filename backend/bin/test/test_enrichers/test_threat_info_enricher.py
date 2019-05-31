import unittest

from main.enrichers.threat_info_enricher import ThreatInfoEnricher


class TestThreatInfoEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.threat_dict = {
            "": "",
            "domain-threatUnspecified": "THREAT_TYPE_UNSPECIFIED",
            "domain-threatMalware": "MALWARE",
            "domain-threatSocialEngineering": "SOCIAL_ENGINEERING",
            "domain-threatSoftware": "UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION",
            "domain-threatMalwareAndSoftware": "MALWARE,UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION"
        }
        cls.threat_info_enricher = ThreatInfoEnricher()
        cls.normal_domains = ["www.hsr.ch", "www.google.ch"]
        cls.threat_domains = ["domain-threatSocialEngineering", "domain-threatSoftware",
                              "domain-threatMalwareAndSoftware"]

    def test_generate_request_data(self) -> None:
        domain_entries = self.threat_info_enricher.get_domain_entries(self.normal_domains)
        expected_dict = {
            "threatInfo": {
                "threatTypes": ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                                "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": domain_entries
            }
        }
        actual_dict = self.threat_info_enricher.generate_request_data(self.normal_domains)
        self.assertDictEqual(actual_dict, expected_dict)

    def setUp(self) -> None:
        self.threat_info_enricher = ThreatInfoEnricher()

    def test_get_domain_entries(self) -> None:
        expected_list = [{"url": "www.hsr.ch"}, {"url": "www.google.ch"}]
        self.assertListEqual(self.threat_info_enricher.get_domain_entries(self.normal_domains), expected_list)

    def test_update_threat_dict_empty(self) -> None:
        expected_dict = {"": ""}
        self.assertEqual(self.threat_info_enricher.threat_dict, expected_dict)
        response_dict = {}
        self.threat_info_enricher.update_threat_dict(response_dict)
        self.assertEqual(self.threat_info_enricher.threat_dict, expected_dict)

    def test_update_threat_dict_full(self) -> None:
        expected_dict = {"": ""}
        self.assertDictEqual(self.threat_info_enricher.threat_dict, expected_dict)
        response_dict = {
            "matches": [
                {
                    "threat": {"url": "domain-threatUnspecified"},
                    "threatType": "THREAT_TYPE_UNSPECIFIED"
                },
                {
                    "threat": {"url": "domain-threatMalware"},
                    "threatType": "MALWARE"
                },
                {
                    "threat": {"url": "domain-threatSocialEngineering"},
                    "threatType": "SOCIAL_ENGINEERING"},
                {
                    "threat": {"url": "domain-threatSoftware"},
                    "threatType": "UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION"},
                {
                    "threat": {"url": "domain-threatMalwareAndSoftware"},
                    "threatType": "MALWARE,UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION"},
            ]}
        self.threat_info_enricher.update_threat_dict(response_dict)
        self.assertDictEqual(self.threat_info_enricher.threat_dict, self.threat_dict)

    def test_reduce_threat_information(self) -> None:
        self.threat_info_enricher.threat_dict = self.threat_dict
        expected_set = {"SOCIAL_ENGINEERING", "MALWARE", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"}
        self.assertSetEqual(self.threat_info_enricher.reduce_threat_information(self.threat_domains), expected_set)

    def test_get_threat_number(self) -> None:
        threat_types = ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                        "POTENTIALLY_HARMFUL_APPLICATION"]
        threat_number = 1
        for threat_type in threat_types:
            self.assertEqual(self.threat_info_enricher.get_threat_number(threat_type), str(threat_number))
            threat_number += 1


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestThreatInfoEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
