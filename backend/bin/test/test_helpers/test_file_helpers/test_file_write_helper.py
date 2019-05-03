import unittest
from os import path, remove

from main.helpers.file import file_write_helper


class TestFileWriteHelperMethods(unittest.TestCase):
    def test_write_line(self):
        line = "test123"
        test_file_path = path.join(".", "test.csv")
        with open(test_file_path, mode="w") as test_file:
            file_write_helper.write_line(test_file, line)

        with open(test_file_path) as test_file:
            self.assertEqual(test_file.read(), line + "\n")

        remove(test_file_path)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileWriteHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
