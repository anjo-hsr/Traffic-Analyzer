import unittest

from main.helpers.Combiner import Combiner
from main.helpers.Locator import Locator
from main.helpers.NameResolver import NameResolver


class TestCombinerMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.locator = Locator()
        cls.name_resolver = NameResolver()

        cls.source = "10.0.0.1"
        cls.destination = "8.8.8.8"

        cls.fqdns = {cls.destination: "google-public-dns-a.google.com", cls.source: ""}
        cls.locations = {cls.destination: "[8.1551, 47.144901]", cls.source: ""}

    def test_delimiter(self):
        csv_delimiter = ","
        self.assertEqual(Combiner.delimiter, csv_delimiter)

    def test_get_src_dst(self):
        packet = {"ip.dst": "8.8.8.8", "ip.src": "10.0.0.1"}
        dst_src_list = {"dst": "8.8.8.8", "src": "10.0.0.1"}

        self.assertEqual(Combiner.get_dst_src(packet), dst_src_list)

    def test_combine_fields(self):
        row = "number,name,description"

        fqdns_string = "{},{}".format(self.fqdns[self.destination], self.fqdns[self.source])
        locations_string = "{},{}".format(self.locations[self.destination], self.locations[self.source])
        combined_line_without_quotes = '{},{},{}'.format(row, fqdns_string, locations_string)
        combined_line_with_quotes = '"{}","{}","{}"'.format(row, fqdns_string, locations_string)
        self.assertEqual(Combiner.combine_fields([row, fqdns_string, locations_string], True), combined_line_with_quotes)
        self.assertEqual(Combiner.combine_fields([row, fqdns_string, locations_string]), combined_line_without_quotes)

    def test_combine_fqdns(self):
        combined_fqdns = '"{}","{}"'.format(self.fqdns[self.destination], self.fqdns[self.source])
        self.assertEqual(Combiner.combine_fqdns(self.fqdns, self.destination, self.source), combined_fqdns)

    def test_combine_default_fields(self):
        packet = {"ip.dst": "8.8.8.8", "ip.src": "10.0.0.1"}
        joined_cells = '"8.8.8.8","10.0.0.1"'
        self.assertEqual(Combiner.join_default_cells(packet), joined_cells)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCombinerMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
