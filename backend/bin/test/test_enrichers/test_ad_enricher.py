import unittest

from main.enrichers.ad_enricher import AdEnricher


class TestCipherSuiteEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blacklist_urls = [
            "adserver.news.com.au",
            "yab-adimages.s3.amazonaws.com",
            "analytics.google.com",
            "adserver01.de",
            "webtrends.telegraph.co.uk",
        ]
        cls.normal_urls = [
            "www.hsr.ch",
            "www.google.com",
        ]
        cls.mixex_urls = [
            "analytics.google.com",
            "zrh04s15-in-f14.1e100.net",
        ]
        cls.empty_urls = [
            "",
            "",
        ]

        cls.ad_enricher = AdEnricher(cls.blacklist_urls)

    def test_url_normal(self):
        for normal_url in self.normal_urls:
            self.assertFalse(self.ad_enricher.test_url(normal_url))

    def test_url_blacklist(self):
        for blacklist_url in self.blacklist_urls:
            self.assertTrue(self.ad_enricher.test_url(blacklist_url))

    def test_url_blacklist_subdomain(self):
        for blacklist_url in self.blacklist_urls:
            blacklist_url = "subdomain." + blacklist_url
            self.assertTrue(self.ad_enricher.test_url(blacklist_url))

    def test_url_mixed(self):
        mixed_urls_string = ",".join(self.mixex_urls)
        self.assertTrue(self.ad_enricher.test_urls(mixed_urls_string))

    def test_url_mixed_empty(self):
        empty_urls_string = ",".join(self.empty_urls)
        self.assertTrue(self.ad_enricher.test_urls(empty_urls_string))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCipherSuiteEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
