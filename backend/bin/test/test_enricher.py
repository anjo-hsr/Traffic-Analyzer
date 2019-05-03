import unittest

from main.dicts.information_dict import fill_dict
from main.enricher import Enricher


class TestEnrichmentClassesMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enricher = Enricher()

    def test_reset_variables(self):
        fqdn_key = "fqdn_information"
        fqdn_value = "www.hsr.ch"
        self.assertEqual(self.enricher.information_dict[fqdn_key], None)
        fill_dict(self.enricher.information_dict, [(fqdn_key, fqdn_value)])
        self.assertEqual(self.enricher.information_dict[fqdn_key], fqdn_value)
        self.enricher.reset_variables()
        self.assertEqual(self.enricher.information_dict[fqdn_key], None)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichmentClassesMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
