import unittest

from main.enrichers.ad_enricher import AdEnricher


class TestCipherSuiteEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.information_dict = {}
        cls.packet = {}
        cls.blacklist_domains = [
            "adserver.news.com.au",
            "yab-adimages.s3.amazonaws.com",
            "analytics.google.com",
            "adserver01.de",
            "webtrends.telegraph.co.uk",
        ]
        cls.ips = [
            "152.96.36.100",
            "8.8.8.8",
        ]
        cls.normal_domains = [
            "www.hsr.ch",
            "www.google.com",
        ]
        cls.mixex_domains = [
            "analytics.google.com",
            "zrh04s15-in-f14.1e100.net",
        ]
        cls.empty_domains = [
            "",
            "",
        ]

        cls.ad_enricher = AdEnricher(cls.blacklist_domains)

    def test_header(self) -> None:
        expected_header = "ad_category"
        self.assertEqual(self.ad_enricher.header, expected_header)

    def test_domain_normal(self) -> None:
        for normal_domain in self.normal_domains:
            self.assertFalse(self.ad_enricher.is_ad_domain(normal_domain))

    def test_ips(self) -> None:
        for ip in self.ips:
            self.assertFalse(self.ad_enricher.is_ad_domain(ip))

    def test_domain_blacklist(self) -> None:
        for blacklist_domain in self.blacklist_domains:
            self.assertTrue(self.ad_enricher.is_ad_domain(blacklist_domain))

    def test_domain_blacklist_subdomain(self) -> None:
        for blacklist_domain in self.blacklist_domains:
            blacklist_domain = "subdomain." + blacklist_domain
            self.assertTrue(self.ad_enricher.is_ad_domain(blacklist_domain))

    def test_domain_mixed(self) -> None:
        self.information_dict["domains"] = ",".join(self.mixex_domains)
        self.ad_enricher.get_information(self.packet, self.information_dict)
        ad_category = "1"
        self.assertEqual(self.information_dict["ad_category"], ad_category)

    def test_domain_empty(self) -> None:
        self.information_dict["domains"] = ",".join(self.empty_domains)
        self.ad_enricher.get_information(self.packet, self.information_dict)
        ad_category = "0"
        self.assertEqual(self.information_dict["ad_category"], ad_category)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCipherSuiteEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
