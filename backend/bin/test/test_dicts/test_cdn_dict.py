import unittest

from main.dicts.cdn_dict import CdnDict


class TestBlacklistDictMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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
        cls.cdn_dict = CdnDict()

    def test_get_cdn_domains_to_names(self) -> None:
        company_name = "Google"
        domains = [
            ".google.",
            "googlesyndication.",
            "youtube.",
            ".googleusercontent.com"
        ]

        domain_to_company = self.cdn_dict.get_cdn_domains_to_names()
        self.assertEqual(len(domain_to_company), 147)
        for domain in domains:
            self.assertEqual(domain_to_company[domain], company_name)

    def test_check_domain_cdn(self) -> None:
        cdn_domains = [
            "www.google.com",
            "www.youtube.ch",
            "traffic-analyzer.googleusercontent.com"
        ]
        for domain in cdn_domains:
            self.assertTrue(self.cdn_dict.check_domain(domain))

    def test_check_domain_normal(self) -> None:
        normal_domains = [
            "www.hsr.ch",
            "www.20min.ch"
        ]
        for domain in normal_domains:
            self.assertFalse(self.cdn_dict.check_domain(domain))

    def test_check_domains_cdn(self):
        cdn_domains = [
            "analytics.google.com,zrh04s15-in-f14.1e100.net",
            "www.youtube.ch,zrh04s15-in-f14.1e100.net",
        ]
        for domains in cdn_domains:
            self.assertTrue(self.cdn_dict.check_domains(domains))

    def test_check_domains_normal(self):
        cdn_domains = [
            "www.hsr.ch,lb-ext-web1.hsr.ch",
            "www.github.com,lb-140-82-118-4-ams.github.com"
        ]
        for domains in cdn_domains:
            self.assertFalse(self.cdn_dict.check_domains(domains))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBlacklistDictMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
