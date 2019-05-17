import unittest
from unittest.mock import patch, MagicMock

import main.helpers.tshark_helper as tshark_helper
from main.helpers.platform_detection_helper import PlatformDetectionHelper


class TestPlatformMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.windows_defaults = tshark_helper.get_windows_defaults()

    @patch("platform.system", MagicMock(return_value="Linux"))
    @patch("os.path.isfile", MagicMock(return_value=True))
    def test_detect_platform_linux(self) -> None:
        tshark_path_linux = "tshark"
        self.assertEqual(PlatformDetectionHelper.detect_platform(), tshark_path_linux)

    @patch("platform.system", MagicMock(return_value="Windows"))
    @patch("os.path.isfile", MagicMock(return_value=True))
    def test_detect_platform_windows_x86(self) -> None:
        self.assertEqual(PlatformDetectionHelper.detect_platform(), self.windows_defaults["x86"])

    @patch("platform.system", MagicMock(return_value="Linux"))
    @patch("os.path.isfile", MagicMock(return_value=False))
    def test_linux_wireshark_not_found(self) -> None:
        self.assertEqual(PlatformDetectionHelper.detect_platform(), None)

    @patch("platform.system", MagicMock(return_value="Windows"))
    @patch("os.path.isfile", MagicMock(return_value=False))
    def test_windows_wireshark_not_found(self) -> None:
        self.assertEqual(PlatformDetectionHelper.detect_platform(), None)

    @patch("platform.system", MagicMock(return_value="Java"))
    def test_unsupported_platform(self) -> None:
        self.assertEqual(PlatformDetectionHelper.detect_platform(), None)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlatformMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
