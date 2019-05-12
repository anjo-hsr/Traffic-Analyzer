import unittest

from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.helpers.combine_helper import CombineHelper


class TestCombineHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.csv_delimiter = ","
        cls.location_enricher = LocationEnricher()
        cls.name_resolver_enricher = NameResolverEnricher()

        cls.source = "10.0.0.1"
        cls.destination = "8.8.8.8"

        cls.row = "number,name,description"
        cls.fqdns = {cls.destination: "google-public-dns-a.google.com", cls.source: ""}
        cls.locations = {cls.destination: "[8.1551, 47.144901]", cls.source: ""}

    def test_delimiter(self) -> None:
        self.assertEqual(CombineHelper.delimiter, self.csv_delimiter)

    def test_get_src_dst(self) -> None:
        packet = {"ip.dst": "8.8.8.8", "ip.src": "10.0.0.1"}
        dst_src_list = {"dst": "8.8.8.8", "src": "10.0.0.1"}

        self.assertEqual(CombineHelper.get_dst_src(packet), dst_src_list)

    def test_combine_fields_with_quotes(self) -> None:
        row = "number,name,description"
        fqdns_string = self.csv_delimiter.join([self.fqdns[self.destination], self.fqdns[self.source]])
        locations_string = self.csv_delimiter.join([self.locations[self.destination], self.locations[self.source]])
        elements = [row, fqdns_string, locations_string]

        expected_line = self.csv_delimiter.join('"{0}"'.format(element) for element in elements)
        given_line = CombineHelper.combine_fields([self.row, fqdns_string, locations_string], True)
        self.assertEqual(given_line, expected_line)

    def test_combine_fields_without_quotes(self) -> None:
        fqdns_string = self.csv_delimiter.join([self.fqdns[self.destination], self.fqdns[self.source]])
        locations_string = self.csv_delimiter.join([self.locations[self.destination], self.locations[self.source]])

        expected_line = self.csv_delimiter.join([self.row, fqdns_string, locations_string])
        given_line = CombineHelper.combine_fields([self.row, fqdns_string, locations_string])
        self.assertEqual(given_line, expected_line)

    def test_combine_default_fields(self) -> None:
        field_names = ["ip.dst", "ip.src"]
        packet = {"ip.dst": "8.8.8.8", "ip.src": "10.0.0.1"}
        joined_cells = '"8.8.8.8","10.0.0.1"'
        self.assertEqual(CombineHelper.join_default_cells(packet, field_names), joined_cells)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCombineHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
