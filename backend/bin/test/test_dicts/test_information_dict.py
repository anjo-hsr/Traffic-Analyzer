import unittest
from collections import OrderedDict

from main.dicts.information_dict import get_information_dict
from test.test_dicts.keys import id_keys


class TestInformationDict(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.information_keys = [
            "location_information",
            "fqdn_information",
            "cipher_suite_information",
            "tls_ssl_version",
            "ip_type_information",
            "stream_id",
            "dns_lookup_information",
            "ad_value"
        ]

    def setUp(self) -> None:
        self.information_dict = get_information_dict()

    def test_create_enrichers_is_dict(self) -> None:
        self.assertTrue(isinstance(self.information_dict, OrderedDict))

    def test_create_information_keys(self) -> None:
        self.assertEqual(list(self.information_dict.keys()), self.information_keys)

    def test_information_dict_keys(self) -> None:
        id_index = 0
        information_enricher_key_ids = [key.split("_")[id_index] for key in self.information_dict.keys()]
        self.assertEqual(information_enricher_key_ids, id_keys)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInformationDict)
    unittest.TextTestRunner(verbosity=2).run(suite)
