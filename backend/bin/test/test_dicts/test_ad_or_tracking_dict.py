import unittest

from main.dicts.ad_or_tracking_dict import AdOrTrackingDict


class TestAdOrTrackingDictMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ad_or_tracking_domains = [
            "adserver.news.com.au",
            "yab-adimages.s3.amazonaws.com",
            "analytics.google.com",
            "adserver01.de",
            "webtrends.telegraph.co.uk",
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

        cls.ad_or_tracking_dict = AdOrTrackingDict(cls.ad_or_tracking_domains)

    def test_create_ad_or_tracking_dict(self) -> None:
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
        self.assertDictEqual(self.ad_or_tracking_dict.ad_or_tracking_dict, expected_dict)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdOrTrackingDictMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
