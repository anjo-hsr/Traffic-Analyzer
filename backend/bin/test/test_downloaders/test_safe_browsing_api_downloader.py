import unittest

from main.downloaders.safe_browsing_api_downloader import SafeBrowsingApiDownloader


class TestSafeBrowsingApiDownloader(unittest.TestCase):
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
        cls.safe_browsing_api_downloader = SafeBrowsingApiDownloader()
        cls.normal_domains = ["www.hsr.ch", "www.google.ch"]
        cls.threat_domains = ["domain-threatSocialEngineering", "domain-threatSoftware",
                              "domain-threatMalwareAndSoftware"]

    def test_generate_request_data(self) -> None:
        domain_entries = self.safe_browsing_api_downloader.get_domain_entries(self.normal_domains)
        expected_dict = {
            "threatInfo": {
                "threatTypes": ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                                "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": domain_entries
            }
        }
        actual_dict = self.safe_browsing_api_downloader.generate_request_data(self.normal_domains)
        self.assertDictEqual(actual_dict, expected_dict)

    def test_get_domain_entries(self) -> None:
        expected_list = [{"url": "www.hsr.ch"}, {"url": "www.google.ch"}]
        self.assertListEqual(self.safe_browsing_api_downloader.get_domain_entries(self.normal_domains), expected_list)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSafeBrowsingApiDownloader)
    unittest.TextTestRunner(verbosity=2).run(suite)
