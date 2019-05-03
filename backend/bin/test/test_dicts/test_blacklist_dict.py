import unittest

from main.dicts.blacklist_dict import BlacklistDict


class TestBlacklistDictMethods(unittest.TestCase):
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

        cls.blacklist_dict = BlacklistDict(cls.blacklist_urls)

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
        self.assertDictEqual(self.blacklist_dict.blacklist_dict, expected_dict)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBlacklistDictMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
