import unittest
from unittest.mock import patch, MagicMock, mock_open

from main.downloaders.safe_browsing_api_downloader import SafeBrowsingApiDownloader
from test.mock_classes.mock_response import MockResponse


class TestSafeBrowsingApiDownloader(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.safe_browsing_api_downloader = SafeBrowsingApiDownloader()
        cls.threat_dict = {
            "": "",
            "domain-threatUnspecified": "THREAT_TYPE_UNSPECIFIED",
            "domain-threatMalware": "MALWARE",
            "domain-threatSocialEngineering": "SOCIAL_ENGINEERING",
            "domain-threatSoftware": "UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION",
            "domain-threatMalwareAndSoftware": "MALWARE,UNWANTED_SOFTWARE,POTENTIALLY_HARMFUL_APPLICATION"
        }
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

    @patch("os.path.isfile", MagicMock(return_value=True))
    @patch("main.helpers.file.file_read_helper.open",
           new=mock_open(read_data="[Stanza]\n" + "safe_browsing_api_key = "))
    def test_get_domains_threat_infomation_empty_key(self) -> None:
        self.safe_browsing_api_downloader = SafeBrowsingApiDownloader()
        self.assertFalse(self.safe_browsing_api_downloader.is_api_key_correct)
        self.safe_browsing_api_downloader.get_domains_threat_information(self.normal_domains)
        self.assertFalse(self.safe_browsing_api_downloader.is_api_key_correct)

    @patch("os.path.isfile", MagicMock(return_value=True))
    @patch("main.helpers.file.file_read_helper.open",
           new=mock_open(read_data="[Stanza]\n" + "safe_browsing_api_key = false_key"))
    def test_get_domains_threat_infomation_false_key(self) -> None:
        self.safe_browsing_api_downloader = SafeBrowsingApiDownloader()
        self.assertTrue(self.safe_browsing_api_downloader.is_api_key_correct)
        self.safe_browsing_api_downloader.get_domains_threat_information(self.normal_domains)
        self.assertFalse(self.safe_browsing_api_downloader.is_api_key_correct)

    @patch("os.path.isfile", MagicMock(return_value=True))
    @patch("main.helpers.file.file_read_helper.open",
           new=mock_open(read_data="[Stanza]\n" + "safe_browsing_api_key = correct_key"))
    @patch("requests.post", MagicMock(return_value=MockResponse(content="{}")))
    def test_get_domains_threat_infomation_false_key(self) -> None:
        self.safe_browsing_api_downloader = SafeBrowsingApiDownloader()
        self.assertTrue(self.safe_browsing_api_downloader.is_api_key_correct)
        actual_return_value = self.safe_browsing_api_downloader.get_domains_threat_information(self.normal_domains)
        self.assertEqual(actual_return_value, {})
        self.assertTrue(self.safe_browsing_api_downloader.is_api_key_correct)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSafeBrowsingApiDownloader)
    unittest.TextTestRunner(verbosity=2).run(suite)
