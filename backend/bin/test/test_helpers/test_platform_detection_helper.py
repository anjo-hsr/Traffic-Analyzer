import unittest
from unittest.mock import patch, MagicMock

from main.helpers.platform_detection_helper import PlatformDetectionHelper
from main.helpers.tshark_helper import get_windows_defaults


class TestPlatformMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.windows_defaults = get_windows_defaults()

    @patch("platform.system", MagicMock(return_value="Linux"))
    @patch("os.path.isfile", MagicMock(return_value=True))
    def test_detect_platform_linux(self) -> None:
        tshark_path_linux = "tshark"
        self.assertEqual(PlatformDetectionHelper.detect_tshark(), tshark_path_linux)

    @patch("platform.system", MagicMock(return_value="Windows"))
    @patch("os.path.isfile", MagicMock(return_value=True))
    def test_detect_platform_windows_x86(self) -> None:
        self.assertEqual(PlatformDetectionHelper.detect_tshark(), self.windows_defaults["x86"])

    @patch("platform.system", MagicMock(return_value="Linux"))
    @patch("os.path.isfile", MagicMock(return_value=False))
    def test_linux_wireshark_not_found(self) -> None:
        self.assertEqual(PlatformDetectionHelper.detect_tshark(), None)

    @patch("platform.system", MagicMock(return_value="Windows"))
    @patch("os.path.isfile", MagicMock(return_value=False))
    def test_windows_wireshark_not_found(self) -> None:
        self.assertEqual(PlatformDetectionHelper.detect_tshark(), None)

    @patch("platform.system", MagicMock(return_value="Java"))
    def test_unsupported_platform(self) -> None:
        self.assertEqual(PlatformDetectionHelper.detect_tshark(), None)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlatformMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
