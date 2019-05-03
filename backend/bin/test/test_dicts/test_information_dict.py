import unittest

from main.enricher import Enricher
from test.test_dicts.keys import id_keys

class TestInformationDict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enricher = Enricher()
        cls.test_keys = [
            "location_information",
            "fqdn_information",
            "cipher_suite_information",
            "tls_ssl_version",
            "ip_type_information",
            "stream_id",
            "dns_lookup_information",
            "ad_value"
        ]

    def setUp(self):
        self.enricher.reset_variables()

    def test_get_information_dict(self):
        information_dict = self.enricher.get_information_dict(None, None)
        self.assertEqual(list(information_dict.keys()), self.test_keys)

    def test_information_dict_keys(self):
        information_dict = self.enricher.get_information_dict(None, None)
        id_index = 0
        key_ids = [key.split("_")[id_index] for key in information_dict.keys()]
        self.assertEqual(key_ids, id_keys)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInformationDict)
    unittest.TextTestRunner(verbosity=2).run(suite)
