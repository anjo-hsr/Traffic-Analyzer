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

        cls.ad_enricher = AdEnricher(cls.blacklist_urls)

    def test_create_blacklist_dict(self):
        expected_dict = {
            "au": {"com": {"news": {
                "adserver": "adserver.news.com.au"
            }}},
            "com": {
                "amazonaws": {"s3": {
                    "yab-adimages": "yab-adimages.s3.amazonaws.com"
                }},
                "google": {
                    "analytics": "analytics.google.com"
                },
            },
            "de": {
                "adserver01": "adserver01.de"
            },
            "uk": {"co": {"telegraph": {
                "webtrends": "webtrends.telegraph.co.uk"
            }}},
        }
        self.assertDictEqual(self.ad_enricher.blacklist_dict, expected_dict)

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


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCipherSuiteEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
