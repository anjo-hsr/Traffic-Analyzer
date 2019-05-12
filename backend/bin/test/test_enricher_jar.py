import unittest

from main.dicts.information_dict import fill_dict
from main.enricher_jar import EnricherJar


class TestEnricherJarMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.enricher_jar = EnricherJar()

    def test_reset_variables(self) -> None:
        fqdn_key = "fqdn_information"
        fqdn_value = "www.hsr.ch"
        self.assertEqual(self.enricher_jar.information_dict[fqdn_key], None)
        fill_dict(self.enricher_jar.information_dict, [(fqdn_key, fqdn_value)])
        self.assertEqual(self.enricher_jar.information_dict[fqdn_key], fqdn_value)
        self.enricher_jar.reset_variables()
        self.assertEqual(self.enricher_jar.information_dict[fqdn_key], None)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnricherJarMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
